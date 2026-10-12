"""FastAPI entry for streaming-llm-chat."""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="streaming-llm-chat", description="Token-streaming chat UI backend (SSE) with pluggable OpenAI-compatible local providers.")

class Health(BaseModel):
    status: str = "ok"

@app.get("/health", response_model=Health)
def health() -> Health:
    return Health()


class In(BaseModel):
    text: str = Field(..., min_length=1)

class Out(BaseModel):
    result: str
    detail: dict = Field(default_factory=dict)

@app.post("/process", response_model=Out)
def process(body: In) -> Out:
    text = body.text.strip()
    tokens = text.split()
    return Out(
        result=f"processed {{len(tokens)}} tokens",
        detail={"preview": text[:160], "note": "Swap this handler for real model inference"},
    )


def main() -> None:
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
