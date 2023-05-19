from django.contrib import admin
from theblog.models import Post, Category, Profile, Comment

# blog postlarımızın admin kısmından erişilebilir olmasını sağlıyor.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)

