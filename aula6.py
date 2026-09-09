import keyboard
import pygame

# inicia sistema de áudio
pygame.mixer.init()

# carrega o som
som = pygame.mixer.Sound("som.wav")

print("Programa iniciado...")
print("Cada tecla fará um som!")

# função chamada ao apertar tecla


def tocar_som(event):
    som.play()


# escuta todas as teclas
keyboard.on_press(tocar_som)

# mantém programa rodando
keyboard.wait()
