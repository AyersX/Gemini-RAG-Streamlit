from config.settings import USER_AVATAR, AI_AVATAR
from rag.llm_client import GeminiClient
from rag.memory import FileMemory
from rag.retriever import Retriever

import streamlit as st
import time


class MainPage:
  def __init__(self):
    if "chat_history" not in st.session_state:
      st.session_state["chat_history"] = []
    if "retriever" not in st.session_state:
      st.session_state.retriever = Retriever()
    if "client" not in st.session_state:
      st.session_state.client = GeminiClient()
    if "memory" not in st.session_state:
      st.session_state.memory = FileMemory()

    self.Client = st.session_state.client
    self.Retriever = st.session_state.retriever
    self.Memory = st.session_state.memory

  def display_chat_disk(self):
    if "chat_disk" not in st.session_state:
      st.session_state["chat_disk"] = self.Memory.load_dict_chat()
    status = ""
    if st.session_state["chat_disk"] and status:
      try:
        for chat in st.session_state.chat_disk:
          logo = USER_AVATAR if chat["role"] == "user" else AI_AVATAR
          with st.chat_message(chat["role"], avatar=logo):
            st.markdown(chat["content"])
        status = "done"
      except Exception as e:
        st.session_state["chat_disk"] = []
        print(f"DEBUGG display_chat_disk: {e}")

  def display_chat(self):
    for chat in st.session_state["chat_history"]:
      logo = USER_AVATAR if chat["role"] == "user" else AI_AVATAR
      with st.chat_message(chat["role"], avatar=logo):
        st.markdown(chat["content"])
        if "token_info" in chat and chat["token_info"]:
          st.caption(chat["token_info"])

  def retrieve_knowledge(self, query):
    if st.session_state.chunks:
      with st.spinner("looking relevant data from knowledge"):
        try:
          chunks = st.session_state.chunks
          index = st.session_state.index
          knowledge = self.Retriever.retrieve(query, index, chunks)
          return knowledge
        except Exception as e:
          print(f"DEBUG RETRIEVE_KNOWLEDGE: {e}")
          raise e
    else:
      return "Knowledge is empty"

  def built_prompt(self, query):
    LIST_CHAT = self.Memory.load_history()
    KNOWLEDGE = self.retrieve_knowledge(query)

    ALL_PROMPTS = f"""
<KNOWLEDGE>
{KNOWLEDGE}
<END OF KNOWLEDGE>\n
<CHATS HISTORY>
{LIST_CHAT}
<END OF CHAT HISTORY>\n
<USER INPUT>
{query}
<END OF USER INPUT>\n""".strip()
    return ALL_PROMPTS

  def ai_response(self, query, all_prompt):
    max_retries = 5
    delay_retry = 3
    response_succeed = False
    for attempt in range(max_retries):
      try:
        ai_resp, token_info = self.Client.get_response(all_prompt)
        response_succeed = True
        break
      except Exception as e:
        print(f"DEBUGG AI_RESPONSE: {attempt + 1} failed: {e}")
        if attempt < max_retries - 1:
          st.warning("server in high demand or check your api rate limit")
          st.info(f"retrying in {delay_retry} second (attempt {attempt + 1}/{max_retries})")
          time.sleep(delay_retry)
        else:
          st.error("failed to connect, try again later")
          raise e
    if response_succeed:
      ai_content = {"role": "ai", "content": ai_resp, "token_info": token_info}
      st.session_state["chat_history"].append(ai_content)
      self.Memory.save_chat(query, ai_resp)
      print(all_prompt)
      st.rerun()

  def run(self):
    st.title("AyersX AI")

    self.display_chat_disk()
    self.display_chat()

    with st.form(key="user", clear_on_submit=True):
      query = st.text_area(
        "chat with AyersX..", placeholder="Chat with AyersX", label_visibility="collapsed"
      )
      submit_button = st.form_submit_button("Send")

    if submit_button:
      if query:
        with st.spinner("thinking"):
          try:
            st.session_state["chat_history"].append({"role": "user", "content": query})
            all_prompt = self.built_prompt(query)
            self.ai_response(query, all_prompt)
          except Exception as e:
            print(f"DEBUGG USER INPUT: {e}")
      else:
        st.warning("input your questions first")
