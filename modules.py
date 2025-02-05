from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, BigInteger
from tabulate import tabulate
from connect import engine

from colorama import init, Fore, Style

init()

#with engine.connect() as connection:
#	result = connection.execute(text("select 'hello world!', 'yesss'"))
#	print(result.scalar())
"""
metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("user_id", BigInteger),
    Column("last_name", String(30))
)

address_table = Table(
    "addresses",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("user_id", ForeignKey('users.id')),
    Column("address", String(100))
)
"""


# создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass


# создаем модель, объекты которой будут храниться в бд
class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=False)


class Accounts(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    user_name = Column(String, ForeignKey('people.user_name'), nullable=False)
    account_number = Column(String, unique=True)
    balance = Column(BigInteger, nullable=False, default=100)
    is_deleted = Column(String, default='False')


def create_examples(p_engine):
    # Добавление данных - create
    # создаем сессию подключения к бд
    # with Session(autoflush=False, bind=p_engine) as db:
    #     # создаем объект Person для добавления в бд
    #     tom = Person(name="Tom", age=38)
    #     db.add(tom)  # добавляем в бд
    #     db.commit()  # сохраняем изменения
    #     print(tom.id)  # можно получить установленный id

    with Session(autoflush=False, bind=p_engine) as db:
        # добавляем два объекта
        bob = Person(user_name="1", last_name="1", password="1", age=1)
        sam = Person(user_name="Sam", last_name="samson", password="samichon", age=25)
        db.add(bob)
        #db.add(sam)
        db.commit()

    # with Session(autoflush=False, bind=p_engine) as db:
    #     alice = Person(name="Alice", age=33)
    #     kate = Person(name="Kate", age=28)
    #     db.add_all([alice, kate])
    #     db.commit()

    #with Session(autoflush=False, bind=p_engine) as db:
    #bob_acc = Accounts(user_id=1, user_name="Bob", account_number="1111")
    #sam_acc = Accounts(user_id=2, user_name="Sam", account_number="2222")
    #db.add(bob_acc)
    #db.add(sam_acc)
    #db.commit()


def select_all(p_engine, name_of_table):
    with Session(autoflush=False, bind=p_engine) as db:
        try:
            first = db.query(name_of_table).filter(name_of_table.id == 1).first()
        except BaseException as e:
            print(e)
        if first:
            return first

        else:
            return None


def main_menu(username, p_engine):
    car = p_engine
    print("Приветствую ", username, "!!!")
    while True:
        iko = "│" + " " * 21 + "6. Получить список всех пользователей в базе" + " " * 8 + "│"
        print(Fore.CYAN + "╭" + "─" * (len(iko) - 2 - 2) + "╮")
        print("│" + " " * 11 + "Главное меню:" + " " * (len(iko) - 28) + "│")
        print("│" + " " * 11 + "1. Получить список счетов" + " " * (len(iko) - 40) + "│")
        print("│" + " " * 11 + "2. Создать счет" + " " * (len(iko) - 30) + "│")
        print("│" + " " * 11 + "3. Удалить счет" + " " * (len(iko) - 30) + "│")
        print("│" + " " * 11 + "4. Снять деньги со счета" + " " * (len(iko) - 39) + "│")
        print("│" + " " * 11 + "5. Перевести деньги на другой счет" + " " * (len(iko) - 45 - 4) + "│")
        print("│" + " " * 11 + "6. Получить список всех пользователей в базе" + " " * 16 + "│")
        print("│" + " " * 11 + "0. Выход" + " " * (len(iko) - 23) + "│")
        print("╰" + "─" * (len(iko) - 2 - 2) + "╯")
        print(11 * " " + "|", end='')
        choice = input("Выберите действие|\n" + " " * 11 + "─" * 19 + "\n" + " " * 20)
        print()

        if choice == "1":
            get_account_list(username, car)

        if choice == "2":
            add_account(username, car)

        if choice == "3":
            delete_account(username, car)

        if choice == "4":
            withdraw_many(username, car)

        if choice == "5":
            transfer_many(username, car)

        if choice == "6":
            get_all_users_and_accounts(car)

        if choice == "0":
            break


def add_user(p_engine):
    get_name = input("Введите имя пользователя:")
    get_last_name = input("Введите свою фамилию:")
    get_password = input("Введите свой пароль:")
    get_age = int(input("Сколько вам лет:"))
    with Session(autoflush=False, bind=p_engine) as db:
        new_user = Person(user_name=get_name, last_name=get_last_name, password=get_password, age=get_age)
        db.add(new_user)
        db.commit()


def login_user(p_engine):
    car = p_engine
    get_name = input("Введите имя пользователя:")
    get_password = input("Введите свой пароль:")
    with Session(autoflush=False, bind=p_engine) as db:
        user = db.query(Person).filter_by(user_name=get_name, password=get_password).first()
        if user:
            print(Fore.GREEN + "Вход выполнен успешно!")
            main_menu(get_name, car)
        else:
            print(Fore.RED + "Неверное имя пользователя или пароль.")


def get_account_list(username, p_engine):
    with Session(autoflush=False, bind=p_engine) as db:
        accounts = db.query(Accounts).filter_by(user_name=username, is_deleted='False').all()
        if accounts:
            print("Список счетов пользователя:", username)
            for account in accounts:
                print(
                    Fore.GREEN + f"Номер счета: {str(account.account_number).ljust(20)} Баланс счета: {account.balance}")
        else:
            print(Fore.RED + "У вас пока что нет счетов!!!")


def add_account(username, p_engine):
    get_account_number = input("Введите номер нового счета:")
    try:
        with Session(autoflush=False, bind=p_engine) as db:
            id_person = db.query(Person).filter_by(user_name=username).first()
            new_account = Accounts(account_number=get_account_number, user_id=id_person.id, user_name=username)
            db.add(new_account)
            print(Fore.GREEN + "Вы успешно создали новый аккаунт!!!")
            db.commit()
    except BaseException as e:
        print(Fore.RED + "Похоже у нас уже есть счет с таким номером счета")


def delete_account(username, p_engine):
    get_account_number = input("Введите номер счета для удаления:")
    with Session(autoflush=False, bind=p_engine) as db:
        id_person = db.query(Accounts).filter_by(user_name=username, account_number=get_account_number,
                                                 is_deleted='False').first()
        if id_person:
            id_person.is_deleted = 'True'
            print(Fore.GREEN + "Счет успешно удалён!")
            db.commit()
        else:
            print(Fore.RED + "Счет не найден или же вы не имеете право на удаление этого счета!")


def withdraw_many(username, p_engine):
    get_account_number = input("Введите номер счета с которого вы бы хотели снять деньги:")
    get_num_withdraw = int(input("Сколько вы бы хотели снять:"))
    with Session(autoflush=False, bind=p_engine) as db:
        id_person = db.query(Accounts).filter_by(user_name=username, account_number=get_account_number,
                                                 is_deleted='False').first()
        if id_person:
            if id_person.balance > get_num_withdraw:
                id_person.balance = id_person.balance - get_num_withdraw
                print(Fore.GREEN + "Снятия было выполнено успешно!")
                db.commit()
            else:
                print(Fore.RED + "На счету меньше чем вы хотите снять!")
        else:
            print(Fore.RED + "Счет не найден или же вы не имеете право на снятие денег с этого счета!")


def transfer_many(username, p_engine):
    get_account_number = input("Введите номер счета отправителя:")
    get_account_number_2 = input("Введите номер счета получателя:")
    get_num_withdraw = int(input("Сколько вы бы хотели перевести:"))
    with Session(autoflush=False, bind=p_engine) as db:
        id_person = db.query(Accounts).filter_by(user_name=username, account_number=get_account_number,
                                                 is_deleted='False').first()
        id_person_2 = db.query(Accounts).filter_by(account_number=get_account_number_2, is_deleted='False').first()
        if id_person and id_person_2:
            if id_person.balance > get_num_withdraw:
                id_person.balance = id_person.balance - get_num_withdraw
                id_person_2.balance = id_person_2.balance + get_num_withdraw
                print(Fore.GREEN + "Перевод денег был выполнено успешно!")
                db.commit()
            else:
                print(Fore.RED + "На счету меньше чем вы хотите отправить!")
        else:
            print(Fore.RED + "Опс похоже вы что-то указали неверно!")


def get_all_users_and_accounts(p_engine):
    Session = sessionmaker(bind=p_engine)
    with Session(autoflush=False) as db:
        users_data = db.query(Person).all()
        if users_data:
            print(Fore.GREEN + "Таблица пользователей:")
            user_table = [[user.id, user.user_name, user.last_name, user.age] for user in users_data]
            print(tabulate(user_table, headers=["ID", "Логин пользователя(имя тоже)", "Фамилия", "Возраст"]))
        else:
            print(Fore.RED + "Таблица пользователей пуста!")

        accounts_data = db.query(Accounts).all()
        if accounts_data:
            print("\nТаблица счетов пользователей:")
            accounts_table = [[account.id, account.user_id, account.user_name, account.account_number, account.balance,
                               account.is_deleted] for account in accounts_data]
            print(tabulate(accounts_table,
                           headers=["ID счета", "ID владельца", "Логин Пользователя счета", "Номер счета", "Баланс",
                                    "Удалён или нет"]))
        else:
            print(Fore.RED + "Таблица счетов пользователей пуста!")
