from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from Product.models import Product, Image, Color, Size, NotifyUser
from Category.models import Category
from Slider.models import Slider
from Article.models import Article
from Like_And_DisLike.models import Like_And_DisLike
from django.http import JsonResponse
from Newsletter.serializer import NewsletterSerializer
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from .serializer import CommentSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Star.serializer import StarSerializer
from Star.models import Star
from Setting.models import Setting
from Cart.models import Cart
from Contact_us.serializer import ContactUsSerializer
from WishList.serializer import WishlistSerializer
from Cart.serializer import CartSerializer
from Product.serializer import NotifyUserSerializer
from django.db.models import Q, Count

default_pagination_number = 10


def paginate(paginator, page, type='products', sorting=None):
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    if type == 'products':
        html = render_to_string(
            template_name="partials/products_list.html",
            context={'products': objects, 'sorting': sorting}
        )
        data_dict = {"products": html}
        return data_dict

    html = render_to_string(
        template_name="partials/blogs_list.html",
        context={'blogs': objects, 'sorting': sorting}
    )
    data_dict = {"blogs": html}
    return data_dict


def StaticData():
    context = {}
    context['categories'] = Category.objects.filter(parent__isnull=True)

    context['settings'] = {}
    context['settings']['description'] = Setting.objects.get_or_create(
        key='description',
        defaults={'key': 'description', 'value': 'این یک متن تستی توضیحات درباره سایت در فوتر است'},
    )[0].value

    context['settings']['newsletter_text'] = Setting.objects.get_or_create(
        key='newsletter_text',
        defaults={'key': 'newsletter_text', 'value': 'این یک متن تستی برای ثبت نام در خبرنامه است'},
    )[0].value

    context['settings']['transport_cost'] = Setting.objects.get_or_create(
        key='transport_cost',
        defaults={'key': 'transport_cost', 'value': 15000},
    )[0].value

    context['settings']['phone'] = Setting.objects.get_or_create(
        key='phone',
        defaults={'key': 'phone', 'value': '09396988720'},
    )[0].value

    context['settings']['email'] = Setting.objects.get_or_create(
        key='email',
        defaults={'key': 'email', 'value': 'karimiashkan8186@gmail.com'},
    )[0].value

    context['settings']['telegram_id'] = Setting.objects.get_or_create(
        key='telegram_id',
        defaults={'key': 'telegram_id', 'value': 'ashkn_k'},
    )[0].value

    context['settings']['copy_right'] = Setting.objects.get_or_create(
        key='copy_right',
        defaults={'key': 'copy_right',
                  'value': 'تمامی حقوق مادی و معنوی این سایت متعلق به Ashkan می باشد و هرگونه کپی برداری غیرقانونی محسوب خواهد شد'},
    )[0].value

    context['settings']['logo_description'] = Setting.objects.get_or_create(
        key='logo_description',
        defaults={'key': 'logo_description',
                  'value': 'این یک متن تستی برای لوگو هدر است'},
    )[0].value

    context['settings']['logo'] = Setting.objects.get_or_create(
        key='logo',
        defaults={'key': 'logo',
                  'value': 'https://raw.githubusercontent.com/MrGheibi/Blazar/main/src/assets/Blazar-logo-git.png'},
    )[0].value

    context['settings']['logo_title'] = Setting.objects.get_or_create(
        key='logo_title',
        defaults={'key': 'logo_title',
                  'value': 'Blazar Shop'},
    )[0].value

    context['settings']['transfer_detail'] = Setting.objects.get_or_create(
        key='transfer_detail',
        defaults={'key': 'transfer_detail',
                  'value': 'محصولات شما ظرف 48 ساعت درب منزل تحویل داده میشوند و نحوه پرداخت هم به تصمیم و میل شما که هنگام تسویه حساب انتخاب میکنید انجام خواهد شد'},
    )[0].value

    return context


def GetFilterBarOptions(context):
    context['filter_bar'] = {}
    context['filter_bar']['colors'] = Color.objects.all()
    context['filter_bar']['sizes'] = Size.objects.all()
    context['filter_bar']['categories'] = Category.objects.filter(parent__isnull=False)

    return context


