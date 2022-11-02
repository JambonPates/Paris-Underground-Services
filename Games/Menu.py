import pygame
import math
import sys


# Initialisation des éléments pygame
tailleEcran = (1375, 700)
pygame.init()
screen = pygame.display.set_mode(tailleEcran)
pygame.display.set_caption("Paris Underground Services")

# Création des polices d'écriture

font = pygame.font.Font(None, 15)
moyfont = pygame.font.Font(None, 30)
grandfont = pygame.font.Font(None, 45)
quitfont = pygame.font.Font(None, 55)
megafont = pygame.font.Font(None, 70)


# Définiton des couleurs 

Blanc = (255, 255, 255)
Bleu = (60, 140, 220)
Bleu_fonce = (0, 85, 200)
Gris = (20, 20, 20)
Gris_clair = (125, 125, 125)
Marron = (90, 35, 10)
Noir = (0, 0, 0)
Or = (211, 155,   0)
Orange = (255, 90, 0)
Rouge_coquelicot = (255, 20, 0)
Rouge = (150, 0, 0)
Vert = (0, 100, 60)
Vert_clair = (130, 220, 115)
Violet = (100, 0, 130)




def main():
    
    while True:

        screen.fill(Noir)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Affichage Final


if __name__ == '__main__':
    main()