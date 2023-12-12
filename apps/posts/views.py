from django.shortcuts import render
from posts import models

# Create your views here.
def post_list(request):
    posts = models.PostagemForum.objects.filter(ativo=True)
    context = {
        'posts': posts
    }
    return render(request, 'posts/list-post-forum.html', context=context)