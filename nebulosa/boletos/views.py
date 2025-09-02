from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Boleto

def home(request):
    return render(request, "boletos/venta_publica.html")

def lista_boletos(request):
    boletos = Boleto.objects.all().order_by('-creado_en')
    return render(request, "boletos/venta_publica.html", {"boletos": boletos})

def detalle_boleto(request, pk):
    boleto = get_object_or_404(Boleto, pk=pk)
    return render(request, "boletos/detalle_boleto.html", {"boleto": boleto})

def marcar_usado(request, pk):
    boleto = get_object_or_404(Boleto, pk=pk)
    if boleto.marcar_usado():
        return HttpResponseRedirect(reverse("detalle_boleto", args=[pk]))
    return HttpResponse("El boleto ya fue usado.", status=400)

@login_required
def lista_boletos_venta(request):
    user = request.user
    if user.groups.filter(name="Vendedores").exists():
        from .models import Boleto
        boletos = Boleto.objects.filter(vendedor=user)
        return render(request, "boletos/lista_boletos_venta.html", {"boletos": boletos})
    return redirect('home')
