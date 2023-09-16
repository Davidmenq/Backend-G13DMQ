import { Router } from "express";
import * as categoriasController from '../controllers/categorias.controllers.js'
import asyncHandler from 'express-async-handler'

export const categoriaRouter = Router()

categoriaRouter.route('/categorias')
                .post(asyncHandler(categoriasController.crearCategoria))
                .get(asyncHandler(categoriasController.devolverCategorias))

categoriaRouter.route('/categoria/:id').put(asyncHandler(categoriasController.modificarCategoria))