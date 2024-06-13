from fastapi import FastAPI
from pydantic import BaseModel
from huggingface_hub import login

from transformers import pipeline


# Hugging Face token
huggingface_token = "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"

# Login to Hugging Face (optional, primarily for the first setup)
# login(token=huggingface_token)



pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B", token="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")
# pipe = pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)
pipe = pipeline("text-generation", model="Writer/palmyra-small")

class Query(BaseModel):
    query: str



app = FastAPI()



@app.get("/")
def start():
    return "hello"


@app.post("/query")
def query(query:Query):
    print(query.query)
    res = pipe(query.query)
    print(res)

    return {"res":res}