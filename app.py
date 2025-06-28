import streamlit as st
from rag_pipeline.retriever import load_vector_store, retrieve_context, close_vector_store
from rag_pipeline.evaluator import evaluate_answer
from rag_pipeline.embedder import split_text_into_chunks, create_and_save_vector_store
from utils.question_generator import generate_questions
from utils.pdf_reader import extract_text_from_pdf
import os
import json
import stat
import gc

st.set_page_config(page_title="📖 AI ExamPrep Assistant", page_icon="📝", layout="wide")

# Helper: to remove file lock issues on Windows
def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# Helper: reset vector store and related session state
def reset_vector_store():
    if 'vectordb' in st.session_state and st.session_state.vectordb:
        close_vector_store(st.session_state.vectordb)
        st.session_state.vectordb = None
        gc.collect()

    if os.path.exists("vector_store"):
        for root, dirs, files in os.walk("vector_store", topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.chmod(file_path, stat.S_IWRITE)
                    os.remove(file_path)
                except Exception as e:
                    print(f"❌ Error deleting file {file_path}: {e}")
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    os.rmdir(dir_path)
                except Exception as e:
                    print(f"❌ Error deleting dir {dir_path}: {e}")

    st.session_state.questions = {}
    st.session_state.answers = {}
    st.session_state.evaluations = {}

# Sidebar navigation
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Go to", ["Upload Notes", "Generate Questions", "Take Test", "View Results"])

# Session state initialization
for key in ["vectordb", "questions", "answers", "evaluations"]:
    if key not in st.session_state:
        st.session_state[key] = None if key == "vectordb" else {}

# 📄 Upload Notes
# 📄 Upload Notes
if page == "Upload Notes":
    st.title("📄 Upload & Process PDF Notes")

    uploaded_pdfs = st.file_uploader("Upload your study notes as PDF", type=["pdf"], accept_multiple_files=True)

    if uploaded_pdfs:
        os.makedirs("pdfs", exist_ok=True)
        for uploaded_pdf in uploaded_pdfs:
            pdf_path = os.path.join("pdfs", uploaded_pdf.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.read())
        st.success(f"✅ {len(uploaded_pdfs)} PDF(s) uploaded!")

        if st.button("🧠 Process & Embed Notes"):
            reset_vector_store()

            combined_text = ""
            for uploaded_pdf in uploaded_pdfs:
                pdf_path = os.path.join("pdfs", uploaded_pdf.name)
                text = extract_text_from_pdf(pdf_path)
                combined_text += "\n" + text

            docs = split_text_into_chunks(combined_text)
            create_and_save_vector_store(docs)
            st.session_state.vectordb = load_vector_store()
            st.write("📄 Processed Files:")
            for uploaded_pdf in uploaded_pdfs:
                st.write(f"- {uploaded_pdf.name}")
            st.success("✅ All notes processed & Vector DB created!")

# ✨ Generate Questions
elif page == "Generate Questions":
    st.title("✨ Generate Questions from Notes")

    if not os.path.exists("vector_store"):
        st.warning("⚠️ Please upload and process notes first.")
    else:
        if st.session_state.vectordb is None:
            st.session_state.vectordb = load_vector_store()

        topic = st.text_input("📌 Enter Topic / Concept for Questions")
        qtype = st.selectbox("📝 Question Type", ["MCQ", "True/False", "Fill in the blanks", "Short Answer", "Long Answer", "Essay"])
        num_qs = st.slider("How many questions?", 1, 20, 10)

        if st.button("✨ Generate"):
            context_docs = retrieve_context(topic, st.session_state.vectordb)
            combined_context = "\n".join([doc.page_content for doc in context_docs])

            if not combined_context.strip():
                st.error("❌ No relevant context found for the topic you entered.")
            else:
                questions = generate_questions(combined_context, topic, question_type=qtype, num_questions=num_qs, max_retries=5)
                if questions:
                    st.session_state.questions = questions
                    st.session_state.answers = {}
                    st.session_state.evaluations = {}
                    st.success(f"✅ {len(questions)} Questions Generated!")
                else:
                    st.error("⚠️ Failed to generate questions. Check if the notes cover your topic.")

        if st.session_state.questions:
            st.markdown(f"### 📑 {len(st.session_state.questions)} questions ready for Test in 'Take Test' section")

# 📝 Take Test
elif page == "Take Test":
    st.title("📝 Take the Test")

    if not st.session_state.questions:
        st.warning("⚠️ Please generate questions first.")
    else:
        for idx, q in enumerate(st.session_state.questions, 1):
            st.markdown(f"**Q{idx}. {q['question']}**")

            if "options" in q:
                st.session_state.answers[f"ans_{idx}"] = st.radio(
                    f"Choose option for Q{idx}:", q["options"], key=f"mcq_{idx}"
                )
            elif "reason_required" in q:
                st.session_state.answers[f"ans_{idx}"] = st.radio(
                    f"Is this True or False?", ["True", "False"], key=f"tf_{idx}"
                )
            else:
                st.session_state.answers[f"ans_{idx}"] = st.text_area(
                    f"Your Answer for Q{idx}:", key=f"text_{idx}"
                )
            st.markdown("---")

        if st.button("📊 Submit Test for Evaluation"):
            for idx, q in enumerate(st.session_state.questions, 1):
                user_answer = st.session_state.answers.get(f"ans_{idx}", "")
                context_docs = retrieve_context(q["question"], st.session_state.vectordb)
                combined_context = "\n".join([doc.page_content for doc in context_docs])
                result = evaluate_answer(q["question"], combined_context, user_answer)

                try:
                    parsed_result = json.loads(result)
                    st.session_state.evaluations[f"ans_{idx}"] = parsed_result
                except json.JSONDecodeError:
                    st.session_state.evaluations[f"ans_{idx}"] = {
                        "marks": 0,
                        "feedback": "Invalid evaluation response received."
                    }

            st.success("✅ Test submitted and evaluated! See 'View Results' section.")

# 📊 View Results
elif page == "View Results":
    st.title("📊 Test Results & Analytics")

    if not st.session_state.evaluations:
        st.warning("⚠️ No test attempted yet.")
    else:
        total_marks = 0
        max_marks_per_question = 10
        num_questions = len(st.session_state.evaluations)

        for idx, q in enumerate(st.session_state.questions, 1):
            st.markdown(f"**Q{idx}. {q['question']}**")
            user_ans = st.session_state.answers.get(f'ans_{idx}', '')
            result = st.session_state.evaluations.get(f'ans_{idx}', {"marks": 0, "feedback": "Not evaluated."})
            marks = result.get("marks", 0)
            feedback = result.get("feedback", "No feedback.")

            st.markdown(f"- **Your Answer:** {user_ans}")
            st.markdown(f"- **Marks Obtained:** {marks}")
            st.markdown(f"- **Feedback:** {feedback}")
            st.markdown("---")

            total_marks += marks

        score_percentage = (total_marks / (num_questions * max_marks_per_question)) * 100 if num_questions else 0
        st.success(f"📈 Final Score: {total_marks}/{num_questions * max_marks_per_question} ({score_percentage:.2f}%)")
