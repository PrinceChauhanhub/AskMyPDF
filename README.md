# AskMyPDF 📚

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


## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/PrinceChauhanhub/AskMyPDF.git
cd AskMyPDF

2. Create and activate a virtual environment

conda create -p venv python==3.10 -y
conda activate venv/

3. Install dependencies

pip install -r requirements.txt

4. Set up your .env file

GOOGLE_API_KEY=your_google_generative_ai_key

5. Run the App
streamlit run app.py
