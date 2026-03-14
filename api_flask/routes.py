from flask import request, jsonify
from config import database
from models import Product

"""Realtime Database usa push() para crear registros, y child() para navegar la estructura.
Los datos se guardan como JSON anidado en vez de colecciones y documentos."""

def register_routes(app): #definir una función register_routes que recibe la aplicación Flask como argumento para registrar las rutas de la API

    @app.route('/api/products', methods=['POST'])
    def create_product(): #definir la ruta POST /api/products para crear un nuevo producto en la base de datos de firebase
        data = request.get_json()

        if not data or 'name' not in data or 'price' not in data or 'stock' not in data:
            return jsonify({'error': 'Missing fields'}), 400

        new_product = Product(name=data['name'], price=data['price'], stock=data['stock'])

        ref = database.child('products').push(new_product.to_dict())
        new_product.id = ref.key

        return jsonify({'id': new_product.id, 'name': new_product.name}), 201


    @app.route('/api/products', methods=['GET'])
    def get_products(): #definir la ruta GET /api/products para obtener la lista de productos desde la base de datos de firebase
        ref = database.child('products').get()

        if not ref:
            return jsonify([]), 200

        products = []
        for key, value in ref.items():
            value['id'] = key
            products.append(value)

        return jsonify(products), 200


    @app.route('/api/products/<id>', methods=['GET'])
    def verify_stock(id): #definir la ruta GET /api/products/<id> para verificar el stock de un producto específico en la base de datos de firebase utilizando su id
        ref = database.child('products').child(id).get()

        if not ref:
            return jsonify({'error': 'Product not found'}), 404

        return jsonify({
            'id':        id,
            'name':      ref['name'],
            'price':     ref['price'],
            'stock':     ref['stock'],
            'available': ref['stock'] > 0
        }), 200


    @app.route('/api/products/<id>', methods=['PUT'])
    def update_stock(id): #definir la ruta PUT /api/products/<id> para actualizar el stock de un producto específico en la base de datos de firebase utilizando su id y el nuevo stock enviado en el cuerpo de la solicitud
        data = request.get_json()

        if not data or 'amount' not in data:
            return jsonify({'error': 'El campo amount es requerido'}), 400

        ref = database.child('products').child(id)
        product = ref.get()

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        previous_stock = product['stock']
        new_stock = previous_stock - data['amount']

        if new_stock < 0:
            return jsonify({'error': 'Stock insuficiente'}), 400

        ref.update({'stock': new_stock})

        return jsonify({
            'id':             id,
            'name':           product['name'],
            'message':        'Stock updated successfully',
            'previous_stock': previous_stock,
            'new_stock':      new_stock
        }), 200