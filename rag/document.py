from config.settings import DOCUMENT_DIR, DOCUMENT_METADATA, FILE_CHUNKS_PATH, CHUNK_SIZE, OVERLAP

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import json
import re
import os


class DocumentProccessor:
  def clean_pdf_text(self, text):
    # replace >= 3 \n to 2 \n
    text = re.sub(r"\n{3,}", "\n\n", text)
    # remove
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    # remove form feed
    text = text.replace("\f", " ")
    # remove 2 space
    text = re.sub(r" {2,}", " ", text).strip()
    return text

  def load_metadata(self):
    try:
      with open(DOCUMENT_METADATA, "r") as file:
        for data in file:
          metadata = json.loads(data.strip())
      return metadata
    except Exception as e:
      raise Exception(f"DEBUG LOAD_METADA: {e}")

  def extract_doc(self, pdf_file):
    if pdf_file:
      try:
        reader = PdfReader(pdf_file)

        text = ""
        for pages in reader.pages:
          text += pages.extract_text()
        return text
      except Exception as e:
        raise Exception(f"DEBUG EXTRACT_DOC: {e}")
    else:
      raise ValueError("pdf is none")

  def make_pdf_chunks(self, pdf_file):
    text = self.extract_doc(pdf_file)
    if text:
      try:
        cleaned_text = self.clean_pdf_text(text)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=OVERLAP)

        chunks = text_splitter.split_text(cleaned_text)
        chunk_format = []
        for row in chunks:
          chunk_format.append(f"passage: {row}")
        self.save_pdf_chunk(chunk_format)
        return chunk_format
      except Exception as e:
        raise Exception(f"DEBUG MAKE_PDF_CHUNK[elif 1]: {e}")

    elif os.path.getsize(FILE_CHUNKS_PATH) > 0:
      try:
        chunks = self.load_chunk()
        return chunks
      except Exception as e:
        raise Exception(f"DEBUG MAKE_PDF_CHUNK[if 1]: {e}")

    else:
      raise ValueError("Text and file chunks is empty, pls run read_doc first")

  def save_pdf_chunk(self, pdf_chunks):
    if os.path.getsize(FILE_CHUNKS_PATH) == 0:
      try:
        with open(FILE_CHUNKS_PATH, "w", encoding="utf-8") as file:
          json.dump(pdf_chunks, file, indent=2, ensure_ascii=False)
        print("save_pdf_chunk")
      except Exception as e:
        raise Exception(f"DEBUG SAVE_PDF_CHUNK: {e}")

    else:
      print("chunks already exists, (not saving data)")

  def load_chunk(self):
    try:
      with open(FILE_CHUNKS_PATH, "r", encoding="utf-8") as file:
        if file:
          chunks = json.load(file)
          return chunks
        else:
          raise ValueError("cannot load chunks(empty)")
    except Exception as e:
      raise Exception(f"DEBUG LOAD_CHUNK: {e}")

  def save_uploaded(self, metadata=None, uploaded=None):
    if metadata:
      try:
        with open(DOCUMENT_METADATA, "a", encoding="utf-8") as file:
          file.write(json.dumps(metadata) + "\n")
        print("saved metadata")
      except Exception as e:
        raise Exception(f"DEBUG SAVE_UPLOADED[metadata]: {e}")

    if uploaded:
      try:
        file_path = DOCUMENT_DIR / uploaded.name
        with open(file_path, "wb") as file:
          file.write(uploaded.getvalue())
          print("saved uploaded file")
      except Exception as e:
        raise Exception(f"DEBUG SAVE_UPLOADED[filename]: {e}")
    if not metadata and not uploaded:
      print("skip save_uploaded")
