from config.settings import run_settings
from rag.document import DocumentProccessor
from rag.embedd import Embedding

import streamlit as st
import os
import json
from pathlib import Path
from datetime import datetime


class KnowledgePage:
  def __init__(self):
    self.setup_file = ""
    if not self.setup_file:
      run_settings()
      self.setup_file = "Done"
    if "chunks" not in st.session_state:
      st.session_state.chunks = []
    if "index" not in st.session_state:
      st.session_state.index = None
    if "metadata" not in st.session_state:
      st.session_state.metadata = []
    if "Proccessor" not in st.session_state:
      st.session_state.Proccessor = DocumentProccessor()
    if "Embedding" not in st.session_state:
      st.session_state.Embedding = Embedding()

    self.Doc = st.session_state.Proccessor
    self.Embedd = st.session_state.Embedding

  def display_upload_section(self):
    with st.form("upload pdf"):
      uploaded_file = st.file_uploader("choose file", type="pdf", label_visibility="collapsed")
      submit_btn = st.form_submit_button("import")
      load_btn = st.form_submit_button("Load")

    if submit_btn and uploaded_file:
      with st.spinner("first time loading may take a while.."):
        print(f"tipe pdf{type(uploaded_file)}")
        self.handle_file(uploaded_file)
    elif load_btn:
      self.handle_file()

  def handle_file(self, file=None):
    if file:
      try:
        chunks = self.Doc.make_pdf_chunks(file)
        st.session_state.chunks = chunks
        index = self.Embedd.vector_index(chunks)
        st.session_state.index = index
        print("added index and chunks to session")
        document_metadata = {
          "name": file.name,
          "size": file.size,
          "timestamp": datetime.now().isoformat(timespec="seconds"),
          "num_chunks": len(chunks),
        }
        self.Doc.save_uploaded(document_metadata, file)
        st.session_state.metadata.append(document_metadata)
      except Exception as e:
        st.session_state.index = None
        st.session_state.index = []
        st.session_state.chunks = []
        raise Exception(f"DEBUGG HANDLE_FILE: {e}")

    elif not file:
      try:
        load_chunks = self.Doc.load_chunk()
        st.session_state.chunks = load_chunks
        index = self.Embedd.vector_index(load_chunks)
        st.session_state.index = index
        print("load succeed. index and chunks to session")
        metadata_load = self.Doc.load_metadata()
        st.session_state.metadata.append(metadata_load)

      except Exception as e:
        st.session_state.index = None
        st.session_state.chunks = []
        st.session_state.chunks = []
        raise Exception(f"DEBUGG HANDLE_FILE: {e}")

  def display_uploaded_file(self):
    if st.session_state.metadata:
      for data in st.session_state.metadata:
        st.caption(data["name"])
        break

    else:
      st.caption("no data was added")

  def run(self):
    st.title("Upload pdf to AyersX")

    self.display_upload_section()
    self.display_uploaded_file()
