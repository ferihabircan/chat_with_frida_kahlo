# frida_chatbot_project/config.py
import os
# Import the correct class for chat models from LangChain Google Generative AI
from langchain_google_genai import ChatGoogleGenerativeAI

# Variable to hold the API key value found
_api_key_value = None

# --- Priority Order for finding the API Key ---

# 1. Try importing from api_key.py (as specified by the user)
try:
    from api_key import GEMINI_API_KEY as imported_api_key
    _api_key_value = imported_api_key
   
except ImportError:
    # api_key.py doesn't exist or doesn't contain GEMINI_API_KEY
    pass
except AttributeError:
     # api_key.py exists but doesn't contain GEMINI_API_KEY

    pass


# 2. If not found from api_key.py, try GOOGLE_API_KEY environment variable (LangChain standard)
if _api_key_value is None:
    _api_key_value = os.getenv("GOOGLE_API_KEY")
 

# 3. If not found, try GEMINI_API_KEY environment variable (backward compatibility/older naming)
if _api_key_value is None:
     _api_key_value = os.getenv("GEMINI_API_KEY")
     

# --- End of Priority Check ---

# Check if an API key was found
if not _api_key_value:
    print(" API key not found in api_key.py, GOOGLE_API_KEY env, or GEMINI_API_KEY env.")
    GOOGLE_API_KEY_AVAILABLE = False
    LLM = None
else:
    GOOGLE_API_KEY_AVAILABLE = True
    try:
        # Instantiate the ChatGoogleGenerativeAI model
        # Use a chat model like "gemini-pro" or "gemini-1.5-flash"
        # temperature=0.7 matches your original desire.
        LLM = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", # Or "gemini-1.5-flash"
            temperature=0.7,
            # Pass the found API key explicitly to the model constructor
            google_api_key=_api_key_value
        )
       
    except Exception as e:
        # Catch potential errors during model initialization (e.g., invalid key)
        print(f" Error initializing ChatGoogleGenerativeAI model: {e}")
        GOOGLE_API_KEY_AVAILABLE = False
        LLM = None

# Keep this alias for compatibility with llm_interaction import
GEMINI_API_KEY_AVAILABLE = GOOGLE_API_KEY_AVAILABLE