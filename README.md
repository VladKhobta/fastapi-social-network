# fastapi-social-network

Интсрукции по установке:

1. Скачать папку проекта (любым удобным способом).
2. Открыть терминал в папке проекта.
3. Для управления зависимостями и в качестве виртуальной среды использовался пакет pipenv. Если он не установлен:
```
pip install pipenv
```
4. Создать виртуальное окружение и установить пакеты из Pipfile.
```
pipenv shell
pipenv install
```
5. Переименовать файл .env.example в .env и поменять изменить значения переменных на ваши.
6. Создать пустую базу данных:
    1. Открыть оболочку python.
    ```
    python
    ```
    2. В оболочке python^
    ```python
    >>> from backend.db.database import engine
    >>> from backend.db.models.base import Base
    >>> Base.metadata.create_all(engine)
    ```
    3. Закрыть оболочку python.
    ```python
    >>> exit()
    ```
7. Все готово для работы. Запуск приложения.(Мы все еще должны быть с запущенной виртуальной средой pipenv из п. 4)
```
python -m backend
```
