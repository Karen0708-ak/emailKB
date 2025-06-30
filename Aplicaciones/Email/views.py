from django.shortcuts import render, redirect, get_object_or_404
from .models import Email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import os
import mimetypes

# Mostrar listado de mensajes
def inicio(request):
    mensajes = Email.objects.all()
    return render(request, "listarMensajes.html", {'mensajes': mensajes})

# Mostrar formulario de nuevo mensaje
def nuevoMensaje(request):
    return render(request, "nuevoMensaje.html")

# Guardar nuevo mensaje
def guardarMensaje(request):
    destinatario = request.POST["destinatario"]
    asunto = request.POST["asunto"]
    mensaje_txt = request.POST["mensaje"]
    archivo = request.FILES.get("archivo")
    
    Email.objects.create(
        destinatario=destinatario,
        asunto=asunto,
        mensaje=mensaje_txt,
        archivo=archivo
    )
    
    messages.success(request, "Mensaje GUARDADO exitosamente")
    return redirect('listarMensajes')

# Eliminar mensaje
def eliminarMensaje(request, id):
    mensaje = Email.objects.get(id=id)
    # Eliminar archivo adjunto si existe
    if mensaje.archivo and os.path.isfile(mensaje.archivo.path):
        os.remove(mensaje.archivo.path)
    mensaje.delete()
    messages.success(request, "Mensaje ELIMINADO exitosamente")
    return redirect('listarMensajes')

# Mostrar formulario de edición
def editarMensaje(request, id):
    mensajeEditar = Email.objects.get(id=id)
    return render(request, "editarMensaje.html", {'mensajeEditar': mensajeEditar})

# Procesar edición de mensaje
def procesarEdicionMensaje(request):
    id = request.POST["id"]
    destinatario = request.POST["destinatario"]
    asunto = request.POST["asunto"]
    mensaje_txt = request.POST["mensaje"]
    archivo = request.FILES.get("archivo")
    
    mensaje = Email.objects.get(id=id)
    mensaje.destinatario = destinatario
    mensaje.asunto = asunto
    mensaje.mensaje = mensaje_txt
    
    if archivo:
        if mensaje.archivo and os.path.isfile(mensaje.archivo.path):
            os.remove(mensaje.archivo.path)
        mensaje.archivo = archivo
    
    mensaje.save()
    messages.success(request, "Mensaje ACTUALIZADO exitosamente")
    return redirect('listarMensajes')

# Enviar mensaje por correo
def enviarMensaje(request, id):
    mensaje = get_object_or_404(Email, id=id)
    
    email = EmailMessage(
        subject=mensaje.asunto,
        body=mensaje.mensaje,
        from_email=settings.EMAIL_HOST_USER,
        to=[mensaje.destinatario],
    )
    
    if mensaje.archivo:
        file_type, _ = mimetypes.guess_type(mensaje.archivo.name)
        with open(mensaje.archivo.path, 'rb') as f:
            email.attach(mensaje.archivo.name, f.read(), file_type)
    
    email.send(fail_silently=False)
    messages.success(request, "Mensaje ENVIADO exitosamente")
    return redirect('listarMensajes')