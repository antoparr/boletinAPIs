from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PatineteViewSet, AlquilerViewSet, PatinetesLibresViewSet, PatinetesOcupadosViewSet,
                    UserOrderByDebitoView, TopTenPatinetesAlquiladosView, TopUsuariosConMasAlquileresView)

router = DefaultRouter()
router.register(r'patinetes', PatineteViewSet)
router.register(r'alquileres', AlquilerViewSet)
router.register(r'patinetes-libres', PatinetesLibresViewSet, basename='patinetes_libres')
router.register(r'patinetes-ocupados', PatinetesOcupadosViewSet, basename='patinetes_ocupados')
router.register(r'usuarios-debito', UserOrderByDebitoView, basename='usuarios_debito')
router.register(r'topten-patinetes-alquilados', TopTenPatinetesAlquiladosView, basename='topten_alquilados')
router.register(r'top-usuarios-con-alquiler', TopUsuariosConMasAlquileresView, basename='top_usuarios')

urlpatterns = [
    path('', include(router.urls)),
]