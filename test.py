from langchain_google_genai import ChatGoogleGenerativeAI
import logging

def test_google_genai():
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
        response = llm.invoke("What is the capital of France?")
        if response is None:
            logging.error("The API returned an empty response.")
            return "API returned an empty response."
        return response
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

if __name__ == '__main__':
    result = test_google_genai()
    print(result)
