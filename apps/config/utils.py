from django.contrib import messages

from django.db.models import Q

def add_form_errors_to_messages(request, form):
    for field, error_list in form.errors.items():
        for error in error_list:
            messages.error(request, f"Erro no campo '{form[field].label}': {error}")

# Busca apenas um valor
'''def filter_model(model, **filters):
    queryset = model.objects.all()
    for field, value in filters.items():
        lookup = f"{field}__icontains"
        queryset = queryset.filter(**{lookup: value})
    return queryset'''

# Busca por mais de um valor
def filter_model(queryset, **filters):


    q_objects = Q() # inicializa um objeto Q vazio

    for field, value in filters.items():
        q_objects |= Q(**{field + '__icontains': value})

    queryset = queryset.filter(q_objects)
    return queryset