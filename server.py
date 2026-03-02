from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from fastapi import FastAPI
from langserve import add_routes

load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model_name="openai/gpt-oss-120b",groq_api_key=groq_api_key)

#create a prompt template
system_template="translate the following text into {language}"
prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system",system_template),
        ("user","{text}")    
    ]
)

parser=StrOutputParser()

#create chain
chain=prompt_template|model|parser

#app definition
app= FastAPI(title="Translation API",
            version="1.0",
            description="A simple API server using langchain runnable interfaces for translating text from one language to another"
)

##adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
