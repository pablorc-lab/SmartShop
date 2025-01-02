from config_selenium import web_driver, unaccent
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

"""
Función que extrae la información de cada producto. Concretamente la URL de la imagen, el titulo 
y el precio del mismo utilizando BeatifulSoup para extraer la etiqueta HTML y su correspondiente

La función `enlace_productos` toma el `driver` y luego, utilizando Selenium WebDriver y BeautifulSoup, 
la función busca cada imagen, y cuando toma cada una buscamos el onmbre y precio de su producto.

Esto lo hacemos puesto que en muchos casos la imagen tarda mas en cargar y a veces se puede capturar el 
nombre y precio pero no la imagen del producto, de esta forma nos aseguramos que tengamos todo
"""
def productos_alcampo(driver, lista_alcampo):
    scroll_pause_time = 5  # Pausa entre cada scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Tamaño de ventana
    i = 1

    while True:
        # Hacer scroll hacia abajo
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        sleep(scroll_pause_time)

        # Extraemos las URL de las imagenes
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        imagenes = soup.findAll("img", attrs={"data-test":"lazy-load-image"})
        for imagen in imagenes:
            product_card = imagen.parent.parent.parent.parent
            
            nombre = imagen.get("alt") # En la propia imagen aparece en "alt" su nombre
            
            precio = product_card.find("span", attrs={"data-test":"fop-price"})
            precio = precio.text.split()[0]
            precio = precio.replace(',', '.')  # Reemplazar la coma por un punto

            precio_kg = product_card.find("span", attrs={"data-test":"fop-price-per-unit"})
            precio_kg = (precio_kg.text.replace("(","")).replace(")","")
            lista_alcampo.add((nombre, float(precio), precio_kg, imagen.get("src"), 1, unaccent(nombre.lower())))

        # Comprobar si es el final de la página
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break



# Este fragmento de código se encarga de tomar los valores de los productos 
# pertenecientes a las categorías deseadas
def categorias_alcampo():
    lista_alcampo = set()

    # Acceso a la pagina inicial donde visualizo las diferentes categorias
    driver = web_driver()
    driver.get("https://www.compraonline.alcampo.es/categories?source=navigation")
    sleep(8)

    boton = driver.find_element(By.ID,"onetrust-accept-btn-handler")
    boton.click()
    sleep(8)
    boton = driver.find_element(By.CLASS_NAME,"box-close")
    boton.click()
    sleep(2)
    

    seleccionables = [
        "Frescos","Leche, Huevos, Lácteos, Yogures y Bebidas vegetales",
        "Desayuno y Merienda",
        "Congelados","Comida Preparada",
        "Bebidas"]
    
    for categoria in seleccionables:
        # Pincho sobre dicho categoria, localizando el boton
        boton = driver.find_element(By.XPATH,f'//a[text()="{categoria}"]')

        # Scraping sobre la categoria deseada
        boton.click()
        sleep(5) #esperamos a que se carguen los recursos de la nueva pagina web abierta
        
        # Ejecutamos la función para el WebScrapping
        productos_alcampo(driver, lista_alcampo)

        # Tras escrapear, volvemos a la pagina inicial para pinchar en la siguiente categoria
        driver.get("https://www.compraonline.alcampo.es/categories?source=navigation")
        sleep(5)

    driver.quit()
    return lista_alcampo

