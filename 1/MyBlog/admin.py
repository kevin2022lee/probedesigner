from django.contrib import admin
from MyBlog.models import BlogPost,ReplyPost,PostType

# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('u','title', 'content','artcle_type','timestamp')
    
class ReplyPostAdmin(admin.ModelAdmin):
    list_display = ('rcontent','createtime')
    
class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('typename','addtime')
    
admin.site.register(ReplyPost,ReplyPostAdmin)
admin.site.register(BlogPost,BlogPostAdmin)
admin.site.register(PostType,PostTypeAdmin)