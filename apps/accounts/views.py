from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from accounts.forms import CustomUserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from accounts.models import MyUser
from accounts.permission import grupo_colaborador_required
from user_profile.models import UserProfile # teste
from user_profile.forms import ProfileForm

# Create your views here.
def timeout_view(request):
    return render(request, 'accounts/timeout.html')

# Login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'accounts/login.html')

# Registro
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, user=request.user)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)

            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('login')
        else:
            # Tratar quando usuario já existe, senhas... etc...
            messages.error(request, 'A senha deve ter pelo menos 1 caractere maiúsculo, \
    1 caractere especial e no minimo 8 caracteres.')
    form = CustomUserCreationForm(user=request.user)
    return render(request, "accounts/register.html",{"form": form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required()
def update_my_user(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
        return redirect('home')
    else:
        form = UserChangeForm(instance=request.user, user=request.user)
    return render(request, 'accounts/user_update.html', {'form': form})

@login_required()
@grupo_colaborador_required(['administrador','colaborador'])
def update_user(request, username):
    user = get_object_or_404(MyUser, username=username)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=user, user=request.user)
    return render(request, 'accounts/user_update.html', {'form': form})

@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def user_list(request): # Lista Cliente
    lista_usuarios = MyUser.objects.select_related('perfil').filter(is_superuser=False)
    return render(request, 'accounts/user_list.html', {'lista_usuarios': lista_usuarios})

'''@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def add_user(request):
    user_form = CustomUserCreationForm(user=request.user)
    perfil_form = ProfileForm(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, user=request.user)
        perfil_form = ProfileForm(request.POST, request.FILES, user=request.user)

        if user_form.is_valid() and perfil_form.is_valid():
            # Salve o usuário
            usuario = user_form.save()

            # Crie um novo perfil para o usuário
            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
            messages.success(request, 'Usuário adicionado com sucesso.')
            return redirect('lista_usuarios')
        
    context = {'user_form': user_form, 'perfil_form': perfil_form}
    return render(request, "accounts/add-user.html", context)'''

@login_required
@grupo_colaborador_required(['administrador','colaborador'])
def add_user(request):
    user_form = CustomUserCreationForm(user=request.user)
    perfil_form = ProfileForm(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, user=request.user)
        perfil_form = ProfileForm(request.POST, request.FILES, user=request.user)

        if user_form.is_valid() and perfil_form.is_valid():
            # Salve o usuário
            usuario = user_form.save()

            # Atualize ou crie um novo perfil para o usuário
            perfil, created = UserProfile.objects.get_or_create(usuario=usuario)
            perfil_form = ProfileForm(request.POST, request.FILES, instance=perfil, user=request.user)
            if perfil_form.is_valid():
                perfil_form.save()
            
            messages.success(request, 'Usuário adicionado com sucesso.')
            return redirect('user_list')
        
    context = {'user_form': user_form, 'perfil_form': perfil_form}
    return render(request, "accounts/add-user.html", context)

           
