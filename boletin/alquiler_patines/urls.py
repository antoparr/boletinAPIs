from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatineteViewSet, AlquilerViewSet, PatinetesLibresViewSet

router = DefaultRouter()
router.register(r'patinetes', PatineteViewSet)
router.register(r'alquileres', AlquilerViewSet)
router.register(r'patinetes-libres', PatinetesLibresViewSet, basename='patinetes_libres')


urlpatterns = [
    path('', include(router.urls)),
]