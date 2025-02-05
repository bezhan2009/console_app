from sqlalchemy import create_engine
# db_url = 'postgresql://username:password@host:port/dbname'

good_question = int(input("Настроить подключение к базе данных(автоматически = 0 или в ручную = 1):"))

if good_question >= 1:
    db_name = input("Введите название вашей базы данных(по умолчанию = postgres):")
    if len(db_name) <= 0:
        print("Вставляем имя базы данных по умолчанию...")
        db_name = "postgres"

    user = input("Введите имя подключение (user) (по умолчанию = postgres):")
    if len(user) <= 0:
        print("Вставляем имя подключение по умолчанию...")
        user = "postgres"

    password = input("Введите пароль для подключение к базе данных:")

    port = input("Введите порт(по умолчанию = 5432):")
    if len(port) <= 0:
        print("Вставляем порт по умолчанию...")
        port = 5432
    else:
        port = int(port)

    host = input("Введите host подключение(по умолчанию = 127.0.0.1)")
    if len(host) <= 0:
        print("Вставляем host подключение по умолчанию...")
        host = "127.0.0.1"
else:
    db_name = "postgres"
    user = "postgres"
    password = "bezhan2009"
    port = "5432"
    host = "127.0.0.1"

db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(db_url, echo=False)
