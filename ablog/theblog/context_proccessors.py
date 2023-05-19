from theblog.models import Category


def navbar_context(request):
    return {'cat_menu': Category.objects.all(), }

# part-15'teki yorumdan sonra eklendi.