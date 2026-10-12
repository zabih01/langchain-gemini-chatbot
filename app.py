
import streamlit as st
from chatbot import stream_response

from langchain_core.messages import HumanMessage

st.set_page_config(
    page_title="LangChain Gemini Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 LangChain Gemini Chatbot")
st.caption("Powered by LangChain and Google Gemini")

# Initialize Streamlit state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []

# Sidebar
with st.sidebar:
    st.header("Chat Settings")
    st.write("Model:", "Gemini")
    st.write("Streaming:", "Enabled")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent_messages = []
        st.rerun()

# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare assistant response
    with st.chat_message("assistant"):
        state_container = {}

        try:
            with st.spinner("Thinking..."):
                response = st.write_stream(
                    stream_response(
                        prompt,
                        st.session_state.agent_messages,
                        state_container,
                    )
                )

            if not response:
                st.warning("The model returned an empty response.")
            else:
                # Save UI history only after successful completion.
                st.session_state.messages.extend(
                    [
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": response},
                    ]
                )

                # Preserve the complete LangChain agent state,
                # including AI tool calls and their results.
                if "messages" in state_container:
                    st.session_state.agent_messages = (
                        state_container["messages"]
                    )
                else:
                    st.session_state.agent_messages.extend(
                        [
                            HumanMessage(content=prompt),
                        ]
                    )

        except Exception as error:
            st.error(f"Error: {error}")
            st.info(
                "The request failed. Please check your API quota, "
                "model configuration, and internet connection."
            )