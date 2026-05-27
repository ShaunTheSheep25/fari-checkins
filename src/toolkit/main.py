from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from fari_checkins.database import engine, get_db
from fari_checkins.models import Base, Resident, Caregiver, Checkin
from fari_checkins.schemas import ResidentCreate, ResidentResponse, CaregiverCreate, CaregiverResponse, CheckinCreate, CheckinResponse

Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.post("/residents/", response_model = ResidentResponse)
def create_resident(res: ResidentCreate, db: Session = Depends(get_db)):
    db_res = Resident(name = res.name, address = res.address, number = res.number)
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res

@app.get("/residents/", response_model = list[ResidentResponse])
def get_residents(db: Session = Depends(get_db)):
    res_list = db.query(Resident).all()
    return res_list

@app.get("/residents/{resident_id}", response_model = ResidentResponse)
def get_resident(resident_id: int, db: Session = Depends(get_db)):
    res = db.query(Resident).filter(Resident.id == resident_id).first()
    if not res:
        raise HTTPException(status_code = 404, detail = "Resident not found.")
    return res

@app.put("/residents/{resident_id}", response_model = ResidentResponse)
def update_resident(resident_id: int, new_data: ResidentCreate, db: Session = Depends(get_db)):
    res = db.query(Resident).filter(Resident.id == resident_id).first()
    if not res:
        raise HTTPException(status_code = 404, detail = "Resident not found.")
    res.name = new_data.name
    res.address - new_data.address
    res.number = new_data.number
    db.commit()
    db.refresh(res)
    return res

@app.delete("/residents/{resident_id}")
def delete_resident(resident_id: int, db: Session = Depends(get_db)):
    res = db.query(Resident).filter(Resident.id == resident_id).first()
    if not res:
        raise HTTPException(status_code = 404, detail = "Resident not found.")
    db.delete(res)
    db.commit()
    return {"message": "Resident successfully deleted."}

@app.post("/caregivers/", response_model = CaregiverResponse)
def create_caregiver(cg: CaregiverCreate, db: Session = Depends(get_db)):
    db_cg = Caregiver(name = cg.name, number = cg.number, res_id = cg.res_id)
    db.add(db_cg)
    db.commit()
    db.flush(db_cg)
    return db_cg

@app.get("/caregivers/", response_model = list[CaregiverResponse])
def get_caregivers(db: Session = Depends(get_db)):
    cg_list = db.query(Caregiver).all()
    return cg_list

@app.get("/caregivers/{caregiver_id}", response_model = CaregiverResponse)
def get_caregiver(caregiver_id: int, db: Session = Depends(get_db)):
    cg = db.query(Caregiver).filter(Caregiver.id == caregiver_id).first()
    if not cg:
        raise HTTPException(status_code = 404, detail = "Caregiver not found.")
    return cg

@app.delete("/caregivers/{caregiver_id}", response_model = CaregiverResponse)
def delete_caregiver(caregiver_id: int, db: Session = Depends(get_db)):
    cg = db.query(Caregiver).filter(Caregiver.id == caregiver_id).first()
    if not cg:
        raise HTTPException(status_code = 404, detail = "Caregiver not found.")
    db.delete(cg)
    db.commit()
    return {"message": "Caregiver successfully deleted."}
