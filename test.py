HOURS_PATTERN = ['час', 'часа', 'часов']
MINUTES_PATTERN = ['минута', 'минуты', 'минут']
HOURS_PATTERN_SHORT = ['ч', 'ч', 'ч']
MINUTES_PATTERN_SHORT = ['мин', 'мин', 'мин']

def decline_of_time(number, titles):
    """
    возвращает текстовое описание времени со склонением часа/часов
    :param number: число для слонения
    :param titles: паттерны описания ['день', 'дня', 'дней']
    :return:
    """
    cases = [2, 0, 1, 1, 1, 2]

    num = 0
    if 4 < number % 100 < 20:
        num = 2
    else:
        num = cases[number % 10 if number % 10 < 5 else 5]

    return titles[num]

def minutes_to_text(time, with_sign=False, is_short=False):
    """
    Получает строку вида 1 час 35 минут если передали например 95
    :param time: время в минутах
    :param with_sign: выводить знак или нет
    :return:
    """
    # знак + выводим только по условию
    sign = '-' if time < 0 else ('+' if with_sign and time > 0 else '')

    # убираем знак для корректного расчета
    time = abs(time)

    # преобразуем часы и минуты по падежу
    patterns = (HOURS_PATTERN, MINUTES_PATTERN) if not is_short else (HOURS_PATTERN_SHORT, MINUTES_PATTERN_SHORT)
    nums = zip(divmod(time, 60), patterns)

    time_str = sign + ' '.join(map(lambda num: (str(num[0]) + ' ' + decline_of_time(*num)) if num[0] > 0 else '', nums))

    return time_str

print(minutes_to_text(75))