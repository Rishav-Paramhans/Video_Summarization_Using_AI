from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv('GOOGLE_GEMINI_API_KEY'))