##########################################

def Search(search_word):
    query = Q(title__icontains=search_word) | Q(slug__icontains=search_word) | Q(short_text__icontains=search_word) | \
            Q(text__icontains=search_word) | Q(tags__icontains=search_word) | Q(price__icontains=search_word) | \
            Q(colors__name__icontains=search_word) | Q(sizes__title__icontains=search_word) | Q(
        category__name__icontains=search_word)

    products = Product.objects.filter(query).distinct()
    return products


def Filter(request, allProducts, context=None):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    sizes = request.GET.getlist('size[]')

    if 'minPrice' in request.GET and 'maxPrice' in request.GET:
        minPrice = request.GET['minPrice']
        maxPrice = request.GET['maxPrice']
        allProducts = allProducts.filter(price__gte=minPrice).filter(price__lte=maxPrice)

    if len(colors) > 0:
        allProducts = allProducts.filter(colors__in=colors).distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(category_id__in=categories).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(sizes__in=sizes).distinct()

    try:
        allProducts = allProducts.order_by(request.GET['sorting'])
        context['sorting'] = request.GET['sorting']
    except:
        pass

    return allProducts


class Index(View):
    def get(self, request):
        context = StaticData()
        context = GetFilterBarOptions(context)

        if 'search' in request.GET:
            context['products'] = Search(request.GET['search'])
            context['products'] = Filter(request, context['products'], context)
            context['search'] = request.GET['search']

            page = request.GET.get('page', 1)
            paginator = Paginator(context['products'], default_pagination_number)
            if request.is_ajax():
                data_dict = paginate(paginator, page, sorting=context.get('sorting'))
                return JsonResponse(data_dict, safe=False)

            context['products'] = paginator.page(1)
            return render(request, 'front/products-search.html', context)

        context['special_products'] = Product.objects.filter(status=True).annotate(
            payments_count=Count('orders')).order_by('-payments_count')
        context['most_visited_products'] = Product.objects.filter(status=True).order_by('-viewCount')
        context['new_products'] = Product.objects.filter(status=True).order_by('-created_at')[:8]
        context['most_liked_products'] = Product.objects.filter(status=True).order_by('-likeCount')[:8]
        context['sliders'] = Slider.objects.filter(status=True).order_by('priority')
        context['last_articles'] = Article.objects.filter(status=1).order_by('-created_at')[:6]

        return render(request, 'front/index.html', context)


class Contact_us(View):
    def get(self, request):
        context = StaticData()
        context['contact_us_description'] = 'برای تماس با ما کافی است اطلاعات رو وارد کنید و متن درخواست خود را بنویسید و ارسال کنید و ما در اولین فرصت و نزدیک ترین زمان بررسی و رسیدگی میکنیم (یک متن تستی)'
        return render(request, 'front/contact_us.html', context)

    def post(self, request):
        serializer = ContactUsSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()

        else:
            return JsonResponse({'detail': 'خطایی پیش آمیده است لطفا موارد را به دقت پر کنید.'} , status=400 , safe=False)

        return JsonResponse({'detail': 'پیام تماس باما شما با موفقیت ثبت شد و بررسی خواهد شد.'}, safe=False)


