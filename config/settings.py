from pathlib import Path

# Base directory path
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
# Filepath
HISTORY_PATH = Path(STORAGE_DIR / "history.jsonl")
SYS_PROMPT_PATH = Path(STORAGE_DIR / "prompts.txt")


# --- Streamlit ---
USER_AVATAR = "😎"
AI_AVATAR = "✨"


# --- RAG Configuration ---

# Sentence Transformer Model
EMBEDDING_MODEL = "intfloat/multilingual-e5-base"
# Chunk config
CHUNK_SIZE = 2048
OVERLAP = 0

# Top K config
TOP_K_RETRIEVAL = 5
THRESHOLD: float = 0.372


# Folderpath
DOCUMENT_DIR = Path(STORAGE_DIR / "documents")


# Filenames for FAISS index and chunk metadata
FILE_INDEX_PATH = DOCUMENT_DIR / "knowledge.bin"
FILE_CHUNKS_PATH = DOCUMENT_DIR / "knowledge_chunks.json"
DOCUMENT_METADATA = DOCUMENT_DIR / "document_metadata.jsonl"


def run_settings():
  # Folder maker
  STORAGE_DIR.mkdir(parents=True, exist_ok=True)
  DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)

  # File maker
  HISTORY_PATH.touch(exist_ok=True)
  SYS_PROMPT_PATH.touch(exist_ok=True)

  FILE_INDEX_PATH.touch(exist_ok=True)
  FILE_CHUNKS_PATH.touch(exist_ok=True)

  DOCUMENT_METADATA.touch(exist_ok=True)
