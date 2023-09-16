import express from 'express';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import { categoriaRouter } from './routes/categorias.routes.js';

dotenv.config();

const server = express()
server.use(express.json())
const PORT = process.env.PORT ?? 3000

const conectarBd = async()=>{
    await mongoose.connect(process.env.MONGODB_URL);
    console.log('conexion exitosa a la base de datos');
}

//creamos un manejador de errores
//SE VA A COMPORTAR COMO UN MIDDLEWARE
function errorHandler(error, req, res, next){
    // console.log(error)
    // console.log("________")
    // console.log(error.status)
    // console.log("________")
    // console.log(error.message)

    return res.status(error.status ?? 400).json({
        message: error.message,
    })
}

//aca recien van nuestras routes, va siempre antes del errorHandler
server.use(categoriaRouter)

// aca utilizaremos el manejador de errores
// ESTE MENSAJE SIEMPRE DEBE IR DESPUES DE TODAS LAS RUTAS!!!
server.use(errorHandler);



server.listen(PORT, async()=>{
    console.log(`Servidor corriendo exitosamente en el puerto ${PORT}`)
    await conectarBd()
})