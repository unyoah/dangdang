import datetime, time

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect

from car.models import *


# Create your views here.
def to_order(request):
    user = request.session.get('is_login')
    if not user:
        return redirect('/login/?url=/to_order/')
    user = TUser.objects.get(username=user)
    address = user.taddress_set.all()
    cart = user.tcar_set.all()
    total = 0
    for i in cart:
        total += i.total()
    content = {'user': user, 'address': address, 'cart': cart, 'total': total}
    return render(request, 'indent.html', content)


def select_addr(request):
    addr = int(request.GET.get('addr_id'))
    user = request.session.get('is_login')
    user = TUser.objects.get(username=user)
    addr = user.taddress_set.get(id=addr)

    def serial(u):
        return {'name': addr.name, 'post_code': addr.post_code, 'mobile': addr.cellphone, 'tel': addr.telephone,
                'address': addr.detail_address}

    return JsonResponse({'addr': addr}, json_dumps_params={'default': serial})


def order(request):
    user = request.session.get('is_login')
    user = TUser.objects.get(username=user)
    total = request.POST.get('total')
    if request.POST.get('addr'):
        addr = int(request.POST.get('addr'))
        ordr = user.torder_set.create(address_id=addr, create_time=datetime.datetime.now().strftime('%F %T'),
                                      order_no=str(time.time()).split('.')[1], storage='天津出版公司', total_price=total)
    else:
        name = request.POST.get('name')
        address = request.POST.get('address')
        post = request.POST.get('post')
        mobile = request.POST.get('mobile')
        tel = request.POST.get('tel')
        if user.taddress_set.filter(name=name, detail_address=address, post_code=post, cellphone=mobile,
                                    telephone=tel):
            addr = user.taddress_set.get(detail_address=address)
        else:
            with transaction.atomic():
                addr = user.taddress_set.create(name=name, detail_address=address, post_code=post, cellphone=mobile,
                                                telephone=tel)
        ordr = user.torder_set.create(address_id=addr.id, create_time=datetime.datetime.now().strftime('%F %T'),
                                      order_no=str(time.time()).split('.')[1], storage='天津出版公司', total_price=total)
    for cart in user.tcar_set.all():
        with transaction.atomic():
            user.torder_set.get(order_no=ordr.order_no).orderitem_set.create(count=cart.count, book_id=cart.book_id)
            cart.delete()
    return JsonResponse({'order': ordr.order_no})


def to_order_ok(request):
    user = request.session.get('is_login')
    if not user:
        return redirect('/login/')
    order_no = request.GET.get('order_no')
    user = TUser.objects.get(username=user)
    order = user.torder_set.get(order_no=order_no)
    count = 0
    items = list(OrderItem.objects.filter(order_id=order.id))
    for item in items:
        count += item.count
    content = {'user': user, 'order': order, 'count': count, 'items': items}
    return render(request, 'indent ok.html', content)
