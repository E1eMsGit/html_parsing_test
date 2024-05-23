# -*- coding: utf-8 -*-
"""
=======================================================
Программа парсинга html файлов.
=======================================================
Главный модуль.
=======================================================
* Запускает программу;
=======================================================
"""
import sys
from html_parser import HtmlParser


def main(lines_count):
    """
    Главная функция. Запускает парсинг html файлов в папке files.

    Args:
        lines_count (int): количество строк которые ищем.
    """
    html_parser = HtmlParser()
    html_parser.start(lines_count)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            main(int(f"{sys.argv[1]}"))
        else:
            print("Error.\nInput int value.")
    elif len(sys.argv) == 1:
        main(6)
    else:
        print("Error.\nInput \"python main.py\" for parsing 6 parameters lines in file.\nInput \"python main.py int_value\" where \"int_value\" - parameters lines count.")
    
    
