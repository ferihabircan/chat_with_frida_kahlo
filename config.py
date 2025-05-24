# frida_chatbot_project/config.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Define Temporary Audio Directory ---
# Geçici ses dosyaları için yeni bir klasör.
# Projenizin kök dizininde 'temp_audio' adında bir klasör oluştururuz.
# __file__ -> config.py'nin yolu
# os.path.dirname(__file__) -> config.py'nin bulunduğu klasör (örneğin, frida_chatbot_project/)
# os.path.join(..., "..") -> Bir üst klasöre çık (proje kökü)
# os.path.join(..., "temp_audio") -> temp_audio klasörünün tam yolu
TEMP_AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "temp_audio")

# Klasörün var olduğundan emin olun, yoksa oluşturun
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
print(f"Geçici ses dosyaları klasörü: {TEMP_AUDIO_DIR}")


# --- API Key Handling Logic ---

# Variables to hold the API key values found
_gemini_key_value = None
_elevenlabs_key_value = None

# 1. Try importing from api_key.py
try:
    from api_key import GEMINI_API_KEY as imported_gemini_api_key
    _gemini_key_value = imported_gemini_api_key
    print("Gemini API key found in api_key.py")
except ImportError:
    print(" api_key.py not found or GEMINI_API_KEY not defined in it.")
except AttributeError:
     print(" GEMINI_API_KEY not defined in api_key.py.")

try:
    from api_key import ELEVEN_LABS_API_KEY as imported_elevenlabs_api_key
    _elevenlabs_key_value = imported_elevenlabs_api_key
    print("Eleven Labs API key found in api_key.py")
except ImportError:
    print(" api_key.py not found or ELEVEN_LABS_API_KEY not defined in it.")
except AttributeError:
    print(" ELEVEN_LABS_API_KEY not defined in api_key.py.")


# 2. If not found from api_key.py, try Environment Variables
if _gemini_key_value is None:
    _gemini_key_value = os.getenv("GOOGLE_API_KEY")
    if _gemini_key_value:
        print("Gemini API key found in GOOGLE_API_KEY env var.")
    else:
         _gemini_key_value = os.getenv("GEMINI_API_KEY") # Also check GEMINI_API_KEY env var
         if _gemini_key_value:
              print("Gemini API key found in GEMINI_API_KEY env var.")
         else:
             print(" Gemini API key not found in environment variables (GOOGLE_API_KEY or GEMINI_API_KEY).")


if _elevenlabs_key_value is None:
     _elevenlabs_key_value = os.getenv("ELEVEN_LABS_API_KEY")
     if _elevenlabs_key_value:
          print("Eleven Labs API key found in ELEVEN_LABS_API_KEY env var.")
     else:
         print(" Eleven Labs API key not found in environment variable (ELEVEN_LABS_API_KEY).")


# --- Check Availability and Initialize LLM ---

GEMINI_API_KEY_AVAILABLE = _gemini_key_value is not None
ELEVEN_LABS_API_KEY_AVAILABLE = _elevenlabs_key_value is not None
ELEVEN_LABS_API_KEY = _elevenlabs_key_value # Eleven Labs key'i dışa aktarıyoruz, tts_utils kullanacak

LLM = None # Initialize LLM variable

if not GEMINI_API_KEY_AVAILABLE:
    print(" ERROR: Google AI API key not found. LLM will not be initialized.")
    print(" Please provide key in api_key.py or as GOOGLE_API_KEY/GEMINI_API_KEY env var.")
else:
    try:
        # Instantiate the ChatGoogleGenerativeAI model using the found key
        LLM = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", # Or your preferred Gemini chat model
            temperature=0.7,
            google_api_key=_gemini_key_value # Pass the found key
        )
        print(" ChatGoogleGenerativeAI model initialized successfully.")

    except Exception as e:
        # Catch potential errors during model initialization (e.g., invalid key)
        print(f" ERROR initializing ChatGoogleGenerativeAI model: {e}")
        GEMINI_API_KEY_AVAILABLE = False # Mark as unavailable if init failed
        LLM = None # Ensure LLM is None on failure


if not ELEVEN_LABS_API_KEY_AVAILABLE:
     print(" WARNING: Eleven Labs API key not found. Text-to-Speech will be disabled.")
     print(" Please provide key in api_key.py or as ELEVEN_LABS_API_KEY env var.")
else:
    print(" Eleven Labs API key is available.")


# Note: LLM, API key values, and availability flags are exported for other modules to use.
# TEMP_AUDIO_DIR is also exported.