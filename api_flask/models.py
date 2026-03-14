from config import db #importar la referencia a la base de datos de firebase desde el archivo config.py para poder acceder a los datos de la base de datos en esta clase

class Product:
    def __init__(self, name, price, stock,id=None): #se define el constructor de la clase Product, con los atributos name, price, stock y un id opcional
        self.id=id
        self.name = name
        self.price = price
        self.stock = stock

    def to_dict(self): #convertir el objeto a un diccionario para facilitar su uso en JSON
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

    