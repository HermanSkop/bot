import sqlite3
from _sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


connection = create_connection('db.sqlite')

create_definitions_table = """
CREATE TABLE IF NOT EXISTS definitions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT
);
"""
create_figures_table = """
CREATE TABLE IF NOT EXISTS definitions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  photo 
);
"""

create_defs = """
INSERT INTO
  definitions (name, description)
VALUES
  ('Ферма', 'множественное оборудование для майнинга криптовалют, объединенных в одну сеть'),
  ('Тело свечи', 'термин, демонстрирующий промежуток между ценами открытия и закрытия временного периода'),
  ('Тень свечи', 'показатель минимального и максимального курса криптовалюты во временном промежутке'),
  ('Сатоши Накамото', 'псевдоним предполагаемого создателя первой в мире криптовалюты биткоин'),
  ('Разворот', 'состояние, когда настроение рынка меняется на противоположную сторону'),
  ('Газ', 'комиссия майнерам для выполнения транзакции в сети Эфире'),
  ('Вторичка', 'покупка NFT из вторых рук в меркетплейсе'),
  ('Листинг', 'выставление NFT на продажу в маркетплейсе'),
  ('Делистинг', 'снятие NFT с продажи'),
  ('Рар, рарность', 'степень редкости NFT в коллекции. Чем реже NFT, тем она дороже'),
  ('Минт', 'покупка NFT на сайте создателей коллекции'),
  ('Вайт лист', 'список человек, имеющих право на минт NFT в числе первых'),
  ('Паблик сейл', 'открытие продаж для всех желающих'),
  ('Ревил', 'открытие вашего NFT. Почти все коллекции скрыты, чтобы избежать массового слива в первые дни листинга'),
  ('холд', 'хранение NFT в долгосрок');
"""

# Created_table = execute_read_query(connection, create_definitions_table)
Inserted_values = execute_read_query(connection, create_defs)

select_definitions = 'SELECT name, description from definitions'
select_number_of_definitions = 'SELECT COUNT(name) from definitions'

definitions = execute_read_query(connection, select_definitions)
number_of_definitions = execute_read_query(connection, select_number_of_definitions)[0][0]
delete_comment = "DELETE FROM definitions WHERE id = 1"


# returns description of the definition
def get_description(name):
    for definition in definitions:
        if definition[0] == name:
            return definition[1]
    return 'No description yet('