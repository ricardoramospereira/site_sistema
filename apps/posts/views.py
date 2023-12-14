from config.utils import add_form_errors_to_messages
from posts import models
from django.shortcuts import get_object_or_404, render, redirect

from posts.forms import PostagemForumForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
import re

# Create your views here.
def post_list(request):
    posts = models.PostagemForum.objects.filter(ativo=True)
    context = {
        'posts': posts
    }
    return render(request, 'posts/list-post-forum.html', context=context)

def dash_list_post(request):
    form_dict = {}
    # Valida Rotas (Forum ou Dashboard)
    if request.path == '/posts/': # Pagina forum da home, mostrar tudo ativo.
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'posts/list-post.html' # lista de post da rota /forum/
    else: # Mostra no Dashboard
        user = request.user
        grupos = ['administrador', 'colaborador']
        template_view = 'posts/dash-list-post.html' 

        if any(grupo.name in grupos for grupo in user.groups.all()) or user.is_superuser:
            # Usuário é administrador ou colaborador, pode ver todas as postagens
            postagens = models.PostagemForum.objects.filter(ativo=True)
        else:
            # Usuário é do grupo usuário, pode ver apenas suas próprias postagens
            postagens = models.PostagemForum.objects.filter(usuario=user)

    # Como existe uma lista de objetos, para aparecer o formulário
    # correspondente no modal precisamos ter um for
    for el in postagens:
        form = PostagemForumForm(instance=el)
        form_dict[el] = form
    context = {'postagens': postagens,'form_dict': form_dict}

    return render(request, template_view, context)
        


def create_post(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.usuario = request.user
            form.save()
            # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
            messages.success(request, 'Seu Post foi cadastrado com sucesso!')
            return redirect('post_list')
        else:
            add_form_errors_to_messages(request, form)
    
    return render(request, 'posts/form-post.html', {'form': form})

def detail_post(request, id):
    post = get_object_or_404(models.PostagemForum, id=id)
    form = PostagemForumForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request,'posts/detail-post.html', context)


@login_required
def edit_post(request, id):
    redirect_route = request.POST.get('redirect_route', '')

    post = get_object_or_404(models.PostagemForum, id=id)
    message = 'Seu Post '+ post.titulo +' \
                foi atualizado com sucesso!'

    # Verifica se o usuário autenticado é o autor da postagem
    grupos = ['administrador', 'colaborador']
    if request.user != post.usuario and not (
            any(grupo.name in grupos for grupo in request.user.groups.all())
            or request.user.is_superuser):
            messages.warning(request, 'Seu usuário não tem permissões para acessar essa página')
            return redirect('post_list') # Redireciona para uma página de erro ou outra página adequada
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.warning(request, message)
            return redirect(redirect_route)
        else:
            add_form_errors_to_messages(request, form)
    '''else:
        form = PostagemForumForm(instance=postagem)
    return render(request, 'posts/form-post.html', {'form': form})'''
    return JsonResponse({'status': 'Ok'}) # Coloca por enquanto.

@login_required
def delete_post(request, id):
    redirect_route = request.POST.get('redirect_route', '') # Adiciona
    postagem = get_object_or_404(models.PostagemForum, id=id)

    message = 'Seu Post '+ postagem.titulo +' foi deletado com sucesso!' # 
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, message)

        if re.search(r'/posts/detail-post/([^/]+)/', redirect_route): # se minha rota conter
            return redirect('post_list')
        return redirect(redirect_route)
    
    return render(request, 'posts/detail-post.html', {'postagem': postagem})