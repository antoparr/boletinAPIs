from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.contrib import django_filters
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Marca, Vehiculo
from .serializers import GroupSerializer, UserSerializer, MarcaSerializer, VehiculoSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['GET'])
    def listadoVehiculos(self, request, pk):
        marca = get_object_or_404(Marca, pk=pk)
        vehiculos = Vehiculo.objects.filter(marca=marca)
        serializer = VehiculoSerializer(vehiculos, many=True, context={'request': request})
        return Response(serializer.data)


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['marca']

    @extend_schema(
        parameters=[
            OpenApiParameter(name='marca', description="", required=False, type=str)
        ]
    )
    @action(detail=False, methods=['GET'], description="Filter on marca get parameter")
    def filtro_marca(self, request):
        vehiculos_marca = Vehiculo.objects.all()
        marca = self.request.query_params.get('marca')
        if marca:
            vehiculos_marca = vehiculos_marca.filter(marca__nombre=marca)

        serializer = self.get_serializer(vehiculos_marca, many=True)
        return Response(serializer.data)