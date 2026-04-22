from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .producto import Producto
    from .ingrediente import Ingrediente


class ProductoIngrediente(SQLModel, table=True):
    """
    Modelo de relación N:N entre Producto e Ingrediente
    Representa los ingredientes de cada producto con sus cantidades
    """
    
    __tablename__ = "producto_ingrediente"
    
    # Clave foránea hacia Producto (parte de la clave primaria compuesta)
    producto_id: Optional[int] = Field(
        default=None, 
        foreign_key="producto.id", 
        primary_key=True
    )
    
    # Clave foránea hacia Ingrediente (parte de la clave primaria compuesta)
    ingrediente_id: Optional[int] = Field(
        default=None, 
        foreign_key="ingrediente.id", 
        primary_key=True
    )
    
    # Campo de cantidad (específico de la relación)
    cantidad: float = Field(gt=0)
    
    # Relación bidireccional hacia Producto
    producto: Optional["Producto"] = Relationship(back_populates="ingrediente_links")
    
    # Relación bidireccional hacia Ingrediente
    ingrediente: Optional["Ingrediente"] = Relationship(back_populates="producto_links")
