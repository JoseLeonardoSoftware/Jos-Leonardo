#Reprodutor de áudio mp3
import pygame
pygame.mixer.init()
pygame.mixer.music.load('mix.mp3')
pygame.mixer.music.play()
input('Pressione Enter para encerrar...')
