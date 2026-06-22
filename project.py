from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///library.db", echo=True)
print(engine)

metadata = MetaData()

authors = Table(
    "authors", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("birth_year", Integer),
)

books = Table(
    "books", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("year", Integer),
    Column("author_id", Integer, ForeignKey("authors.id")),
)

metadata.drop_all(engine)
metadata.create_all(engine)

conn = Session(bind=engine)

conn.execute(insert(authors), [
    {"name": "Булгаков Михаил", "birth_year": 1891},
    {"name": "Пушкин Александр", "birth_year": 1799},
    {"name": "Тургенев Иван", "birth_year": 1818},
])
conn.commit()

conn.execute(insert(books), [
    {"title": "Мастер и Маргарита", "year": 1967, "author_id": 1},
    {"title": "Собачье сердце", "year": 1925, "author_id": 1},
    {"title": "Евгений Онегин", "year": 1833, "author_id": 2},
    {"title": "Капитанская дочка", "year": 1836, "author_id": 2},
    {"title": "Отцы и дети", "year": 1862, "author_id": 3},
])
conn.commit()

print("\nВсе авторы:")
result = conn.execute(select(authors))
for row in result:
    print(row[1])

print("\nИзменение имени автора:")
conn.execute(
    update(authors).where(authors.c.name == "Тургенев Иван").values(name="И. С. Тургенев")
)
conn.commit()
row = conn.execute(select(authors).where(authors.c.id == 3)).fetchone()
print(f"Новое имя: {row[1]}")

print("\nУдаление книги:")
conn.execute(delete(books).where(books.c.title == "Капитанская дочка"))
conn.commit()
print("Удалена: Капитанская дочка")

print("\nВсе книги (от новых к старым):")
result = conn.execute(select(books).order_by(books.c.year.desc()))
for row in result:
    print(f"  {row[1]} ({row[2]})")

print("\nКниги после 1950 года:")
result = conn.execute(select(books).where(books.c.year > 1950))
for row in result:
    print(f"  {row[1]} ({row[2]})")

print("\nАвтор по имени 'Пушкин Александр':")
result = conn.execute(select(authors).where(authors.c.name == "Пушкин Александр"))
row = result.fetchone()
print(f"  {row[1]}, {row[2]} г.р.")

print("\nКоличество книг:")
result = conn.execute(select(func.count(books.c.id)))
print(f"  Всего книг: {result.scalar()}")

print("\nПервые 3 книги по алфавиту:")
result = conn.execute(select(books).order_by(books.c.title).limit(3))
for row in result:
    print(f"  {row[1]} ({row[2]})")

conn.close()
