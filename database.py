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
INSERT OR REPLACE INTO
  figures (name, description, photo)
VALUES
  ('Модель Голова и плечи (head and shoulders)', 'Это классическая графическая модель разворота тренда. Эта модель состоит из трех последовательных пиков:средний пик (так называемая «голова») самый высокий;левый и правый пики (так называемые плечи) примерно равны друг другу и ниже среднего пика.', 'figures/6440bbcd-1ba1-4b21-a22c-9241028df85f.jfif'),
  ('Прямоугольник', 'Эта графическая фигура на графике представляет собой консолидацию цены в преддверии продолжения определенного тренда в первоначальном направлении.', 'figures/1a59c347-2c23-44f0-8931-094113036c90.jfif'),
  ('Вымпел', 'Это паттерн продолжения, который используется трейдерами для прогнозирования предстоящих рыночных движений. Этот паттерн похож на фигуру треугольник, но между ними есть ряд важных отличий.', 'figures/ea899cea-e471-47e6-9f5d-cf2d900ac08d.jfif'),
  ('Флаг', 'Это паттерн продолжения, который используется трейдерами для прогнозирования предстоящих рыночных движений. Этот паттерн похож на фигуру треугольник, но между ними есть ряд важных отличий.', 'figures/49bfe9af-ec5a-471a-ac4d-8fd7c38e2c97.jfif'),
  ('Канал', 'Это графическая модель (паттерн), также известная как параллельный канал или равноудаленный канал, которая состоит из двух параллельных линий, которые соединяют последовательные максимумы и минимумы и содержат цены между ними.', 'figures/995f892c-36e6-4ecf-a083-31f8d8c61819.jfif'),
  ('Двойная вершина', 'Это медвежий разворотный паттерн, который сигнализирует об окончании восходящего тренда. Он образован двумя ценовыми максимумами, образующимися на одном уровне, и линией выреза, которая выступает в качестве локальной поддержки.', 'figures/1f52ddb9-3b70-4d81-b297-682639fbf1df.jfif'),
  ('Двойное дно', 'Это бычий паттерн разворота на свечном графике, также может быть виден на диаграммах и даже линейных графиках. Его также называют зеркальным отражением паттерна двойной вершины (М-образная форма), который является медвежьим паттерном разворота (двойная вершина).', 'figures/8e812fb2-c7e4-4a06-a9dd-3043fdf60a46.jfif'),
  ('Восходящий канал', 'Это графическая модель, состоящая из двух параллельных наклонных восходящих линий. Она появляется, когда на графике есть более высокие максимальные колебания и более низкие минимальные колебания.', 'figures/f530802c-59f2-4477-9b6e-59b02ab9fbad.jfif'),
  ('Восходящий треугольник', 'Фигура технического анализа, которая предвещает рост цены. Восходящий треугольник — фигура роста. Это значит, что независимо от того, какая была «погода» перед фигурой, после завершения и подтверждения фигуры, цена на финансовый инструмент идет вверх.', 'figures/895da2fd-3dc5-4a86-a398-1eb09bc041f3.jfif'),
  ('Нисходящий треугольник', 'Фигура технического анализа «нисходящий треугольник» предвещает падение цены, независимо от предшествующего тренда.Но стоит помнить, что в большинстве случаев, нисходящий треугольник формируется после нисходящего тренда. Поэтому его также могут относить к фигурам продолжения тренда.', 'figures/a01a46ae-f2b0-45c4-a363-3200a66c3260.jfif'),
  ('Восходящий клин', 'Фигура, которая образуется на колеблющемся графике, и обуславливается сужающейся амплитудой. Если провести прямые линии по максимумам и минимумам соответственно, то две прямые будут образовывать воображаемый угол, который будет сужаться с течением времени.', 'figures/58969fec-677d-4569-bc58-5ee3aad19ec0.jfif'),
  ('Нисходящий клин', 'Фигура разворота. Это значит, что невозможно точно сказать, куда пойдет цена пока фигура не завершена. Обычно, цена после фигуры направляется вверх, таким образом разворачивая цену, но так бывает далеко не всегда.', 'figures/6e173132-b37f-48c1-8154-418367b7e1a5.jfif'),
  ('Пин Бар', 'Фигура разворота,модель из трех баров (свечей) средняя из которых отличается маленьким телом и одной короткой тенью или ее отсутствием. Это значит, что невозможно точно сказать, куда пойдет цена пока фигура не завершена. Обычно, цена после фигуры направляется вверх, таким образом разворачивая цену, но так бывает далеко не всегда.', 'figures/307d0c22-7f4a-4d91-a067-bb374800ed1c.jfif'),
  ('Симметричный треугольник', 'Фигура появляется в то время, когда цена достигает более низких максимумов и более высоких минимумов. Обычно это означает, что ни у покупателей, ни у продавцов не получается взять рынок под контроль, из-за чего цена колеблется внутри треугольника.', 'figures/b45256f1-6361-4f99-a07e-e33f6d6d678f.jfif'),
  ('Три Индейца', 'Модель графического анализа. Ее суть заключается в поиске на графике линии сопротивления или поддержки. При этом, цена должна трижды коснутся этой прямой перед тем, как получится сигнал.Данный паттерн является одним из наиболее простых в графическом анализе. Тем не менее, он также требует определенных навыков в построении трендовых линий для того, чтобы принимать правильные торговые решения.', 'figures/cae463cb-ffb7-4808-9fc5-1ffc3e6169a3.jfif');
"""

select_definitions = """SELECT name, description from definitions"""
select_figures = """SELECT name, description from figures"""
select_photo = """SELECT photo from figures where name=?"""
select_number_of_definitions = """SELECT COUNT(name) from definitions"""
select_number_of_figures = """SELECT COUNT(name) from figures"""
select_last_library_id = """SELECT last_message_id from users WHERE id = ?"""
select_user_on_page = """SELECT on_page from users WHERE id = ?"""

delete_figures = """DELETE FROM figures"""
delete_comment = """DELETE FROM users WHERE id = ?"""

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
def get_definition_description(name):
    try:
        for definition in definitions:
            if definition[0] == name:
                return definition[1]
        return 'No description yet('
    except IndexError:
        return 'No description yet('


# returns description of the figure
def get_figure_description(name):
    try:
        for figure in figures:
            if figure[0] == name:
                return figure[1]
        return 'No description yet('
    except IndexError:
        return 'No description yet('


# returns description of the figure
def get_image_of_figure(name):
    try:
        return execute_param_read_query(connection, select_photo, (name,))[0][0]
    except IndexError and TypeError:
        return 'no way'

