from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        clave = request.POST.get('clave')
        if clave == '32231':
            request.session['autenticado'] = True
            return redirect('dashboard')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Clave incorrecta'})
    return render(request, 'usuarios/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')
