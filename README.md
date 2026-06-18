# AyersX AI Chatbot

## Project Description

AyersX AI is an interactive chatbot application built with Streamlit and powered by the Google Gemini API. This project lets users upload PDF documents to create a knowledge base. The AI can then answer questions by finding relevant information from these documents. It also saves chat history and has an easy way to manage API keys.

## Key Features

*   **Interactive User Interface:** Made with Streamlit for a simple and responsive user experience.
*   **Retrieval Augmented Generation (RAG):** Combines information retrieval from uploaded documents to give more accurate and relevant answers.
*   **Google Gemini API Integration:** Uses the Gemini large language model for smart and natural responses.
*   **PDF Document Processing:** Can get text from PDF files, split them into "chunks," and create "embeddings" for the knowledge base.
*   **Vector Search with FAISS:** Uses FAISS for fast and efficient vector storage and search, with Sentence Transformers for creating embeddings.
*   **Data Persistence:** Saves chat history, document chunks, and vector index locally so data is not lost.
*   **API Key Configuration:** A special page to set up and check your Google Gemini API key.
*   **Error Handling & Retries:** Includes a retry system for API calls to make the application more robust.

## Technologies Used

*   **Python** (version 3.10.20)
*   **Streamlit:** For building the web user interface.
*   **Google Gemini API:** The large language model for text generation.
*   **FAISS:** For efficient vector similarity search.
*   **Sentence Transformers:** To create vector embeddings from text.
*   **LangChain Text Splitters:** To divide documents into smaller pieces (chunks).
*   **PyPDF:** For extracting text from PDF files.
*   **python-dotenv:** For managing environment variables (like API keys).

## Installation

Follow these steps to set up and run the project on your computer:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/AyersX/Gemini-RAG-Streamlit.git
    cd Gemini-RAG-Streamlit
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    This project uses `pyproject.toml` for dependency management. You can install dependencies using `uv` (recommended for speed) or `pip`.

    **Using `uv` (Recommended):**
    First, install `uv` if you haven't already:
    ```bash
    pip install uv
    ```
    Then, install the project dependencies:
    ```bash
    uv pip install -e .
    ```

    **Using `pip`:**
    You can install dependencies directly from `pyproject.toml` using `pip`:
    ```bash
    pip install .
    ```
    *(Alternatively, you can generate a `requirements.txt` from `pyproject.toml` using `uv pip freeze > requirements.txt` and then `pip install -r requirements.txt`.)*

4.  **Set Up Google Gemini API Key:**
    *   Get your API Key from Google AI Studio.
    *   Create a file named `.env` in the main project folder and add your API key like this:
        ```
        GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
        ```

## Usage

1.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```
    The app will open in your web browser (usually at `http://localhost:8501`).

2.  **Configure API Key:**
    *   When you first run it, you will go to the "API setup" page.
    *   The app will try to check the API key from your `.env` file. If it's not found or not valid, you can type your API key there.

3.  **Upload Documents (RAG Page):**
    *   Go to the "RAG" page (📚 icon).
    *   Use the file uploader to add your PDF documents.
    *   Click the "import" button to process and index the documents.
    *   You can also click "Load" to load existing knowledge.

4.  **Chat with the Chatbot (Chatbot AI Page):**
    *   Go to the "Chatbot AI" page (💬 icon).
    *   Start asking questions. The AI will use the knowledge from your uploaded documents to give relevant answers.

## Project Structure
```
.
├── app.py                      # Main Streamlit application
├── config/                     # Project configuration settings
│   └── settings.py             # Global configuration variables
├── pages/                      # Streamlit page modules
│   ├── chat_page.py            # Chatbot interface page
│   ├── context_page.py         # Page to manage RAG documents
│   └── page_setup.py           # Page for API key configuration
├── rag/                        # Core RAG components
│   ├── document.py             # Document processing (extraction, chunking)
│   ├── embedd.py               # Embedding creation and FAISS index
│   ├── llm_client.py           # Client for Google Gemini API interaction
│   ├── memory.py               # Chat history and system prompt management
│   └── retriever.py            # Logic for retrieving information from the index
├── storage/                    # Directory for persistent data (created automatically)
│   ├── documents/              # Stores uploaded PDF files, FAISS index, metadata
│   ├── history.jsonl           # Chat history
│   └── prompts.txt             # System prompt
└── pyproject.toml              # Project metadata and dependencies
```
## Future Development & Improvements

This project can be improved further, including:

*   **Better Knowledge Update Workflow:** Allow adding or updating knowledge documents more easily without replacing the whole database.
*   **More Flexible RAG Configuration:** Add options to change chunking parameters (like `OVERLAP`) and retrieval threshold (`THRESHOLD`) through the user interface.
*   **System Prompt Editor:** Provide a user interface to edit the AI's system prompt directly.
*   **Multi-Document Management:** Support managing and searching across several documents at the same time.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
