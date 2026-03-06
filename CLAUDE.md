# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LangChain Chatbot - A local AI chatbot powered by LangChain and Ollama with both CLI and web (Streamlit) interfaces.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama (required before running the app)
ollama serve
ollama pull qwen2.5-coder:3b

# Run CLI chatbot
python main.py

# Run web interface
streamlit run streamlit_app.py
```

## Architecture

- **main.py**: CLI chatbot using LangChain with chat history management and turn limits
- **streamlit_app.py**: Streamlit web UI with custom styling, sidebar controls, and message rendering
- **.env**: Configuration for model name, temperature, and max conversation turns
- Both interfaces use the same LangChain components: ChatOllama, ChatPromptTemplate, and StrOutputParser

## Key Details

- Default model: `qwen2.5-coder:3b`
- Configurable via environment variables in `.env`
- Chat history is maintained in memory (not persisted)
- Maximum conversation turns enforced to prevent context overflow

## README

See README.md for full installation and usage instructions.