class About_us(View):
    def get(self, request):
        context = StaticData()
        context['about_us_texts'] = {}

        context['about_us_texts']['programmer_text'] = Setting.objects.get_or_create(
            key='programmer_text',
            defaults={'key': 'programmer_text',
                      'value': 'برنامه نویس و نویسنده سایت اشکان کریمی است'},
        )[0].value
        context['about_us_texts']['programmer_title'] = Setting.objects.get_or_create(
            key='programmer_title',
            defaults={'key': 'programmer_title',
                      'value': 'برنامه نویس'},
        )[0].value
        context['about_us_texts']['programmer_image'] = Setting.objects.get_or_create(
            key='programmer_image',
            defaults={'key': 'programmer_image',
                      'value': 'https://d3oj8nq9p0q26f.cloudfront.net/blog/assets/images/posts/coding-52aa9f6bac9cda8536906f30df9732aaff341e804e80d5706ce90d3d0137e0a6.jpg'},
        )[0].value

        context['about_us_texts']['manager_text'] = Setting.objects.get_or_create(
            key='manager_text',
            defaults={'key': 'manager_text',
                      'value': 'مدیر و صاحب این سایت اشکان کریمی است'}
        )[0].value
        context['about_us_texts']['manager_title'] = Setting.objects.get_or_create(
            key='manager_title',
            defaults={'key': 'manager_title',
                      'value': 'صاحب سایت'}
        )[0].value
        context['about_us_texts']['manager_image'] = Setting.objects.get_or_create(
            key='manager_image',
            defaults={'key': 'manager_image',
                      'value': 'https://miro.medium.com/max/1187/1*0FqDC0_r1f5xFz3IywLYRA.jpeg'}
        )[0].value

        context['about_us_texts']['shopper_text'] = Setting.objects.get_or_create(
            key='shopper_text',
            defaults={'key': 'shopper_text',
                      'value': 'محصولات شما ظرف 48 ساعت درب منزل تحویل داده میشوند و نحوه پرداخت هم به تصمیم و میل شما که هنگام تسویه حساب انتخاب میکنید انجام خواهد شد'},
        )[0].value
        context['about_us_texts']['shopper_title'] = Setting.objects.get_or_create(
            key='shopper_title',
            defaults={'key': 'shopper_title',
                      'value': 'فروشنده'},
        )[0].value
        context['about_us_texts']['shopper_image'] = Setting.objects.get_or_create(
            key='shopper_image',
            defaults={'key': 'shopper_image',
                      'value': 'https://miro.medium.com/max/1187/1*0FqDC0_r1f5xFz3IywLYRA.jpeg'}
        )[0].value

        ####

        context['about_us_texts']['about_us_header'] = Setting.objects.get_or_create(
            key='about_us_header',
            defaults={'key': 'about_us_header',
                      'value': 'این یک سایت نمونه رزومه با فریم ورک جنگو است'}
        )[0].value

        context['about_us_texts']['about_us_text'] = Setting.objects.get_or_create(
            key='about_us_text',
            defaults={'key': 'about_us_text',
                      'value': 'ورم ایپسوم متنی است که ساختگی برای طراحی و چاپ آن مورد است. صنعت چاپ زمانی لازم بود شرایطی شما باید فکر ثبت نام و طراحی، لازمه خروج می باشد. در ضمن قاعده همفکری ها جوابگوی سئوالات زیاد شاید باشد، آنچنان که لازم بود طراحی گرافیکی خوب بود. کتابهای زیادی شرایط سخت ، دشوار و کمی در سالهای دور لازم است. هدف از این نسخه فرهنگ پس از آن و دستاوردهای خوب شاید باشد. حروفچینی لازم در شرایط فعلی لازمه تکنولوژی بود که گذشته، حال و آینده را شامل گردد. سی و پنج درصد از طراحان در قرن پانزدهم میبایست پرینتر در ستون و سطر حروف لازم است، بلکه شناخت این ابزار گاه اساسا بدون هدف بود و سئوالهای زیادی در گذشته بوجود می آید، تنها لازمه آن بود ورم ایپسوم متنی است که ساختگی برای طراحی و چاپ آن مورد است. صنعت چاپ زمانی لازم بود شرایطی شما باید فکر ثبت نام و طراحی، لازمه خروج می باشد. در ضمن قاعده همفکری ها جوابگوی سئوالات زیاد شاید باشد، آنچنان که لازم بود طراحی گرافیکی خوب بود. کتابهای زیادی شرایط سخت ، دشوار و کمی در سالهای دور لازم است. هدف از این نسخه فرهنگ پس از آن و دستاوردهای خوب شاید باشد. حروفچینی لازم در شرایط فعلی لازمه تکنولوژی بود که گذشته، حال و آینده را شامل گردد. سی و پنج درصد از طراحان در قرن پانزدهم میبایست پرینتر در ستون و سطر حروف لازم است، بلکه شناخت این ابزار گاه اساسا بدون هدف بود و سئوالهای زیادی در گذشته بوجود می آید، تنها لازمه آن بود ورم ایپسوم متنی است که ساختگی برای طراحی و چاپ آن مورد است. صنعت چاپ زمانی لازم بود شرایطی شما باید فکر ثبت نام و طراحی، لازمه خروج می باشد. در ضمن قاعده همفکری ها جوابگوی سئوالات زیاد شاید باشد، آنچنان که لازم بود طراحی گرافیکی خوب بود. کتابهای زیادی شرایط سخت ، دشوار و کمی در سالهای دور لازم است. هدف از این نسخه فرهنگ پس از آن و دستاوردهای خوب شاید باشد. حروفچینی لازم در شرایط فعلی لازمه تکنولوژی بود که گذشته، حال و آینده را شامل گردد. سی و پنج درصد از طراحان در قرن پانزدهم میبایست پرینتر در ستون و سطر حروف لازم است، بلکه شناخت این ابزار گاه اساسا بدون هدف بود و سئوالهای زیادی در گذشته بوجود می آید، تنها لازمه آن بود ورم ایپسوم متنی است که ساختگی برای طراحی و چاپ آن مورد است. صنعت چاپ زمانی لازم بود شرایطی شما باید فکر ثبت نام و طراحی، لازمه خروج می باشد. در ضمن قاعده همفکری ها جوابگوی سئوالات زیاد شاید باشد، آنچنان که لازم بود طراحی گرافیکی خوب بود. کتابهای زیادی شرایط سخت ، دشوار و کمی در سالهای دور لازم است. هدف از این نسخه فرهنگ پس از آن و دستاوردهای خوب شاید باشد. حروفچینی لازم در شرایط فعلی لازمه تکنولوژی بود که گذشته، حال و آینده را شامل گردد. سی و پنج درصد از طراحان در قرن پانزدهم میبایست پرینتر در ستون و سطر حروف لازم است، بلکه شناخت این ابزار گاه اساسا بدون هدف بود و سئوالهای زیادی در گذشته بوجود می آید، تنها لازمه آن بود ورم ایپسوم متنی است که ساختگی برای طراحی و چاپ آن مورد است. صنعت چاپ زمانی لازم بود شرایطی شما باید فکر ثبت نام و طراحی، لازمه خروج می باشد. در ضمن قاعده همفکری ها جوابگوی سئوالات زیاد شاید باشد، آنچنان که لازم بود طراحی گرافیکی خوب بود. کتابهای زیادی شرایط سخت ، دشوار و کمی در سالهای دور لازم است. هدف از این نسخه فرهنگ پس از آن و دستاوردهای خوب شاید باشد. حروفچینی لازم در شرایط فعلی لازمه تکنولوژی بود که گذشته، حال و آینده را شامل گردد. سی و پنج درصد از طراحان در قرن پانزدهم میبایست پرینتر در ستون و سطر حروف لازم است، بلکه شناخت این ابزار گاه اساسا بدون هدف بود و سئوالهای زیادی در گذشته بوجود می آید، تنها لازمه آن بود'}
        )[0].value

        return render(request, 'front/about-us.html', context)


