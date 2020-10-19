from car.models import *


class Book:
    def __init__(self, id, count):
        book = TBook.objects.get(id=id)
        self.id = id
        self.book_name = book.book_name
        self.count = int(count)
        self.price = book.discount
        self.picture = book.picture
        self.total_price = self.price * self.count


class Car:
    def __init__(self):
        self.book_list = []

    def get_book(self, id):
        for book in self.book_list:
            if book.id == id:
                return book

    def add_book(self, id, count=1):
        book = self.get_book(id)
        if book:
            book.count += int(count)
            book.total_price = book.price * book.count
        else:
            book = Book(id, count)
            self.book_list.append(book)

    def remove_book(self, id):
        book = self.get_book(id)
        self.book_list.remove(book)

    def __iter__(self):
        return list.__iter__(self.book_list)
