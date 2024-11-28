from aiogram import Bot, types, Dispatcher, executor
from python_weather import Client,IMPERIAL


def read_token_from_file(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()  # Удаляем лишние пробелы и символы новой строки


# Инициализация бота
token_file = 'token.txt'  # Имя файла с токеном
bot_token = read_token_from_file(token_file)  # Считываем токен
bot = Bot(token=bot_token)  # Замените "YOUR_BOT_TOKEN" на ваш токен
dp = Dispatcher(bot)

# Обработка команды /weather
@dp.message_handler(commands=['weather'] or ['weather@name_bot'])
# команда weather или weather@"name_bot" для работы с ботом в чатах (нужно вставить имя)
async def get_weather(message: types.Message):
    city = ["Joensuu","Санкт-Петербург","Saratov"]

    if not city:
        await message.answer("Пожалуйста, укажите город после команды /weather.")
        return

    try:
        client = Client(format=IMPERIAL, locale="ru-RU")
        for city_name in city:
            weather = await client.find(city_name)
            # Получаем температуру в Фаренгейтах и преобразуем в Цельсии
            cel = round((weather.current.temperature - 32) / 1.8)

            resp_msg = f"Погода в {weather.location_name}:\n"
            resp_msg += f"Текущая температура: {cel}°C\n"
            resp_msg += f"Состояние: {weather.current.sky_text}\n"

            await message.answer(resp_msg)
        await client.close()
    except Exception as e:
        await message.answer("Не удалось получить данные о погоде. Пожалуйста, проверьте название города.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
