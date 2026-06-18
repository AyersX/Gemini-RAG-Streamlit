from rag.memory import FileMemory

from google import genai
from google.genai import types
from google.genai.types import Tool
from dotenv import load_dotenv
import os


class GeminiClient:
  def __init__(self):
    self.sys_prompt = FileMemory().sys_prompt()
    load_dotenv()
    env_api_key = os.getenv("GOOGLE_API_KEY")
    self.api_key = env_api_key if env_api_key else None
    self.client = None

  def verify_api(self, api_input=None):
    self.api_key = api_input if api_input else self.api_key
    if self.api_key:
      try:
        self.client = genai.Client(api_key=self.api_key)
        self.client.models.list(config={"page_size": 1})
        return "valid"
      except:
        self.client = None
        return "invalid"
    else:
      return "empty"

  def model_config(self):
    ai_config = types.GenerateContentConfig(
      system_instruction=self.sys_prompt,
      max_output_tokens=65000,
      temperature=0.2,
      thinking_config=types.ThinkingConfig(thinking_budget=8000),
      tools=[Tool(google_search=types.GoogleSearch())],
    )
    return ai_config

  def get_response(self, all_prompt):
    if self.client is not None:
      try:
        response_obj = self.client.models.generate_content(
          model="gemini-2.5-flash", contents=all_prompt, config=self.model_config()
        )
        token_info_str = self.get_token_info(response_obj)
        ai_text = response_obj.text
        if ai_text is None:
          if response_obj.candidates:
            finish_reason = response_obj.candidates[0].finish_reason
            raise ValueError(f"DEBUG AI TEXT: {finish_reason})")

        return ai_text, token_info_str
      except Exception as e:
        raise Exception(f"DEBUGG LLM: {e}")
    else:
      raise RuntimeError("DEBUGG LLM: SELF CLIENT IS NONE")

  def get_token_info(self, response_object):
    if response_object and response_object.usage_metadata:
      return f"""📊 Token Input:{response_object.usage_metadata.prompt_token_count} | Output: {response_object.usage_metadata.candidates_token_count}"""

    print("token info empty")
    return "None"