class Cat(View):
    def get(self, request, slug):
        context = StaticData()
        context = GetFilterBarOptions(context)

        context['products'] = Product.objects.filter(status=True).filter(category__slug=slug)
        context['products'] = Filter(request, context['products'], context)

        page = request.GET.get('page', 1)

        paginator = Paginator(context['products'], default_pagination_number)
        if request.is_ajax():
            data_dict = paginate(paginator, page, sorting=context.get('sorting'))
            return JsonResponse(data_dict, safe=False)

        context['products'] = paginator.page(1)
        context['category'] = Category.objects.get(slug=slug)

        return render(request, 'front/category.html', context)


class Products(View):
    def get(self, request):
        context = StaticData()
        context = GetFilterBarOptions(context)

        context['products'] = Product.objects.filter(status=True).order_by('-created_at')
        context['products'] = Filter(request, context['products'], context)

        page = request.GET.get('page', 1)

        paginator = Paginator(context['products'], default_pagination_number)
        if request.is_ajax():
            data_dict = paginate(paginator, page, sorting=context.get('sorting'))
            return JsonResponse(data_dict, safe=False)

        context['products'] = paginator.page(1)
        return render(request, 'front/products.html', context)


class ProductDetail(View):
    def get(self, request, slug):
        context = StaticData()
        context = GetFilterBarOptions(context)

        context['product'] = get_object_or_404(Product, slug=slug)
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['images'] = Image.objects.filter(product__slug=slug)

        context['colors_list'] = context['product'].colors.all()
        context['sizes_list'] = context['product'].sizes.all()
        context['related_products'] = context['product'].category.product_set.exclude(slug=slug)

        return render(request, 'front/product-single.html', context)


