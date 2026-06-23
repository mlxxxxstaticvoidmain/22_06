from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///library.db", echo=True)

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(Integer)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.id'))

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

authors = [
    Author(name="Булгаков Михаил", birth_year=1891),
    Author(name="Пушкин Александр", birth_year=1799),
    Author(name="Тургенев Иван", birth_year=1818),
]
session.add_all(authors)
session.commit()

books = [
    Book(title="Мастер и Маргарита", year=1967, author_id=1),
    Book(title="Собачье сердце", year=1925, author_id=1),
    Book(title="Евгений Онегин", year=1833, author_id=2),
    Book(title="Капитанская дочка", year=1836, author_id=2),
    Book(title="Отцы и дети", year=1862, author_id=3),
]
session.add_all(books)
session.commit()

print("\nВсе авторы:")
authors_all = session.query(Author).all()
for author in authors_all:
    print(author.name)

print("\nИзменение имени автора:")
author_to_update = session.query(Author).filter(Author.name == "Тургенев Иван").first()
author_to_update.name = "И. С. Тургенев"
session.commit()
print(f"Новое имя: {author_to_update.name}")

print("\nУдаление книги:")
book_to_delete = session.query(Book).filter(Book.title == "Капитанская дочка").first()
session.delete(book_to_delete)
session.commit()
print("Удалена: Капитанская дочка")

print("\nВсе книги (от новых к старым):")
books_sorted = session.query(Book).order_by(Book.year.desc()).all()
for book in books_sorted:
    print(f"{book.title} ({book.year})")

print("\nКниги после 1950 года:")
books_after_1950 = session.query(Book).filter(Book.year > 1950).all()
for book in books_after_1950:
    print(f"{book.title} ({book.year})")

print("\nАвтор по имени 'Пушкин Александр':")
author = session.query(Author).filter(Author.name == "Пушкин Александр").first()
print(f"{author.name}, {author.birth_year} г.р.")

print("\nКоличество книг:")
count = session.query(func.count(Book.id)).scalar()
print(f"Всего книг: {count}")

print("\nПервые 3 книги по алфавиту:")
first_three = session.query(Book).order_by(Book.title).limit(3).all()
for book in first_three:
    print(f"{book.title} ({book.year})")

session.close()
