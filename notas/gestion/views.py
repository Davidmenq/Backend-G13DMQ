from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from boto3 import session
from os import environ
from django.conf import settings

# Create your views here.
class Prueba(APIView):
    def get(self,request):
        return Response(data={'message':'hola'})
    
@api_view(['POST'])
def registrar(request:Request):
    serializador= RegistroSerializer(data=request.data)

    if serializador.is_valid():
        nuevoUsuario = Usuario(**serializador.validated_data)
        nuevoUsuario.set_password(serializador.validated_data.get('password'))
        
        nuevoUsuario.save()
        
        return Response(data={'message':'Usuario registrado exitosamente'}, status=201)
    else:
        return Response(data={
            'message':'Error al crear el usuario',
            'content': serializador.errors
        })

@api_view(['POST'])
def login(request: Request):
    serializador = loginSerializer(data=request.data)

    if serializador.is_valid():
        usuarioEncontrado = Usuario.objects.filter(
            correo=serializador.validated_data.get('correo')).first()
        
        if not usuarioEncontrado:
            return Response(data={
                'message': 'El usuario no existe'
            }, status=400)
        
        validacion_password = usuarioEncontrado.check_password(
            serializador.validated_data.get('password')
        )

        if validacion_password == False:
            return Response(data={
                'message':'Credenciales invalidas'
            }, status=400)
        
        token=AccessToken.for_user(usuarioEncontrado)

        return Response(data={
            'content': str(token)
        })

    else:
        return Response(data={
            'message': 'Error al hacer el login',
            'content': serializador.errors
        })

class NotaController(APIView):
    
    permission_classes=[IsAuthenticated]
    
    def post(self, request:Request):
        print('paso')
        serializador = NotaSerializer(data=request.data)
        print(request.user)
        print(request.user.nombre)
        usuarioLogeado: Usuario = request.user
        print('_____')
        print(request.auth)

        if serializador.is_valid():
            nuevaNota =Nota(usuario= usuarioLogeado, **serializador.validated_data)
            nuevaNota.save()

            if nuevaNota.imagen:
                subir_imagen_s3('{}/media/{}'.format(settings.BASE_DIR, nuevaNota))

            return Response(data={
                'message': 'Nota creada exitosamente'
            }, status=201)
        else:
            return Response(data={
                'message':'Error al crear la nota',
                'content': serializador.errors
            }, status=400)

    def get(self, request):
        pass

def subir_imagen_s3(nombre_imagen):
    if nombre_imagen in None:
        return 
    
    
    nuevaSesion=session.Session(aws_access_key_id=environ.get('AWS_ACCESS_KEY'), 
                                 aws_secret_access_key=environ.get('AWS_SECRET_KEY'),
                                   region_name=environ.get('AWS_BUCKET_REGION'))
    s3Client = nuevaSesion.client('s3')
    bucket=environ.get('AWS_BUCKET_NAME')
    with open(nombre_imagen, 'rb') as archivo:

        object_name=''
        
        try:    
            s3Client.upload_file(nombre_imagen, bucket, object_name)
        except Exception as e:
            print(e)

def devolver_url_firmada(nombre_imagen):
        if nombre_imagen in None:
            return 

        nuevaSesion=session.Session(aws_access_key_id=environ.get('AWS_ACCESS_KEY'), 
                                 aws_secret_access_key=environ.get('AWS_SECRET_KEY'),
                                   region_name=environ.get('AWS_BUCKET_REGION'))
        
        bucket=environ.get('AWS_BUCKET_NAME')
        s3Client = nuevaSesion.client('s3')
        
        

