from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly


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
        print('ingreso')

        serializador = NotaSerializer(data=request.data)
        if serializador.is_valid():
            pass
        else:
            return Response(data={
                'message':'Error al crear la nota',
                'content': serializador.errors
            }, status=400)

    def get(self, request):
        pass

