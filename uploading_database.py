# ----------------
# version 0.4 для мвидео
# ________________
import datetime
import models1 as db1  # mvideo
import models2 as db2  # mts
import models3 as db3  # dns
import models4 as db4  # eldorado


class ParserFile:
    def __init__(self, db):
        self.price_db = {'Наименование': [], 'Цена': [], 'Цена2': [], 'дата': [], 'Вывод': []}
        self.db = db

    def unloading_from_the_database(self):
        """
        Выгружаем данные из базы даннхы для анализа
        """
        self.price_db.clear()
        self.price_db = {'Наименование': [], 'Цена': [], 'Цена2': [], 'дата': [], 'Вывод': []}
        dt = datetime.date.today()
        with self.db.db:
            for data in self.db.PriceParser.select().where(self.db.PriceParser.date_recording == dt):
                # for data in self.db.PriceParser.select():
                self.price_db['Наименование'].append(data.name)
                self.price_db['Цена'].append(data.price_old)
                self.price_db['Цена2'].append(data.price_new)
                self.price_db['дата'].append(data.date_recording)
                self.price_db['Вывод'].append(data.display)

    def search_for_discounts(self, pr1=20):
        """
        Фильтрация результатов
        2)Анализ данных
        3)Вывод отфильтрованных данных
        """
        data_str = ''
        display_dict = {}
        stop = len(self.price_db['Наименование'])
        for i in range(0, stop):
            try:
                name = self.price_db['Наименование'][i]
                price_1 = int(self.price_db['Цена'][i])
                price_2 = int(self.price_db['Цена2'][i])
                display = int(self.price_db['Вывод'][i])
                discount = price_1 - price_2

                if pr1 == 30:
                    percentage_start = 30
                    percentage_limiter = 1000
                elif pr1 == 1520:
                    percentage_start = 15
                    percentage_limiter = 20
                elif pr1 == 2030:
                    percentage_start = 20
                    percentage_limiter = 30

                if price_2 != 0:
                    if price_2 < 80000 and discount > 2000:
                        percentage_price_1 = (price_2 / price_1 * 100 - 100) * (-1)
                        percentage_input = percentage_start
                        if percentage_price_1 >= percentage_input:
                            if percentage_price_1 <= percentage_limiter:
                                percent = int((price_2 / price_1 - 1) * 100)
                                data = f"{name} {price_2} {percent}% \n\n"
                                data_str = data_str + data
                                # display_dict.update({name: display + 1})
            except Exception:
                print('Ошибка')
        # self.updating_the_database_display(display_dict)
        return data_str

    def updating_the_database_display(self, data):
        """
        Запись просмотров в базу данных
        """
        with self.db.db:
            for key, value in data.items():
                name = key
                display = value
                product = self.db.PriceParser.get(self.db.PriceParser.name == name)
                product.display = display
                product.save()


def start(pr1, pr2):
    """
    :param pr1:Название компании
    :param pr2:Процент скидки
    """
    shop = {'mvideo': db1, 'mts': db2, 'dns': db3, 'eldorado': db4}
    data = 'Нет данных для заданных параметров'
    for i in shop.keys():
        if pr1 == i:
            shop_db = shop.get(i)
            db_price = ParserFile(shop_db)
            db_price.unloading_from_the_database()
            data = db_price.search_for_discounts(pr2)
    return data
