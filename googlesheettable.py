import gspread
from cofig import CREDENTIALS_FILENAME, SPREADSHEET_URL

class Getlists:
    def __init__(self, spreadsheet_url=SPREADSHEET_URL):
        self.account = gspread.service_account(filename=CREDENTIALS_FILENAME)
        self.spreadsheet = self.account.open_by_url(spreadsheet_url)

    def get_topics(self):
        # Получаем список листов
        sheets = self.spreadsheet.worksheets()
        # Возвращаем список названий листов
        return [sheet.title for sheet in sheets]

    def get_book_data(self, sheet_id):
        """Возвращает список словарей с данными о книгах из листа с указанным ID.

        Args:
            sheet_id: ID листа (число перед символом '_').

        Returns:
            Список словарей вида [{'title': 'Название книги', 'link': 'Ссылка на скачивание'}, ...]
        """

        for sheet_name in self.get_topics():
            if sheet_name.startswith(str(sheet_id) + '_'):
                worksheet = self.spreadsheet.worksheet(sheet_name)
                book_data = []
                for row in worksheet.get_all_values():
                    title = row[0]
                    link = row[1]
                    book_data.append({'title': title, 'link': link})
                return book_data
        return []  # Возвращаем пустой список, если лист с указанным ID не найден

    def get_book_by_id(self, sheet_id, book_id):
        """Ищет книгу по ее ID в листе с указанным ID.

        Args:
            sheet_id: ID листа (число перед символом '_').
            book_id: ID книги (число перед символом '_').

        Returns:
            Словарь вида {'title': 'Название книги', 'link': 'Ссылка на скачивание'}
            или None, если книга не найдена.
        """

        book_data = self.get_book_data(sheet_id)
        for book in book_data:
            if book['title'].startswith(str(book_id) + '_'):
                return book
        return None



    def delete_book_by_id(self, sheet_id, book_id):
        """Удаляет книгу по ее ID из листа с указанным ID.

        Args:
            sheet_id: ID листа (число перед символом '_').
            book_id: ID книги (число перед символом '_').

        Returns:
            True, если книга была удалена, False в противном случае.
        """

        book_found = False
        for sheet_name in self.get_topics():
            if sheet_name.startswith(str(sheet_id) + '_'):
                worksheet = self.spreadsheet.worksheet(sheet_name)
                book_data = worksheet.get_all_values()
                if book_data:  # Проверяем, не пуст ли список данных
                    for row_index, row in enumerate(book_data):
                        if row and row[0].startswith(str(book_id) + '_'):
                            book_found = True
                            worksheet.delete_rows(row_index + 1)

                            # Сдвигаем остальные строки вверх (исправленная часть)
                            start_row = row_index + 1
                            start_col = 1
                            end_row = len(book_data)
                            end_col = len(book_data[0])
                            range_name = f"{chr(ord('A') + start_col - 1)}{start_row}:{chr(ord('A') + end_col - 1)}{end_row}"


                            break  # Прерываем цикл, так как книга найдена и удалена
                    break  # Прерываем цикл по листам, так как книга найдена и удалена
        return book_found
    def create_new_sheet(self, sheet_name):
        """Создает новый лист с указанным названием и ID, на 1 больше максимального найденного.

        Args:
            sheet_name: Название нового листа.
        """

        sheet_ids = []
        for sheet_title in self.get_topics():
            # Извлекаем ID из названия листа
            sheet_id = int(sheet_title.split('_')[0])
            sheet_ids.append(sheet_id)

        # Находим максимальный ID
        max_id = max(sheet_ids) if sheet_ids else 0
        # Генерируем новое ID
        new_sheet_id = max_id + 1
        # Формируем название нового листа
        new_sheet_name = f"{new_sheet_id}_{sheet_name}"

        # Создаем новый лист
        self.spreadsheet.add_worksheet(title=new_sheet_name, rows=100, cols=2)
        print(f"Создан новый лист: {new_sheet_name}")

    def delete_sheet_by_id(self, sheet_id):
        """Удаляет лист с указанным ID.

        Args:
            sheet_id: ID листа (число перед символом '_').
        """

        for sheet_name in self.get_topics():
            if sheet_name.startswith(str(sheet_id) + '_'):
                worksheet = self.spreadsheet.worksheet(sheet_name)
                self.spreadsheet.del_worksheet(worksheet)
                print(f"Лист {sheet_name} удален.")
                break  # Прерываем цикл, так как лист найден и удален

    def add_book_to_sheet_by_id(self, sheet_id, book_title, book_link):
        """Добавляет книгу в лист с указанным ID,
        генерируя новый ID для книги, на 1 больше максимального.

        Args:
            sheet_id: ID листа (число перед символом '_').
            book_title: Название книги.
            book_link: Ссылка на книгу.
        """

        for sheet_name in self.get_topics():
            if sheet_name.startswith(str(sheet_id) + '_'):
                worksheet = self.spreadsheet.worksheet(sheet_name)
                # Получаем данные со всех строк листа
                book_data = worksheet.get_all_values()

                # Находим максимальный ID среди существующих книг
                max_id = 0
                for row in book_data:
                    if row:  # Проверяем, не пуста ли строка
                        try:
                            current_id = int(row[0].split('_')[0])
                            max_id = max(max_id, current_id)
                        except (IndexError, ValueError):
                            pass  # Пропускаем строку, если формат не соответствует

                # Генерируем новый ID для книги
                new_id = max_id + 1
                new_book_title = f"{new_id}_{book_title}"

                # Добавляем книгу в лист
                worksheet.append_row([new_book_title, book_link])
                print(f"Книга '{book_title}' добавлена в лист '{sheet_name}' с ID {new_id}")
                break  # Прерываем цикл, так как лист найден