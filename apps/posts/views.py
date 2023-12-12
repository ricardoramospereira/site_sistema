from config.utils import add_form_errors_to_messages
from posts import models
from django.shortcuts import get_object_or_404, render, redirect

from posts.forms import PostagemForumForm
from django.contrib import messages

# Create your views here.
def post_list(request):
    posts = models.PostagemForum.objects.filter(ativo=True)
    context = {
        'posts': posts
    }
    return render(request, 'posts/list-post-forum.html', context=context)



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
    return render(request, 'posts/detail-post.html', {'post': post})