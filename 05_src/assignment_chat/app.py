import gradio as gr
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

from main import get_graph

load_dotenv('.secrets')


api_key = os.getenv("API_GATEWAY_KEY")
if not api_key:
    raise RuntimeError("Missing API_GATEWAY_KEY.")

llm = get_graph()

def responder(message: str, history: list[dict]) -> str:
    langchain_messages = []
    n = 0

    for msg in history:
        if msg['role'] == 'user':
            langchain_messages.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'assistant':
            langchain_messages.append(AIMessage(content=msg['content']))
            n += 1
    langchain_messages.append(HumanMessage(content=message))

    print(langchain_messages)

    state = {
        "messages": langchain_messages,
        "llm_calls": n
    }

    response = llm.invoke(state)
    return response['messages'][len(response['messages']) - 1].content


demo = gr.ChatInterface(
    fn=responder,
    type="messages",
    save_history= True,
    title="SimpleCoach",
    description = "Your personal AI coach",
    flagging_mode="manual",
    flagging_options=["Like", "Dislike"],
    theme=gr.themes.Soft(
        primary_hue="gray",
        secondary_hue="gray",
        neutral_hue="gray",
    ),
    css="p { text-align: center; }"
)

demo.launch()