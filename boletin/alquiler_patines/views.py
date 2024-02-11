from django.db import models
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly  # Correct import
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Alquiler, Patinete, Usuario
from .serializers import AlquilerSerializer, PatineteSerializer, UserSerializer
from django.utils import timezone
from rest_framework import viewsets
from .models import Alquiler, IsAdminOrReadOnly, permissions, IsOwnerOrReadOnly
from .serializers import AlquilerSerializer
from rest_framework import generics
from django.contrib.auth.models import User


class PatineteViewSet(viewsets.ModelViewSet):
    queryset = Patinete.objects.all()
    serializer_class = PatineteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def alquilar(self, request):
        # Lógica para iniciar un alquiler
        patinete_numero = request.data.get('patinete_numero', None)

        try:
            patinete = Patinete.objects.get(numero=patinete_numero)
            usuario = request.user

            # Realizar lógica para iniciar el alquiler, establecer fecha_desbloqueo, etc.
            alquiler = Alquiler.objects.create(usuario=usuario, patinete=patinete, fecha_desbloqueo=timezone.now())

            return Response({'message': 'Alquiler iniciado correctamente'}, status=status.HTTP_201_CREATED)
        except Patinete.DoesNotExist:
            return Response({'error': 'El patinete no existe'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['POST'])
    def liberar(self, request):
        patinete_numero = request.data.get('patinete_numero', None)

        try:
            patinete = Patinete.objects.get(numero=patinete_numero)
            usuario = request.user
            alquiler = Alquiler.objects.filter(patinete=patinete, usuario=usuario, fecha_entrega__isnull=True).latest('fecha_desbloqueo')

            # Para terminar el alquiler, establecer fecha_entrega, calcular coste_final, etc.
            alquiler.fecha_entrega = timezone.now()
            alquiler.coste_final = calcular_coste_final(alquiler)
            alquiler.save()

            # Aumentar el débito del usuario
            usuario.debito += alquiler.coste_final
            usuario.save()

            return Response({'message': 'Alquiler liberado correctamente'}, status=status.HTTP_200_OK)
        except Patinete.DoesNotExist:
            return Response({'error': 'El patinete no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Alquiler.DoesNotExist:
            return Response({'error': 'No hay un alquiler activo para este patinete y usuario'}, status=status.HTTP_400_BAD_REQUEST)


class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]  # Agregar el nuevo permiso


class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # Agregar el nuevo permiso


class PatinetesLibresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patinete.objects.filter(alquiler__isnull=True)
    serializer_class = PatineteSerializer


class PatinetesOcupadosViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patinete.objects.filter(alquiler__isnull=False)
    serializer_class = PatineteSerializer


class UserOrderByDebitoView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-debito')
    serializer_class = UserSerializer


class TopTenPatinetesAlquiladosView(generics.ListAPIView):
    queryset = Patinete.objects.annotate(num_alquileres=models.Count('alquileres')).order_by('-num_alquileres')[:10]
    serializer_class = PatineteSerializer


class TopUsuariosConMasAlquileresView(generics.ListAPIView):
    queryset = User.objects.annotate(num_alquileres=models.Count('alquileres')).order_by('-num_alquileres')[:3]
    serializer_class = UserSerializer