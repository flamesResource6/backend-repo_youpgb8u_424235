from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents
from schemas import Lead

app = FastAPI(title="LeadGen API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LeadCreate(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    service_needed: Optional[str] = None
    role: str  # "client" or "professional"
    message: Optional[str] = None

@app.get("/", tags=["health"]) 
async def root():
    return {"status": "ok", "service": "LeadGen API"}

@app.post("/leads", tags=["leads"]) 
async def create_lead(payload: LeadCreate):
    try:
        data = payload.model_dump()
        created = await create_document("lead", data)
        return created
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leads", response_model=List[Lead], tags=["leads"]) 
async def list_leads(role: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {"role": role} if role else {}
        docs = await get_documents("lead", filter_dict, limit)
        # Convert to Pydantic Lead list for response validation
        return [Lead(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
