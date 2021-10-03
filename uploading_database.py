# ----------------
# version 0.4 для мвидео
# ________________
import datetime
import models as db_universal

shop = {'mvideo': db_universal.Mvm,
        'dns': db_universal.Dns,
        'mts': db_universal.Mts,
        'eldorado': db_universal.Eld}


class ParserFile:
    def __init__(self, table_shop):
        self.price_db = {}
        self.table_shop = table_shop

    def unloading_from_the_database(self):
        """
        Выгружаем данные из базы даннхы для анализа
        """
        self.price_db.clear()
        self.price_db = {}
        with db_universal.db:
            # for data in self.db.PriceParser.select().where(self.db.PriceParser.date_recording == dt):
            for d in self.table_shop.select():
                self.price_db[d.name] = [d.price_old, d.price_new, d.date_recording, d.display]
            print(self.price_db)

    def search_for_discounts(self, discount_rang):
        """
        Фильтрация результатов
        2)Анализ данных
        3)Вывод отфильтрованных данных
        """
        data_str = ''
        for name, value in self.price_db.items():
            try:
                price_1, price_2, display = int(value[0]), int(value[1]), int(value[3])
                discount = price_1 - price_2

                if price_2 != 0:
                    if price_2 < 80000 and discount > 2000:
                        percentage_price_1 = (price_2 / price_1 * 100 - 100) * (-1)
                        percentage_input = discount_rang[0]
                        if percentage_price_1 >= percentage_input:
                            if percentage_price_1 <= discount_rang[1]:
                                percent = int((price_2 / price_1 - 1) * 100)
                                data = f"{name} {price_2}Р {percent}% \n\n"
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
        with self.table_shop.table_shop:
            for key, value in data.items():
                name = key
                display = value
                product = self.table_shop.PriceParser.get(self.table_shop.PriceParser.name == name)
                product.display = display
                product.save()


def start(pr1, pr2):
    """
    :param pr1:Название компании (mvideo)
    :param pr2:Процент скидки (1520) - от 15 - 20%
    """

    for key, value in shop.items():
        if pr1 == key:
            mp = ParserFile(shop[key])
            mp.unloading_from_the_database()
            data = mp.search_for_discounts(pr2)
        else:
            data = 'Нет данных для заданных параметров'
        return data


start(pr1='mvideo', pr2=[15, 20])
