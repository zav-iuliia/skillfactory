import numpy as np


def game_core(number):
    '''Функция принимает загаданное число и возвращает число попыток
    за которое она отгадывает его'''
    count = 0
    minimum = 1
    maximum = 101
    predict = np.random.randint(1, 101)
    while number != predict:
        count += 1
        # нахожу среднию точку из доступного отрезка
        predict = (minimum + maximum) // 2
        # определяю начало и конец отрезка на сдедующем этапе цикла
        if number > predict:
            minimum = predict
        elif number < predict:
            maximum = predict
    return (count)  # выход из цикла, когда число угадано


def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1, 101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return (score)


# Проверяем
score_game(game_core)
