# frida_chatbot_project/app.py
import gradio as gr
from llm_interaction import get_frida_response
import config

# Check if API key is available (this can be here)
if not config.GEMINI_API_KEY_AVAILABLE:
    print("WARNING: Google AI API key not available. Chatbot will provide placeholder responses.")
else:
     if config.LLM is not None:
         print("-----------------------------------------------")
     else:
         print("⚠️ Google AI API key is available, but LLM initialization failed. Check config.py output.")

# --- THIS FUNCTION DEFINITION MUST COME BEFORE THE CHATINTERFACE CALL ---
def chat_with_frida(message, chat_history):
    """
    Handles the chat interaction for Gradio.
    'chat_history' is a list of tuples: [(user_msg1, bot_msg1), (user_msg2, bot_msg2), ...]
    """
    # print(f"DEBUG: Message: {message}, History: {chat_history}") # For debugging
    bot_message = get_frida_response(message, chat_history)
    return bot_message
# --- END OF FUNCTION DEFINITION ---


# Define constants (can be here or before the function, but must be before use)
frida_avatar_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Frida_Kahlo%2C_by_Guillermo_Kahlo.jpg/440px-Frida_Kahlo%2C_by_Guillermo_Kahlo.jpg"


# --- THE CHATINTERFACE INSTANTIATION COMES AFTER THE FUNCTION IS DEFINED ---
chat_interface = gr.ChatInterface(
    fn=chat_with_frida, # This name must be defined above this line
    title="Chat with Frida Kahlo",
    description="Ask me anything, mi amor. I'll share my thoughts, my art, my life, with all the passion of my Mexican heart! (This chatbot embodies Frida Kahlo and will use your RAG documentation once integrated.)",
    chatbot=gr.Chatbot(
        height=600,
        label="Frida Kahlo",
        avatar_images=(None, frida_avatar_url),
        type='messages' # Explicitly set type to suppress warning and match llm_interaction.py
    ),
    textbox=gr.Textbox(
        placeholder="Type your question or thought here for Frida...",
        label="Your Message to Frida:"
    ),
    examples=[
        "Selam,sen Kimsin?",
        "Resim yapmayı seviyor musun?",
        "Diego Rivera ile ilişkin nasıldı?"
        "En sevdiğin resim hangisi?"

    ],
    theme=gr.themes.Soft(primary_hue="purple", secondary_hue="yellow"),
    type='messages', # Explicitly set type to suppress warning
    # Ensure retry_btn, undo_btn, clear_btn are removed as per previous fix
)
# --- END OF CHATINTERFACE INSTANTIATION ---


# --- The main execution block comes last ---
if __name__ == "__main__":

    if not config.GEMINI_API_KEY_AVAILABLE:
        print("\n**************************************************************************")
        print("WARNING: GOOGLE_API_KEY is not set or LLM failed to initialize.")
        print("The chatbot will likely respond with a message about API key issues.")
        print("Please set the GOOGLE_API_KEY environment variable and restart.")
        print("**************************************************************************\n")
    chat_interface.launch()
# --- END OF MAIN BLOCK ---