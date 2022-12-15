# Develop
- перейдите в директорию с проектом
- добавьте виртуальное окружение Python
- установите дополнительные пакеты из requirements.txt
- создайте базу данных sqlite -  python manage.py migrate
- добавьте суперюзера - python manage.py ensure_admin
- запустите проект python manage.py runserver


## Запуск Celery для тестов
1. Зайдите в директорию fr_sender в двух отдельных терминальных окнах
2. Выполните в одном 
   - celery -A fr_sender worker -l INFO --pool=solo 
   - или celery -A fr_sender worker -l INFO --pool=prefork --concurrency=4
3. Выполните 
   - celery -A fr_sender beat -l INFO
4. Для запуска Celery вне оркестрации понадобится Redis
5. Если Docker Desktop запущен - в любом терминале сделайте 
   - docker pull redis
6. Откройте Docker Desktop - выберите образ redis, запустите его, укажите проброс портов 6379 в выпадающем меню Optional Settings -> Ports -> local host: 6379

# Kind of prod
- установите Docker Desktop
- перейдите в директорию с проектом
- выполните команду docker-compose up --build
- При первом запуске база данных будет заполняться сотрудниками,
 - проект доступен по адресу http://localhost:8000/