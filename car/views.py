from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from car.car import *


# Create your views here.
def to_car(request):
    user = request.session.get('is_login')
    car = request.session.get('car')
    if user:
        user = TUser.objects.get(username=user)
        tcar = list(user.tcar_set.filter(user_id=user.id))
        if tcar:
            car = Car()
            for i in tcar:
                car.add_book(i.book_id, i.count)
    else:
        car = request.session.get('car')
    total = count = 0
    if car:
        for i in car:
            total += i.total_price
            count += i.count
    content = {'user': user, 'car': car, 'total': total, 'count': count}
    return render(request, 'car.html', content)


def add_car(request):
    id = request.GET.get('id')
    num = int(request.GET.get('num'))
    user = request.session.get('is_login')
    car = request.session.get('car')
    if user:
        user = TUser.objects.get(username=user)
        if user.tcar_set.filter(book_id=id):
            with transaction.atomic():
                t_car = user.tcar_set.get(book_id=id)
                t_car.count += num
                t_car.save()
        else:
            user.tcar_set.create(book_id=id, count=num)
        total = count = 0
        for i in user.tcar_set.filter(user_id=user):
            total += (i.book.discount * i.count)
            count += i.count
        content = {'price': user.tcar_set.get(book_id=id).book.discount * user.tcar_set.get(book_id=id).count,
                   'total': total,
                   'count': count, }
        return JsonResponse(content)
    else:
        if car:
            pass
        else:
            car = Car()
        car.add_book(id, num)
        request.session['car'] = car
        total = count = 0
        for i in car:
            total += i.total_price
            count += i.count
        return JsonResponse({'price': f'{car.get_book(id).total_price}', 'total': total, 'count': count})


def del_car(request):
    id = request.GET.get('id')
    user = request.session.get('is_login')
    if user:
        car = Car()
        user = TUser.objects.get(username=user)
        with transaction.atomic():
            user.tcar_set.get(user_id=user.id, book_id=id).delete()
        for i in user.tcar_set.filter(user_id=user.id):
            car.add_book(i.id, i.count)
        total = count = 0
        for i in user.tcar_set.filter(user_id=user):
            total += (i.book.discount * i.count)
            count += i.count
        content = {'msg': 'ok',
                   'total': total,
                   'count': count, }
        return JsonResponse(content)
    else:
        car = request.session.get('car')
        car.remove_book(id)
        request.session['car'] = car
        total = count = 0
        for i in car:
            total += i.total_price
            count += i.count
        return JsonResponse({'msg': 'ok', 'total': total, 'count': count})


def set_car(request):
    user = request.session.get('is_login')
    id = request.GET.get('id')
    num = int(request.GET.get('num'))
    if user:
        car = Car()
        user = TUser.objects.get(username=user)
        with transaction.atomic():
            cart = user.tcar_set.get(user_id=user.id, book_id=id)
            cart.count = num
            cart.save()
        for i in user.tcar_set.filter(user_id=user.id):
            car.add_book(i.book_id, i.count)
        total = count = 0
        for i in user.tcar_set.filter(user_id=user):
            total += (i.book.discount * i.count)
            count += i.count
        content = {'price': user.tcar_set.get(book_id=id).book.discount * user.tcar_set.get(book_id=id).count,
                   'total': total,
                   'count': count, }
        return JsonResponse(content)
    else:
        car = request.session.get('car')
        car.get_book(id).count = num
        car.get_book(id).total_price = car.get_book(id).price * num
        request.session['car'] = car
        total = count = 0
        for book in car.book_list:
            total += book.total_price
            count += book.count
        return JsonResponse({'price': f'{car.get_book(id).total_price}', 'msg': 'ok', 'total': total, 'count': count})
