# -*- coding: utf-8 -*-
"""
Модуль анализа html файлов.
=======================================================
* Парсит html файлы в папке files;
* Записывает результат в файл.
=======================================================
"""
import os
import natsort
import os.path
from prettytable import PrettyTable
from bs4 import BeautifulSoup
  
from constants import Constants as const

class HtmlParser:
    """
    Парсер html файлов.
    """ 
    
    def __init__(self):
        # № витка.
        self._number = 0
        self._channels = "456"
        self._lines_count = 0

        # Контроль выходной мощности сигнала ПРД
        self._table_prd  = PrettyTable()
        self._table_prd.field_names = ["№ витка", "Дата", "Время", "Частота", "Интерливинг","Мощность (О)", "Статус (О)", "Комплект (О)", "Мощность (Р)", "Статус (Р)", "Комплект (Р)", "ФЦП (О)", "ФЦП (Р)", "Каналы"]
        self._prd_o_lines_indexes_and_data = list()
        self._prd_r_lines_indexes_and_data = list()
        self._fcp_o_lines_indexes_and_data = list()
        self._fcp_r_lines_indexes_and_data = list()
        self._freq_lines_indexes_and_data = list()
        self._inter_lines_indexes_and_data = list()
      
    def start(self, lines_count):
        """
        Начать анализ html файлов в папке files.

        Args:
            lines_count (int): количество строк которые ищем.
        """
        self._lines_count = lines_count
        files = natsort.natsorted(os.listdir(path="files"))        
        print("Started ", end="")

        for file in files:
            if file.endswith(".html"):
                # получаем имя файла.
                name = os.path.basename(file)
                
                if name[0] == const.ZERO:
                    # поиск номера витка между символами '_' '_'.
                    _ = name[name.find('_')+1:]
                    self._number = _[:_.find('_')]
                elif name[0] == const.CE:
                    # поиск номера витка между символами '-'  '.'.
                    self._number = name[name.find('-')+1:name.find('.')]

                print(".", end="")
                self._find_all_data(file)          

        self._write_table_to_file()  
        print(" Completed")                     
                                      
    def _find_all_data(self, file_name):
        """
        Поиск нужных строчек в файле.

        Args:
            file_name (str): имя файла.
        """
        
        with open(f"files/{file_name}", encoding="utf8") as file:           
            for line_text in file:
                soup = BeautifulSoup(line_text, features="html.parser")
                text = soup.get_text()
                
                # Меняю текст, потому что эти долбоебы не могут придерживаться одного шаблона строки.
                text = text.replace("ИНТРЛВГ ", const.INTER)
                text = text.replace("Откл.осн.ФЦП", "Откл осн.ФЦП")
                text = text.replace("Откл.рез.ФЦП", "Откл рез.ФЦП")

                self._prd_o_lines_indexes_and_data = self._get_indexes_and_data(text, 0, const.PRD_O, const.V_TMSH) 
                self._prd_r_lines_indexes_and_data = self._get_indexes_and_data(text, self._prd_o_lines_indexes_and_data[0], const.PRD_R, const.V_TMSH)
                self._freq_lines_indexes_and_data = self._get_indexes_and_data(text, 0, const.KV_F, const.ED_TMSH)
                self._inter_lines_indexes_and_data = self._get_indexes_and_data(text, 0, const.INTER, const.ED_TMSH)
                self._fcp_o_lines_indexes_and_data = self._get_indexes_and_data(text, 0, const.FCP_O, const.ED_TMSH)
                self._fcp_r_lines_indexes_and_data = self._get_indexes_and_data(text, 0, const.FCP_R, const.ED_TMSH)
                self._find_channels(text)

                self._add_rows_to_table()          

    def _get_indexes_and_data(self, text, start_index, string_to_find, article_to_find):
        """
        Получение индексов начала строк с данными и списков с данными строк.

        Args:
            text (str): текст html страницы, распарсеный через BeautifulSoup.
            start_index (int): индекс начала поиска в тексте.
            string_to_find (str): слово в строкие, которую ищем.
            article_to_find (str): абзац который ищем.
        Returns:
            list[int, list, *]: 
            [индекс начала строки, список с данными строки, *].
        """

        index = text.find(article_to_find, start_index)
        indexes_data_list = list()

        for i in range(self._lines_count):
            line_ind = 0
            line_data = list()
            if index > 0:
                line_ind, line_data = self._find_line(text, index + 5, string_to_find)
            if line_ind <= 0:
                line_data = ["","","","",""] 
            index = line_ind
            indexes_data_list.append(line_ind)
            indexes_data_list.append(line_data)

        return indexes_data_list

    def _find_line(self, text, start_index, string_to_find):
        """
        Поиск строки с данными.

        Args:
            text (str): текст html страницы, распарсеный через BeautifulSoup.
            start_index (int): индекс начала поиска.
            string_to_find (str): заголовок строки, которую ищем.

        Returns:
            int, list: индекс начала строки с данными, список с данными
        """

        line_ind = text.find(string_to_find, start_index)
        line = text[line_ind-40:line_ind+5].split(" ")
        while("" in line):
            line.remove("")
        
        # Иногда длина списка 5, иногда 4, теперь всегда 5.
        if len(line) == 4:
            line.insert(0, " ")
        
         # Иногда длина списка 6, теперь всегда 5.
        if len(line) == 6:
            line.pop(0)

        return line_ind, line

    def _find_channels(self, text):
        """
        Поиск включенных каналов.

        Args:
            text (str): текст html страницы, распарсеный через BeautifulSoup.
        """

        for i, channel_statuses in enumerate(const.CHANNELS_STATUSES):
            if channel_statuses[0] in text:
                # если значение отсутствует, то добавляем.
                if self._channels.find(f'{i+1}') == -1 :
                    self._channels = self._channels + f'{i+1}'
            elif channel_statuses[1] in text:
                self._channels = self._channels.replace(f'{i+1}', '')

    def _add_rows_to_table(self):
        """
        Добавляем найденые строки в таблицу.

        Args:
            lines_count (int): количество добавляемых строк.
        """

        lines_indexes = list()
        # Индексы начинаются с 0, через 1.
        start_index = 0
        # 4 строки.
        for i in range(self._lines_count):
            lines_indexes.append(self._get_row_indexes_list(start_index))
            start_index += 2
        
        # Данные начинаются с 1, через 1.
        start_index = 1
        for line in lines_indexes:
            for i in line:
                if i > 0:
                    self._table_prd.add_row(self._get_row_data(start_index))
                    start_index += 2
                    break
    
    def _get_row_indexes_list(self, index):
        """
        Возвращает список с индексами всех параметров строки.

        Args:
            index (int): индекс для поиска индексов в списках параметров.
        
        Returns:
            list: список индексов всех параметров в строке.
        """
        
        return [self._prd_o_lines_indexes_and_data[index], self._prd_r_lines_indexes_and_data[index], 
                self._fcp_o_lines_indexes_and_data[index], self._fcp_r_lines_indexes_and_data[index], 
                self._freq_lines_indexes_and_data[index], self._inter_lines_indexes_and_data[index]]

    def _get_row_data(self, index):
        """
        Возвращает список с данными всех параметров для строки таблицы.

        Args:
            index (int): индекс строки списков параметров для поиска данных.

        Returns:
            list: список с данными всех параметров для строки таблицы.
        
        Remark:
            [номер витка, дата (со строчки с прд), время (со строчки с прд), частота, интерливинг, мощность (прд о), статус (прд о), 
            комплект (прд о), мощность (прд р), статус (прд р), комплект (прд р), статус фцп (о), статус фцп (р), каналы].
        """

        return [self._number if index == 1 else "", self._prd_o_lines_indexes_and_data[index][0], self._prd_o_lines_indexes_and_data[index][1],
                f"{self._freq_lines_indexes_and_data[index][3]} {self._freq_lines_indexes_and_data[index][4]}",
                self._inter_lines_indexes_and_data[index][3], self._prd_o_lines_indexes_and_data[index][2], self._prd_o_lines_indexes_and_data[index][3],
                self._prd_o_lines_indexes_and_data[index][4], self._prd_r_lines_indexes_and_data[index][2], self._prd_r_lines_indexes_and_data[index][3], 
                self._prd_r_lines_indexes_and_data[index][4], self._fcp_o_lines_indexes_and_data[index][3], self._fcp_r_lines_indexes_and_data[index][3], 
                self._channels if index == 1 else ""]

    def _write_table_to_file(self):
        """
        Запись таблицы в файл.
        """   

        data_prd = self._table_prd.get_string()
        with open('TM.txt', 'w') as f:
            f.write(data_prd)    


if __name__ == "__main__":
    print("Use main.py file!")

