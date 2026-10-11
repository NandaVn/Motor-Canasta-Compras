#                                      ---------- TAREA 1 Y 3 ----------
class Nodo:
    """
    Representa un elemento individual en la lista enlazada.
    """
    def __init__(self, datos):
        self.datos = datos      
        self.siguiente = None   

class ListaEnlazada:
    """
    Estructura manual para gestionar líneas de compra sin listas nativas.
    """
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def contar(self):
        return self.tamano

    def insertar(self, posicion, datos):
        if posicion < 0 or posicion > self.tamano:
            raise IndexError("Posición de inserción fuera de rango.")
        
        nuevo_nodo = Nodo(datos)
        
        if posicion == 0:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            for _ in range(posicion - 1):
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
            
        self.tamano += 1

    def eliminar(self, posicion):
        if posicion < 0 or posicion >= self.tamano:
            raise IndexError("Posición de eliminación fuera de rango.")
        
        if posicion == 0:
            datos_eliminados = self.cabeza.datos
            self.cabeza = self.cabeza.siguiente
        else:
            actual = self.cabeza
            for _ in range(posicion - 1):
                actual = actual.siguiente
            nodo_a_eliminar = actual.siguiente
            datos_eliminados = nodo_a_eliminar.datos
            actual.siguiente = nodo_a_eliminar.siguiente
            
        self.tamano -= 1
        return datos_eliminados

    def recorrer(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.datos
            actual = actual.siguiente

    def buscar_producto_recursivo(self, nodo_actual, stock_code, resultados=None):
        """Busca líneas de un producto de forma recursiva (Problema 3)."""
        if resultados is None:
            resultados = []
            
        if nodo_actual is None: # Caso base
            return resultados
            
        if nodo_actual.datos['StockCode'] == stock_code:
            resultados.append(nodo_actual.datos)
            
        # Caso recursivo
        return self.buscar_producto_recursivo(nodo_actual.siguiente, stock_code, resultados)
