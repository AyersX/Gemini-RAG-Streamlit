import streamlit as st
from pages.chat_page import MainPage
from pages.context_page import KnowledgePage
from pages.page_setup import PageSetup


st.set_page_config(page_title="AyersX AI", page_icon="🤖", layout="wide")

if "api_status" not in st.session_state:
  st.session_state["api_status"] = "unset"

chat_page = st.Page(MainPage().run, title="Chatbot AI", icon="💬", url_path="chat")

context_page = st.Page(KnowledgePage().run, title="RAG", icon="📚", url_path="knowledge")

setup_page = st.Page(PageSetup().run, title="API setup", icon="⚙️", url_path="setup-api")


if st.session_state["api_status"] == "valid":
  navigation_menu = st.navigation([chat_page, context_page, setup_page], position="sidebar")

else:
  navigation_menu = st.navigation([setup_page], position="sidebar")


navigation_menu.run()
