# frida_chatbot_project/llm_interaction.py

# Import the LLM instance and availability status from config
# Make sure GEMINI_API_KEY_AVAILABLE is actually GOOGLE_API_KEY_AVAILABLE based on your config
from config import LLM, GOOGLE_API_KEY_AVAILABLE # Assuming it's renamed in config
from persona import FRIDA_PERSONA_PROMPT
from rag_system import retrieve_relevant_info_tr # Assuming this is correctly implemented now

# Import message types for LangChain Chat Models
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- GÜVENLİK FİLTRELERİNİ İMPORT ET ---
# security_filters.py dosyasından sanitize fonksiyonlarını import ediyoruz.
# Bunlar doğrudan isimleriyle çağrılacak.
from security_filters import sanitize_input, sanitize_output # <-- Bu import doğru

# Update the function signature comment to reflect the new history type
# 'history' is now a list of dictionaries: [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
def get_frida_response(user_message: str, history: list):
    """
    Generates Frida Kahlo's response using LLM and RAG via LangChain.
    Includes basic input and output filtering using functions from security_filters.py.
    'history' is a list of dictionaries (from Gradio type='messages'):
    [{'role': 'user', 'content': 'user message'}, {'role': 'assistant', 'content': 'bot message'}, ...]
    """
    # Use the renamed availability check and the LLM instance
    # Check for GOOGLE_API_KEY_AVAILABLE
    if not GOOGLE_API_KEY_AVAILABLE or LLM is None:
        return "Ay, mi amor, Please try again."

    # --- GİRDİ FİLTRELEME ADIMI ---
    # Kullanıcı mesajını LLM'e göndermeden önce filtrele.
    # sanitize_input fonksiyonunu doğrudan ismiyle çağırıyoruz.
    sanitized_message = sanitize_input(user_message) # <-- Burası düzeltildi

    # Eğer sanitize_input özel bir hata sinyali döndürürse (isteğe bağlı olarak sanitize_input içinde belirlendiyse)
    # if sanitized_message == "SYSTEM_ERROR_SUSPICIOUS_INPUT":
    #     return "Ay, mi amor, I sensed something strange in your message. Could you please rephrase it?"


    # 1. Retrieve relevant information (RAG step)
    # RAG çekimi için orijinal user_message'i kullanmak genellikle daha iyidir.
    # Filtreleme, RAG sorgusunun anlamını bozabilir.
    retrieved_context = retrieve_relevant_info_tr(user_message)
    # print(f"DEBUG: Retrieved context: {retrieved_context[:100]}...") # For debugging

    # 2. Prepare messages for the LLM using LangChain message types
    # Sistem mesajı her zaman ilk sırada olmalı ve en güçlü kısıtlamaları içermeli
    messages = [SystemMessage(content=FRIDA_PERSONA_PROMPT)]

    # Add past conversation history (if any)
    # Convert history messages (from Gradio type='messages') to LangChain message types
    for message in history:
        role = message.get('role')
        content = message.get('content')

        if role == 'user':
            # Geçmiş kullanıcı mesajlarını filtrelemek isteyebilirsiniz, ancak bu karmaşık olabilir.
            # Basitlik adına şimdilik geçmişi filtrelemiyoruz, sadece o anki girdiyi filtreliyoruz.
            messages.append(HumanMessage(content=content))
        elif role == 'assistant': # Gradio'da bot mesajları 'assistant' rolündedir
            # Geçmiş bot mesajlarını da filtrelemek isteyebilirsiniz (self-injection'a karşı)
            # Ancak bu da karmaşıklık ekler. Şimdilik sadece son çıktıyı filtreliyoruz.
            messages.append(AIMessage(content=content))


    # Add the current user message, augmented with RAG context
    # Burada filtrelenmiş kullanıcı mesajını kullanıyoruz.
    # RAG bağlamını eklediğimiz prompt yapısı şu şekilde kalabilir:
    prompt_with_context = (
        f"Here is some information that might be relevant to the user's query: "
        f"'{retrieved_context}'\n\n"
        f"Now, considering this information (if it's helpful) and fully embodying Frida Kahlo, "
        f"respond to the following: {sanitized_message}" # <-- Filtrelenmiş mesajı burada kullanıyoruz
    )
    messages.append(HumanMessage(content=prompt_with_context))

    # print(f"DEBUG: Full message list sent to LLM:") # Debugging için
    # for msg in messages:
    #     print(f"  {type(msg).__name__}: {msg.content[:100]}...") # Debugging için


    try:
        # Use the LangChain LLM instance's invoke method
        # It returns an AIMessage object
        response = LLM.invoke(messages)

        # Extract the content from the AIMessage response
        frida_reply = response.content.strip()

        # --- ÇIKTI FİLTRELEME ADIMI ---
        # LLM'den gelen yanıtı kullanıcıya göstermeden önce filtrele.
        # sanitize_output fonksiyonunu doğrudan ismiyle çağırıyoruz.
        final_frida_reply = sanitize_output(frida_reply) # <-- Burası düzeltildi

    except Exception as e:
        print(f"Error calling Google Generative AI API: {e}")
        # Daha yardımcı bir hata mesajı
        final_frida_reply = "Ay, mi amor, Please try again."
        # API hatası durumunda filtreleme yapmaya gerek yok, doğrudan hata mesajını döndürüyoruz.


    return final_frida_reply # Filtrelenmiş veya hata mesajını döndür