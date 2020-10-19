from django.core.paginator import Paginator
from django.shortcuts import render

from car.car import Car
from car.models import *
import datetime


# Create your views here.
def index(request):
    user = request.session.get('is_login')
    car = request.session.get('car')
    if user:
        user = TUser.objects.get(username=user)
        tcar = list(user.tcar_set.filter(user_id=user.id))
        if tcar:
            car = Car()
            for i in tcar:
                car.add_book(i.book_id, i.count)
    count = 0
    if car:
        for i in car:
            count += i.count
    cate_1 = Category.objects.filter(level=1)
    cate_2 = Category.objects.filter(level=2)
    new_book = TBook.objects.all().order_by('pub_time')[:8]
    top_selling1 = TBook.objects.filter(
        pub_time__gte=str(datetime.datetime.now() + datetime.timedelta(days=-200))[:10]).order_by('-sales_volume')[:5]
    top_comments = TBook.objects.order_by('comments')
    top_selling2 = TBook.objects.filter(
        pub_time__gte=str(datetime.datetime.now() + datetime.timedelta(days=-1000))[:10]).order_by('-sales_volume')[:10]
    content = {'cate_1': cate_1, 'cate_2': cate_2, 'new_book': new_book, 'top_selling1': top_selling1,
               'top_comments': top_comments, 'top_selling2': top_selling2, 'user': user, 'count': count}
    return render(request, 'index.html', content)


def book_detail(request):
    user = request.session.get('is_login')
    car = request.session.get('car')
    if user:
        user = TUser.objects.get(username=user)
        tcar = list(user.tcar_set.filter(user_id=user.id))
        if tcar:
            car = Car()
            for i in tcar:
                car.add_book(i.book_id, i.count)
    count = 0
    if car:
        for i in car:
            count += i.count
    book_id = request.GET.get('book_id')
    book = TBook.objects.get(id=book_id)
    cate1 = Category.objects.get(id=book.category.parent_id)
    content = {'book': book, 'cate': cate1, 'user': user, 'count': count}
    return render(request, 'Book details.html', content)


def book_list(request):
    user = request.session.get('is_login')
    car = request.session.get('car')
    if user:
        user = TUser.objects.get(username=user)
        tcar = list(user.tcar_set.filter(user_id=user.id))
        if tcar:
            car = Car()
            for i in tcar:
                car.add_book(i.book_id, i.count)
    count = 0
    if car:
        for i in car:
            count += i.count
    cate_1 = Category.objects.filter(level=1)
    cate_2 = Category.objects.filter(level=2)
    level = request.GET.get('level', 1)
    num = request.GET.get('num', 1)
    cate_id = request.GET.get('cate_id', 1)

    cate = Category.objects.filter(id=0)

    if level == '1':
        book = TBook.objects.filter(category__parent_id=cate_id)
        cate = cate | Category.objects.filter(id=cate_id)
    else:
        book = TBook.objects.filter(category_id=cate_id)
        cc = Category.objects.filter(id=cate_id)
        cate = cate | Category.objects.filter(id=cc[0].parent_id) | cc
    paginator = Paginator(book, per_page=2)
    page = paginator.page(num)
    content = {'cate_1': cate_1, 'cate_2': cate_2, 'title': cate, 'page': page, 'paginator': paginator, 'level': level,
               'num': num, 'user': user, 'count': count}
    return render(request, 'booklist.html', content)
