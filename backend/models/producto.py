from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .categoria import Categoria
    from .producto_ingrediente import ProductoIngrediente


class Producto(SQLModel, table=True):
    """Modelo para Producto"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=100)
    precio: float = Field(gt=0)
    descripcion: Optional[str] = Field(default=None, max_length=300)

    # Relación 1:N - un producto pertenece a una categoría
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    categoria: Optional["Categoria"] = Relationship(back_populates="productos")

    # Relación N:N - un producto tiene muchos ingredientes (a través de ProductoIngrediente)
    ingrediente_links: List["ProductoIngrediente"] = Relationship(back_populates="producto")
