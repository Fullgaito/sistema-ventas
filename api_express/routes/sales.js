const express = require('express') // Rutas para manejar las ventas
const router = express.Router() // Controlador de ventas
const Sale = require('../models/Sale') // Modelo de venta

// ── POST /sales ──────────────────────────────────────────────────
router.post('/', async (req, res) => { // Registrar una nueva venta
    try {
        const { usuario_id, productos, total } = req.body // Extraer datos de la venta

        if (!usuario_id || !productos || !total) { // Validar campos requeridos
            return res.status(400).json({ error: 'Missing fields' })
        }

        const newSale = new Sale({ usuario_id, productos, total }) // Crear una nueva instancia de venta
        await newSale.save() // Guardar la venta en la base de datos

        return res.status(201).json({ // Responder con éxito
            message: 'Sale registered successfully',
            id:      newSale._id
        })
    } catch (error) { // Manejar errores
        return res.status(500).json({ error: error.message })
    }
})

// ── GET /sales ───────────────────────────────────────────────────
router.get('/', async (req, res) => { // Obtener todas las ventas
    try { // Buscar todas las ventas en la base de datos
        const sales = await Sale.find()
        return res.status(200).json(sales)
    } catch (error) { // Manejar errores
        return res.status(500).json({ error: error.message })
    }
})

// ── GET /sales/fecha?start=&end= ─────────────────────────────────
router.get('/fecha', async (req, res) => { // Obtener ventas por rango de fechas
    try { // Extraer parámetros de fecha de la consulta
        const { start, end } = req.query

        if (!start || !end) { // Validar que ambos parámetros estén presentes
            return res.status(400).json({ error: 'Los campos start y end son requeridos' })
        }

        const sales = await Sale.find({ // Buscar ventas dentro del rango de fechas
            fecha: { // Comparar la fecha de la venta con el rango proporcionado
                $gte: new Date(start),
                $lte: new Date(end)
            }
        })

        return res.status(200).json(sales) // Responder con las ventas encontradas
    } catch (error) { // Manejar errores
        return res.status(500).json({ error: error.message })
    }
})

// ── GET /sales/usuario/:usuario_id ───────────────────────────────
router.get('/usuario/:usuario_id', async (req, res) => { // Obtener ventas por ID de usuario
    try {
        const sales = await Sale.find({ usuario_id: req.params.usuario_id })

        if (!sales.length) { // Si no se encuentran ventas para el usuario, responder con un error 404
            return res.status(404).json({ error: 'No se encontraron ventas para este usuario' })
        }

        return res.status(200).json(sales) // Responder con las ventas encontradas para el usuario
    } catch (error) { // Manejar errores
        return res.status(500).json({ error: error.message })
    }
})

module.exports = router // Exportar el router para usarlo en server.js