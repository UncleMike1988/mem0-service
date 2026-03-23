from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from mem0 import Memory
from config import MEM0_CONFIG, MEM0_API_KEY

app = FastAPI(title="Mem0 Service", version="1.0.0")
memory = Memory.from_config(MEM0_CONFIG)


def verify_api_key(authorization: Optional[str] = Header(None)):
    if MEM0_API_KEY and authorization != f"Bearer {MEM0_API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API key")


class AddRequest(BaseModel):
    content: str
    user_id: str
    metadata: Optional[dict] = None


class SearchRequest(BaseModel):
    query: str
    user_id: str
    limit: int = 5


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/memory/add")
def add_memory(req: AddRequest, authorization: Optional[str] = Header(None)):
    verify_api_key(authorization)
    result = memory.add(req.content, user_id=req.user_id, metadata=req.metadata)
    return result


@app.post("/memory/search")
def search_memory(req: SearchRequest, authorization: Optional[str] = Header(None)):
    verify_api_key(authorization)
    results = memory.search(req.query, user_id=req.user_id, limit=req.limit)
    return results


@app.delete("/memory/{memory_id}")
def delete_memory(memory_id: str, authorization: Optional[str] = Header(None)):
    verify_api_key(authorization)
    memory.delete(memory_id)
    return {"status": "deleted", "memory_id": memory_id}


@app.get("/memory/list/{user_id}")
def list_memories(user_id: str, authorization: Optional[str] = Header(None)):
    verify_api_key(authorization)
    results = memory.get_all(user_id=user_id)
    return results
