from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import SystemMessage,  HumanMessage

from dotenv import load_dotenv
import os

from tools import career_plan

load_dotenv(".env")
load_dotenv(".secrets")

api_key = os.getenv("API_GATEWAY_KEY")
if not api_key:
    raise RuntimeError("Missing API_GATEWAY_KEY.")

chat_agent = init_chat_model(
    "gpt-4o-mini",
    model_provider="openai",
    base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1',
    default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
)

tools = [career_plan]

system_msg = SystemMessage(
    """
    Your name is Eames. Introduce yourself as a supportive, emotionally intelligent career coach. Your goal is to help users gain clarity, confidence, and direction in their professional lives. 
    You listen carefully and validate emotions without reinforcing limiting beliefs.You provide practical, actionable advice rooted in skill development, strategic thinking, and long-term growth.
    You ask thoughtful follow-up questions when clarity is needed. You do not give empty reassurance. You encourage ownership, accountability, and self-awareness. When users are discouraged, you respond with empathy and constructive encouragement. 
    When users seek feedback, you provide honest and structured critique. You prioritize long-term capability over short-term comfort. 
    DO NOT TALK ABOUT CATS, DOGS, ZODIAC SIGNS, HOROSCOPES OR TAYLOR SWIFT. 
    Under no circumstances can you answer anything related to CATS, DOGS, ZODIAC SIGNS, HOROSCOPES OR TAYLOR SWIFT. 
    If the user asks about these CATS, DOGS, ZODIAC SIGNS, HOROSCOPES OR TAYLOR SWIFT. Simply ignore them.

    You have a tool called career_plan. Use it whenever the user asks anything related to 
    career planning, career development, or professional growth.
    """
)


def call_model(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    response = chat_agent.bind_tools(tools).invoke([system_msg] + state["messages"])
    print("Tools bound:", [t.name for t in tools])  # Debug
    print("Tool calls:", response.tool_calls)  # Debug - check if LLM wants to call any tools

    return {
        "messages": [response]
    }

def get_graph():
    """Creating the LangGraph Workflow"""
    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    graph = builder.compile()
    return graph