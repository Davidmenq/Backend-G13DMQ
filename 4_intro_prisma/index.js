import express from "express";
import Prisma, {NivelAcademico, TipoSanguineo} from "@prisma/client";
import Joi from "joi";
import swaggerUI from "swagger-ui-express";
import archivoSwagger from "./swagger.json" assert {type:"json"};
import cors from "cors";


const conexion =  new Prisma.PrismaClient()

const servidor = express();

const seccionSchema = Joi.object({
    nombre: Joi.string().required(),
});

const alumnoSchema = Joi.object({
    nombre: Joi.string().required(),
    apellido: Joi.string().required(),
    correo: Joi.string().email().required(),
    telefonoEmergencia: Joi.string().pattern(new RegExp("^[0-9]")).required(),
    grupoSanguineo: Joi.string()
        .valid(
            TipoSanguineo.AB_NEGATIVO,
            TipoSanguineo.AB_POSITIVO,
            TipoSanguineo.A_NEGATIVO,
            TipoSanguineo.A_POSITIVO,
            TipoSanguineo.B_NEGATIVO,
            TipoSanguineo.B_POSITIVO,
            TipoSanguineo.O_NEGATIVO,
            TipoSanguineo.O_POSITIVO,
         )
        .optional(),
})

const anioLectivoSchema = Joi.object({
    alumnoId: Joi.string().uuid({version:"uuidv4"}).required(),
    gradoId: Joi.string().uuid({version:"uuidv4"}).required(),
    seccionId: Joi.string().uuid({version: "uuidv4"}).required(),
    anio: Joi.string().required(),
    nivel: Joi.string()
        .valid(NivelAcademico.PRIMARIA, NivelAcademico.SECUNDARIA)
        .required(),
});

servidor.use(
    cors({
        origin:[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://mifrontend.com",
        ],
        methods:["GET", "POST", "PUT", "DELETE"],
        allowedHeaders:["Authorization", "Content-Type", "Accept"],
    })
);
servidor.use('/docs', swaggerUI.serve, swaggerUI.setup(archivoSwagger))
servidor.use(express.json());

const PORT = 3000;

servidor
    .route("/grados")
    .post(async(req,res)=>{
        const { body: data } = req;

        try{
            const resultado = await conexion.grado.create({
                data,
                // {
                //     nombreNumerico: body.nombreNumerico,
                //     nombreTexto: body.nombreTexto,
                // }
            });

            console.log(resultado);

            res.json({
                message: "Grado creado exitosamente",
            });
        } catch(error){
            res.json({
                message: "Error al crear el grado",
            })
        }
    })
    .get(async(req, res)=> {
        const resultado = await conexion.grado.findMany();

        res.json({
            content: resultado,
        })
    })

servidor
    .route('/grado/:id')
    .all(async(req, res, next) => {
        //console.log("yo me ejecuto");
        const {id}= req.params;
        try{
            const gradoEncontrado = await conexion.grado.findUniqueOrThrow({
                where: {id:id},
            });
            req.grado = gradoEncontrado;
        } catch (error){
            if(error instanceof Prisma.Prisma.PrismaClientKnownRequestError){
                return res.status(400).json({
                    message: "Id del curso invalido",
                })

            }
            return res.status(400).json({
                message:" Error al buscar el curso",
            });
        }

        next();
    })
    .get(async(req, res) => {
        console.log(req.grado);

        return res.json({
            content: req.grado,
        });
    })
    .put(async(req, res) => {
        const {body}=req;

        const respuesta = await conexion.grado.update({
            where: {id:req.grado.id},
            data: body,
        });

        return res.json({
            message: "Grado actualizado exitosamente",
            content: respuesta,
        })
    } )
    .delete(async(req, res) => {
        const respuesta = await conexion.grado.delete({
            where: {id: req.grado.id},
        });

        return res.json({
            message: "Grado eliminado exitosamente",
            content: respuesta,
        });
    })
  
servidor.route("/secciones").post(async(req,res)=>{
    const {body}=req;
    const {value, error}= seccionSchema.validate(body);

    if(error){
        return res.status(400).json({
            message: " Error al crear la seccion",
            content: error,
        })
    }
    
    const seccionCreada = await conexion.seccion.create({data: value});
    
    return res.json({
        message: "seccion creada exitosamente",
        content: seccionCreada,
    });
  
})
.get(async(req, res)=>{
    const resultado = await conexion.seccion.findMany();

    return res.json({
        content: resultado,
    })
})

servidor.route("/alumnos").post(async(req, res)=>{
    const { error, value }=alumnoSchema.validate(req.body);

    if(error){
        return res.json({
            message: "Error al crear el alumno",
            content: error.details,        
        })
    }

    const respuesta = await conexion.alumno.create({data:value});

    return res.status(201).json({
        message:"Alumno creado exitosamente",
        content: respuesta,
    });

})

servidor.route("/anio-lectivo").post(async(req,res)=>{
    const {error, value} = anioLectivoSchema.validate(req.body);

    if (error){
        return res.json({
            message: "Error al crear el año lectivo",
            content: error.details,
        });
    }

    // TODO: VALIDAR QUE EL ALUMNOID, GRADOID Y SECCIONID existan, 
    // sino existe no permitir la creacion del año lectivo
    await conexion.anioLectivo.create({data:value});

    return res.status(201).json({
        message: "Año lectivo creado exitosamente",
    });

});


servidor.listen(PORT,()=>{
    console.log(`servidor corriendo exitosamente en el puerto ${PORT}`);
});