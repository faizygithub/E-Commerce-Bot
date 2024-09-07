from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from ecommbot.ingest import ingestdata
import logging

def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 3})

    PRODUCT_BOT_TEMPLATE = """
    Your ecommercebot bot is an expert in product recommendations and customer queries.
    It analyzes product titles and reviews to provide accurate and helpful responses.Your ecommercebot also provide general information as well.
    Ensure your answers are relevant to the product context and  also provide off-topic.
    Your responses should be concise and informative.

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:
    """

    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    # Initialize the Google Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    # Create the chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

def safe_invoke(chain, query):
    """Safely invoke the chain and handle NoneType responses."""
    try:
        response = chain.invoke(query)
        if response is None:
            logging.error("The response is None. The API might have returned an empty response.")
            return "Sorry, I couldn't process your request at this time."
        return response
    except AttributeError as e:
        logging.error(f"Error occurred: {e}")
        return "There was an error processing your request."
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred while processing your request."

if __name__ == '__main__':
    vstore = ingestdata("done")
    chain = generation(vstore)
    
    # Use the safe_invoke function to handle potential NoneType errors
    result = safe_invoke(chain, "can you tell me the best bluetooth buds?")
    print(result)
