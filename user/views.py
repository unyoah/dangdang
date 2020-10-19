import random
import string

from django.db import transaction

from car.models import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from captcha.image import ImageCaptcha


def captcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 4)
    random_code = ''.join(code)
    request.session['code'] = random_code
    print(random_code)
    date = image.generate(random_code)
    return HttpResponse(date, 'image/png')


def register(request):
    url = request.GET.get('url')
    if request.GET.get('cate_id'):
        url += ('&cate_id=' + request.GET.get('cate_id'))
    return render(request, 'register.html', {'url': url})


def login(request):
    url = request.GET.get('url')
    car = request.session.get('car')
    if request.GET.get('cate_id'):
        url += ('&cate_id=' + request.GET.get('cate_id'))
    if request.COOKIES.get("name"):
        request.session['is_login'] = request.COOKIES.get("name")
        user = TUser.objects.get(username=request.session['is_login'])
        if car:
            for book in car:
                if user.tcar_set.filter(book_id=book.id):
                    t_car = user.tcar_set.get(book_id=book.id)
                    with transaction.atomic():
                        t_car.count += book.count
                        t_car.save()
                else:
                    user.tcar_set.create(book_id=book.id, count=book.count)
            del request.session['car']
        if url:
            return redirect(url)
        else:
            return redirect('index:index')
    return render(request, 'login.html', {'url': url})


def log_out(request):
    del request.session['is_login']
    return HttpResponse('clear')


def reg_ok(request):
    url = request.GET.get('url')
    if request.GET.get('cate_id'):
        url += ('&cate_id=' + request.GET.get('cate_id'))
    user = request.session.get('is_login')
    if not user:
        return redirect('/login')
    flag = True if '@' in user else False
    content = {'user': user, 'flag': str(flag), 'url': url}
    return render(request, 'register ok.html', content)


def reg(request):
    agreement = request.POST.get('chb_agreement')
    code = request.POST.get('txt_vcode')
    user_name = request.POST.get('txt_username')
    password = request.POST.get('txt_password')
    session_code = request.session.get('code')
    if not agreement:
        return HttpResponse('agreement_wrong')
    if code.lower() != session_code.lower():
        return HttpResponse('code_wrong')
    if TUser.objects.filter(username=user_name):
        return HttpResponse('user_repeat')
    with transaction.atomic():
        TUser.objects.create(username=user_name, password=password)
    request.session['is_login'] = user_name
    return HttpResponse('ok')


def log(request):
    user_name = request.POST.get('txtUsername')
    password = request.POST.get('txtPassword')
    code = request.POST.get('txtVerifyCode')
    session_code = request.session.get('code')
    car = request.session.get('car')
    autologin = request.POST.get('autologin')
    if code.lower() != session_code.lower():
        return HttpResponse('code_wrong')
    if TUser.objects.filter(username=user_name, password=password):
        request.session['is_login'] = user_name
        res = HttpResponse('success')
        user = TUser.objects.get(username=request.session['is_login'])
        if car:
            for book in car:
                if user.tcar_set.filter(book_id=book.id):
                    t_car = user.tcar_set.get(book_id=book.id)
                    with transaction.atomic():
                        t_car.count += book.count
                        t_car.save()
                else:
                    user.tcar_set.create(book_id=book.id, count=book.count)
            del request.session['car']
        if autologin:
            res.set_cookie('name', user_name, max_age=7 * 24 * 3600)
            res.set_cookie('password', password, max_age=7 * 24 * 3600)
        return res
    return HttpResponse('failed')
