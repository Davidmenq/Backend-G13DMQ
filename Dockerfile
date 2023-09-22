# indica la imagen para construir el contenedor
FROM python:3.11.5-alpine

WORKDIR /app

# crea la carpeta de trabajo dentro del contenedor
# esta ubicacion solo existe en el contenedor
# RUN mkdir -p /app

# copia todo el contenido local hacia la carpeta creada en el comando anterior
COPY . .

RUN     apk update \
        && apk add musl-dev libpq-dev gcc

#ejecuta un comando
RUN pip install -r requirements.txt

# exponemos el puerto que podra acceder al contenedor de manera externa
EXPOSE 8000

#para ejecutar el comando
CMD ["python", "notas/manage.py", "runserver", "0.0.0.0:8000"]
