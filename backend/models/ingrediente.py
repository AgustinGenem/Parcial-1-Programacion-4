from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .producto_ingrediente import ProductoIngrediente


class Ingrediente(SQLModel, table=True):
    """Modelo para Ingrediente"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=50)
    unidad: str = Field(max_length=20)
    
    # Relación N:N hacia productos (a través de ProductoIngrediente)
    producto_links: List["ProductoIngrediente"] = Relationship(back_populates="ingrediente")
