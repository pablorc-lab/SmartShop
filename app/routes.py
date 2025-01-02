from app import app
from flask import render_template, jsonify, request
import sqlalchemy as sa
from app.models import Supermercado,Producto
from app import db
import unicodedata
from sqlalchemy import or_
import random
import database



@app.route('/')
def home():
    #tomo 3 objetos aleatorios por cada supermercado
    
    lista_productos=[]
    for i in range(1,4):
        super = db.session.get(Supermercado,i)
        query=super.productos.select().order_by(db.func.random()).limit(3)
        lista_productos.extend(db.session.scalars(query))
    random.shuffle(lista_productos)
    #return render_template('index.html',lista_productos=lista_productos)
    return render_template('index.html',titulo="Inicio",clase_cabecera="cabecera-inicio",lista_productos=lista_productos)


#ruta donde se procesa la palabra ingresada por el usuario
@app.route('/products',methods=['POST'])
def mostrar_productos():

    palabra=request.form['producto']
    producto_a_buscar=database.unaccent(palabra.lower())
    #consulto la b
    query = sa.select(Producto).where(or_(Producto.nombre_busqueda.like(f'% {producto_a_buscar} %'),Producto.nombre_busqueda.like(f'{producto_a_buscar} %'),Producto.nombre_busqueda.like(f'% {producto_a_buscar}')))
    lista_productos=db.session.scalars(query).all()
    if not lista_productos:
        return render_template('resultado.html',titulo="Resultado No Encontrado",clase_cabecera="cabecera-resultado",producto_a_buscar=palabra)
    random.shuffle(lista_productos)
    return render_template('resultado.html',titulo="Resultado Encontrado",clase_cabecera="cabecera-resultado",producto_a_buscar=palabra,lista_productos=lista_productos)

#aplicar filtro seleccionado
#URL parametrizada --> usa como parametro el nombre del producto a buscar
@app.route('/productos_filtrados/<producto_a_buscar>',methods=['POST'])
def filtrar(producto_a_buscar):
    id_supermercados=request.form.getlist('supermercado')
    ordenprecio=request.form.get('precio')
    num_super_seleccionados=len(id_supermercados)
    #unifico la palabra a buscar para la consulta que realice a posteriori
    producto_a_buscar=database.unaccent(producto_a_buscar.lower())
    #parte inicial de la consulta a realizar
    query = sa.select(Producto).where(or_(Producto.nombre_busqueda.like(f'% {producto_a_buscar} %'),Producto.nombre_busqueda.like(f'{producto_a_buscar} %'),Producto.nombre_busqueda.like(f'% {producto_a_buscar}')))

    if num_super_seleccionados==1 or num_super_seleccionados==2:
        #impongo restriccion --> seleccionar productos de determinados supers
        condiciones = [Producto.id_supermercado==id_super for id_super in id_supermercados]
        query=query.where(or_(*condiciones))

    if ordenprecio:
        #ordenar por precio, ¿creciente o decreciente?
        if ordenprecio=="Creciente":
            query=query.order_by(Producto.precio.asc())
        else:
            query=query.order_by(Producto.precio.desc())
    lista_productos=db.session.scalars(query).all()
    #en el caso de no ordenar por precio, permutamos los productos a imprimir por pantalla para evitar que aparezcan por orden de supermercado
    if not ordenprecio:
        random.shuffle(lista_productos)
    return render_template('resultado.html',titulo="Resultado Encontrado",clase_cabecera="cabecera-resultado",producto_a_buscar=producto_a_buscar,lista_productos=lista_productos)




    




    