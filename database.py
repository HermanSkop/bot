import sqlite3
from _sqlite3 import Error


def default_query_run(insert_statement):
    execute_read_query(connection, insert_statement)


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_param_query(connection, query, params):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_param_read_query(connection, query, params):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        connection.commit()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
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
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    on_page INTEGER,
    last_message_id INTEGER
);
"""
create_figures_table = """
CREATE TABLE IF NOT EXISTS figures (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  photo TEXT
);
"""

insert_defs = """
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
insert_figures = """
INSERT INTO
  figures (name, description)
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

select_definitions = """SELECT name, description from definitions"""
select_figures = """SELECT name, description from figures"""
select_number_of_definitions = """SELECT COUNT(name) from definitions"""
select_number_of_figures = """SELECT COUNT(name) from figures"""
select_last_library_id = """SELECT last_message_id from users WHERE id = ?"""
select_user_on_page = """SELECT on_page from users WHERE id = ?"""

delete_comment = """DELETE FROM users WHERE id = ?"""

# execute_param_query(connection, delete_comment, (872759497, ))

update_user = """INSERT OR REPLACE INTO users (id, on_page, last_message_id) VALUES (?, ?, ?)"""

definitions = execute_read_query(connection, select_definitions)
figures = execute_read_query(connection, select_figures)
number_of_definitions = execute_read_query(connection, select_number_of_definitions)[0][0]
number_of_figures = execute_read_query(connection, select_number_of_figures)[0][0]


def update_library_page(user_id, page_number):
    data = None
    try:
        data = (user_id, page_number, execute_param_read_query(connection, select_last_library_id, (user_id,))[0][0])
    except IndexError:
        data = (user_id, page_number, 0)
    finally:
        execute_param_query(connection, update_user, data)


def update_last_library_id(user_id, message_id):
    data = None
    try:
        data = (user_id, execute_param_read_query(connection, select_user_on_page, (user_id,))[0][0], message_id)
    except IndexError:
        data = (user_id, 0, message_id)
    finally:
        execute_param_query(connection, update_user, data)


def get_library_page(user_id):
    try:
        data = (user_id,)
        return execute_param_read_query(connection, select_user_on_page, data)[0][0]
    except IndexError as e:
        print(f'{e} in get_library_page')
        return None


def get_last_library_id(user_id):
    try:
        data = (user_id,)
        return execute_param_read_query(connection, select_last_library_id, data)[0][0]
    except IndexError as e:
        print(f'{e} in get_library_page')
        return None


# returns description of the definition
def get_description(name):
    for definition in definitions:
        if definition[0] == name:
            return definition[1]
    return 'No description yet('
