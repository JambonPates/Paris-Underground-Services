import pygame
import math
import sys
import time
import random

# Initialisation des éléments pygame
tailleEcran = (1350, 700)
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

class Argent:
    """gestion de l'argent dans le jeu"""

    def __init__(self) -> None:
        self.solde = 10000
        pass


    def Ajouter(self, montant) -> None:
        """Ajoute le montant demandé au porte monnaie du joueur"""

        self.solde += montant


    def enlever(self, montant) -> None:
        """Enleve le montant demandé au porte monnaie du joueur"""

        self.solde -= montant

class Train:
    """gestion des trains dans le jeu"""

    def __init__(self, dir) -> None:
        """Constructeur"""

        if dir == "D":
            self.pos = [0, 79]
        elif dir == "G":
            self.pos = [1080, 0]
        else:
            pass
        
        self.dir = "Sans Voyageurs"

        if self.dir == "Sans Voyageurs":
            self.voyageurs = 0
        else:
            self.voyageurs = random.randint(0, 300)
        
        self.taille = (130, 30)

        # Self.train = (couleur, position, taille, nb de voyageurs, direction (jeu), direction (écran))
        self.train = [Rouge, self.pos, self.taille, self.voyageurs, self.dir, dir]
        


    def deplacer(self):
        # self.pos = [self.pos[0]+ 5, self.pos[1]]
        # print(self.pos)
        if self.train[1][0] != 510:
            self.train[1][0] += 0.25
        else:
            pygame.time.wait(2000)
            self.train[1][0] += 0.25


    def Affiche(self):
        """Affiche les éléments de l'interface"""

        # Affichage rails
        pygame.draw.rect(screen, Gris, ((0, 82), (1350, 26)))
        # Affichage du quai
        pygame.draw.rect(screen, Gris_clair, ((500, 32), (150, 45)))
        # Affichage du train
        pygame.draw.rect(screen, self.train[0], (self.train[1], self.train[2]))

def main():

    run = False
    while True:

        
        screen.fill(Noir)
        

        # if pygame.time.get_ticks() > tmps + 4000:
        #     print("ok")
        #     train = Train("D")
        #     tmps = pygame.time.get_ticks()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_d:
                    train = Train("D")
                    # tmps = pygame.time.get_ticks()
                    run = not run

        if run:
            train.deplacer()   
            train.Affiche()
        
        pygame.display.flip()  # Affichage Final


if __name__ == '__main__':
    main()

