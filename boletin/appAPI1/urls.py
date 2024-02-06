from django.urls import path, include
from rest_framework import routers
from .views import MarcaViewSet, VehiculoViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register(r'marcas', MarcaViewSet)
router.register(r'vehiculos', VehiculoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/vehiculos/por_fecha_fabricacion/', VehiculoViewSet.as_view({'get': 'vehiculos_por_fecha_fabricacion'}), name='vehiculos_por_fecha_fabricacion'),
    path('api/vehiculos/por_fecha_matriculacion/', VehiculoViewSet.as_view({'get': 'vehiculos_por_fecha_matriculacion'}), name='vehiculos_por_fecha_matriculacion'),
    path('api/vehiculos/filtrados/', VehiculoViewSet.as_view({'get': 'vehiculos_filtrados'}), name='vehiculos_filtrados'),
]