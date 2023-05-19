from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from theblog.models import Post, Category, Comment
from theblog.forms import PostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
"""
ListView, bir modelin tüm öğelerini listeleyen bir genel görünüm sınıfıdır.
ListView, bir veritabanı sorgusunu otomatik olarak gerçekleştirir.
ListView, sıralama, sayfalama, filtreleme ve arama gibi işlevler için destek sağlar.

DetailView, bir model öğesinin ayrıntılarını görüntülemek için 
kullanılan bir genel görünüm sınıfıdır.
DetailView, belirli bir model öğesiyle çalışır ve o öğenin tüm özelliklerini, 
yani alanlarını görüntüleyebilir.

def home(request):
   return render(request, 'home.html', {})
"""
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user.id)
    else:
        post.likes.add(request.user.id)

    return HttpResponseRedirect(reverse('theblog:article-detail', args=[str(pk)]))


class HomeView(ListView):
    # tüm blog postları homepagede listelemek istiyoruz.o yüzden listview
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']
    """
    ordering = ['-id']  -> son eklenen postun en üstte görünmesini sağlar.
    Post modelinde id alanı tanımlamamıza rağmen django bir model oluşturduğumuzda
    default olarak id atar. bu sayede id ile işlem yapabiliyoruz.
    """
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        # stuff = get_object_or_404(Post, id=self.kwargs["pk"])
        # total_likes = stuff.total_likes()
        # context["total_likes"] = total_likes
        return context

"""
def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})
"""

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(
        request, 'categories.html',
        {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts}
    )


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    # def get_context_data(self, **kwargs):
    #     stuff = get_object_or_404(Post, id=self.kwargs["pk"])
    #     total_likes = stuff.total_likes()
    #
    #     liked = False
    #     if stuff.likes.filter(id=self.request.user.id):
    #         liked=True

class AddPostView(CreateView):
    model = Post
    form_class = PostForm #formu buraya da ekledik
    template_name = 'add_post.html'
    """
    yoruma aldık çünkü artık form kullanacak ve
    PostFormda fieldları belirttik zaten.
    fields = '__all__' -> models.pydaki Post classının tüm fieldlerini getirir.
    fields = ('title', 'body') -> sadece title ve body kısmını gösterir.
    """

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('theblog:home')


class AddCategoryView(CreateView):
    model = Category
    #form_class = PostForm #bir tane alan olduğu için bunu kullanmadık
    fields = '__all__'
    template_name = 'add_category.html'


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'
    #fields = ['title', 'title_tag', 'body']

    def get_form(self, form_class=None):
        """
        form_class parametresi, form sınıfını belirtir.
        Bu parametre, varsayılan olarak None olarak ayarlanır.
        """
        form = super().get_form(form_class)
        #form.fields.pop('author')
        # edit işlemi sırasında author alanını formdan çıkarır
        return form


class DeletePostView(DeleteView):
    """
    8000/article/1/remove sayfasında Delete Post! butonuna tıkladığımızda
    normalde bizi home page'e yönlendirmesi gerekir;
    (models.py'daki Post classındaki return reverse('home')'dan dolayı)
    Fakat DeletePostView'da bu işe yaramıyor.
    hata mesajında bizden success_url istiyor.
    delete işleminden sonra özellikle nereye gideceğini belirtmemiz gerekiyor.
    reverse bu aşamada işe yaramıyor bu yüzden
    reverse_lazy'yi import etmemiz gerekiyor.
    """
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('theblog:home')

