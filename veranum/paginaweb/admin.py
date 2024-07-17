from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Hotel, ServicioAdicional, ServicioPorHotel, TipoHabitacion, Habitacion, Usuario, Promocion

class UsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'rut', 'rol')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'rut', 'rol'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Hotel)
admin.site.register(ServicioAdicional)
admin.site.register(ServicioPorHotel)
admin.site.register(TipoHabitacion)
admin.site.register(Habitacion)
admin.site.register(Promocion)
