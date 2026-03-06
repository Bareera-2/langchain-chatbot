from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
        model="qwen2.5-coder:3b",
        temperature = 0.7
        )

prompt = ChatPromptTemplate.from_messages(
    [
    ("system","You are helpful AI Assistant"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{question}")
    ]
)

chain = prompt | llm | StrOutputParser()

chat_history = []

MAX_TURNS = 10  # 10 exahnges = 20 messages(Human + AI)

def chat(question):
    current_turns = len(chat_history) // 2
    if current_turns >= MAX_TURNS:
        return (
            "Context window is full"
            "The AI may not follow our previous thread properly"
            "Please type 'clear' for new chat"
        )
    
    response = chain.invoke({
        "question":question,
        "chat_history": chat_history
        })
    
    chat_history.append(HumanMessage(content = question))
    chat_history.append(AIMessage(content = response))

    remaining = MAX_TURNS - (current_turns +1)
    if remaining <= 2:
        response += f"\n\nYour {remaining} turn(s) left."

    return response

# print(chat("What is RAG?"))
# print(chat("Give me a python example of it?"))
# print(chat("Now explain the code that you just gave"))


def main():
    print("Langchain Chatbot ready! (Type 'quit' for exit , 'clear' reset the history)")
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            break

        if user_input.lower() == "clear":
            chat_history.clear()
            print("History cleared!, Starting fresh!")
            continue
        
        print(f"AI: {chat(user_input)}\n")

main()