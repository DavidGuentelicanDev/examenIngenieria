from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Hotel, ServicioAdicional, TipoHabitacion, Habitacion, Promocion, ServicioPorHotel
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PromocionForm, GerenciaPromocionForm


#INDEX Y LOGIN
#pagina index
def index(request):
    return render(request, 'paginaweb/index.html')

#login
def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('clave')
        #autentificar usando username y password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Ingreso exitoso.', 'rol': user.rol})
        else:
            return JsonResponse({'success': False, 'message': 'Credenciales incorrectas.'})
    return render(request, 'paginaweb/login.html')

#redireccionar al login si usuario no esta logueado
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login_admin'))
        return view_func(request, *args, **kwargs)
    return wrapper

#logout
@login_required
def cierre_sesion(request):
    logout(request)
    return redirect('index')


#PAGINA WEB
#hoteles
def hoteles(request):
    hoteles = Hotel.objects.all()
    return render(request, 'paginaweb/hoteles.html', {'hoteles': hoteles})

#ficha hoteles
def ficha_hoteles(request, id_hotel):
    hotel = get_object_or_404(Hotel, id_hotel=id_hotel)
    habitaciones = Habitacion.objects.filter(hotel=hotel)
    servicios = ServicioPorHotel.objects.filter(hotel=hotel)
    return render(request, 'paginaweb/ficha_hotel.html', {'hotel': hotel, 'habitaciones': habitaciones, 'servicios': servicios})

#tipo habitaciones
def tipo_habitaciones(request):
    tipo_habitaciones = TipoHabitacion.objects.all()
    return render(request, 'paginaweb/tipo_habitaciones.html', {'tipo_habitaciones': tipo_habitaciones})

#pagina de servicios adicionales
def servicios_adicionales(request):
    servicios_adicionales = ServicioAdicional.objects.all()
    return render(request, 'paginaweb/servicios_adicionales.html', {'servicios_adicionales': servicios_adicionales})

#promociones aprobadas
def promociones(request):
    promociones = Promocion.objects.filter(estado_promocion='A')
    return render(request, 'paginaweb/promociones.html', {'promociones': promociones})


#ADMINISTRACION GENERAL
#portal admin
@login_required
def portal_admin(request):
    promociones = Promocion.objects.all()
    if request.user.rol == 'G':
        promociones = promociones.filter(estado_promocion='P')
    return render(request, 'paginaweb/portal_admin.html', {'promociones': promociones})

#promocion preliminar para revision
@login_required
def preliminar(request, codigo_promocion):
    promocion = get_object_or_404(Promocion, codigo_promocion=codigo_promocion)
    form = GerenciaPromocionForm(instance=promocion)
    return render(request, 'paginaweb/promocion_preliminar.html', {'promocion': promocion, 'form': form})


#MARKETING
#crear promocion
@login_required
def crear_promocion(request):
    if request.method == 'POST':
        form = PromocionForm(request.POST, request.FILES)
        if form.is_valid():
            promocion = form.save(commit=False)
            promocion.publicada_por = request.user
            if 'imagen_promocion' in request.FILES:
                imagen_promocion = request.FILES['imagen_promocion']
                direccion_guardado = FileSystemStorage(location = 'paginaweb/static/assets')
                nombre_archivo = direccion_guardado.save(imagen_promocion.name, imagen_promocion)
                imagen_promocion_URL = 'assets/' + nombre_archivo
                promocion.imagen_promocion = imagen_promocion_URL
            promocion.save()
            return JsonResponse({'success': True, 'message': 'Promoción creada exitosamente.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Error en la validación del formulario.', 'errors': errors})
    else:
        form = PromocionForm()
    return render(request, 'paginaweb/crear_promocion.html', {'form': form})

#editar promocion
@login_required
def editar_promocion(request, codigo_promocion):
    promocion = get_object_or_404(Promocion, codigo_promocion=codigo_promocion)
    if request.method == 'POST':
        form = PromocionForm(request.POST, request.FILES, instance=promocion)
        if form.is_valid():
            promocion = form.save(commit=False)
            promocion.publicada_por = request.user
            if 'imagen_promocion' in request.FILES:
                imagen_promocion = request.FILES['imagen_promocion']
                direccion_guardado = FileSystemStorage(location='paginaweb/static/assets')
                nombre_archivo = direccion_guardado.save(imagen_promocion.name, imagen_promocion)
                imagen_promocion_URL = 'assets/' + nombre_archivo
                promocion.imagen_promocion = imagen_promocion_URL
            promocion.save()
            return JsonResponse({'success': True, 'message': 'Promoción actualizada exitosamente.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Error en la validación del formulario.', 'errors': errors})
    else:
        form = PromocionForm(instance=promocion)
    return render(request, 'paginaweb/editar_promocion.html', {'form': form, 'promocion': promocion})

#eliminar promocion
@login_required
def eliminar_promocion(request, codigo_promocion):
    try:
        promocion = Promocion.objects.get(codigo_promocion=codigo_promocion)
        promocion.delete()
        return JsonResponse({'success': True})
    except Promocion.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Promocion no encontrada.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


#GERENCIA
#aprobar o rechazar promocion
@login_required
def aprobar_rechazar(request, codigo_promocion):
    promocion = get_object_or_404(Promocion, codigo_promocion=codigo_promocion)
    if request.method == 'POST':
        form = GerenciaPromocionForm(request.POST, instance=promocion)
        if form.is_valid():
            #guardar el comentario y la revision por el usuario de gerencia
            promocion.comentario = form.cleaned_data['comentario']
            promocion.revisada_por = request.user
            #validacion si aprueba o rechaza
            if 'aprobar' in request.POST:
                promocion.estado_promocion = 'A'
            elif 'rechazar' in request.POST:
                promocion.estado_promocion = 'R'
            promocion.save()
            return JsonResponse({'success': True, 'message': 'Estado de promoción actualizado correctamente.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Error en la validación del formulario.', 'errors': errors})
