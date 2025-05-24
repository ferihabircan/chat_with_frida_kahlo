# frida_chatbot_project/app.py
import gradio as gr
# Import the LLM interaction function (only text)
from llm_interaction import get_frida_response
# Import the TTS utility function
from tts_utils import generate_audio_file
import config # Import config for availability flags and temp directory info
import os # Needed for os.path.exists in play_saved_audio

def process_user_message(message: str, history: list):
    """
    Processes user input, updates chat history with AI text response,
    and generates audio for the AI response.

    Args:
        message: The user's latest message (str).
        history: The current chat history list from gr.Chatbot (list of tuples).

    Returns:
        A tuple containing:
        - The updated chat history list for gr.Chatbot.
        - The path to the generated audio file (str) or None.
    """
    # 1. Get AI Text Response using the existing llm_interaction logic
    print(f"Calling get_frida_response for text for message: {message}")
    ai_response_text = get_frida_response(message, history) # Use the original function

    # 2. Append the user message and AI response to the history for the chatbot display
    # The chat history format for Gradio's Chatbot is list of lists: [[user, bot], ...]
    history = history + [[message, ai_response_text]]
    print("Chat history updated for display.")

    # 3. Generate Audio using the new tts_utils function
    print(f"Calling generate_audio_file for text: {ai_response_text[:50]}...")
    audio_filepath = generate_audio_file(ai_response_text) # Use the new TTS function

    # 4. Return the updated history and the audio file path
    # These will be used by Gradio to update the chatbot and the gr.State component.
    return history, audio_filepath

# --- Function to play the audio ---
# This function is called when the "AI Cevabını Oku" button is clicked.
# It receives the audio file path from the gr.State and returns it to the gr.Audio component.
def play_saved_audio(audio_path: str | None):
    """
    Receives the path to the audio file and returns it to the gr.Audio component for playback.
    Gradio's gr.Audio can play directly from a file path string or a tuple (sample_rate, numpy_array).
    Returning the file path string is the simplest method here.
    """
    print(f"Attempting to play audio from path: {audio_path}")
    if audio_path and os.path.exists(audio_path):
        print(f"Playing audio from: {audio_path}")
        return audio_path
    else:
        print("No valid audio path provided or file not found for playback.")
        return None # Return None to clear the audio player

# --- Helper function to clean up temp files (can be triggered manually or on startup/shutdown) ---
def run_cleanup():
    """Simple wrapper to call the cleanup function from tts_utils."""
    cleanup_old_audio_files(age_seconds=600) # Clean files older than 10 minutes (adjust as needed)
    # You could return a message to display cleanup status in the UI if you add an output component


# --- Define constants ---
frida_avatar_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Frida_Kahlo%2C_by_Guillermo_Kahlo.jpg/440px-Frida_Kahlo%2C_by_Guillermo_Kahlo.jpg"
frida_title = "Chat with Frida Kahlo"
frida_description = "Ask me anything, mi amor. I'll share my thoughts, my art, my life, with all the passion of my Mexican heart! (TTS powered by Eleven Labs)"


