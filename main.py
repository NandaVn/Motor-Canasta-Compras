#                     ---------- TAREA 2 , 4 Y 5 ----------
'''
import pandas as pd: Trae la libreria Pandas que es el estadar de la industria para manipular tablas de datos.
from estructuras import ListaEnlazada: Conecta el archivo principal con el TDA que construimos a mano.
'''
import sys
import pandas as pd
from estructuras import Nodo, ListaEnlazada
'''
Lee la pestaña 'online Retal' del excel, elimina filas que no tengan numero de factura o codigo de producto(dropna), y crea un diccionario llamado facturas_db. Si una factura no existe en el diccionario, crea una nueva ListaEnlazadavacia, si ya existe,inserta el producto en esa lista.
'''

def cargar_y_vincular_datos(ruta_archivo, limite_filas=None):
    df = pd.read_excel(ruta_archivo, sheet_name='Online Retail')
    df = df.dropna(subset=['InvoiceNo', 'StockCode'])
    if limite_filas:
        df = df.head(limite_filas)
        
    facturas_db = {}
    for index, fila in df.iterrows():
        invoice_no = fila['InvoiceNo']
        datos_linea = {
            'StockCode': fila['StockCode'],
            'Description': fila['Description'],
            'Quantity': fila['Quantity'],
            'UnitPrice': fila['UnitPrice'],
            'CustomerID': fila['CustomerID']
        }
        if invoice_no not in facturas_db:
            facturas_db[invoice_no] = ListaEnlazada()
            
        lista_actual = facturas_db[invoice_no]
        lista_actual.insertar(lista_actual.contar(), datos_linea)
        
    return facturas_db

'''
La primera iteracion calcula el total de una sola factura multiplicando cantidad por precio unitario. La segunda busca en todo el diccionario facturas_db las listas que le pertenecen a un clinete especifico (customer_id) y suma sus facturas para ver cuanto ha gastado en total.
'''

def calcular_total_factura_enlazada(lista_factura):
    total = 0.0
    for linea in lista_factura.recorrer():
        total += linea['Quantity'] * linea['UnitPrice']
    return total

def calcular_acumulado_cliente_enlazada(facturas_db, customer_id):
    total_acumulado = 0.0
    for invoice_no, lista_factura in facturas_db.items():
        if lista_factura.cabeza and lista_factura.cabeza.datos['CustomerID'] == customer_id:
            total_acumulado += calcular_total_factura_enlazada(lista_factura)
    return total_acumulado

'''
Aumenta el limite de memoria del sistema con sys.setrecursionlimit(2500) para soportar listas largas. Luego, abre cada factura del diccionario y detona la busqueda recursiva que programamos en estructuras.py. 
'''

def buscar_producto_en_subconjunto(facturas_db, stock_code):
    lineas_encontradas = []
    sys.setrecursionlimit(2500) # Prevención de límite de recursión
    
    for invoice_no, lista_factura in facturas_db.items():
        if lista_factura.cabeza is not None:
            resultados_factura = lista_factura.buscar_producto_recursivo(
                lista_factura.cabeza, 
                stock_code
            )
            lineas_encontradas.extend(resultados_factura)
            
    return lineas_encontradas

'''
Asegura que el codigo principal solo corra si tu ejecutas el archivo directamente. aqui cargas solo 5,000 filas (para no saturar la RAM de la computadora) e inicias la prueba buscando el codigo '85123A'. 
'''

if __name__ == "__main__":
    print("Cargando base de datos...")
    # Prueba con las primeras 5000 filas para rapidez
    base_de_datos = cargar_y_vincular_datos("Online Retail.xlsx", limite_filas=5000)
    
    producto_a_buscar = '85123A'
    resultados = buscar_producto_en_subconjunto(base_de_datos, producto_a_buscar)
    print(f"Se encontraron {len(resultados)} líneas con el producto {producto_a_buscar}.")