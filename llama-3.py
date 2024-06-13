from fastapi import FastAPI
from pydantic import BaseModel
from huggingface_hub import login
import torch
from transformers import pipeline


# Hugging Face token
huggingface_token = "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"

# Login to Hugging Face (optional, primarily for the first setup)
# login(token=huggingface_token)



pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B", token="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",model_kwargs={"torch_dtype": torch.bfloat16}, device="auto")
# pipe = pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)
# pipe = pipeline("text-generation", model="Writer/palmyra-small")

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

prompt = pipeline.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
)
terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]
class Query(BaseModel):
    query: str



app = FastAPI()



@app.get("/")
def start():
    return "hello"


@app.post("/query")
def query(query:Query):
    print(query.query)
    res = pipe(query.query,
                max_new_tokens=256,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
                pad_token_id = tokenizer.eos_token_id)
    print(res)

    return {"res":res}