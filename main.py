
from modules import *
from connect import *
import sys

init()



# ...

try:
    init()
    Base.metadata.create_all(bind=engine)

    view_for_bugs = select_all(engine, Person)
    view_for_bugs_2 = select_all(engine, Accounts)
    if not view_for_bugs and not view_for_bugs_2:
        create_examples(engine)
except BaseException as e:
    print(e)

while True:
    get_question = int(input("Вы хотите войти или же пройти регистрацию(Регистрация = 0 , Вход = 1, Автоматически Вход = 2 или Завершение программы >= 3):"))
    if get_question == 0:
        add_user(engine)
    if get_question == 1:
        login_user(engine)
    if get_question == 2:
        main_menu("1", engine)
    else:
        print("Выход")
        break
