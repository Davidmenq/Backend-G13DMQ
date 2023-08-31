import sumar from "./funcionabilidad.js";
import { restar } from "./funcionabilidad.js";
import isOdd from "is-odd-num";
import esPar, { esMayor } from "./practica.js"

const nombre = 'eduardo';
let edad = 20;

edad = 18;

console.log(edad);

let resultado = sumar(5,4);

console.log(resultado);

resultado = isOdd(10);

console.log(resultado);

console.log(esPar(10));

console.log(esMayor());


