from fastapi import FastAPI, Request, APIRouter
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import uuid

from starlette import status

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", name="index")
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"url_for": request.url_for},
    )

@app.get("/about", name="about")
def about(request: Request):
    return templates.TemplateResponse(
        request,
        "about.html",
        {"url_for": request.url_for},
    )

@app.get("/books", name="books")
def books(request: Request):
    return templates.TemplateResponse(
        request,
        "books.html",
        {"url_for": request.url_for},
    )


class Book(BaseModel):
    id: str
    title: str
    author: str
    year: int
    price: float

class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    price: float

books_list = [Book(id = str(uuid.uuid4()), title= "Книга 1",author="Автор 1",year = 2003,price = 100.5),
              Book(id=str(uuid.uuid4()), title="Книга 2", author="Автор 2", year=2004, price=129.5),
              ]


api_router = APIRouter(prefix="/api")
book_router = APIRouter(prefix="/book",tags=["book"])

@book_router.get("/", response_model=List[Book])
def get_all_books() -> List[Book]:
    """
    Получаем все книги

    """
    return books_list

@book_router.get("/{id}", response_model=Book)
def get_book_by_id(id: str) -> Book:
    """Ищем по ид возвращаем книгу по ид либо говорим что нет такой книги"""
    for book in books_list:
        if book.id == id:
            return book
    return {"message": "Book not found"}


@book_router.post("/", response_model=Book,status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    new_book = Book(id = str(uuid.uuid4()),
                    title = book.title,
                    author = book.author,
                    year = book.year,
                    price = book.price)
    books_list.append(new_book)
    return new_book

api_router.include_router(book_router, tags=["book"])
app.include_router(api_router)




"""
Домашнее задание №5
Первое веб-приложение

- в модуле `app` создайте базовое FastAPI приложение
- создайте обычные представления
  - создайте index view `/`
  - добавьте страницу `/about/`, добавьте туда текст, информацию о сайте и разработчике
  - создайте базовый шаблон (используйте https://getbootstrap.com/docs/5.0/getting-started/introduction/#starter-template)
  - в базовый шаблон подключите статику Bootstrap 5 (подключите стили), примените стили Bootstrap
  - в базовый шаблон добавьте навигационную панель `nav` (https://getbootstrap.com/docs/5.0/components/navbar/)
  - в навигационную панель добавьте ссылки на главную страницу `/` и на страницу `/about/` при помощи `url_for`
  - добавьте новые зависимости в файл `requirements.txt` в корне проекта
    (лучше вручную, но можно командой `pip freeze > requirements.txt`, тогда обязательно проверьте, что туда попало, и удалите лишнее)
- создайте api представления:
  - создайте api router, укажите префикс `/api`
  - добавьте вложенный роутер для вашей сущности (если не можете придумать тип сущности, рассмотрите варианты: товар, книга, автомобиль)
  - добавьте представление для чтения списка сущностей
  - добавьте представление для чтения сущности
  - добавьте представление для создания сущности"""