# salary_fork

Показывает статистику по самым популярным языками программирования с сайтов [hh](https://hh.ru/) и [superjob](https://www.superjob.ru/). В статистику входят три числа: 1) общее число вакансий, 2) число вакансий с указанной зарплатой, 3) средняя зарплата. [Страница с используемым API в HH](https://github.com/hhru/api), [страница с используемым API в SuperJob](https://api.superjob.ru/).

# Установка

Скачать гит репозиторий. В корне репозитория создать файл `.env` и поместить внутрь следующую строку:
1. `SUPERJOB_API_SECRET_KEY=ваш_токен`, где заменить строку `ваш_токен` на ваш уникальный токен с сайта [Superjob](https://api.superjob.ru/).

# Требования к использованию

Требуется [Python](https://www.python.org/downloads/) версии 3.7 или выше и установленный [pip](https://pip.pypa.io/en/stable/getting-started/). Для установки необходимых зависимостей используйте команду:  
1. Для Unix/macOs:
```commandline
python -m pip install -r requirements.txt
```
2. Для Windows:
```commandline
py -m pip download --destination-directory DIR -r requirements.txt
```