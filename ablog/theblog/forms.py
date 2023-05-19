from django import forms
from theblog.models import Post, Category, Comment

# choices = [('coding', 'coding'), ('sports', 'sports'), ('entertainment', 'entertainment'),]
choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):
    """
    Post modeli fieldlarını forma dönüştürmek için.
    ModelForm sınıfı, bir modelin bir veya daha fazla alanını kullanarak otomatik
    olarak bir form oluşturmak için kullanılır.
    Bu, aynı veri modelini hem veritabanında hem de web formunda kullanarak
    tutmanıza olanak tanır.
    """

    class Meta:
        """
        Meta sınıfı, formun hangi model sınıfını kullanacağını ve
        hangi alanların formda görüneceğini belirler.
        """

        model = Post
        fields = ('title', 'title_tag', 'category', 'body', 'header_image') #authoru sildik.
        widgets = {
            """
            widgets -> styling stuff
            'class':'form-control' -> cssteki form classı atadık.
            'placeholder':'This is Title Placeholder Stuff' 
            -> yazmaya başlamadan önce görünen silik yazı.
            """
            
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'title_tag' : forms.TextInput(attrs={'class':'form-control'}),
            #'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),

            """
            'author' : forms.Select(attrs={'class':'form-control'}),
             yoruma aldık çünkü kullanıcının yeni bir post eklerken 
             başka bir kullanıcıyı seçmesini istemiyoruz.
            """
            
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'body' : forms.Textarea(attrs={'class':'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
        }