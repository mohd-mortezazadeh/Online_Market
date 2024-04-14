from django import template
from django.db.models import Sum, Count

from Cart.models import Cart

register = template.Library()


@register.simple_tag
def cal_stars(value):
    queries = value.aggregate(sum=Sum('score'), count=Count('score'))
    sum = queries['sum']
    count = queries['count']

    avg = 0
    if sum != None and count != None:
        avg = sum / count

    return round(avg)


@register.simple_tag
def cal_online_user_stars(product, user):
    try:
        stars = product.stars.get(user_id=user.id)
        return stars.score
    except:
        return 0


@register.simple_tag
def cal_unstars(stars):
    return 5 - stars


@register.filter
def get_loop_mul(value):
    return value % 4


@register.simple_tag
def get_product_accepted_comments(product):
    return product.comments.filter(status=True, parent_id=None)


@register.simple_tag
def get_blog_accepted_comments(blog):
    return blog.comments.filter(status=True, parent_id=None)


@register.filter
def show_commented_user_image(image):
    if image:
        return image.url

    return 'https://i.pinimg.com/originals/51/f6/fb/51f6fb256629fc755b8870c801092942.png'


@register.filter
def is_product_added_to_cart(product, user_id):
    if product.cart_set.filter(user_id=user_id).exists():
        return True
    return False


@register.filter
def is_product_added_to_notify_user(product, user_id):
    if product.notifies.filter(user_id=user_id).exists():
        return True
    return False


@register.filter
def cal_cart_sum(user_id, transport_cost=0):
    carts = Cart.objects.filter(user_id=user_id)

    total_carts_price = 0
    for item in carts:
        total_carts_price += int(item.product.price) * item.count

    return total_carts_price + int(transport_cost)


@register.filter
def get_likes_count(product):
    return product.likes_and_dislikes.filter(type='like').count()


@register.filter
def get_dislikes_count(product):
    return product.likes_and_dislikes.filter(type='dislike').count()


@register.simple_tag
def get_user_like_dislike_type(user, product):
    if user.is_authenticated:
        if product.likes_and_dislikes.filter(user=user).filter(type='like'):
            return 'like'

        if product.likes_and_dislikes.filter(user=user).filter(type='dislike'):
            return 'dislike'

    return None


@register.filter
def is_user_add_to_wishlist(user, product):
    if product.wishlist_set.filter(user=user):
        return True

    return False


@register.filter
def is_user_suggested_product(user, product):
    if product.suggests.filter(user=user):
        return True

    return False
