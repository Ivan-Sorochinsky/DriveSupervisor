import pygame
import time

SLEEP_STATE = 0
NO_HANDS_STATE = 1


# если обнаружена аномалия в поведении водителя, вызывается этот метод
def bad_vodiva(state, semaphore, event):
    event.set()
    semaphore.acquire()  # уменьшает счетчик (-1)
    pygame.init()
    if state == SLEEP_STATE:
        song = pygame.mixer.Sound('sleep.mp3')
    else:
        pass
        # song = pygame.mixer.Sound('baranka.mp3')
    #song.play()
    time.sleep(5)
    pygame.quit()
    event.clear()
    semaphore.release()  # увеличивает счетчик (+1)
