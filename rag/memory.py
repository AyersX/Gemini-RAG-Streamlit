from config.settings import HISTORY_PATH, SYS_PROMPT_PATH

import json
from pathlib import Path
from collections import deque
from datetime import datetime
from zoneinfo import ZoneInfo
from pypdf import PdfReader


class FileMemory:
  def load_dict_chat(self, limit=5):
    if HISTORY_PATH.stat().st_size == 0:
      print("history file is empty")
      return ""

    with HISTORY_PATH.open(encoding="utf-8") as file:
      last_lines = deque(maxlen=limit)
      for line in file:
        last_lines.append(line)

    history_list = []
    for row in last_lines:
      try:
        data = json.loads(row)
        history_list.append({"role": "user", "content": data.get("user", "")})
        history_list.append({"role": "ai", "content": data.get("ai", "")})
      except Exception as e:
        print(f"DEBUGG load_dict_chat: {e}")
        raise e
    return history_list

  def load_history(self, limit=15):
    if HISTORY_PATH.stat().st_size == 0:
      print("history file is empty")
      return "history is empty"

    with HISTORY_PATH.open(encoding="utf-8") as file:
      last_lines = deque(maxlen=limit)
      for line in file:
        last_lines.append(line)

    chats = ""
    for row in last_lines:
      data = json.loads(row)
      chats += f"timestamp: {data['timestamp']}\nuser: {data['user']}\nai: {data['ai']}\n\n\n"
    return chats

  def save_chat(self, user, ai):
    if user and ai:
      current_time = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%A, %d-%m-%Y %H:%M")

      chat = {"timestamp": current_time, "user": user, "ai": ai}
      with HISTORY_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(chat, ensure_ascii=False) + "\n")
        print("auto saved chat")
    else:
      print("no data was saved")

  def sys_prompt(self):
    if SYS_PROMPT_PATH.stat().st_size == 0:
      print("prompt is empty")
      return "Default"
    else:
      prompts = SYS_PROMPT_PATH.read_text(encoding="utf-8")
      return prompts
