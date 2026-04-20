from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, Optional
from sqlmodel import Session, select
from database import get_session
from models.producto import Producto
from schemas.schemas import IngredienteCreate

router = APIRouter(prefix="/productos", tags=["Productos"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=list[Producto])
def get_productos(
    session: SessionDep,
    nombre: Annotated[Optional[str], Query(max_length=100)] = None,
    categoria_id: Annotated[Optional[int], Query(ge=1)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    query = select(Producto)
    if nombre:
        query = query.where(Producto.nombre.contains(nombre))
    if categoria_id:
        query = query.where(Producto.categoria_id == categoria_id)
    return session.exec(query.offset(offset).limit(limit)).all()

@router.get("/{producto_id}", response_model=Producto)
def get_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", response_model=Producto, status_code=201)
def crear_producto(producto: Producto, session: SessionDep):
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

@router.put("/{producto_id}", response_model=Producto)
def editar_producto(producto_id: int, datos: Producto, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.nombre = datos.nombre
    producto.precio = datos.precio
    producto.descripcion = datos.descripcion
    producto.categoria_id = datos.categoria_id
    session.commit()
    session.refresh(producto)
    return producto

@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()