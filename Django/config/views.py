from django.shortcuts import render

from Comment.models import Comment
from Product.models import Product , Color , Size
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


def index(request):

    products = Product.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()

    context = {
        'products' : products,
        'colors': colors,
        'sizes': sizes,
    }

    return render(request , 'payments.html' , context)


def comment(request):

    products = Product.objects.all()
    users = get_user_model().objects.all()
    content_types = ContentType.objects.all()

    # ContentType.objects.get_for_model(Product)
    # Comment.objects.create(content_object=product , title='ffffffff' , text='aaaaaaaaaa' , user=request.user)


    context = {
        'products' : products,
        'users': users,
        'content_types' : content_types
    }

    return render(request , 'comments.html' , context)