class Articles(View):
    def get(self, request):
        context = StaticData()
        context = GetFilterBarOptions(context)

        context['blogs'] = Article.objects.filter(status=1)
        context['archive_blogs'] = Article.objects.filter(status=2)

        page = request.GET.get('page', 1)

        paginator = Paginator(context['blogs'], default_pagination_number)
        if request.is_ajax():
            data_dict = paginate(paginator, page, 'blogs')
            return JsonResponse(data_dict, safe=False)

        context['blogs'] = paginator.page(1)
        return render(request, 'front/blog.html', context)


class ArticleDetail(View):
    def get(self, request, slug):
        context = StaticData()
        context = GetFilterBarOptions(context)

        context['blog'] = get_object_or_404(Article, slug=slug)
        context['related_blogs'] = Article.objects.filter(status=1).exclude(slug=slug)[:10]

        return render(request, 'front/blog-single.html', context)


##########################################################################

class Newsletter(APIView):
    def post(self, request):
        serializer = NewsletterSerializer(data=request.POST)

        if not serializer.is_valid():
            raise ValidationError({'email': ['لطفا یک ایمیل معتبر وارد کنید']})
        serializer.save()

        return Response({'detail': 'شما با موفقیت به خبرنامه اضافه شدید'}, 200)


@method_decorator(csrf_protect, name='dispatch')
class SubmitComment(View):
    def post(self, request):
        request.POST._mutable = True
        request.POST['user_id'] = request.user.id

        serializer = CommentSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        product = Product.objects.get(pk=request.POST['object_id'])
        html = render_to_string(
            template_name="partials/comments.html",
            context={'object': product}
        )

        data_dict = {"comments": html, 'detail': 'نظر شما با موفقیت ثبت شد و بعد از تایید مدیر در سایت قرار میگیرد'}
        return JsonResponse(data_dict, safe=False)


@method_decorator(csrf_protect, name='dispatch')
class SubmitStar(View):
    def post(self, request):
        request.POST._mutable = True
        request.POST['user_id'] = request.user.id

        serializer = None
        try:
            star = Star.objects.get(product_id=request.POST['product_id'], user_id=request.user.id)
            if request.POST['score'] == '1' and star.score == 1:
                star.delete()
            else:
                serializer = StarSerializer(instance=star, data=request.POST)

        except:
            serializer = StarSerializer(data=request.POST)

        if serializer and serializer.is_valid(raise_exception=True):
            serializer.save()

        product = Product.objects.get(pk=request.POST['product_id'])
        html = render_to_string(
            template_name="partials/stars.html",
            context={'product': product, 'user': request.user}
        )

        data_dict = {"stars": html}
        return JsonResponse(data_dict, safe=False)


@method_decorator(csrf_protect, name='dispatch')
class SubmitCart(View):
    def post(self, request):
        request.POST._mutable = True
        request.POST['user'] = request.user.id

        message = ''

        try:
            cart = Cart.objects.get(product_id=request.POST['product'], user_id=request.user.id)
            if 'page' in request.POST:
                cart.delete()
                message = 'محصول مورد نظر با موفقیت از سبد خرید حذف شد'
            else:
                message = 'محصول مورد نظر با موفقیت به سبد خرید اضافه شد'
        except:
            serializer = CartSerializer(data=request.POST)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = 'محصول مورد نظر با موفقیت به سبد خرید اضافه شد'

        product = Product.objects.get(pk=request.POST['product'])
        html = render_to_string(
            template_name="partials/product_single_buttons.html",
            context={'product': product, 'user': request.user}
        )

        cart_html = render_to_string(
            template_name="partials/carts.html",
            context={'user': request.user}
        )

        data_dict = {"products": html, 'carts': cart_html, 'message': message}
        return JsonResponse(data_dict, safe=False)


