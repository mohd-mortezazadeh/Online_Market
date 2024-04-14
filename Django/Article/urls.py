from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('' , ArticleViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('authors/list/' , AuthorListView.as_view()),
    path('author/<int:pk>/' , AuthorView.as_view())
] 
