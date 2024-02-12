from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import Usuario, Alquiler, Patinete
from .serializers import UsuarioSerializer, AlquilerSerializer, PatineteSerializer


def calcular_coste_final(alquiler):
    tiempo = alquiler.fecha_desbloqueo - alquiler.fecha_entrega
    coste_final = tiempo * alquiler.patinete.precio_minuto + alquiler.patinete.precio_desbloqueo
    return coste_final


# Create your views here.
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['get'])
    def usuarios_por_debito(self, request):
        usuarios_ordenados = Usuario.objects.order_by('-debito')
        serializer = UsuarioSerializer(usuarios_ordenados, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_tres_usuarios_alquileres(self, request):
        usuarios_top_tres = Usuario.objects.annotate(num_alquileres=Count('alquiler')).order_by('-num_alquileres')[:3]
        serializer = UsuarioSerializer(usuarios_top_tres, many=True)
        return Response(serializer.data)


class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer

    @action(detail=False, methods=['post'])
    def alquilar(self, request):
        usuario = request.user
        patinete_id = request.data.get('patinete_id')

        try:
            patinete = Patinete.objects.get(id=patinete_id)
        except Patinete.DoesNotExist:
            return Response({'error': 'Patinete no encontrado'}, status=400)

        # Verificar si el patinete está disponible
        if patinete.alquiler is not None and patinete.alquiler.fecha_entrega is None:
            return Response({'error': 'Patinete ya está en alquiler'}, status=400)

        fecha_desbloqueo = timezone.now()

        Alquiler.objects.create(usuario=usuario, patinete=patinete, fecha_desbloqueo=fecha_desbloqueo)

        return Response({'success': 'Alquiler iniciado correctamente'})

    @action(detail=False, methods=['post'])
    def liberar(self, request):
        usuario = request.user
        patinete_id = request.data.get('patinete_id')  # Asegúrate de que este campo esté presente en tu request

        try:
            alquiler = Alquiler.objects.get(usuario=usuario, patinete__id=patinete_id, fecha_entrega=None)
        except Alquiler.DoesNotExist:
            return Response({'error': 'No se encontró un alquiler activo para este usuario y patinete'}, status=400)

        # Calcula el coste final y actualiza el débito del usuario
        alquiler.coste_final = calcular_coste_final(alquiler)
        usuario.debito -= alquiler.coste_final
        usuario.save()

        # Marca el alquiler como entregado
        alquiler.fecha_entrega = timezone.now()
        alquiler.save()

        return Response({'success': 'Alquiler liberado correctamente'})

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def alquileres_admin(self, request):
        alquileres = Alquiler.objects.all()
        serializer = AlquilerSerializer(alquileres, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def alquileres_usuario(self, request):
        usuario = request.user
        alquileres = Alquiler.objects.filter(usuario=usuario)
        serializer = AlquilerSerializer(alquileres, many=True)
        return Response(serializer.data)


class PatineteViewSet(viewsets.ModelViewSet):
    queryset = Patinete.objects.all()
    serializer_class = PatineteSerializer

    @action(detail=False, methods=['get'])
    def patinetes_libres(self, request):
        filtro_patinetes_libre = Q(alquiler__isnull=True) | Q(alquiler__fecha_desbloqueo__isnull=False)
        patinetes_libres = Patinete.objects.filter(filtro_patinetes_libre)
        serializer = PatineteSerializer(patinetes_libres, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def patinetes_ocupados(self, request):
        filtro_patinetes_libre = Q(alquiler__isnull=True) | Q(alquiler__fecha_desbloqueo__isnull=False)
        patinetes_ocupados = Patinete.objects.exclude(filtro_patinetes_libre)
        serializer = PatineteSerializer(patinetes_ocupados, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_ten_patinetes_alquilados(self, request):
        patinetes_top_ten = Patinete.objects.annotate(num_alquileres=Count('alquiler')).order_by('-num_alquileres')[:10]
        serializer = PatineteSerializer(patinetes_top_ten, many=True)
        return Response(serializer.data)
