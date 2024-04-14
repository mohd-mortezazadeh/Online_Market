from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from Payment.models import Payment
from zeep import Client
from Product.models import Product
from Coupon.models import Coupon
from datetime import datetime
from Setting.models import Setting

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
amount = 0  # Toman / Required
description = "خرید محصول از فروشگاه آزمایشی اینترنتی اشکان"  # Required
email = 'karimiashkan8186@gmail.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://127.0.0.1:8000/payment/verify/'  # Important: need to edit for realy server.


def CheckCoupon(code, user):
    coupon = Coupon.objects.filter(code=code).first()

    if coupon:
        if coupon.user and coupon.user != user:
            return {'error': 'این کد تخفیف برای کاربر دیگر تنظیم شده است!'}

        if coupon.uses_number == 0:
            return {'error': 'محدودیت استفاده از این کد تخفیف به پایان رسیده است!'}

        today = datetime.today()
        expiration = datetime.strptime(coupon.expiration, '%Y-%m-%d')

        if expiration > today:
            return {'error': 'کد تخفیف وارد شده منقضی شده است!'}

        return coupon

    else:
        return {'error': 'همچین کد تخفیفی وجود ندارد!'}


def CalculateCouponAmount(coupon_percent, price):
    percent_amount = (price * coupon_percent) / 100
    NewPrice = price - percent_amount
    return round(NewPrice)


##############################################################################################################

@login_required(login_url='/login')
def pay(request):
    data = request.POST
    coupon = None
    total_amount = 0

    if not request.user.carts.all():
        return redirect('/')

    for item in request.user.orders.filter(status='sending'):
        product = Product.objects.get(pk=item.product_id)
        amount = int(product.price) * int(item.count)

        if 'coupon_code' in data and data['coupon_code']:
            coupon = CheckCoupon(data['coupon_code'], request.user)
            if type(coupon) is Coupon:
                amount = CalculateCouponAmount(coupon.percent, amount)
            else:
                request.session['coupon_error'] = coupon
                return redirect(reverse('orders-verification'))

        total_amount += amount

    transport_cost = Setting.objects.get(key='transport_cost').value
    total_amount += int(transport_cost)

    payment = Payment.objects.create(user_id=request.user.id, status=False, amount=round(total_amount), coupon=coupon)

    result = client.service.PaymentRequest(MERCHANT, total_amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        payment.authority = result.Authority
        payment.save()

        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


@login_required(login_url='/login')
def verify(request):
    payment = get_object_or_404(Payment, authority=request.GET['Authority'])
    amount = payment.amount

    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            payment.status = True
            payment.ref_code = result.RefID
            payment.save()

            if payment.coupon:
                payment.coupon.uses_number = payment.coupon.uses_number - 1
                payment.coupon.save()

            request.user.orders.filter(status='sending').update(payment=payment)
            request.user.orders.filter(status='sending').update(status='posted')
            request.user.carts.all().delete()

            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
