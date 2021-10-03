from uploading_database import *

print('Программа для выгрузки скидок из базы данных\n')
while True:
    action_1 = input('Выбери магазин:\n'
                     '1)МВИДЕО\n'
                     '2)МТС\n'
                     '3)ЭЛЬДОРАДО\n'
                     '4)ДНС\n'
                     '5)Выйти\n')
    if action_1 == '5':
        break
    else:
        action_2 = int(input('Укажи процент скидки (15):\n'))

    if action_1 == '1':
        data = start('mvideo', action_2)
    elif action_1 == '2':
        data = start('mts', action_2)
    elif action_1 == '3':
        data = start('eldorado', action_2)
    elif action_1 == '4':
        data = start('dns', action_2)
    else:
        data = 'Выбери из предложеного...'
    print(data)
