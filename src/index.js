import express from 'express';
import mongoose from 'mongoose';

const server = express()
const PORT = process.env.PORT ?? 3000

const conectarBd = async()=>{
    await mongoose.connect(process.env.MONGODB_URL)
    console.log('conexion exitosa a la base de datos')
}

server.listen(PORT,async()=>{
    console.log(`Servidor corriendo exitosamente en el puerto ${PORT}`)
    await conectarBd;
})