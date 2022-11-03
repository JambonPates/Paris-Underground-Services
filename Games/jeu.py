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

        self.dir = "Test"
        
        self.taille = (230, 30)
        
        if dir == "D":
            self.pos = [(0 - self.taille[0]), 79]
        elif dir == "G":
            self.pos = [1350, 113]
        else:
            pass

        if self.dir == "Sans Voyageurs":
            self.voyageurs = 0
        else:
            self.voyageurs = random.randint(1, 300)

        self.run = True

        # Self.train = (couleur, position, taille, nb de voyageurs, direction (jeu), direction (écran))
        self.train = [Rouge, self.pos, self.taille, self.voyageurs, self.dir, dir, self.run]
        


    def deplacer(self):
        # self.pos = [self.pos[0]+ 5, self.pos[1]]
        # print(self.pos)

        if self.train[6]:
            if self.train[5] == "D":
                if self.train[1][0] != 510:
                    self.train[1][0] += 0.25
                else:
                    self.train[6] = False
                    self.train[1][0] += 0.25
                    self.tmps_arret = pygame.time.get_ticks() + random.randint(5000, 20000)
                
            elif self.train[5] == "G":
                if self.train[1][0] != 510:
                    self.train[1][0] -= 0.25
                else:
                    self.train[6] = False
                    self.train[1][0] -= 0.25
                    self.tmps_arret = pygame.time.get_ticks() + random.randint(5000, 15000)

        else:
            if self.tmps_arret <= pygame.time.get_ticks():
                self.train[6] = True


    
    def Affiche(self):

        # Affichage du train
        pygame.draw.rect(screen, self.train[0], (self.train[1], self.train[2]), 0, 5)

class signalisation:
    """gestion et affichage du systèpme de signalisation dans le jeu"""




class Ecran:
    """Affichage de l'interface sur l'écran"""

    def __init__(self) -> None:
        pass

    def Affiche(self):
        """Affiche les éléments de l'interface"""

        # Aiguillage
        pygame.draw.polygon(screen, Rouge, ((300, 82),  (360, 140), (386, 140), (326, 82)))
        # Affichage rails
        pygame.draw.rect(screen, Gris, ((0, 82), (1350, 26)))
        pygame.draw.rect(screen, Gris, ((0, 115), (1350, 26)))
        # Affichage du quai
        pygame.draw.rect(screen, Gris_clair, ((500, 32), (250, 45)))
        pygame.draw.rect(screen, Gris_clair, ((500, 147), (250, 45)))
        



def main():

    run = False
    display = True
    HUD = Ecran()
    train = Train("D")
    train2 = Train("G")

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
                    # tmps = pygame.time.get_ticks()
                    run = not run

        if run:
            train.deplacer()  
            train2.deplacer() 
        if display:
            HUD.Affiche()
            train.Affiche()
            train2.Affiche()
        
        pygame.display.flip()  # Affichage Final


if __name__ == '__main__':
    main()

