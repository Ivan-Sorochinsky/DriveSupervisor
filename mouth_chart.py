import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.style.use('dark_background')

fig = plt.figure()

# рот
ax = fig.add_subplot(1, 1, 1)


def animate(i):
    try:
        # данные о уровне открытия рта
        with open('mouth_data.txt') as mouth_file:
            mouth_data = mouth_file.read()

        # общий счетчик
        with open('counter.txt') as counter_file:
            data_counter = counter_file.read()

        # str to list
        m_y_str = mouth_data.split(', ')
        x_str = data_counter.split(', ')
        # str_list to number_list
        m_y = [float(item) for item in m_y_str]
        x = [int(item) for item in x_str]

        ax.clear()
        ax.plot(x, m_y, label="Рот")

        ax.legend(loc='lower left')

        plt.xlabel('Итерации основного потока')
        plt.ylabel('MAR')
        plt.title('Анализ уровня открытия рта в реальном времени')
    except Exception:
        pass


ani = animation.FuncAnimation(fig, animate, interval=30)
plt.show()
