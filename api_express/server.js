const express = require('express') // Framework para construir la API
const mongoose = require('mongoose') // ODM para interactuar con MongoDB
const dotenv = require('dotenv') // Cargar variables de entorno
const salesRoutes = require('./routes/sales') // Rutas para manejar las ventas

dotenv.config() // Cargar variables de entorno desde el archivo .env

const app = express() // Crear una instancia de Express
app.use(express.json()) // Middleware para parsear JSON en las solicitudes

// ── Conexión a MongoDB ───────────────────────────────────────────
mongoose.connect(process.env.MONGODB_URI)
    .then(() => console.log('Conectado a MongoDB'))
    .catch(err => console.error('Error conectando a MongoDB:', err))

// ── Rutas ────────────────────────────────────────────────────────
app.use('/sales', salesRoutes)

// ── Arrancar servidor ────────────────────────────────────────────
const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
    console.log(`Servidor corriendo en puerto ${PORT}`)
})