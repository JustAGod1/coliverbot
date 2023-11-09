# Инструкция по запуску бота

Не забыть перетащить .env со всеми нужными переменными

Запуск бота (указать флаг -d для запуска в фоне):
    
```bash
docker compose up --force-recreate --build
```

Перезапустить бота:

```bash
docker compose restart
```

Остановить бота:

```bash
docker compose stop
```

Помня, что виндоводы меняют "$(pwd)" на "${PWD}", инструкция как перетащить все из одного инстанса бд в другой:

Запаковать все внутренности вольюма бд в архив:

```bash
docker run --rm -v coliver_bot_pgdata:/dbdata -v $(pwd):/backup alpine tar cvf /backup/backup.tar /dbdata
```

Перетащить backup.tar из корневой папки проекта исходного инстанса (например, локального) в корневую папку проекта принимающего инстанса (например, удаленного)

Распаковать из архива в вольюм бд:

```bash
docker run --rm -v coliver_bot_pgdata:/dbdata -v $(pwd):/backup alpine ash -c "cd /dbdata && tar xvf /backup/backup.tar --strip 1"
```

# Особые благодарности 

Особое спасибо @JustAGod1 за неоценимую поддержку
