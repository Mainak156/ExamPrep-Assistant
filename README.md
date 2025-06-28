# 📖 AI ExamPrep Assistant

An interactive AI-powered exam preparation assistant built using **Streamlit**, **LangChain**, **HuggingFace Embeddings**, **Groq LLM**, and **Chroma Vector Database**.  
This app allows students to upload their study notes (PDFs), automatically generate customized exam questions, take tests, and get AI-evaluated feedback — all in one place.

---

## 🚀 Features

- 📄 Upload multiple PDF study notes  
- 🧠 AI-powered **question generation** from your notes  
- Supports multiple question types:
  - Multiple Choice Questions (MCQ)
  - True/False
  - Fill in the blanks
  - Short Answer
  - Long Answer
  - Essay  
- 📝 Take a test based on generated questions  
- 📊 AI auto-evaluates answers and provides marks + feedback  
- 🔍 Uses **Chroma vector database** for efficient context retrieval  
- 🦙 Powered by **Groq’s Llama 3-70B** via LangChain  

---

## 🛠️ Tech Stack

- 🐍 Python 3.11  
- 🖥️ Streamlit (UI)  
- 🧠 LangChain  
- 🗂️ Chroma Vector DB  
- 🤖 HuggingFace Sentence Transformers (GTE-small)  
- 🔥 Groq API (Llama 3-70B)  
- 📄 PyPDF2 (PDF extraction)  
- 🌿 dotenv (for API key management)  

---

## 📂 Project Structure

```
├── app.py                     # Streamlit app with navigation and workflow
├── rag_pipeline/
│   ├── retriever.py           # Vector DB loader and context retriever
│   ├── embedder.py            # PDF text chunking and vector DB creator
│   ├── evaluator.py           # Answer evaluation via LLM
├── utils/
│   ├── pdf_reader.py          # PDF text extraction
│   ├── question_generator.py  # AI question generation module
├── vector_store/              # Chroma persistent DB (auto-created)
├── pdfs/                      # Uploaded PDF files
├── .env                       # API keys (not pushed to GitHub)
├── requirements.txt           # Python dependencies
└── README.md
```

---

## 📦 Installation

**1️⃣ Clone this repo:**  
```bash
git clone https://github.com/your-username/ai-examprep-assistant.git
cd ai-examprep-assistant
```

**2️⃣ Install dependencies:**  
```bash
pip install -r requirements.txt
```

**3️⃣ Add your Groq API Key in a `.env` file:**  
```bash
GROQ_API_KEY=gsk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**4️⃣ Run the app:**  
```bash
streamlit run app.py
```

---

## 📣 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)  
- [HuggingFace Sentence Transformers](https://www.sbert.net/)  
- [Chroma Vector DB](https://www.trychroma.com/)  
- [Groq API](https://console.groq.com/)  
- [Streamlit](https://streamlit.io/)  
- [PyPDF2](https://github.com/py-pdf/pypdf)  

---

📚 **Made for students, by AI enthusiast!**
