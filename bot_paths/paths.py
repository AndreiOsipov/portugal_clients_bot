import os


ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
TOKENS_PATH = os.path.join(ROOT, "tokens")
BOT_TOKEN = os.path.join(TOKENS_PATH, "bot_token.json")
GOOGLE_API_TOKEN_PATH = os.path.join(TOKENS_PATH, "token.json")
GOOGLE_API_CREDS_PATH = os.path.join(TOKENS_PATH, "credentials.json")