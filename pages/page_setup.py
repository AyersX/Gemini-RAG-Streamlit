from rag.llm_client import GeminiClient

import streamlit as st


class PageSetup:
  def __init__(self):
    if "client" not in st.session_state:
      st.session.state.client = GeminiClient()
    self.GC = st.session_state.client

  def cek_env(self):
    status = self.GC.verify_api()
    if status == "valid":
      st.session_state["api_status"] = "valid"
      st.rerun()

    elif status == "invalid":
      st.session_state["api_status"] = "invalid"

    elif status == "empty":
      st.session_state["api_status"] = "empty"

  def session_notif(self):
    if st.session_state["api_status"] == "invalid":
      st.info("built in API key is invalid or expired")

    elif st.session_state["api_status"] == "empty":
      st.info("API key is empty, input new key")

    if st.session_state["api_status"] == "invalid2":
      st.warning("API key is invalid or expired")

    elif st.session_state["api_status"] == "no input":
      st.warning("API key is empty")

  def run(self):
    st.title("⚙️ API Configuration Setup")
    st.divider()
    if st.session_state["api_status"] == "unset":
      self.cek_env()

    self.session_notif()
    if st.session_state["api_status"] != "valid":
      with st.form("form_input_api"):
        api_input = st.text_input("API KEY", type="password")
        submit_btn = st.form_submit_button("Apply")

      if submit_btn:
        if api_input:
          with st.spinner("Verify.."):
            status = self.GC.verify_api(api_input)
            if status == "valid":
              st.session_state["api_status"] = "valid"
              st.success("succeed")
              st.rerun()
            elif status == "invalid":
              st.session_state["api_status"] = "invalid2"
              st.rerun()
            elif status == "empty":
              st.session_state["api_status"] = "empty"
              st.rerun()
        else:
          st.session_state["api_status"] = "no input"
          st.rerun()

    if st.session_state["api_status"] == "valid":
      st.info("API key already exists")
      if st.button("➜]Logout API key"):
        st.session_state["api_status"] = "unset"
        st.rerun()
