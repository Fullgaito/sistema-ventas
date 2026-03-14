const mongoose = require('mongoose') // Esquema para la colección de ventas

const saleSchema = new mongoose.Schema({ // Definición del esquema de venta
    usuario_id: { // ID del usuario que realizó la compra
        type: String,
        required: true
    },
    productos: [ // Lista de productos comprados
        {
            producto_id: { type: String, required: true },
            nombre:      { type: String, required: true },
            cantidad:    { type: Number, required: true },
            precio:      { type: Number, required: true }
        }
    ],
    total: { // Total de la venta
        type: Number,
        required: true
    },
    fecha: { // Fecha de la venta
        type: Date,
        default: Date.now
    }
})

module.exports = mongoose.model('Sale', saleSchema)