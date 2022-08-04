Цей темплейт використовується для розробки Telegram ботів з використанням бібліотеки [`aiogram v3.0+`]

### Для того, щоб почати використовувати:
1. Скопіюйте `.env.dist` в `.env` i заповніть необхідні дані.
2. Створіть нові хендлери.
3. **Docker:**
   1. Можете одразу запускати проєкт із Docker, а якщо в вас його немає, то [завантажте, та встановіть](https://docs.docker.com/get-docker/).
   2. Запустіть проєкт з команди `docker-compose up`
4. **Без Docker:**
   1. Створіть [venv](https://docs.python.org/3/library/venv.html)
   2. Встановить залежності із requirements.txt: `pip install -r requirements.txt`
   3. Запустіть проєкт з команди `python3 bot.py`