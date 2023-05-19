from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
"""
admin kısmında groups ve users gibi post kısmı da görmemizi sağlar.
postun altında tanımladığımız title, author ve body kısımları yer alıyor.
"""


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('theblog:home')


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    pinterest_url = models.CharField(max_length=255, null=True, blank=True)
    mail_to = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('theblog:home')

class Post(models.Model):
    """
    default="My Blog!" özelliğini sonradan iptal ettik
    models.CASCADE kullanıcıların oluşturduğu blogları silmeye yarar.
    bir kullanıcı hesabı silindiğinde,
    bu kullanıcıya ait tüm Author (yazar) nesneleri de silinecektir.
    "author" alanı, "User" modeline bir ForeignKey alanıdır.
    Yani, bir "Post" modeli oluşturulurken,
    "author" alanına yalnızca "User" modelinde tanımlanmış bir kullanıcı atanabilir.
    """
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #body = models.TextField()
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255, default='coding')
    likes = models.ManyToManyField(User, related_name="blog_posts", blank=True)


    # Bu yöntem, "Post" nesnesinin başlığını ve yazarını içeren bir dize döndürür.
    def __str__(self):
        """
        self.author bir obje olduğu için onu strye çevirdik.
        title ve post isimleriyle görmemizi sağlar.
        """
        return f"{self.title} | {self.author}"


    def get_absolute_url(self):
        """
        addpost sayfasında postu kaydederken hata aldık
        ve o hatada get_absolute_urlin eksik olduğunu söylediği için
        bu fonksiyonu ekledik.
        get_absolute_url, Django'da modellerin özel bir yöntemidir.
        return reverse('article-detail', args=(str(self.id)))
        """
        return reverse('theblog:home')


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)