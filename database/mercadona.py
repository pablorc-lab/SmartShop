import requests
from config_selenium import unaccent

def productos_mercadona(url, lista_mercadona):
    headers = {'Content-Type': 'application/json;charset=UTF-8', 'Access-Control-Allow-Origin': '*'}

    # Obtener el contenido
    r = requests.get(url, headers=headers)

    # Convertir el contenido JSON en un diccionario
    contenido = r.json()

    for categoria in contenido['categories']:
      for producto in categoria['products']:
        nombre = producto['display_name']
        
        peso = str(producto['price_instructions']['unit_size']) 
        unidad_peso = producto['price_instructions']['size_format']

        if peso != "None":
            nombre = nombre + " " + peso + " " + unidad_peso # Le añadimos el peso

        if producto['price_instructions']['unit_name'] is not None:
            nombre = nombre + " (" + str(producto['price_instructions']['unit_name']) + ")"  # Agregar el nombre de la unidad

        precio_unit = producto['price_instructions']['bulk_price'] + " €/" + unidad_peso
        precio = producto['price_instructions']['unit_price']
        imagen = producto['thumbnail']
        
        lista_mercadona.add((nombre, float(precio), precio_unit, imagen, 3, unaccent(nombre.lower())))



# Esta funcion busca los valores en cada categoría
def categorias_mercadona():
    lista_mercadona = set()

    #Subcategoria aceites
    categorias = {
        "Aceite, vinagre y sal": "112",
        "Refresco de cola" : "158",
        "Refresco de naranja y de limón" : "159",
        "Refresco de té y sin gas" : "162",
        "Arroz" : "118",
        "Legumbres" : "121",
        "Pasta y fideos" : "120",
        "Aves y pollo" : "38",
        "Cerdo" : "37",
        "Hamburguesas y picadas" : "44",
        "Vacuno" : "40",
        "Empanador y elaborados" : "45",
        "Marisco" : "32",
        "Pescado congelado" : "34",
        "Pescado fresco" : "31",
        "Atún y otras conseras" : "122",
        "Leche y bebidas vegetales" : "72",
        "Huevos" : "77",
        "Gelatina y otros postres" : "111",
        "Yogures líquidos" : "108",
        "Yogures naturales y sabores" : "104",
        "Yogures y postres infantiles" : "107",
        "Pizzas" : "138",
        "Platos preparados calientes" : "140",
        "Platos preparados fríos" : "142",
        "Pan de horno" : "59",
        "Pan de molde y otros" : "60",
        "Bollería envasada" : "66",
        "Fruta" : "27",
        "Lechuga y ensalada preparada" : "28",
        "Verdura" : "29",
        "Queso curado, semicurado y tierno" : "54",
        "Queso lonchas, rallado y en porciones" : "56",
        "Jamón Serrano" : "50",
        "Cereales" : "78",
        "Galletas" : "80",
        "Helados" : "154",
        "Patatas fritas y snacks" : "132",
        "Fruta variada" : "99"
    }

    url_base = 'https://tienda.mercadona.es/api/categories/'

    # Recorremos las categorías
    for nombre in categorias:
        id_categoria = categorias[nombre]
        productos_mercadona(url_base+id_categoria, lista_mercadona)

    return lista_mercadona