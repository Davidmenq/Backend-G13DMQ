export default function esPar(num){

    if (num%2===0) {
        return console.log('es un numero par');
    } else{
        return console.log('es impar');
    }

}

export function esMayor(){
    let notas = [12,7,14,8,4,8,18];
    let mayoresADiez = notas.filter((num)=> num>10); 
    return mayoresADiez;
}

export function notas(){

}

let num =20;

if (num%2===0) {
    console.log('es un numero par');
} else{
    console.log('es impar');
}
