# AItalent
# 実行
streamlit run Main.py

# ファイル構成
- Main.py
- text_samples.py
- comment_samples.py
- env.py
- .env

# env.py
from dotenv import load_dotenv
load_dotenv()

import os
openai_key = os.getenv('openai_key')

# .env
openai_key = @@@@@@@@@@@@@@@  #自分のOpenAI key
