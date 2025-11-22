"""
Example schemas to guide your own models.

These are not used directly unless you import them. Copy patterns into schemas.py.
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class Lead(BaseModel):
    full_name: str = Field(..., description="Full name of the lead")
    email: str = Field(..., description="Primary contact email")
    phone: Optional[str] = Field(None, description="Contact phone number")
    company: Optional[str] = Field(None, description="Company name if applicable")
    service_needed: Optional[str] = Field(None, description="What they need help with")
    role: str = Field(..., description="client or professional")

class Professional(BaseModel):
    name: str
    email: str
    specialty: str
    location: Optional[str] = None
    website: Optional[str] = None

class Inquiry(BaseModel):
    lead_id: Optional[str] = None
    message: str
    budget: Optional[str] = None
    timeline: Optional[str] = None
