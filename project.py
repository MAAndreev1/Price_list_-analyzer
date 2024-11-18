import os


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0


    def load_prices(self, file_path='./price_lists'):
        """
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.

            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена
                
            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        """
        names = ['товар', 'название', 'наименование', 'продукт']
        prices = ['розница', 'цена']
        weights = ['вес', 'масса', 'фасовка']

        # Сканирование папки на наличие необходимых файлов
        for root, directories, files in os.walk(file_path):
            for file in files:
                if file.find('price') != -1:

                    # Открытие и чтение файла
                    with open(f'{root}/{file}', 'r', encoding="utf-8") as csv_file:
                        lines = [_line.strip().split(',') for _line in csv_file]

                        # Определение положения столбцов
                        for _i in names:
                            if _i in lines[0]:
                                name = lines[0].index(_i)
                        for _i in prices:
                            if _i in lines[0]:
                                price = lines[0].index(_i)
                        for _i in weights:
                            if _i in lines[0]:
                                weight = lines[0].index(_i)

                        # загрузка данных
                        for _line in lines[1:]:
                            values = int(_line[price]) / int(_line[weight])
                            self.data.append([_line[name].lower(), _line[price], _line[weight], file, round(values, 2)])
                        self.data = sorted(self.data, key=lambda x: x[4])


    def export_to_html(self, file_name='output.html'):
        """
            Выгружает все данные в html файл.
        """
        _number = 0
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        # Формирование необходимого текста
        for _i in self.data:
            _number += 1
            result += ('<tr>'
                       f'<td>{_number}</td>'
                       f'<td>{_i[0]}</td>'
                       f'<td>{_i[1]}</td>'
                       f'<td>{_i[2]}</td>'
                       f'<td>{_i[3]}</td>'
                       f'<td>{_i[4]}</td>'
                       '</tr>\n')

        # Запись необходимого текста в заданный html файл
        with open(file_name, "w", encoding="utf-8") as html_file:
            html_file.write(result)

    def find_text(self, text):
        """
            Получает текст и возвращает список позиций, содержащий этот текст в названии продукта.
        """
        result = []
        for _line in self.data:
            if _line[0].find(text.lower()) != -1:
                result.append(_line)
        return result


pm = PriceMachine()
pm.load_prices()
pm.export_to_html()

while True:
    i = input('Введите текст для поиска >>> ')
    number = 0

    if i == 'exit':
        print('Работа программы завершена.')
        break
    else:
        print(f'{"№":4} {"Наименование":50} {"Цена":5} {"Вес":5} {"Файл":15} {"Цена за кг.":10}')
        for line in pm.find_text(i):
            number += 1
            print(f'{str(number):4} {line[0]:50} {line[1]:5} {line[2]:5} {line[3]:15} {line[4]:10}')
        print()
