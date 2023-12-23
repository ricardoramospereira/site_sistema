from config.utils import add_form_errors_to_messages, filter_model #TODO:separar
from posts import models
from django.shortcuts import get_object_or_404, render, redirect
from posts.forms import PostagemForumComentarioForm, PostagemForumForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
import re

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def post_list(request):
    # Comece com todas as postagens ativas
    query = models.PostagemForum.objects.filter(ativo=True)

    # Filtragem por título, se um título for fornecido
    titulo = request.GET.get('titulo')
    if titulo:
        query = query.filter(titulo__icontains=titulo)

    # Paginação
    paginator = Paginator(query, 10)  # 10 postagens por página

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'posts/list-post-forum.html', context=context)

@login_required
def dash_list_post(request):
    form_dict = {}
    filtros = {}

    valor_busca = request.GET.get("titulo")
    if valor_busca:
        filtros["titulo__icontains"] = valor_busca  # Busca insensível a maiúsculas e minúsculas

    if request.path == '/posts/':
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'posts/list-post.html'
    else:
        user = request.user
        grupos = ['administrador', 'colaborador']
        template_view = 'posts/dash-list-post.html'

        if any(grupo.name in grupos for grupo in user.groups.all()) or user.is_superuser:
            postagens = models.PostagemForum.objects.filter(ativo=True)
        else:
            postagens = models.PostagemForum.objects.filter(usuario=user)

    postagens = postagens.filter(**filtros)

    for el in postagens:
        form_dict[el] = PostagemForumForm(instance=el)

    paginacao = Paginator(list(form_dict.items()), 10)  # Paginação

    pagina_numero = request.GET.get("page")
    try:
        page_obj = paginacao.get_page(pagina_numero)
    except PageNotAnInteger:
        page_obj = paginacao.page(1)
    except EmptyPage:
        page_obj = paginacao.page(paginacao.num_pages)

    context = {
        'page_obj': page_obj,
        'form_dict': dict(page_obj),  # Converte o objeto da página de volta para um dicionário
    }

    return render(request, template_view, context)


def create_post(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            postagem_imagens = request.FILES.getlist('postagem_imagens')
            if len(postagem_imagens) > 5:  # Count
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
            else:
                try:
                    forum = form.save(commit=False)
                    forum.usuario = request.user
                    form.save()

                    for f in postagem_imagens:
                        models.PostagemForumImagem.objects.create(postagem=forum, imagem=f)
                        
                    messages.success(request, 'Seu Post foi cadastrado com sucesso!')
                    return redirect('post_list')
                except Exception as e:
                    messages.error(request, f'Erro ao salvar postagem: {e}')
        
        else:
            add_form_errors_to_messages(request, form)
    
    return render(request, 'posts/form-post.html', {'form': form})

def detail_post(request, slug):
    post = get_object_or_404(models.PostagemForum, slug=slug)
    form = PostagemForumForm(instance=post)
    form_comentario = PostagemForumComentarioForm()
    context = {
        'form': form,
        'post': post, 
        'form_comentario': form_comentario
        }
    
    return render(request,'posts/detail-post.html', context)


@login_required
def edit_post(request, slug):
    post = get_object_or_404(models.PostagemForum, slug=slug)
    imagens = post.postagem_imagens.all()  # Modificado aqui

    # Verifica se o usuário autenticado é o autor da postagem ou tem permissões necessárias
    if not (post.usuario == request.user or request.user.is_superuser or
            any(grupo.name in ['administrador', 'colaborador'] for grupo in request.user.groups.all())):
        raise PermissionDenied

    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            try:
                post_atualizado = form.save(commit=False)

                contar_imagens = post_atualizado.postagem_imagens.count()
                postagem_imagens = request.FILES.getlist('postagem_imagens')

                if contar_imagens + len(postagem_imagens) > 5:
                    messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
                else:
                    post_atualizado.save()
                    for imagem in postagem_imagens:
                        models.PostagemForumImagem.objects.create(postagem=post_atualizado, imagem=imagem)

                    messages.success(request, f'Seu Post {post_atualizado.titulo} foi atualizado com sucesso!')
                    return redirect('post_list')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar postagem: {e}')
        else:
            add_form_errors_to_messages(request, form)
    else:
        form = PostagemForumForm(instance=post)

    return render(request, 'posts/form-post.html', {'form': form, 'imagens': imagens})


@login_required
def delete_post(request, slug):
    redirect_route = request.POST.get('redirect_route', '') # Adiciona
    postagem = get_object_or_404(models.PostagemForum, slug=slug)

    message = 'Seu Post '+ postagem.titulo +' foi deletado com sucesso!' # 
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, message)

        if re.search(r'/posts/detail-post/([^/]+)/', redirect_route): # se minha rota conter
            return redirect('post_list')
        return redirect(redirect_route)
    
    return render(request, 'posts/detail-post.html', {'postagem': postagem})

def remove_image(request):
    imagem_id = request.GET.get('imagem_id')

    try:
        postagem_imagem = models.PostagemForumImagem.objects.get(id=imagem_id)
        postagem_imagem.imagem.delete()
        postagem_imagem.delete()
        message = 'Imagem removida com sucesso.'
        status = 'success'
    except models.PostagemForumImagem.DoesNotExist:
        message = 'Imagem não encontrada.'
        status = 'error'

    return JsonResponse({'message': message, 'status': status})

def adicionar_comentario(request, slug):
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
    message = 'Comentário Adcionado com sucesso!'
    if request.method == 'POST':
        form = PostagemForumComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.postagem = postagem
            comentario.save()
            messages.warning(request, message)
            return redirect('detail-post', slug=postagem.slug)
    return JsonResponse({'status': message})

def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.PostagemForumComentario, id=comentario_id)
    message = 'Comentário Editado com sucesso!'
    if request.method == 'POST':
        form = PostagemForumComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.info(request, message)
            return redirect('detail-post', slug=comentario.postagem.slug)
    return JsonResponse({'status': message}) # TODO: PAGINA DE ERRO

def deletar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.PostagemForumComentario, id=comentario_id)
    comentario.delete()
    messages.success(request, "Comentário deletado com sucesso!")
    return redirect('detail-post', slug=comentario.postagem.slug)

def responder_comentario(request, comentario_id):
    comentario = get_object_or_404(models.PostagemForumComentario, id=comentario_id)
    if request.method == 'POST':
        form = PostagemForumComentarioForm(request.POST)
        message = 'Comentário Respondido com sucesso!'
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.usuario = request.user
            novo_comentario.parent_id = comentario_id
            novo_comentario.postagem = comentario.postagem
            novo_comentario.save()
            messages.info(request, message)
            return redirect('detail-post', slug=comentario.postagem.slug)
        
    return JsonResponse({'status': message})