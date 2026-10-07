from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from app.database import engine, Base, SessionLocal
from app.models import Tutor, Animal, Atendimento
from app.crud import popular_banco

Base.metadata.create_all(bind=engine)

popular_banco()

app = FastAPI(
    title="API - Clínica VetPet",
    description="Backend completo para gerenciamento de tutores, animais e atendimentos."
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TutorCreate(BaseModel):
    nome_completo: str
    telefone: Optional[str] = None
    email: EmailStr

class TutorResponse(BaseModel):
    id: int
    nome_completo: str
    telefone: Optional[str]
    email: str

    class Config:
        from_attributes = True


class AnimalCreate(BaseModel):
    nome_animal: str
    especie: str
    raca: Optional[str] = None
    peso_kg: float
    tutor_id: int

class AnimalResponse(BaseModel):
    id: int
    nome_animal: str
    especie: str
    raca: Optional[str]
    peso_kg: float
    tutor_id: int

    class Config:
        from_attributes = True


class AtendimentoCreate(BaseModel):
    data_atend: str
    motivo: str
    valor_cons: float
    animal_id: int

class AtendimentoResponse(BaseModel):
    id: int
    data_atend: str
    motivo: str
    valor_cons: float
    animal_id: int

    class Config:
        from_attributes = True

@app.get("/tutores", response_model=List[TutorResponse], tags=["Tutores"])
def listar_tutores(db: Session = Depends(get_db)):
    return db.query(Tutor).all()

@app.post("/tutores", response_model=TutorResponse, status_code=status.HTTP_201_CREATED, tags=["Tutores"])
def cadastrar_tutor(tutor_data: TutorCreate, db: Session = Depends(get_db)):
    tutor_existente = db.query(Tutor).filter(Tutor.email == tutor_data.email).first()
    if tutor_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado!")

    novo_tutor = Tutor(
        nome_completo=tutor_data.nome_completo,
        telefone=tutor_data.telefone,
        email=tutor_data.email
    )
    db.add(novo_tutor)
    db.commit()
    db.refresh(novo_tutor)
    return novo_tutor

@app.get("/animais", response_model=List[AnimalResponse], tags=["Animais"])
def listar_animais(db: Session = Depends(get_db)):
    return db.query(Animal).all()

@app.post("/animais", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED, tags=["Animais"])
def cadastrar_animal(animal_data: AnimalCreate, db: Session = Depends(get_db)):
    # Verifica se o tutor informado existe
    tutor = db.query(Tutor).filter(Tutor.id == animal_data.tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor não encontrado!")

    novo_animal = Animal(
        nome_animal=animal_data.nome_animal,
        especie=animal_data.especie,
        raca=animal_data.raca,
        peso_kg=animal_data.peso_kg,
        tutor_id=animal_data.tutor_id
    )
    db.add(novo_animal)
    db.commit()
    db.refresh(novo_animal)
    return novo_animal


@app.get("/atendimentos", response_model=List[AtendimentoResponse], tags=["Atendimentos"])
def listar_atendimentos(db: Session = Depends(get_db)):
    return db.query(Atendimento).all()

@app.post("/atendimentos", response_model=AtendimentoResponse, status_code=status.HTTP_201_CREATED, tags=["Atendimentos"])
def cadastrar_atendimento(atend_data: AtendimentoCreate, db: Session = Depends(get_db)):
    # Verifica se o animal informado existe
    animal = db.query(Animal).filter(Animal.id == atend_data.animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado!")

    novo_atendimento = Atendimento(
        data_atend=atend_data.data_atend,
        motivo=atend_data.motivo,
        valor_cons=atend_data.valor_cons,
        animal_id=atend_data.animal_id
    )
    db.add(novo_atendimento)
    db.commit()
    db.refresh(novo_atendimento)
    return novo_atendimento


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)