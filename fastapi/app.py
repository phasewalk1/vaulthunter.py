from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import torch
from dotenv import load_dotenv
from embedchain import App
from embedchain.loaders.directory_loader import DirectoryLoader

load_dotenv()

app = FastAPI()


# Define your prompt model
class Prompt(BaseModel):
    text: str


# Initialize global variables
embedchain_app = None
VAULT = os.getenv("VAULT")
loader_config = {
    "recursive": True,
    "extensions": [".md"],
}


@app.on_event("startup")
async def startup_event():
    global embedchain_app
    if torch.cuda.is_available():
        print("GPU available.")
        torch.cuda.set_device(0)
    else:
        torch.set_num_threads(4)
        print("No GPU available.")

    loader = DirectoryLoader(config=loader_config)
    embedchain_app = App.from_config("mistral.yaml")
    embedchain_app.add(VAULT, loader=loader)
    print("Embedchain app initialized.")


@app.post("/query/")
async def query(prompt: Prompt):
    if embedchain_app is None:
        raise HTTPException(
            status_code=503, detail="Embedchain app is not initialized."
        )

    context = embedchain_app.search(prompt.text)
    response = embedchain_app.query(prompt.text)

    print(f"Got source: {context[0]['metadata']['url']}")
    return {
        "response": response,
        "source": context[0]["metadata"]["url"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
