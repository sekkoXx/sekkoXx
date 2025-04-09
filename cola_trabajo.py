class ArrayQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Agrega un elemento al final de la cola"""
        self.items.append(item)

    def dequeue(self):
        """Elimina y retorna el primer elemento de la cola"""
        if self.is_empty():
            return None
        return self.items.pop(0)

    def first(self):
        """Retorna el primer elemento sin eliminarlo"""
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        """Retorna True si la cola está vacía"""
        return len(self.items) == 0

    def size(self):
        """Retorna la cantidad de elementos en la cola"""
        return len(self.items)

    def __str__(self):
        return f"Cola: {self.items}"

    def __repr__(self):
        return self.__str__()
    