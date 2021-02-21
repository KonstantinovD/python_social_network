from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from posting.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'created_date', 'mod_date')
    list_filter = ('created_date', 'mod_date')
    search_fields = ('title',)
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     # Вы можете убедиться, что теперь в списке статей отображаются те поля, которые мы указали в атрибуте list_display.
#     list_display = ('title', 'slug', 'author', 'publish', 'status')
#     # Справа на странице появился блок фильтрации списка, который фильтрует статьи по полям, перечисленным в list_filter
#     list_filter = ('status', 'created', 'publish', 'author')
#     # Также появилась строка поиска. Она добавляется для моделей, для которых определен атрибут search_fields.
#     search_fields = ('tittle', 'body')
#     # Мы настроили Django так, что slug генерируется автоматически из поля title с помощью атрибута prepopulated_fields.
#     prepopulated_fields = {'slug': ('title',)}
#     raw_id_fields = ('author',)
#     # Под поиском благодаря атрибуту date_hierarchy добавлены ссылки для навигации по датам.
#     date_hierarchy = 'publish'
#     # По умолчанию статьи отсортированы по полям status и publish. Эта настройка задается в атрибуте ordering.
#     ordering = ('status', 'publish')