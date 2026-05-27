from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ResidentCreate(BaseModel):
    name: str
    address: str
    number: str

class ResidentResponse(ResidentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CaregiverCreate(BaseModel):
    name: str
    number: str
    res_id: int

class CaregiverResponse(CaregiverCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CheckinCreate(BaseModel):
    res_id: int
    mood: str
    category: str
    notes: str | None = None

class CheckinResponse(CheckinCreate):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)



