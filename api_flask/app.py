from flask import Flask #importar la clase Flask del módulo flask para crear una aplicación web
import routes #importar el módulo routes que contiene las rutas de la aplicación

app=Flask(__name__) #crear una instancia de la aplicación Flask
routes.register_routes(app) #registrar las rutas definidas en el módulo routes.py en la aplicación Flask

if __name__ == '__main__':
    app.run(debug=True)