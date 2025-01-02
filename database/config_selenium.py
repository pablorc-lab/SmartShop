from selenium import webdriver
import unicodedata

def unaccent(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def web_driver():
    
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless') # Sin ventana gráfica
    options.add_argument('--disable-gpu') # Realizar el proceso mas rápido sin interfaz
    options.add_argument("--window-size=1920,1080")  # Ajusta el tamaño de la ventana según tus necesidades
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()  # Maximiza la ventana del navegador
    
    return driver
