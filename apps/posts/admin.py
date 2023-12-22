from django.contrib import admin
from posts import models

# Register your models here.
class PostagemForumImagemInline(admin.TabularInline):
    model = models.PostagemForumImagem
    extra = 0

class PostagemForumAdmin(admin.ModelAdmin):
    inlines = [
    PostagemForumImagemInline,
    ]
    readonly_fields = ('slug',)
# Register your models here.
admin.site.register(models.PostagemForum, PostagemForumAdmin)
admin.site.register(models.PostagemForumComentario)

# admin.site.register(models.PostagemForumImagem)








admin.site.register(models.PostagemForumImagem)
