# AItalent
# 実行
streamlit run Main.py

# ファイル構成
- Main.py
- text_samples.py
- comment_samples.py
- env.py
- .env

env.py
# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
load_dotenv()

# 環境変数を参照
import os
openai_key = os.getenv('openai_key')

.env
openai_key = @@@@@@@@@@ #自分のOpenAI key
