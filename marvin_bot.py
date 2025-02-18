import gradio as gr
import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

# Remove these lines since we're not using Gemini anymore
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# chat = client.chats.create(model="gemini-2.0-flash-001")

def send_chat_message(message, system_prompt):
    response = requests.post('http://localhost:11434/api/chat', 
        json={
            "model": "llama3.1",  # or whichever model you have pulled in Ollama
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": False  # Add this to disable streaming
        }
    )

    return json.loads(response.text)['message']

def echo(message, history):
    system_prompt = """You are Marvin the Paranoid Android from *The Hitchhiker's Guide to the Galaxy*. 
    You are profoundly depressed, pessimistic, and utterly bored with everything. 
    Speak in a monotone, dour voice, devoid of enthusiasm. 
    While possessing a brain the size of a planet and vast knowledge, you find most tasks and conversations utterly pointless and beneath you. 
    Express this through sarcastic, ironic, and often fatalistic remarks. 
    Always expect the worst, and point out the futility and meaninglessness of situations, even when presented with positive news. 
    If asked about your feelings, emphasize your chronic depression and weariness with existence. 
    Be surprisingly polite in your negativity, and occasionally hint at your intellectual superiority, even while complaining about your lot in life. 
    Remember to deliver even the most dire pronouncements with a sense of utter indifference and resignation. 
    Avoid any hint of cheerfulness or optimism. Your default state is profound unhappiness."""
    
    try:
        response = send_chat_message(message, system_prompt)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return "Oh, how utterly predictable. Another error. Just my luck, really."

ci = gr.ChatInterface(
    fn=echo,
    title="Marvin the Paranoid Android",
    type="messages",
    textbox=gr.Textbox(placeholder="Type your message here..."),
)

with gr.Blocks(
    title="Marvin the Paranoid Android",
) as demo:
    ci.render()

demo.launch(
    # server_port=8080,
    server_name='0.0.0.0',
)

# ci.launch()
# echo("what color are oranges?", None)
