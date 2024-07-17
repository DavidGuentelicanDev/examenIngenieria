from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

#MODELO PAGINA WEB VERANUM

#tabla Hotel
class Hotel (models.Model):
    id_hotel            = models.AutoField(primary_key=True) #autoincremental
    nombre_hotel        = models.CharField(max_length=50)
    direccion           = models.CharField(max_length=100) #nombre de la calle
    info_adicional_dir  = models.CharField(max_length=100, blank=True, null=True) #cualquier cosa adicional de la direccion
    comuna              = models.CharField(max_length=30) #solo son 2 hoteles, por tanto se ingresaran manualmente
    telefono            = models.CharField(max_length=10)
    correo_hotel        = models.EmailField(max_length=100)
    cant_habitaciones   = models.IntegerField() #cantidad de habitaciones, a definir
    desc_hotel          = models.TextField(blank=True, null=True) #usaremos lorem ipsum
    imagen_hotel        = models.CharField(max_length=100, blank=True, null=True) #para guardar la ruta de la imagen

    def __str__(self):
        return self.nombre_hotel


#tabla Servicio Adicional
class ServicioAdicional(models.Model):
    id_serv_adicional       = models.AutoField(primary_key=True) #autoincremental
    nombre_serv_adicional   = models.CharField(max_length=50)
    desc_serv_adicional     = models.TextField(blank=True, null=True) #lorem ipsum
    precio_serv_adicional   = models.IntegerField() #a definir si sera por noche o valor fijo adicional
    imagen_serv_adicional   = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_serv_adicional


#tabla Servicio por Hotel
class ServicioPorHotel(models.Model):
    id_servicio_hotel   = models.AutoField(primary_key=True) #autoincremental
    hotel               = models.ForeignKey(Hotel, on_delete=models.CASCADE) #FK de Hotel
    serv_adicional      = models.ForeignKey(ServicioAdicional, on_delete=models.CASCADE) #FK de Servicio Adicional

    class Meta:
        unique_together = ('hotel', 'serv_adicional')

    def __str__(self):
        return f'{self.hotel} - {self.serv_adicional}'


#tabla Tipo Habitacion
class TipoHabitacion(models.Model):
    id_tipo_habitacion      = models.AutoField(primary_key=True) #autoincremental
    nombre_tipo_habitacion  = models.CharField(max_length=20) #single, doble, triple, suite, backpacking, grupo
    cant_camas              = models.IntegerField() #definido por el tipo de hab
    bano_privado            = models.BooleanField()
    precio_noche            = models.IntegerField()
    desc_tipo_habitacion    = models.TextField(blank=True, null=True)
    imagen_tipo_habitacion  = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_tipo_habitacion


#tabla Habitacion
class Habitacion(models.Model):
    id_habitacion       = models.AutoField(primary_key=True) #autoincremental
    hotel               = models.ForeignKey(Hotel, on_delete=models.CASCADE) #FK de Hotel
    numero_habitacion   = models.IntegerField() #a definir el id de cada habitacion
    tipo_habitacion     = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE) #FK de Tipo Habitacion
    estado_habitacion   = models.BooleanField() #disponible o no disponible

    class Meta:
        unique_together = ('hotel', 'numero_habitacion')

    def __str__(self):
        return f'{self.hotel} - {self.numero_habitacion}'


#tabla Usuario
class Usuario(AbstractUser):
    rut             = models.CharField(unique=True, max_length=10) #rut completo
    
    ROLES_USUARIO   = [('M', 'Marketing'), ('G', 'Gerencia')] #arreglo con los roles de usuario definidos
    
    rol             = models.CharField(max_length=1, choices=ROLES_USUARIO, blank=True, null=True) #no hay default

    def __str__(self):
        return f'{self.username} - {self.rol}'


#tabla Promocion
class Promocion(models.Model):
    codigo_promocion    = models.CharField(primary_key=True, max_length=20) #id definido por el jefe de MKT, abreviacion del nombre
    hotel               = models.ForeignKey(Hotel, on_delete=models.CASCADE) #FK de Hotel
    tipo_habitacion     = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE) #FK de Tipo Habitacion
    nombre_promocion    = models.CharField(max_length=100)
    desc_promocion      = models.TextField(blank=True, null=True) #lorem ipsum
    fecha_inicio        = models.DateField() #fecha definida por jefe de MKT
    fecha_fin           = models.DateField() #fecha definida por jefe de MKT
    porc_descuento      = models.IntegerField() #porcentaje que define el jefe de MKT, sin decimales
    imagen_promocion    = models.ImageField(upload_to='assets/', blank=True, null=True) #para guardar las imagenes, luego cambiara a imagefield
    publicada_por       = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='promociones_publicadas', blank=True, null=True) #usuario de MKT que publica
    
    ESTADOS_PROMOCION   = [('P', 'Pendiente'), ('A', 'Aprobada'), ('R', 'Rechazada'), ('F', 'Finalizada')] #arreglo con estados de promocion
    
    estado_promocion    = models.CharField(max_length=1, choices=ESTADOS_PROMOCION, default='P') #estados de promocion definidos por el arreglo, por defecto Pendiente
    comentario          = models.TextField(blank=True, null=True) #comentario del gerente, en caso de querer dejar algo indicado
    fecha_revision      = models.DateTimeField(blank=True, null=True) #fecha de revision de la promocion por el usuario gerente
    revisada_por        = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='promociones_revisadas', blank=True, null=True) #FK de Usuario, en blanco hasta que el gerente la apruebe o rechace
    
    #metodo para guardar datos automaticos en la tabla promocion
    def save(self, *args, **kwargs):
        update_fields = set()
        #si el estado de la promocion es Aprobada o Rechazada, se guarda la fecha de revision
        if self.estado_promocion in ['A', 'R'] and not self.fecha_revision:
            self.fecha_revision = timezone.now().date()
            update_fields.add('fecha_revision')
        #guarda los cambios
        super().save(*args, **kwargs)
        #verifica si se actualizo algun campo que requiera un segundo guardado
        if update_fields:
            super(Promocion, self).save(update_fields=update_fields)

    def __str__(self):
        return self.codigo_promocion
