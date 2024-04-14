from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('' , CategoryViewsSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('null/parent/' , CategoryNullParentView.as_view()),
    path('parent_list/<self_id>/' , ParentListView.as_view()),
    path('parent/<int:pk>/' , ParentView.as_view() , name='parent-detail')
]
