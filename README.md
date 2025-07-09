# 🎥 YouTube Transcript Chatbot

A mini project that extracts the transcript of a YouTube video and enables intelligent question-answering using a **RAG-based (Retrieval-Augmented Generation)** system.

Built with [Streamlit](https://streamlit.io), [LangChain](https://www.langchain.com), and [Google GenAI Embeddings](https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-started).

---

## 🚀 Live Demo

👉 Try it now: https://youtube-transcript-chatbot-mfbmfdjnuojs2bvewoaoan.streamlit.app/ 


---

## ✨ Features

- 🔍 Extracts YouTube video transcripts
- 🧠 Embeds text using **Google Generative AI Embeddings**
- 📚 Indexes transcript data into **FAISS Vector DB**
- 🤖 Answers your questions with context using **LangChain RAG pipeline**
- 💬 Chat-like interface with Streamlit

---

## 🛠️ Technologies Used

- **Streamlit** — Frontend and hosting
- **LangChain** — RAG pipeline and embeddings handling
- **Google GenAI** — `embedding-001` model for vectorization
- **Groq LLM (optional)** — For fast, low-latency responses
- **FAISS** — In-memory vector database
- **YouTube Transcript API** — Transcript extraction

---

## 🧪 How It Works

1. 🧠 You paste a YouTube video URL  
2. 📜 The transcript is fetched using `youtube-transcript-api`  
3. 🧬 The text is split and embedded with `GoogleGenerativeAIEmbeddings`  
4. 📂 Stored in **FAISS** for similarity search  
5. 🗣️ You ask a question → top relevant chunks are retrieved  
6. 🤖 Answer is generated using LLM via **LangChain RAG**

---

## 🔐 API Keys Setup

This app requires a few secrets to be set securely on **Streamlit Cloud**
