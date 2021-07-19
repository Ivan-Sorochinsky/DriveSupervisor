import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.style.use('dark_background')

fig = plt.figure()

# глаза
ax = fig.add_subplot(1, 1, 1)


def animate(i):
    try:
        # данные по правому глазу
        with open('r_eye_data.txt') as r_eye_file:
            r_eye_data = r_eye_file.read()

        # данные по левому глазу
        with open('l_eye_data.txt') as l_eye_file:
            l_eye_data = l_eye_file.read()

        # общий счетчик
        with open('counter.txt') as counter_file:
            data_counter = counter_file.read()

        # str to list
        r_y_str = r_eye_data.split(', ')
        l_y_str = l_eye_data.split(', ')
        x_str = data_counter.split(', ')
        # str_list to number_list
        r_y = [float(item) for item in r_y_str]
        l_y = [float(item) for item in l_y_str]
        x = [int(item) for item in x_str]

        ax.clear()
        ax.plot(x, r_y, label="Правый глаз")
        ax.plot(x, l_y, label='Левый глаз')

        ax.legend(loc='lower left')

        plt.xlabel('Итерации основного потока')
        plt.ylabel('EAR')
        plt.title('Анализ состояния глаз в реальном времени')
    except Exception:
        pass


ani = animation.FuncAnimation(fig, animate, interval=30)
plt.show()
