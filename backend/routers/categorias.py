from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, Optional
from sqlmodel import Session, select
from database import get_session
from models.categoria import Categoria
from schemas.schemas import CategoriaCreate

router = APIRouter(prefix="/categorias", tags=["categorias"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=list[Categoria])
def get_categorias(
    session: SessionDep,
    nombre: Annotated[Optional[str], Query(max_length=50)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    query = select(Categoria)
    if nombre:
        query = query.where(Categoria.nombre.contains(nombre))
    return session.exec(query.offset(offset).limit(limit)).all()

@router.get("/{categoria_id}", response_model=Categoria)
def get_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail = "Categoria no encontrada")
    return categoria

@router.post("/", response_model=Categoria, status_code=201)
def crear_categoria(categoria: Categoria, session: SessionDep):
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.put("/{categoria_id}", response_model=Categoria)
def editar_categoria(categoria_id: int, datos: Categoria, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail = "Categoria no encontrada")
    categoria.nombre = datos.nombre
    categoria.descripcion = datos.descripcion
    session.commit()
    session.refresh(categoria)
    return categoria

@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail = "Categoria no encontrada")
    session.delete(categoria)
    session.commit()
