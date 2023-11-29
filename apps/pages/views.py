from django.shortcuts import render
# test messager
from django.contrib import messages

# Create your views here.
def index(request):
    messages.success(request, 'Mensagem de sucesso')
    messages.debug(request, 'Mensagem de debug')
    messages.info(request, 'Mensagem de info')
    messages.warning(request, 'Mensagem de warning')
    messages.error(request, 'Mensagem de error')


    return render(request, 'index.html')