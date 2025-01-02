from config_selenium import web_driver, unaccent
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Función que realiza lo mismo que la del Alcampo pero 
#  con algunos cambios en la busqueda para el DIA.
def productos_dia(driver, lista_dia):
    URL_base_dia = "https://www.dia.es"

    scroll_pause_time = 5  # Pausa entre cada scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Tamaño de ventana
    i = 1

    while True:
        # Hacer scroll hacia abajo
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        sleep(scroll_pause_time)

        # Comprobar si es el final de la página
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break

    #una vez cargadas todas las imagenes...
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    imagenes = soup.findAll("img", attrs={"class":"search-product-card__product-image"})

    for imagen in imagenes:
        padre = imagen.parent

        #su siguiente hermano contiene el nombre del producto
        nombre = padre.next_sibling.text

        #procedo a tomar el precio del producto
        precio = padre.parent.parent.next_sibling.find("p",attrs={"data-test-id":"search-product-card-unit-price"})
        precio = precio.text.split()[0]
        precio = precio.replace(",",".")
        #precio por kg/L
        precio_kg = padre.parent.parent.next_sibling.find("p",attrs={"data-test-id":"search-product-card-kilo-price"})
        precio_kg = ((precio_kg.text.replace("\xa0"," ")).replace("(","")).replace(")","")
        #guardo en mi lista de productos
        #print((nombre, float(precio), precio_kg, URL_base_dia + imagen.get("src"), 2, unaccent(nombre.lower())))
        lista_dia.add((nombre, float(precio), precio_kg, URL_base_dia + imagen.get("src"), 2, unaccent(nombre.lower())))



# Esta función se encarga de hacer scrapping en las diferentes subcategorías 
# de una categoría principal
def scraping_subcategorias(driver, lista_dia):
    # Identifico las subcategorias dentro de la categoria principal seleccionada
    subcategorias=driver.find_elements(By.CLASS_NAME,"sub-category-item__link")
    for j in range(0,len(subcategorias)):
        #pincho en la subcategoria
        subcategorias[j].click()
        sleep(3)
        productos_dia(driver, lista_dia)



# Este código se encarga de tomar nombre, precio y URL de la imagen de cada producto
def categorias_dia():
    lista_dia = set()

    driver = web_driver()
    driver.get("https://www.dia.es")
    sleep(3)
    
    boton = driver.find_element(By.ID,"onetrust-accept-btn-handler")
    boton.click()
    sleep(3)
    
    boton = driver.find_element(By.CLASS_NAME,"category-button")
    boton.click()
    sleep(3)

    #seleccionar las categorias principales
    categorias_principales = driver.find_elements(By.XPATH,'//div[@class="category-item"]')
    categorias_principales = categorias_principales[:-4]

    #scrapeo las subcategorias de la 1º categoria
    scraping_subcategorias(driver,lista_dia)
    
    for i in range(1,len(categorias_principales)):
        categorias_principales[i].click()
        sleep(3)
        scraping_subcategorias(driver, lista_dia)
    

    driver.quit() #cerramos sesion abierta son selenium
    return lista_dia