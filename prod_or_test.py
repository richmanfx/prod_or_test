# -*- coding: utf-8 -*-
from os import system
import argparse
import prod_or_test_cfg


VERSION = '1.0.0'
__author__ = 'Aleksandr Jashhuk, Zoer, R5AM, www.r5am.ru'


def main():
    clear_console()  # Очистить консоль

    # Обработать аргументы командной строки
    parser = create_parser()
    namespace = parser.parse_args()

    # Проверить аргументы командной строки
    if not argument_validator(namespace):
        exit()                              # Выход из программы если плохие аргументы

    # Запрос prod или test.
    print 'Choose:\n' \
          '\t"1" for prod server\n' \
          '\t"2" for test server\n'
    role = mini_switch(raw_input())         # Роль - prod или test

    # Модифицируем online.settings.xml
    file_path = prod_or_test_cfg.config_files['online.settings.xml']
    full_file_name = file_path + "//online.settings.xml"    # Полное имя файла

    file_lines = []
    try:
        file_obj = open(full_file_name, 'r')       # читаем файл посторочно
        file_lines = file_obj.readlines()
        file_obj.close()
    except IOError:
        print "Error opening file: " + full_file_name
        exit(1)

    if role == 'prod':
        for line_number, line in enumerate(file_lines):
            l1 = line.upper().strip().rstrip('\n')
            if l1 == '<URLS>':
                new_line = '\t<!-- ' + line.upper().strip() + '\n'
                file_lines[line_number] = new_line
            if l1 == '</URLS>':
                new_line = line.upper().rstrip('\n') + ' -->\n'
                file_lines[line_number] = new_line

    else:   # Роль - test
        for line_number, line in enumerate(file_lines):
            l1 = line.upper().strip().rstrip('\n')
            if l1 == '<!-- <URLS>':
                new_line = '\t<URLS> \n'
                file_lines[line_number] = new_line
            if l1 == '</URLS> -->':
                new_line = '\t</URLS>\n'
                file_lines[line_number] = new_line

    file_obj = open(full_file_name, 'w')
    file_obj.writelines(file_lines)    # Перезаписываем файл
    file_obj.close()

    # Модифицируем test.runtime.xml
    file_path = prod_or_test_cfg.config_files['test.runtime.xml']
    full_file_name = file_path + "//test.runtime.xml"  # Полное имя файла

    try:
        file_obj = open(full_file_name, 'r')  # читаем файл посторочно
    except IOError:
        print "Error opening file: " + full_file_name
        exit(1)
    else:
        file_lines = file_obj.readlines()
        file_obj.close()

    if role == 'prod':
        for line_number, line in enumerate(file_lines):
            l1 = line.upper().strip().rstrip('\n')
            if l1.count('<ALLOW_TO_SEND_REQUEST>FALSE</ALLOW_TO_SEND_REQUEST>') == 1:
                new_line = '\t' + l1.replace('FALSE', 'TRUE', 1) + '\n'
                file_lines[line_number] = new_line
    else:  # Роль - test
        for line_number, line in enumerate(file_lines):
            l1 = line.upper().strip().rstrip('\n')
            if l1.count('<ALLOW_TO_SEND_REQUEST>TRUE</ALLOW_TO_SEND_REQUEST>') == 1:
                new_line = '\t' + l1.replace('TRUE', 'FALSE', 1) + '\n'
                file_lines[line_number] = new_line

    file_obj = open(full_file_name, 'w')
    file_obj.writelines(file_lines)  # Перезаписываем файл
    file_obj.close()

    # Модифицируем Uхххх.online.xml
    file_path = prod_or_test_cfg.config_files['Uxxxx.online.xml']
    full_file_name = file_path + "//U" + str(namespace.test_number) + ".online.xml"  # Полное имя файла

    try:
        file_obj = open(full_file_name, 'r')  # читаем файл посторочно
    except IOError:
        print "Error opening file: " + full_file_name
        exit(1)
    else:
        file_lines = file_obj.readlines()
        file_obj.close()

    if role == 'prod':
        for line_number, line in enumerate(file_lines):
            l1 = line.lower()
            if l1.count('testlk.admtyumen.ru') == 1:
                new_line = l1.replace('testlk.admtyumen.ru', 'uslugi.admtyumen.ru', 1)
                file_lines[line_number] = new_line

    if role == 'test':
        for line_number, line in enumerate(file_lines):
            l1 = line.lower()
            if l1.count('uslugi.admtyumen.ru') == 1:
                new_line = l1.replace('uslugi.admtyumen.ru', 'testlk.admtyumen.ru', 1)
                file_lines[line_number] = new_line

    file_obj = open(full_file_name, 'w')
    file_obj.writelines(file_lines)  # Перезаписываем файл
    file_obj.close()

    # Модифицируем testProperties.online.xml
    file_path = prod_or_test_cfg.config_files['testProperties.online.xml']
    full_file_name = file_path + "//testProperties.online.xml"  # Полное имя файла

    try:
        file_obj = open(full_file_name, 'r')  # читаем файл посторочно
    except IOError:
        print "Error opening file: " + full_file_name
        exit(1)
    else:
        file_lines = file_obj.readlines()
        file_obj.close()

    if role == 'prod':
        for line_number, line in enumerate(file_lines):
            l1 = line.strip().rstrip('\n')
            if l1.count('<NAME>isTestUser</NAME>') == 1:
                l2 = file_lines[line_number + 1]
                if l2.count('<VALUE>true</VALUE>'):
                    new_line = file_lines[line_number + 1].replace('<VALUE>true</VALUE>', '<VALUE>false</VALUE>', 1)
                    file_lines[line_number + 1] = new_line

    if role == 'test':
        for line_number, line in enumerate(file_lines):
            l1 = line.strip().rstrip('\n')
            if l1.count('<NAME>isTestUser</NAME>') == 1:
                l2 = file_lines[line_number + 1]
                if l2.count('<VALUE>false</VALUE>'):
                    new_line = file_lines[line_number + 1].replace('<VALUE>false</VALUE>', '<VALUE>true</VALUE>', 1)
                    file_lines[line_number + 1] = new_line

    file_obj = open(full_file_name, 'w')
    file_obj.writelines(file_lines)  # Перезаписываем файл
    file_obj.close()


def mini_switch(case):
    if case == '1':
        role = "prod"
        return role
    elif case == '2':
        role = "test"
        return role
    else:
        print "An out of range number. Bye."
        exit(1)


# Создаёт экземпляр parser с нужными параметрами
def create_parser():
    parser = argparse.ArgumentParser(description='Converter Runner configs from test to prod and back.',
                                     epilog='For example: prod_or_test.py 1234')
    parser.add_argument('--version', '-v', action='version', version='cw_py {}'.format(VERSION))
    parser.add_argument('test_number', type=int, help='Number of the test.')
    return parser


# Проверка диапазона допустимых значений
def valid_range(minimum, maximum, variable):
    if (variable >= minimum) and (variable <= maximum):
        result = True
    else:
        result = False
    return result


# Проверка допустимых значений аргументов командной строки
def argument_validator(namespace):
    validation_result = True
    if not valid_range(1, 99000, namespace.test_number):
        print 'Invalid value for the number of test (1...99000).'
        validation_result = False
    return validation_result


# Очистка консоли в Windows
def clear_console():
        system('cls')


if __name__ == '__main__':
    main()
