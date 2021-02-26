from test import test_data
from functools import reduce
import numpy as np

def get_diff(data):
    # считаем интервалы между элементами последовательности
    return [j - i for i, j in zip(data[:-1], data[1:])]


def old_get_splits(data):
    data_diff = get_diff(data)
    # проверяем, если элементов
    #  если меньше 2, то делить вообще не имеет смысла, возвращаем ошибку
    if len(data) < 2:
        return {'min_interval': None, 'splits': None, 'errors': 'little data'}

    # менее 4 то разбивать нечего, возвращаем всё как 1 разбиение
    if len(data) < 4:
        return {'min_interval': max(data_diff), 'splits': [data]}
    l_res = []
    idx = 0
    # двигаемся по массиву, пока не закончился
    while idx < len(data):
        s = 0
        cnt = 0
        # суммируем разницу между элементами, до тех пор пока она небольше максимальной разницы
        for i in range(idx, len(data_diff)):
            s += data_diff[i]
            cnt += 1
            if s >= max(data_diff):
                # получили больше максимальной складываем срез массива в разбиение
                if idx + cnt == 1:
                    # если максимальный интервал с самого начала
                    l_res += [data[idx:idx + 1 + cnt]]
                    cnt += 1
                else:
                    l_res += [data[idx:idx + cnt]]
                break

        idx += cnt
        # если у нас остался последний элемент основного списка, то добавим его к последнему разбиению
        if idx == len(data) - 1:
            idx += 1
            l_res[-1].append(data[-1])
            break

        # если осталось менее 4 элементов
        if len(data) - idx <= 4:
            l_res += [data[idx:]]
            idx += 4

    return {'min_interval': max(data_diff), 'splits': l_res}

def get_ranges(data, interval=1):
  delta = 0
  # если последний элемент нечетный, то добавить еще интервал
  if data[-1] % interval:
      delta = 1
  return [[data[0]+interval*i, data[0]+interval*(i+1)] for i in range(data[-1]//interval + delta)]

def funct_to_mininimize(l):
  """Функция принимает разбиения и ищет разбиения с кол-вом элементов 1"""
  return reduce(lambda a, b: a + b, map(lambda x: 1 if len(x) == 1 else 0, l))

def get_splits(data, interval):
  ar = np.array(data)
  return [list(ar[(ar >= r[0]) & (ar < r[1])]) for r in get_ranges(data, interval=interval)]

def find_splits(data):
    # проверяем, если элементов
    #  если меньше 2, то делить вообще не имеет смысла, возвращаем ошибку
    if len(data) < 2:
        return {'min_interval': None, 'splits': None, 'errors': 'little data'}

    # менее 4 то разбивать нечего, возвращаем всё как 1 разбиение
    if len(data) < 4:
        return {'min_interval': None, 'splits': [data]}

    h = 1
    res = 100

    while res != 0:
        h =  h + 1
        output = get_splits(data, interval=h)
        res = funct_to_mininimize(output)

    return {'min_interval': h, 'splits': output}

if __name__ == '__main__':
    for t in test_data:
        print(find_splits(t))