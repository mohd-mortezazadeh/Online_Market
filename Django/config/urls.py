"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_honypot/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    path('pay/', index),

    ## Auth ##
    path('api/auth/', include('auth.urls')),
    path('', include('social_django.urls', namespace='social')),

    ## Admin ##
    path('api/admin/categories/', include('Category.urls')),
    path('api/admin/articles/', include('Article.urls')),
    path('api/admin/users/', include('User.urls')),
    path('api/admin/products/', include('Product.urls')),
    path('api/admin/carts/', include('Cart.urls')),
    path('api/admin/coupons/', include('Coupon.urls')),
    path('api/admin/tickets/', include('Ticket.urls')),
    path('api/admin/acl/', include('ACL.urls')),
    path('api/admin/payments/', include('Payment.urls')),
    path('api/admin/comments/', include('Comment.urls')),
    path('api/admin/wishlists/', include('WishList.urls')),
    path('api/admin/sliders/', include('Slider.urls')),
    path('api/admin/likes_dislikes/', include('Like_And_DisLike.urls')),
    path('api/admin/settings/', include('Setting.urls')),
    path('api/admin/newsletters/', include('Newsletter.urls')),
    path('api/admin/stars/', include('Star.urls')),
    path('api/admin/orders/' , include('Order.urls')),
    path('api/admin/contact_us/' , include('Contact_us.urls')),

    ## Panel ##
    path('api/panel/' , include('Panel.urls')),

    ## Client ##
    path('', include('Main.urls')),
    path('checkout/' , include('Cart_Checkout.urls')),
    path('payment/', include('ZarinPal.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
