# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class OrderItem(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey('TBook', models.DO_NOTHING, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey('TOrder', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_item'


class TAddress(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    detail_address = models.CharField(max_length=100, blank=True, null=True)
    post_code = models.CharField(max_length=6, blank=True, null=True)
    cellphone = models.CharField(max_length=11, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_address'


class TAuthor(models.Model):
    author_name = models.CharField(max_length=20, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_author'


class TBook(models.Model):
    book_name = models.CharField(max_length=20, blank=True, null=True)
    author = models.ForeignKey(TAuthor, models.DO_NOTHING, blank=True, null=True)
    press = models.CharField(max_length=20, blank=True, null=True)
    pub_time = models.DateField(blank=True, null=True)
    discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    prime_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    isbn = models.IntegerField(blank=True, null=True)
    sales_volume = models.IntegerField(blank=True, null=True)
    words = models.IntegerField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    edi_recommen = models.TextField(blank=True, null=True)
    content_recommen = models.TextField(blank=True, null=True)
    catalogue = models.TextField(blank=True, null=True)
    media_reviews = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    picture = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    isset = models.IntegerField(blank=True, null=True)
    paper = models.CharField(max_length=20, blank=True, null=True)
    pack = models.CharField(max_length=20, blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    impression = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=20, blank=True, null=True)
    comments = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_book'

    def dis(self):
        return '%.2f' % (self.discount / self.prime_price * 10)


class TCar(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_car'

    def total(self):
        return float('%.2f' % (self.book.discount * self.count))


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    order_no = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    storage = models.CharField(max_length=30, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TUser(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'
