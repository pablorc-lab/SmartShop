#clases modelos de nuestra base de datos

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

#clase que representa los supermercados almacenados en la bd
class Supermercado(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nombre: so.Mapped[str] =  so.mapped_column(sa.String(50), unique=True)
    #modela la relacion en la que participa, pero no es una columna 'real'
    productos: so.WriteOnlyMapped['Producto'] = so.relationship(
        back_populates='supermercado')
    #funcion que indica como se devuelve un objeto de dicha clase
    def __repr__(self):
        return 'Supermercado {}'.format(self.nombre)
    
#definir una tabla Producto por cada Supermercado
class Producto(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nombre: so.Mapped[str] =  so.mapped_column(sa.String(100))
    precio: so.Mapped[float] = so.mapped_column()
    precio_kg: so.Mapped[str] = so.mapped_column(sa.String(50))
    url_imagen: so.Mapped[str] = so.mapped_column(sa.String(255))
    id_supermercado: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Supermercado.id))
    nombre_busqueda: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    #indicamos la relacion que mantiene con la clase Supermercado
    supermercado: so.Mapped[Supermercado] = so.relationship(back_populates='productos')

    #funcion que indica como se devuelve un objeto de dicha clase
    def __repr__(self):
        return 'Producto {}'.format(self.nombre)
    


