import pygame


def initialize_audio(filepath):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)

def play_audio():
    pygame.mixer.music.play()