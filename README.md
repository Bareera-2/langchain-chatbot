# LangChain Chatbot

A modern AI chatbot powered by LangChain and Ollama, featuring both CLI and web interfaces for local AI inference.

## Features

- **Dual Interfaces**: Use via command-line or web browser
- **Local LLM**: Runs entirely on your machine using Ollama
- **Chat History**: Maintains conversation context with configurable turn limits
- **Customizable**: Easy configuration via environment variables

## Requirements

- Python 3.11+
- [Ollama](https://ollama.ai/) installed and running locally

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd langchain-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

4. **Start Ollama**
   ```bash
   ollama serve
   # In another terminal:
   ollama pull qwen2.5-coder:3b
   ```

## Configuration

Edit `.env` to customize the chatbot:

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_NAME` | Ollama model to use | `qwen2.5-coder:3b` |
| `TEMPERATURE` | Response creativity (0-1) | `0.7` |
| `MAX_TURNS` | Maximum conversation turns | `5` |

## Usage

### Web Interface (Streamlit)

```bash
streamlit run streamlit_app.py
```

Open http://localhost:8501 in your browser.

### Command-Line Interface

```bash
python main.py
```

Commands:
- Type your message and press Enter to chat
- Type `clear` to reset conversation history
- Type `quit` to exit

## Project Structure

```
langchain-chatbot/
├── main.py              # CLI chatbot implementation
├── streamlit_app.py      # Web interface (Streamlit)
├── .env                  # Environment configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Tech Stack

- **LangChain** - LLM application framework
- **Ollama** - Local LLM runtime
- **Streamlit** - Web UI framework
- **Python** - Programming language

## License

MIT
