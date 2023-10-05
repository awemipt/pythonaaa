import csv
from collections.abc import Mapping
from typing import Dict, List



def get_data(file: str) -> dict:
    """
    Читает данные из CSV-файла и возвращает их в виде словаря.

    Args:
        file (str): Имя файла для чтения данных
        (Может быть как с расширением .сsv так и без).

    Returns:
        dict: Словарь данных, где ключи - это названия столбцов,
        а значения - списки данных из столбцов.

    Raises:
        FileNotFoundError: Если файл с указанным именем не найден
        в текущей директории.
    """
    if not file.endswith('.csv'):
        file += '.csv'
    try:
        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            tags = next(reader)
            content: Dict[str, List[str]] = {tag: [] for tag in tags}
            for row in reader:
                for i, tag in enumerate(tags):
                    content[tag].append(row[i])
        return content
    except FileNotFoundError:
        raise FileNotFoundError(
            f'Нет файла с именем {file} в локальной директории')


def print_teams(data: dict):
    """
    Выводит информацию о командах и их департаментах.

    Args:
        data (str): Словарь данных о департаментах и подразделениях в них.

    Returns:
        None
    """
    for department in data:
        print(f'Подразделение {department} состоит из {len(data[department])} команд:')
        print('----' + '\n----'.join(list(data[department])))
        print()


def get_teams(file: str) -> dict:
    """
    Возвращает информацию о командах и департаментах из данных в CSV-файле.

    Args:
        file (str): Имя файла для чтения данных.

    Returns:
        dict: Словарь, где ключи - названия департаментов,
        а значения - множества команд в каждом департаменте.
    """
    content = get_data(file=file)
    departments = content[list(content.keys())[1]]
    departments_unique = sorted(set(content[list(content.keys())[1]]))
    divisions = content[list(content.keys())[2]]
    out: dict[str, set[str]] = {key: set() for key in departments_unique}
    for department, division in zip(departments, divisions):
        out[department].add(division)
    return out


def get_reports(file: str) -> dict:
    """
    Генерирует сводный отчет по департаментам на основе данных из CSV-файла.

    Args:
        file (str): Имя файла для чтения данных.

    Returns:
        dict: Словарь с информацией о минимальной и максимальной зарплате,
        численности и средней зарплате в каждом департаменте.
    """
    content = get_data(file=file)
    departments = content[list(content.keys())[1]]
    departments_unique = sorted(set(content[list(content.keys())[1]]))
    salaries = content[list(content.keys())[-1]]
    salaries_by_departments: dict[str, list[int]] = {key: [] for key in departments_unique}
    for department, salary in zip(departments, salaries):
        salaries_by_departments[department].append(int(salary))
    report = {}
    for department, salaries in salaries_by_departments.items():
        min_salary = min(salaries)
        max_salary = max(salaries)
        head_count = len(salaries)
        mean_salary = round(sum(salaries) / head_count, 2)
        report[department] = {'min_salary': min_salary, 'max_salary': max_salary,
                              'head_count': head_count, 'mean_salary': mean_salary}
    return report


def print_report(report: dict):
    """
    Выводит сводный отчет по департаментам.

    Args:
        report (dict): Словарь с информацией о департаментах.

    Returns:
        None
    """
    for department, data in report.items():
        print(
            f'Департамент: {department} состоит из {data["head_count"]} человек')
        print(
            f'--Вилка {data["min_salary"]}-{data["max_salary"]} рублей в месяц')
        print(f'--Cредняя зарплата: {data["mean_salary"]} рублей в месяц')
        print()


def make_report_csv(report: dict):
    """
    Создает CSV-файл с данными из сводного отчета.

    Args:
        report (dict): Словарь с информацией о департаментах.

    Returns:
        None
    """
    report_file_name = input('Введите имя выходного файла: ').strip()
    if not report_file_name.endswith('.csv'):
        report_file_name += '.csv'
    with open(report_file_name, mode='w', encoding='utf-8') as outcsv:
        writer = csv.writer(outcsv, delimiter=';')
        writer.writerow(['Департамент', 'Минимальная зарплата',
                        'Максимальная зарплата', 'Численность', 'Средняя запрлата'])
        for department, data in report.items():
            writer.writerow([department] + list(data.values()))


def main():
    file = input('Введите имя файла: ').strip()

    mode = int(input("""Выберите пункт меню:
    1: Вывести в понятном виде иерархию команд, т.е. департамент и все команды, которые входят в него
    2: Вывести сводный отчёт по департаментам: название, численность, "вилка" зарплат в виде мин – макс, среднюю зарплату
    3: Сохранить сводный отчёт в виде csv-файла
-->>"""))

    if mode == 1:
        teams = get_teams(file=file)
        print_teams(teams)
    elif mode == 2:
        report = get_reports(file)
        print_report(report)
    elif mode == 3:
        make_report_csv(get_reports(file))
    else:
        raise KeyError('Некорректный ввод.')


if __name__ == "__main__":
    main()
