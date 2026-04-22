from typing import TypeVar, Generic, List, Optional
from sqlmodel import Session, select
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)


class BaseRepository(Generic[T]):
    """Repositorio base con operaciones CRUD comunes"""
    
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Obtiene una entidad por ID"""
        return self.session.get(self.model, id)
    
    def get_all(self, offset: int = 0, limit: int = 10) -> List[T]:
        """Obtiene todas las entidades con paginación"""
        statement = select(self.model).offset(offset).limit(limit)
        return self.session.exec(statement).all()
    
    def create(self, obj: T) -> T:
        """Crea una nueva entidad"""
        self.session.add(obj)
        self.session.flush()
        return obj
    
    def update(self, obj: T) -> T:
        """Actualiza una entidad existente"""
        self.session.merge(obj)
        self.session.flush()
        return obj
    
    def delete(self, id: int) -> bool:
        """Elimina una entidad por ID"""
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.flush()
            return True
        return False
