"""
version 0.2
"""
from time import sleep
import telebot
import settings as sett
from uploading_database import *

bot = telebot.TeleBot(sett.TOKEN)
# data = None
permission_p = True
previous_time = datetime.datetime(1991, 1, 1, 0, 0, 0)
masiv = []
story_count = {}
input_data = {}
input_data_dict = {}
text_1 = """
1)Сканируем сайт
2)Обробатываем полученую информацию
3)Сохраняем данные в базу
4)Бот показывает изменения
"""


def price(pr):
    """pr['mts',10]"""
    company_name = pr[0]
    company_pr = pr[1]
    company = company_name + str(company_pr)
    current_time = datetime.datetime.today()

    if story_count.get(company):
        time_last_check = story_count.get(company)[0]
        time_difference = current_time - time_last_check
        if time_difference.total_seconds() >= 3600:
            data = start(company_name, company_pr)
            story_count[company][0] = current_time
            story_count[company][1] = data
        else:
            data = story_count.get(company)[1]
    else:
        data = start(company_name, company_pr)
        story_count.update({company: [current_time, data]})

    data = f'*** {current_time} ***\n\n' \
        f'❗️Товары дополнительно фильтруются: скидка> 2000р, цена товара <80000р.\n\n' \
        f'{data}' \
        f'Конец❤️'

    # if len(data) > 4000:
    #     data = data.replace('\n\n', '\n')
    # if len(data) > 4000:
    #     data = data[0:4000:1]
    #     data = f'{data}\n\n*** К сожалению не влезло... ***'
    return data


@bot.message_handler(content_types=['text'])
def second(message):
    shop = {'МТС': 'mts', 'МВИДЕО': 'mvideo', 'ДНС': 'dns', 'ЭЛЬДОРАДО': 'eldorado'}
    id_user = message.from_user.id

    if message.text == "/start" or message.text == "Главное Меню":
        key = telebot.types.ReplyKeyboardMarkup(True, False)
        key.row('Показать скидосики')
        key.row('Как это работает?!')
        bot.send_message(message.from_user.id, "Привет ,я бот для показа скидок в Мвидео 😍", reply_markup=key)

    if message.text == "Назад":
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row('Показать скидосики')
        keyboard.row('Как это работает?!')
        bot.send_message(message.from_user.id, "Выбери действие☺️", reply_markup=keyboard)

    elif message.text == "Как это работает?!":
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row('Показать скидосики')
        keyboard.row('Назад')
        bot.send_message(message.from_user.id, text_1, reply_markup=keyboard)

    elif message.text == "Показать скидосики" or message.text == "Назад к выбору магазина":
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row('МВИДЕО', 'МТС')
        keyboard.row('ДНС', 'ЭЛЬДОРАДО')
        keyboard.row('Назад')
        bot.send_message(message.from_user.id, "Выбери магазин☺️", reply_markup=keyboard)

    for i in shop.keys():
        rut = message.text.find(i) >= 0
        if message.text == i or rut:
            message_shop = shop.get(i)
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            keyboard.row('>15%<20%', '>20%<30%')
            keyboard.row('Показать все скидки > 30%')
            keyboard.row('Назад к выбору магазина')
            input_data_dict[id_user] = [message_shop, '', i]
            bot.send_message(message.from_user.id, 'Выбери нужный процент☺️', reply_markup=keyboard)

    discount_percentage = {'>15%<20%': 1520, '>20%<30%': 2030, 'Показать все скидки > 30%': 30}
    for i in discount_percentage.keys():
        if message.text == i:
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            input_data_dict[id_user][1] = discount_percentage.get(i)
            keyboard.row('Назад к выбору процента ' + input_data_dict[id_user][2])
            keyboard.row('Назад к выбору магазина')
            data = price(input_data_dict[id_user])

            step = 4050
            for p in range(0, len(data), step):
                data_rez = data[p:p + step:1]
                bot.send_message(message.from_user.id, data_rez, reply_markup=keyboard)


try:
    bot.polling(none_stop=True)
except:
    sleep(15)
    print('Ошибка')
    pass
