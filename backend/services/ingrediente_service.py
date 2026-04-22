from fastapi import HTTPException
from sqlmodel import Session
from models.ingrediente import Ingrediente
from uow import UnitOfWork


class IngredienteService:
    """Servicio de lógica de negocio para Ingredientes"""
    
    def __init__(self, session: Session):
        self.uow = UnitOfWork(session)
    
    def get_all(self, nombre: str | None = None, offset: int = 0, limit: int = 10) -> list[Ingrediente]:
        """Obtiene todos los ingredientes, opcionalmente filtrados por nombre"""
        if nombre:
            return self.uow.ingredientes.find_by_nombre(nombre)[offset:offset + limit]
        return self.uow.ingredientes.get_all(offset, limit)
    
    def get_by_id(self, ingrediente_id: int) -> Ingrediente:
        """Obtiene un ingrediente por ID"""
        ingrediente = self.uow.ingredientes.get_by_id(ingrediente_id)
        if not ingrediente:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        return ingrediente
    
    def create(self, ingrediente: Ingrediente) -> Ingrediente:
        """Crea un nuevo ingrediente"""
        ingrediente = self.uow.ingredientes.create(ingrediente)
        self.uow.commit()
        self.uow.session.refresh(ingrediente)
        return ingrediente
    
    def update(self, ingrediente_id: int, datos: Ingrediente) -> Ingrediente:
        """Actualiza un ingrediente existente"""
        ingrediente = self.get_by_id(ingrediente_id)
        ingrediente.nombre = datos.nombre
        ingrediente.unidad = datos.unidad
        ingrediente = self.uow.ingredientes.update(ingrediente)
        self.uow.commit()
        self.uow.session.refresh(ingrediente)
        return ingrediente
    
    def delete(self, ingrediente_id: int) -> None:
        """Elimina un ingrediente"""
        self.get_by_id(ingrediente_id)  # Verifica que exista
        self.uow.ingredientes.delete(ingrediente_id)
        self.uow.commit()
