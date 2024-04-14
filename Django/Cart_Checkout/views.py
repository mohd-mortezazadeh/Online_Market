from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from rest_framework.permissions import IsAuthenticated

from Main.views import StaticData
from Cart.models import Cart
from Order.models import Order
from .forms import OrderForm


class CartsList(View):
    def get(self, request):
        context = StaticData()
        if 'color_id' in request.session:
            context['color_id'] = request.session['color_id']
            request.session.pop('color_id')

        if 'size_error' in request.session:
            context['size_error'] = request.session['size_error']
            request.session.pop('size_error')

        return render(request, 'front/checkout/carts-list.html', context)


class FillData(View):
    def get(self, request):
        if not request.user.carts.all():
            return redirect('/')

        if request.user.carts.filter(color_id=None):
            request.session['color_id'] = 'لطفا به جزییات محصول بروید و رنگی را برای محصول خود انتخاب کنید'
            return redirect(reverse('carts-list'))

        if request.user.carts.filter(size_id=None):
            request.session['size_error'] = 'لطفا به جزییات محصول بروید و سایزی را برای محصول خود انتخاب کنید'
            return redirect(reverse('carts-list'))

        context = StaticData()
        context['form'] = OrderForm()
        return render(request, 'front/checkout/fill_data.html', context)

    def post(self, request):
        form = None

        for item in request.user.carts.all():
            query = Q(product_id=item.product_id) & Q(user_id=item.user_id) & Q(status='sending')
            order = Order.objects.filter(query).first()

            if not order:
                form = OrderForm(request.POST)
                if form.is_valid():
                    order = form.save(commit=False)
                    order.user_id = request.user.id
                    order.product_id = item.product_id
                    order.color_id = item.color_id
                    order.size_id = item.size_id
                    order.count = item.count
                    order.save()

            else:
                form = OrderForm(request.POST, instance=order)
                if form.is_valid():
                    order = form.save(commit=False)
                    order.user_id = request.user.id
                    order.product_id = item.product_id
                    order.color_id = item.color_id
                    order.size_id = item.size_id
                    order.count = item.count
                    order.save()

        if form.errors:
            context = StaticData()
            context['form'] = form
            return render(request, 'front/checkout/fill_data.html', context)

        return redirect(reverse('payment-method'))


class ChoosePaymentMethod(View):
    def get(self, request):
        context = StaticData()
        return render(request, 'front/checkout/choose_payment_method.html', context)

    def post(self, request):
        for item in request.user.orders.filter(status='sending'):
            if 'method' not in request.POST:
                request.POST._mutable = True
                request.POST['method'] = 'cash'

            item.payment_type = 'online' if request.POST['method'] == 'online' else 'cash'
            item.save()
        return redirect(reverse('orders-verification'))


class Verification(View):
    def get(self, request, *args):
        context = StaticData()
        if 'coupon_error' in request.session:
            context['coupon_error'] = request.session['coupon_error']['error']
            request.session.pop('coupon_error')

        return render(request, 'front/checkout/verification.html', context)


#############################################################

@method_decorator(csrf_protect, name='dispatch')
class ChangeCartCount(View):
    def post(self, request):
        context = StaticData()

        cart = Cart.objects.get(pk=request.POST['cart_id'])
        cart.count = request.POST['new_count']
        cart.save()

        context['user'] = request.user
        html = render_to_string(
            template_name="partials/cart_checkout/carts_lists_partial.html",
            context=context
        )

        data_dict = {"carts_list_partial": html}
        return JsonResponse(data_dict, safe=False)


@method_decorator(csrf_protect, name='dispatch')
class DeleteCart(View):
    def post(self, request):
        context = StaticData()

        try:
            cart = Cart.objects.get(pk=request.POST['cart_id'])
            cart.delete()
            message = 'محصول مورد نظر از سبد خرید شما حذف شد'
        except:
            message = 'خطایی پیش آمده است ، دوباره امتحان کنید'

        context['user'] = request.user
        html = render_to_string(
            template_name="partials/cart_checkout/carts_lists_partial.html",
            context=context
        )

        data_dict = {"carts_list_partial": html, 'detail': message}
        return JsonResponse(data_dict, safe=False)
