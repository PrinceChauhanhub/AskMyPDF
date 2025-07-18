# AskMyPDF 📚

Web-App Link -> https://mathsolverusinggemma.streamlit.app/

AskMyPDF is a powerful Streamlit web application that allows you to upload and interactively chat with multiple PDF documents using Google Gemini models via LangChain. It extracts and semantically understands the content of your PDFs and answers your questions contextually.

---

## 🔧 Features

- Upload and process multiple PDF files
- AI-powered Q&A using **Google Gemini (Gemini 1.5 Flash)**
- Semantic search powered by **FAISS**
- Clean and interactive **Streamlit** interface
- Chunked text processing for large PDFs
- Persistent vector store using FAISS
- Robust error handling and session management

---

## 🧩 Tech Stack

- `streamlit`
- `Google-Gemini`
- `langchain`
- `python`
- `google-generativeai`

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/PrinceChauhanhub/AskMyPDF.git
cd AskMyPDF
```
### 2. Create and activate a virtual environment

```bash
conda create -p venv python==3.10 -y
conda activate venv/
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your .env file
```bash
GOOGLE_API_KEY=your_google_generative_ai_key
```

### 5. Run the App
```bash
streamlit run app.py
```

---

🔐 API Key Requirement
----------------------
You must have a **Gemini API Key** to use the application.  
Sign up and generate a key from: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

---
🤝 Contributing
---------------
Feel free to contribute!  
Whether it's fixing bugs, improving logic, optimizing prompts, or enhancing UI—contributions are always welcome.

1. Fork the repo
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -m 'Add feature xyz'`)
4. Push to the branch (`git push origin feature-xyz`)
5. Open a Pull Request

---

---
🙋 Author
---------
👨‍💻 Prince Chauhan  
🔗 GitHub: https://github.com/PrinceChauhanhub
---
