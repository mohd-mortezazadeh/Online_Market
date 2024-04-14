from django.urls import path, include
from .views import *

urlpatterns = [
    path('' , Index.as_view()),
    path('products/' , Products.as_view() , name='products'),
    path('blogs/' , Articles.as_view() , name='blogs'),
    path('contact_us' , Contact_us.as_view() , name='contact_us'),
    path('about_us', About_us.as_view(), name='about_us'),

    path('categories/<slug>/' , Cat.as_view() , name='category'),
    path('products/<slug>/' , ProductDetail.as_view() , name='product'),
    path('blogs/<slug>/' , ArticleDetail.as_view() , name='blog'),

    path('newsletter/' , Newsletter.as_view() , name='newsletter'),
    path('comment/submit/' , SubmitComment.as_view() , name='submit-comment'),
    path('star/submit/' , SubmitStar.as_view() , name='submit-star'),
    path('cart/submit/' , SubmitCart.as_view() , name='submit-cart'),
    path('notify_users/submit/', SubmitNotifyUser.as_view(), name='submit-notify_user'),
    path('likes_and_dislikes/submit/' , SubmitLike_And_Dislike.as_view() , name='submit-like_dislike'),
    path('wishlist/submit/', SubmitWishlist.as_view(), name='submit-wishlist'),
    path('suggest/submit/', SubmitSuggest.as_view(), name='submit-suggest')
]
