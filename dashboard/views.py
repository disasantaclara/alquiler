from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Local, Pago, Arrendatario
from datetime import date, timedelta

def dashboard(request):
    if not request.session.get('autenticado'):
        return redirect('login')
    locales = Local.objects.select_related('arrendatario').order_by('-id')
    pagos = Pago.objects.order_by('-fecha_pago')

    # Diccionario: local_id -> último pago
    ultimo_pago = {}
    for pago in pagos:
        if pago.local_id not in ultimo_pago:
            ultimo_pago[pago.local_id] = pago

    # Asigna el último pago a cada local
    for local in locales:
        local.ultimo_pago = ultimo_pago.get(local.id)

    return render(request, 'dashboard/dashboard.html', {
        'locales': locales,
        'today': date.today(),
    })

@csrf_exempt
def abonar(request):
    if request.method == 'POST':
        local_id = request.POST.get('local_id')
        monto = request.POST.get('monto')
        local = Local.objects.get(id=local_id)
        arrendatario = local.arrendatario
        hoy = date.today()
        proximo_pago = hoy + timedelta(days=30)
        Pago.objects.create(
            local=local,
            arrendatario=arrendatario,
            fecha_pago=hoy,
            monto=monto,
            es_abono=True,
            tipo_pago='efectivo',
            fecha_proximo_pago=proximo_pago
        )
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)

@csrf_exempt
def editar_local(request):
    if request.method == 'POST':
        local_id = request.POST.get('local_id')
        nombre_local = request.POST.get('nombre_local')
        nombre_arrendatario = request.POST.get('nombre_arrendatario')
        telefono_arrendatario = request.POST.get('telefono_arrendatario')

        local = Local.objects.get(id=local_id)
        local.nombre = nombre_local
        local.save()
        if local.arrendatario:
            arr = local.arrendatario
            arr.nombre = nombre_arrendatario
            arr.telefono = telefono_arrendatario
            arr.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)

@csrf_exempt
def crear_local(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        nombre = request.POST.get('nombre')
        inquilino = request.POST.get('inquilino')
        telefono = request.POST.get('telefono')
        precio = request.POST.get('precio')
        garantia = request.POST.get('garantia')
        rentado = request.POST.get('rentado') == '1'
        from datetime import date
        arr = Arrendatario.objects.create(nombre=inquilino, telefono=telefono, fecha_ingreso=date.today())
        local = Local.objects.create(
            nombre=nombre,
            arrendatario=arr,
            es_departamento=(tipo == 'departamento'),
            es_parqueadero=(tipo == 'parqueadero'),
            precio=precio,
            garantia=garantia,
            rentado=rentado
        )
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)

@csrf_exempt
def actualizar_precio_garantia(request):
    if request.method == 'POST':
        local_id = request.POST.get('local_id')
        precio_local = request.POST.get('precio_local')
        garantia_local = request.POST.get('garantia_local')

        local = Local.objects.get(id=local_id)
        local.precio = precio_local
        local.garantia = garantia_local
        local.save()

        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)

@csrf_exempt
def actualizar_rentado(request):
    if request.method == 'POST':
        local_id = request.POST.get('local_id')
        rentado = request.POST.get('rentado') == 'true'
        local = Local.objects.get(id=local_id)
        local.rentado = rentado
        local.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)
