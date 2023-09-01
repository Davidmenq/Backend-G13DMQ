import express from "express";

const servidor = express();
const PORT = 3000;
servidor.listen(PORT,()=>{
    console.log(`servidor corriendo exitosamente en el puerto ${PORT}`);
});