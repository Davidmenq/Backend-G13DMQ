from psycopg2 import connect

conector =connect(database='postgres',
                  user='postgres',
                  password='root',
                  host='localhost',
                  port='5432')
conector.autocommit=True

cursor=conector.cursor()

def crearBD(bd):
    cursor.execute('SeleCT datname FROM pg_database')
    resultado=cursor.fetchall()
    if(bd,) in resultado:
        print('ya existe')
        return
    cursor.execute(f'CREATE DATABASE {bd}')

    print('BASE DE DATOS CREADA EXITOSAMENTE')
    conector.close()

crearBD('prueba3')