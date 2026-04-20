from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, Optional
from sqlmodel import Session, select
from database import get_session
from models.ingrediente import Ingrediente
from schemas.schemas import IngredienteCreate

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=list[Ingrediente])
def get_ingredientes(
    session: SessionDep,
    nombre: Annotated[Optional[str], Query(max_length=50)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    query = select(Ingrediente)
    if nombre:
        query = query.where(Ingrediente.nombre.contains(nombre))
    return session.exec(query.offset(offset).limit(limit)).all()

@router.get("/{ingrediente_id}", response_model=Ingrediente)
def get_ingrediente(ingrediente_id: int, session: SessionDep):
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente

@router.post("/", response_model=Ingrediente, status_code=201)
def crear_ingrediente(ingrediente: Ingrediente, session: SessionDep):
    session.add(ingrediente)
    session.commit()
    session.refresh(ingrediente)
    return ingrediente

@router.put("/{ingrediente_id}", response_model=Ingrediente)
def editar_ingrediente(ingrediente_id: int, datos: Ingrediente, session: SessionDep):
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    ingrediente.nombre = datos.nombre
    ingrediente.unidad = datos.unidad
    session.commit()
    session.refresh(ingrediente)
    return ingrediente

@router.delete("/{ingrediente_id}", status_code=204)
def eliminar_ingrediente(ingrediente_id: int, session: SessionDep):
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    session.delete(ingrediente)
    session.commit()