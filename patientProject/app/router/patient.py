from fastapi import APIRouter, status, Depends, HTTPException
from app.models import Staff, Patient
from app.schemas import PatientCreate, PatientOut, PatientUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionDep
from app.auth import CurrentStaff
from typing import List
from sqlalchemy import select

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate, 
        db: SessionDep,
        current_staff: CurrentStaff):
    new_patient = Patient(**patient.model_dump(), registered_by_id=current_staff.id)
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
    return new_patient


@router.get("/", response_model=List[PatientOut], status_code=status.HTTP_200_OK)
async def list_patients(db: SessionDep, current_staff: CurrentStaff):
    result = await db.execute(select(Patient))
    return result.scalars().all()

@router.get("/{patient_id}", response_model=PatientOut, status_code=status.HTTP_200_OK)
async def get_patient(patient_id: int, db: SessionDep, current_staff: CurrentStaff):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found!")
    return patient 

@router.patch("/patient/{patient_id}", response_model=PatientOut, status_code=status.HTTP_200_OK)
async def upadate_patient(patient_id: int, data: PatientUpdate, db: SessionDep, current_staff: CurrentStaff):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found!")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    await db.commit()
    await db.refresh(patient)
    return patient 

@router.delete("/patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int, db: SessionDep, current_staff: CurrentStaff):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found!")
    await db.delete(patient)
    await db.commit()