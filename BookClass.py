from dataclasses import dataclass
from typing import TypedDict, List
from uuid import uuid4
from fastapi import HTTPException
from Error.customerror import BadRequestError
from enum import Enum, auto


class Type(Enum):
    """query strings type"""
    RATINGS = "rating"


@dataclass
class Author:
    name: str
    title: str
    age: int


class BookClass:
    id: str
    title: str
    author: Author
    description: str
    rating: int

    def __init__(self, title: str, author: Author, description: str, rating: int):
        self.id = uuid4().hex
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

    def __repr__(self):
        return dict({"id": self.id, "title": self.title, "author": self.author, "description": self.description,
                     "rating": self.rating})

    def setId(self, id: str):
        self.id = id

    def getId(self) -> str:
        return self.id


class Library:
    __books: List[BookClass]

    def __init__(self):
        self.__books: List[BookClass] = []

    def add_book(self, book: BookClass) -> None:
        self.__books.append(book)

    def get_all_books(self) -> List[BookClass]:
        return self.__books

    def find_book(self, book_id: str) -> BookClass:
        book_by_id = [book for book in self.__books if book.getId() == book_id]
        if len(book_by_id) > 0:
            return book_by_id[0]
        raise BadRequestError(error="Invalid ID provided")

    def find_book_by_type(self, type: Type, id: str | int) -> List[BookClass]:
        book_by_type = filter(lambda book: book.__repr__().get(type) == id,
                              self.__books)  # you could also use list comprehension
        return list(book_by_type)

    def edit_book(self, book_id: str, book: BookClass) -> BookClass:
        result: BookClass = None
        for i in range(len(self.__books)):
            if self.__books[i].getId() == book_id:
                book.setId(book_id)
                self.__books[i] = book
                result = self.__books[i]
        return result

    def delete_book(self, book_id) -> str:
        get_book_to_delete = self.find_book(book_id)
        self.__books.remove(get_book_to_delete)
        return "deleted"

    def filter_book(self, query_arr: List[str], search_params: dict[str, str]):
        books: List[BookClass] = []
        for query in query_arr:
            for book in self.__books:
                print(book.__repr__().get(query))
                print(search_params)
                if str(book.__repr__().get(query)) in search_params.values():
                    books.append(book)
            # # print(str(self.__books[0].__repr__()[query]) in search_params.values())
            # book = filter(lambda item: dict(item).get(query) in search_params.values(), self.__books)
            # books = list(book)
            # print(books)

        return books
