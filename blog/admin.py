from django.contrib import admin
from .models import Post, Comment

# Register your models here.
def make_published(modeladmin, request, queryset):
    queryset.update(status='published')
make_published.short_description = "Make selected Posts as published"

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('author', 'publish', 'status', 'created')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish' 
    ordering = ('status', 'publish')
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_published]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        self.exclude = []

        if not is_superuser:
            self.exclude.append('author')

        return form

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

admin.site.register(Post, PostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            for post in Post.published.filter(author=request.user):
                return qs.filter(post_id=post)