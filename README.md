# LangChain Gemini Chatbot

An AI-powered conversational chatbot built with **LangChain**, **Google Gemini**, and **Streamlit**. It features real-time response streaming, conversation history, and custom tools for retrieving the current date and time.

## Features

- **Google Gemini Integration** — Generate intelligent responses using Google's Gemini models.
- **Real-Time Streaming** — Display responses progressively as they are generated.
- **LangChain Agent** — Use an agent that can invoke tools based on the user's request.
- **Date and Time Tools** — Retrieve the current date, weekday, and local time for a specified timezone.
- **Conversation History** — Maintain context across messages during a chat session.
- **Interactive Web Interface** — Chat through a clean, browser-based Streamlit interface.
- **Environment Configuration** — Securely configure API keys and model settings using environment variables.
- **Modern Python Workflow** — Manage dependencies using `uv`.

## Tech Stack

- **Python**
- **LangChain**
- **Google Gemini API**
- **Streamlit**
- **uv**
- **python-dotenv**

## Project Structure

```text
langchain-gemini-chatbot/
├── app.py              # Streamlit web application
├── chatbot.py          # Gemini agent and custom tools
├── .env                # Environment variables (not committed)
├── .gitignore          # Git exclusion rules
├── pyproject.toml      # Project configuration and dependencies
├── uv.lock             # Locked dependency versions
└── README.md           # Project documentation
```

## Prerequisites

Before getting started, make sure you have:

- Python installed.
- [uv](https://docs.astral.sh/uv/) installed.
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/).

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/langchain-gemini-chatbot.git
cd langchain-gemini-chatbot
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install dependencies

If the repository includes `pyproject.toml` and `uv.lock`, install the project dependencies with:

```bash
uv sync
```

If Streamlit or another required package is not yet included, add it with:

```bash
uv add streamlit langchain langchain-core langchain-google-genai python-dotenv
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
MODEL_NAME=your_supported_gemini_model
TEMPERATURE=0.7
```

Replace the placeholder values with your actual API key and a Gemini model ID supported by your API project.

**Security:** Never commit your `.env` file or expose your API key in source code. Keep `.env` listed in `.gitignore`.

### 4. Run the application

Launch the Streamlit web interface:

```bash
uv run streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## Available Tools

The chatbot includes custom tools that the LangChain agent can invoke when appropriate.

| Tool               | Description                                                                  |
| ------------------ | ---------------------------------------------------------------------------- |
| `get_current_date` | Returns the current date and weekday for a specified timezone.               |
| `get_current_time` | Returns the current date, local time, timezone abbreviation, and UTC offset. |

The default timezone is `Asia/Karachi`. You can specify another valid IANA timezone when asking the chatbot about the date or time.

## How It Works

1. The user submits a message through the Streamlit interface.
2. The LangChain agent processes the request using Google Gemini.
3. When needed, the agent invokes the appropriate date or time tool.
4. The response is streamed progressively to the interface.
5. The conversation history is maintained during the active Streamlit session.

## Configuration

| Variable         | Purpose                                   |
| ---------------- | ----------------------------------------- |
| `GOOGLE_API_KEY` | Authenticates requests to the Gemini API. |
| `MODEL_NAME`     | Specifies the Gemini model to use.        |
| `TEMPERATURE`    | Controls response variability.            |

The selected model must be available to your Gemini API project and supported by your installed LangChain integration.

## Troubleshooting

**API quota exceeded (`429 RESOURCE_EXHAUSTED`)**

- Check your usage and limits in [Google AI Studio](https://aistudio.google.com/).
- Wait for the applicable rate limit to reset.
- Review your API plan and billing settings if you need additional quota.

**Missing API key**

- Ensure `.env` exists in the project root.
- Verify that `GOOGLE_API_KEY` is set correctly.
- Restart the application after updating environment variables.

**Module not found**

Install the required packages using `uv add` and synchronize your environment with `uv sync`.

**Streamlit command not found**

Run Streamlit through the project environment:

```bash
uv run streamlit run app.py
```

## Future Improvements

- Persistent chat history using a database.
- Multiple conversation sessions.
- Support for document uploads and retrieval-augmented generation (RAG).
- More custom tools and agent capabilities.
- Deployment to a cloud hosting platform.

## Contributing

Contributions, suggestions, and bug reports are welcome. Feel free to fork the repository and submit a pull request.

## License

Add a `LICENSE` file to specify how others may use, modify, and distribute this project.

---

**Built with Python, LangChain, Google Gemini, and Streamlit.**