# --- Gradio Blocks Interface ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="purple", secondary_hue="yellow")) as demo:
    gr.Markdown(f"## {frida_title}")
    gr.Markdown(frida_description)

    # --- Chatbot Component ---
    # This component displays the text conversation history.
    chatbot = gr.Chatbot(
        height=400, # Adjusted height to make space for audio player
        label="Frida Kahlo",
        avatar_images=(None, frida_avatar_url),
       
        # Default format is list of lists [[user, bot], ...], no need for type='messages' here
    )

    # --- User Input Area ---
    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Type your question or thought here for Frida...",
            label="Your Message to Frida:",
            scale=4 # Give textbox more space
        )
        send_button = gr.Button("Gönder", scale=1)

    # --- Audio Playback Area ---
    with gr.Column(): # Use a column to stack button and audio player vertically
         # --- State to hold the audio file path ---
         # This is crucial for passing the file path from the processing function
         # to the audio playback function. It persists state between function calls.
         audio_filepath_state = gr.State(None)

         # --- Play Audio Button ---
         play_audio_button = gr.Button(
             "AI Cevabını Oku",
             interactive=False # Initially disabled until audio is ready
         )

         # --- Audio Player Component ---
         audio_output = gr.Audio(
             label="Frida'nın Sesli Cevabı",
             interactive=False, # Prevent users from uploading audio here
             # autoplay=False is the default behavior when receiving a file path
         )

         # Optional: Cleanup button for temporary files
         # cleanup_button = gr.Button("Temizle (Geçici Ses Dosyaları)")
         # cleanup_output = gr.Textbox(label="Temizlik Durumu", interactive=False) # Optional output


    # --- Examples ---
    gr.Examples(
        examples=[
            "Selam, sen kimsin?",
            "Resim yapmayı seviyor musun?",
            "Diego Rivera ile ilişkin nasıldı?",
            "En sevdiğin resim hangisi?"
        ],
        inputs=[user_input],
        # Consider adding outputs to clear the chatbot history and audio state
        # when an example is clicked, before setting the new input.
        # fn=lambda user_msg: (user_msg, [], None), # Returns user message, empty history, None audio
        # outputs=[user_input, chatbot, audio_filepath_state]
        # This requires modifying the gr.Examples call to take an fn and outputs
    )

    # --- Event Handling (Connecting Components and Functions) ---

    # When the "Gönder" button is clicked OR Enter is pressed in the textbox
    # We chain events using .then() to ensure order: process -> update button -> clear input
    submit_event = user_input.submit( # Trigger on Enter key press in textbox
        fn=process_user_message, # Call the main processing function
        inputs=[user_input, chatbot], # Pass user input and current chat history
        outputs=[chatbot, audio_filepath_state] # Update chat history display and the audio state
    ).then(
        # After processing, update the play button's interactive state
        # Button should be interactive IF audio_path_state is not None AND TTS is available
        fn=lambda audio_path: gr.Button(interactive=audio_path is not None and config.ELEVEN_LABS_API_KEY_AVAILABLE),
        inputs=[audio_filepath_state], # Read the updated audio state
        outputs=[play_audio_button] # Update the play button's interactive state
    ).then(
         # After updating the button state, clear the user input textbox
         fn=lambda: "", # Lambda function that returns an empty string
         inputs=None, # No inputs needed for this step
         outputs=[user_input] # Update the user input textbox
    )

    send_button.click( # Trigger on button click
        fn=process_user_message,
        inputs=[user_input, chatbot],
        outputs=[chatbot, audio_filepath_state]
    ).then(
         fn=lambda audio_path: gr.Button(interactive=audio_path is not None and config.ELEVEN_LABS_API_KEY_AVAILABLE),
         inputs=[audio_filepath_state],
         outputs=[play_audio_button]
    ).then(
         fn=lambda: "",
         inputs=None,
         outputs=[user_input]
    )


    # When the "AI Cevabını Oku" button is clicked
    play_audio_button.click(
        fn=play_saved_audio, # Call the function that plays the audio
        inputs=[audio_filepath_state], # Pass the audio file path from the state
        outputs=[audio_output] # Update the audio player component
    )

    # Optional: Link cleanup button
    # if 'cleanup_button' in locals(): # Check if cleanup button was created
    #    cleanup_button.click(
    #        fn=run_cleanup,
    #        inputs=None,
    #        outputs=[cleanup_output] # Update cleanup status message
    #    )


# --- Main execution block ---
if __name__ == "__main__":

    print("Starting Gradio app...")
    demo.launch(
        # allowed_paths parametresine, geçici ses dosyalarınızın bulunduğu dizini ekleyin
        allowed_paths=[config.TEMP_AUDIO_DIR]
        # veya tam yolunu yazabilirsiniz: allowed_paths=[r"C:\Users\ferih\Desktop\temp_audio"]
        # config.TEMP_AUDIO_DIR kullanmak daha iyidir.
        # share=True # İsteğe bağlı: Arayüzü dışa açmak için
    )
   