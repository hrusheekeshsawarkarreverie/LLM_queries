from fastapi import FastAPI
from pydantic import BaseModel

from transformers import pipeline



# pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B")
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