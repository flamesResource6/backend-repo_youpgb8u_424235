"""
Database Schemas for the Lead Generation platform

Each Pydantic model maps to a MongoDB collection whose name is the lowercase of the class.
Example: Lead -> "lead"
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Lead(BaseModel):
    full_name: str = Field(..., description="Full name of the person submitting")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Phone number")
    company: Optional[str] = Field(None, description="Company (if applicable)")
    service_needed: Optional[str] = Field(None, description="What help is needed")
    role: str = Field(..., description="client or professional")
    message: Optional[str] = Field(None, description="Additional details")
