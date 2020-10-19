import os,django


from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangdang.settings")
django.setup()
# Create your tests here.
from car.models import *

# for i in range(8):
#     TBook.objects.create(press='商务出版社',pub_time=f'2020-{i+1}-15',discount=6.66,prime_price=70,isbn=978757021,sales_volume=10000,words=37775,pages=367,isset=1,paper='胶纸型',comments=6000,format='平装—胶订')book_pic\book3.jpg
# book_pic\book3.jpg
# book1=TBook.objects.
# print(book1)

import datetime

print(str(datetime.datetime.now() + datetime.timedelta(days=-200))[:10])