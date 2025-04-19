class NodoVuelo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None

class ListaVuelos:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self._longitud = 0

    def insertar_al_frente(self, vuelo):
        nuevo = NodoVuelo(vuelo)
        if not self.primero:
            self.primero = self.ultimo = nuevo
        else:
            nuevo.siguiente = self.primero
            self.primero.anterior = nuevo
            self.primero = nuevo
        self._longitud += 1

    def insertar_al_final(self, vuelo):
        nuevo = NodoVuelo(vuelo)
        if not self.ultimo:
            self.primero = self.ultimo = nuevo
        else:
            nuevo.anterior = self.ultimo
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self._longitud += 1

    def obtener_primero(self):
        return self.primero.vuelo if self.primero else None

    def obtener_ultimo(self):
        return self.ultimo.vuelo if self.ultimo else None

    def longitud(self):
        return self._longitud

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion <= 0:
            self.insertar_al_frente(vuelo)
        elif posicion >= self._longitud:
            self.insertar_al_final(vuelo)
        else:
            nuevo = NodoVuelo(vuelo)
            actual = self.primero
            for _ in range(posicion):
                actual = actual.siguiente
            anterior = actual.anterior
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            anterior.siguiente = nuevo
            actual.anterior = nuevo
            self._longitud += 1

    def extraer_de_posicion(self, posicion):
        if self._longitud == 0 or posicion < 0 or posicion >= self._longitud:
            return None
        if posicion == 0:
            vuelo = self.primero.vuelo
            self.primero = self.primero.siguiente
            if self.primero:
                self.primero.anterior = None
            else:
                self.ultimo = None
        elif posicion == self._longitud - 1:
            vuelo = self.ultimo.vuelo
            self.ultimo = self.ultimo.anterior
            if self.ultimo:
                self.ultimo.siguiente = None
            else:
                self.primero = None
        else:
            actual = self.primero
            for _ in range(posicion):
                actual = actual.siguiente
            vuelo = actual.vuelo
            actual.anterior.siguiente = actual.siguiente
            actual.siguiente.anterior = actual.anterior
        self._longitud -= 1
        return vuelo

    def listar_vuelos(self):
        vuelos = []
        actual = self.primero
        while actual:
            vuelos.append(actual.vuelo)
            actual = actual.siguiente
        return vuelos

    def reordenar(self, nuevo_orden: list):
        vuelos_actuales = self.listar_vuelos()
        if len(nuevo_orden) != len(vuelos_actuales):
            raise ValueError("El nuevo orden no coincide con el número de vuelos")
        nueva_lista = [vuelos_actuales[i] for i in nuevo_orden]
        self.__init__()
        for vuelo in nueva_lista:
            self.insertar_al_final(vuelo)