@method_decorator(csrf_protect, name='dispatch')
class SubmitNotifyUser(View):
    def post(self, request):
        request.POST._mutable = True
        request.POST['user_id'] = request.user.id
        request.POST['active'] = True

        message = ''

        try:
            notify_user = NotifyUser.objects.get(product_id=request.POST['product_id'], user_id=request.user.id)
            notify_user.delete()
            message = 'محصول مورد نظر با موفقیت از اطلاع رسانی های شما حذف شد'
        except:
            serializer = NotifyUserSerializer(data=request.POST)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = 'محصول مورد نظر با موفقیت به اطلاع رسانی های شما اضافه شد'

        product = Product.objects.get(pk=request.POST['product_id'])
        html = render_to_string(
            template_name="partials/product_single_buttons.html",
            context={'product': product, 'user': request.user}
        )

        data_dict = {"products": html, 'message': message}
        return JsonResponse(data_dict, safe=False)


########################################################################################################

def Check_Like_DisLike_Exist(product, user, type):
    liked_disliked = product.likes_and_dislikes.filter(user=user, type=type).first()
    if liked_disliked:
        liked_disliked.delete()


def Create_Like_DisLike(product, user, type):
    Like_And_DisLike.objects.create(content_object=product, type=type, user=user)


@method_decorator(csrf_protect, name='dispatch')
class SubmitLike_And_Dislike(View):
    def post(self, request):
        product = Product.objects.get(pk=request.POST['product_id'])
        if request.POST['type'] == 'like':
            liked = product.likes_and_dislikes.filter(user=request.user, type='like')
            if liked:
                liked.delete()
            else:
                Check_Like_DisLike_Exist(product, request.user, 'dislike')
                Create_Like_DisLike(product, request.user, request.POST['type'])

        else:
            disliked = product.likes_and_dislikes.filter(user=request.user, type='dislike')
            if disliked:
                disliked.delete()
            else:
                Check_Like_DisLike_Exist(product, request.user, 'like')
                Create_Like_DisLike(product, request.user, request.POST['type'])

        html = render_to_string(
            template_name="partials/likes_and_dislikes.html",
            context={'product': product, 'user': request.user}
        )

        data_dict = {"likes_and_dislikes": html}
        return JsonResponse(data_dict, safe=False)


@method_decorator(csrf_protect, name='dispatch')
class SubmitWishlist(View):
    def post(self, request):
        request.POST._mutable = True
        request.POST['user_id'] = request.user.id

        product = Product.objects.get(pk=request.POST['product_id'])
        try:
            wishlist = product.wishlist_set.get(user=request.user)
            wishlist.delete()
        except:
            serializer = WishlistSerializer(data=request.POST)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

        html = render_to_string(
            template_name="partials/wishlist.html",
            context={'product': product, 'user': request.user}
        )

        data_dict = {"wishlist": html}
        return JsonResponse(data_dict, safe=False)


from Product.serializer import SuggestSerializer


@method_decorator(csrf_protect, name='dispatch')
class SubmitSuggest(View):
    def post(self, request):
        request.POST._mutable = True
        request.POST['user_id'] = request.user.id

        product = Product.objects.get(pk=request.POST['product_id'])
        try:
            suggest = product.suggests.get(user=request.user)
            suggest.delete()
        except:
            serializer = SuggestSerializer(data=request.POST)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

        html = render_to_string(
            template_name="partials/suggesting.html",
            context={'product': product, 'user': request.user}
        )

        data_dict = {"suggesting": html}
        return JsonResponse(data_dict, safe=False)
