import mongoose from 'mongoose';

const categoriaSchema = new mongoose.Schema({
    nombre: {
        type: mongoose.Schema.Types.String,
        required: true,
        uppercase: true,
    },
    habilitado:{
        type: mongoose.Schema.Types.Boolean,
        default: true,
    }
},{
    timestamps:{
        updatedAt: false,
        createdAt: 'fecha_creacion',
    }
})

//es la que realizara la creacion y el mapeo de todas las columnas que hemos configurado
export const CategoriaModel = mongoose.model('categorias', categoriaSchema)