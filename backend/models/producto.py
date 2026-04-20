from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .categoria import Categoria
    from .producto_ingrediente import ProductoIngrediente



class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=50)
    precio: float = Field(gt=0)
    descripcion: Optional[str] = Field(default=None, max_length=300)

    #Relacion 1:N - un producto pertenece a una categoria
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    categoria: Optional["Categoria"] = Relationship(back_populates="productos")

    # Relacion N:N - un producto tiene muchos ingredientes
    ingrediente_links: list["ProductoIngrediente"] = Relationship(back_populates="producto")