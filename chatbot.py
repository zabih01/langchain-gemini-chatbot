
import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessageChunk
from langchain.tools import tool

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("MODEL_NAME", "your-working-model-id")
temperature = float(os.getenv("TEMPERATURE", "0.7"))

if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing from .env")

# Initialize Gemini
model = init_chat_model(
    model=model_name,
    model_provider="google_genai",
    temperature=temperature,
    api_key=api_key,
)


# TOOL 1: Current date
@tool
def get_current_date(timezone: str = "Asia/Karachi") -> str:
    """Get today's date and weekday in a specified IANA timezone."""
    try:
        now = datetime.now(ZoneInfo(timezone))
        return now.strftime("%A, %d %B %Y")
    except (ZoneInfoNotFoundError, ValueError):
        return f"Unknown timezone: {timezone}"


# TOOL 2: Current time
@tool
def get_current_time(timezone: str = "Asia/Karachi") -> str:
    """Get the current local time, date, and UTC offset."""
    try:
        now = datetime.now(ZoneInfo(timezone))
        return now.strftime(
            "%A, %d %B %Y, %I:%M:%S %p %Z (UTC%z)"
        )
    except (ZoneInfoNotFoundError, ValueError):
        return f"Unknown timezone: {timezone}"


# Create the agent
agent = create_agent(
    model=model,
    tools=[get_current_date, get_current_time],
    system_prompt=(
        "You are a helpful AI assistant. "
        "Remember the conversation context. "
        "When the user asks for the current date, weekday, or time, "
        "use the appropriate date/time tool instead of guessing. "
        "The default timezone is Asia/Karachi. "
        "Use the tool result accurately in your answer."
    ),
)


def stream_response(prompt, history, state_container):
    """Stream the agent response and capture the latest conversation state."""

    input_messages = [
        *history,
        HumanMessage(content=prompt),
    ]

    for mode, chunk in agent.stream(
        {"messages": input_messages},
        stream_mode=["messages", "values"],
    ):
        # Capture the complete agent state, including tool interactions.
        if mode == "values":
            state_container["messages"] = chunk["messages"]

        # Stream model output to the web interface.
        elif mode == "messages":
            message_chunk, metadata = chunk

            if not isinstance(message_chunk, AIMessageChunk):
                continue

            # Ignore tool-node output and stream assistant model output.
            if metadata.get("langgraph_node") != "model":
                continue

            content = message_chunk.content

            if isinstance(content, str):
                if content:
                    yield content

            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, str):
                        if item:
                            yield item
                    elif (
                        isinstance(item, dict)
                        and item.get("type") == "text"
                        and item.get("text")
                    ):
                        yield item["text"]