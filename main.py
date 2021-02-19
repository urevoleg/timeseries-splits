from test import test_data

def get_diff(data):
    # считаем интервалы между элементами последовательности
    return [j - i for i, j in zip(data[:-1], data[1:])]


def get_splits(data):
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
        for i in range(idx - 1, len(data_diff)):
            s += data_diff[i]
            cnt += 1
            if s > max(data_diff):
                # получили больше максимальной складываем срез массива в разбиение
                l_res += [data[idx:idx + cnt]]
                break
        idx += cnt
        # если у нас остался последний элемент основного списка, то добавим его к последнему разбиению
        if idx == len(data) - 1:
            l_res[-1].append(data[-1])
    return {'min_interval': max(data_diff), 'splits': l_res}

if __name__ == '__main__':
    for t in test_data:
        print(get_splits(t))