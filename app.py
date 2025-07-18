import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import traceback

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")
        st.stop()
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Failed to configure Google AI: {str(e)}")
    st.stop()

def get_pdf_text(pdf_docs):
    text = ""
    try:
        if not pdf_docs:
            raise ValueError("No PDF files provided")
        for pdf in pdf_docs:
            try:
                pdf_reader = PdfReader(pdf)
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
                    except Exception as e:
                        st.warning(f"Could not extract text from page {page_num + 1} of {pdf.name}: {str(e)}")
                        continue
            except Exception as e:
                st.error(f"Error reading PDF file {pdf.name}: {str(e)}")
                continue
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF files")
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDFs: {str(e)}")
        return None

def get_text_chunks(text):
    try:
        if not text or not text.strip():
            raise ValueError("No text provided for chunking")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000, 
            chunk_overlap=1000
        )
        chunks = text_splitter.split_text(text) 
        if not chunks:
            raise ValueError("No chunks created from the text")
        return chunks
    except Exception as e:
        st.error(f"Error splitting text into chunks: {str(e)}")
        return None

def get_vector_store(text_chunks):
    try:
        if not text_chunks:
            raise ValueError("No text chunks provided for vector store creation")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
        return True
    except Exception as e:
        st.error(f"Error creating vector store: {str(e)}")
        return False

def get_conversational_chain():
    try:
        prompt_template = """
        Answer the questions from the provided context, make sure to provide all the details. If the answer is not in provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
        Context: \n {context}?\n
        Question: \n{question}\n
        
        Answer:
        """
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        return chain
    except Exception as e:
        st.error(f"Error creating conversational chain: {str(e)}")
        return None

def user_input(user_question):
    try:
        if not user_question or not user_question.strip():
            st.warning("Please enter a valid question")
            return
        # Check if FAISS index exists
        if not os.path.exists("faiss_index"):
            st.error("No processed documents found. Please upload and process PDF files first.")
            return
        with st.spinner("Searching for answer..."):
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            try:
                new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            except Exception as e:
                st.error(f"Error loading vector database: {str(e)}")
                return
            docs = new_db.similarity_search(user_question)
            if not docs:
                st.warning("No relevant documents found for your question.")
                return
            chain = get_conversational_chain()
            if not chain:
                return
            response = chain(
                {
                    "input_documents": docs, 
                    "question": user_question
                },
                return_only_outputs=True
            )
            if response and "output_text" in response:
                st.write("**Reply:**", response["output_text"])
            else:
                st.error("No response generated. Please try again.")
    except Exception as e:
        st.error(f"Error processing your question: {str(e)}")

def main():
    st.set_page_config(
        page_title="Chat with Multiple PDF",
        page_icon="📚",
        layout="wide"
    )
    
    st.header("Chat with Multiple PDF using Gemini♊")
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'pdf_uploaded' not in st.session_state:
        st.session_state.pdf_uploaded = False
    with st.sidebar:
        st.title("Menu:")
        st.markdown("### Upload PDF Files")
        pdf_docs = st.file_uploader(
            "Upload Your PDF Files and Click on the Submit & Process",
            accept_multiple_files=True,
            type=['pdf']
        )
        if pdf_docs:
            st.session_state.pdf_uploaded = True
            st.success(f"{len(pdf_docs)} PDF file(s) uploaded successfully!")    
            if st.button("Submit & Process"):
                if len(pdf_docs) > 0:
                    try:
                        with st.spinner("Processing PDF files..."):
                            raw_text = get_pdf_text(pdf_docs)
                            if raw_text is None:
                                return
                            text_chunks = get_text_chunks(raw_text)
                            if text_chunks is None:
                                return
                            if get_vector_store(text_chunks):
                                st.session_state.processed = True
                                st.success("✅ PDF files processed successfully! You can now ask questions.")
                                st.rerun()
                            else:
                                st.error("Failed to create vector store")
                    
                    except Exception as e:
                        st.error(f"Error during processing: {str(e)}")
                else:
                    st.warning("Please upload at least one PDF file.")
        else:
            st.session_state.pdf_uploaded = False
            st.session_state.processed = False
    
    if st.session_state.processed:
        st.success("📄 PDF files are processed and ready for questions!")
        
        user_question = st.text_input(
            "Ask a Question from the PDF files:",
            placeholder="Enter your question here..."
        )
        
        if st.button("Get Answer", key="get_answer_btn"):
            if user_question:
                user_input(user_question)
            else:
                st.warning("Please enter a question before clicking 'Get Answer'.")
    
    elif st.session_state.pdf_uploaded:
        st.info("📤 PDF files uploaded. Please click 'Submit & Process' to analyze them.")
    
    else:
        st.info("👈 Please upload PDF files from the sidebar to get started.")
        
        st.markdown("""
        ### How to use:
        1. **Upload PDF files** using the sidebar
        2. **Click 'Submit & Process'** to analyze the documents
        3. **Ask questions** about the content once processing is complete
        
        ### Features:
        - Multiple PDF support
        - AI-powered question answering
        - Context-aware responses
        - Error handling and recovery
        """)

if __name__ == "__main__":
    main()