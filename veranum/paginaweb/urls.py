from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #INDEX Y LOGIN
    path('', views.index, name='index'),
    path('login_admin/', views.login_admin, name='login_admin'), #pagina de logueo
    path('cierre_sesion/', views.cierre_sesion, name='sesion_cierre'), #url de logout
    #PAGINA WEB
    path('hoteles/', views.hoteles, name='lista_hoteles'), #url hoteles
    path('ficha_hoteles/<int:id_hotel>/', views.ficha_hoteles, name='hotel_ficha'), #url de ficha hoteles con id de hotel para buscar
    path('tipo_habitaciones/', views.tipo_habitaciones, name='habitaciones_tipo'), #url de tipo de habitaciones
    path('servicios_adicionales/', views.servicios_adicionales, name='adicionales_servicios'), #url de servicios adicionales
    path('promociones/', views.promociones, name='lista_promociones'), #url promociones aprobadas
    #ADMIN
    #general
    path('portal_admin/', views.portal_admin, name='admin_portal'), #portal de administracion, diferenciado si es MKT o Gerencia
    path('portal_admin/promocion_preliminar/<str:codigo_promocion>/', views.preliminar, name='preliminar_promocion'), #url de promocion preliminar
    #marketing
    path('portal_admin/crear_promocion/', views.crear_promocion, name='promocion_crear'), #url para crear promocion
    path('portal_admin/editar_promocion/<str:codigo_promocion>/', views.editar_promocion, name='promocion_editar'), #url editar promocion
    path('portal_admin/eliminar_promocion/<str:codigo_promocion>/', views.eliminar_promocion, name='promocion_eliminar'), #url de eliminar promocion
    #gerencia
    path('portal_admin/promocion_preliminar/<str:codigo_promocion>/aprobar_rechazar', views.aprobar_rechazar, name='apruebo_o_rechazo'), #url de gerencia para aprobar o rechazar
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
