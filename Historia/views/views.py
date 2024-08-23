from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige al usuario a la página de inicio (home)
        else:
            # Maneja el error de inicio de sesión
            context = {'error': 'Nombre de usuario o contraseña incorrectos.'}
            return render(request, 'login.html', context)
    return render(request, 'login.html')

def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
        return redirect('login')  # Redirigir al usuario a la página de inicio de sesión
    else:
        return redirect('login') 

def home(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')