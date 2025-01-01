import sys

from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    import os

    from dotenv import find_dotenv, load_dotenv

    _ = load_dotenv(find_dotenv())

    if os.getenv("OPENAI_API_KEY") is None:
        print("Please set OPENAI_API_KEY environment variable")
        sys.exit(1)

    model = ChatOpenAI(model="gpt-4o-mini")

    while True:
        prompt = input("Enter a prompt: ")
        if prompt == "exit":
            break
        response = model.invoke(prompt)
        print(response.content)
