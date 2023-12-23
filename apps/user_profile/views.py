from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import MyUser
from django.contrib.auth.decorators import login_required
from accounts.forms import UserChangeForm
from user_profile.forms import ProfileForm
from user_profile.models import UserProfile
#from django.contrib.messages import constants
from django.contrib import messages

from django.core.paginator import Paginator

from posts.forms import PostagemForumForm

from config.utils import filter_model

# Só é permitido ver o perfil para quem está logado
@login_required()
def perfil_view(request, username):
    filtro = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum') # resgata todos os objetos relacionados com myuser em lote
    perfil = get_object_or_404(filtro, username=username)

    ################ FILTRO #############
    perfil_postagens = perfil.user_postagem_forum.all() # Todas as postagens relacionadas com perfil
    filtros = {}

    valor_busca = request.GET.get("titulo") # pego parametro
    if valor_busca:
        filtros["titulo"] = valor_busca # add no dicionario
        filtros["descricao"] = valor_busca # add no dicionario

        perfil_postagens = filter_model(perfil_postagens, **filtros) # faz o filtro

    form_dict = {}
    for el in perfil.user_postagem_forum.all():
        form = PostagemForumForm(instance=el)
        form_dict[el] = form
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3)
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    context = {'obj': perfil, 'page_obj': page_obj, 'form_dict':form_dict}
    return render(request, 'user_profile/profile.html', context)

########### Editar perfil (contas e perfil) ##################
@login_required
def editar_perfil(request, username):
    redirect_route = request.POST.get('redirect_route', '')

    modelo_myuser = MyUser.objects.get(username=username)
    modelo_perfil = UserProfile.objects.get(usuario__username=username)

    message = 'Seu Perfil foi atualizado com sucesso!'

    # Validações
    if request.user.username != modelo_myuser.username and not (
        ['administrador', 'colaborador'] in request.user.groups.all() or request.user.is_superuser):
        messages.error(request, 'Você não tem permissão para alterar esse perfil')
        return redirect('post_list') # Adicionar uma rota "sem permissão"
        
    
    if request.method == 'POST':
        form_contas = UserChangeForm(request.POST, user=request.user, instance=modelo_myuser)
        form_perfil = ProfileForm(request.POST, request.FILES, instance=modelo_perfil, user=request.user)  # Usando ProfileForm

        if form_perfil.is_valid() and form_contas.is_valid():
            form_contas.save()
            form_perfil.save()
            messages.success(request, 'Seu Perfil foi atualizado com sucesso!')
            return redirect(redirect_route)
    else:
        form_contas = UserChangeForm(user=request.user, instance=modelo_myuser)
        form_perfil = ProfileForm(instance=modelo_perfil, user=request.user)  # E aqui

        context = {'form_perfil': form_perfil, 'form_contas': form_contas, 'obj': modelo_myuser}
        return render(request, 'user_profile/editar-perfil-form.html', context)