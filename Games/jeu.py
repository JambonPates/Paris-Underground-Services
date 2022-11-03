import pygame
import math
import sys
import time
import random
import collections
import csv

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
Rouge_fonce = (50, 0, 0)
Rouge = (200, 0, 0)
Vert = (0, 100, 60)
Vert_clair = (50, 165, 50)
Vert_fonce = (0, 30, 30)
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
        self.train = [Rouge_coquelicot, self.pos, self.taille, self.voyageurs, self.dir, dir, self.run]
        


    def deplacer(self):

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

    def detect_signal(self):
        """Permet de dire au signal quand il est franchit"""

        if self.train[1][0] == (475 - self.taille[0]):
            self.train[1][0] += 0.25
            return (True, 0)
        elif self.train[1][0] == (755 - self.taille[0]):
            self.train[1][0] += 0.25
            return (True, 1)
        elif self.train[1][0] == (1080 - self.taille[0]):
            self.train[1][0] += 0.25
            return (True, 2)
        
        return False, 0


    
    def Affiche(self):

        # Affichage du train
        pygame.draw.rect(screen, self.train[0], (self.train[1], self.train[2]), 0, 5)

class signalisation():
    """gestion et affichage du systèpme de signalisation dans le jeu"""

    def __init__(self) -> None:
        """constructeur"""
        
        self.signaux = []

        # Ouverture du fichiez CSV pour positions et sens des signaux
        with open("Saves\signal_test.csv") as csvfile:
            read = csv.reader(csvfile, delimiter=' ')
            for row in read:
                self.signaux.append(row)   
        
        # Conversion en int des tupples et bool
        for i in range(len(self.signaux)):
            self.signaux[i] = [(int(self.signaux[i][0]), int(self.signaux[i][1])), self.signaux[i][2], bool(int(self.signaux[i][3]))]
        
        # forme : ['position "(x, y)", direction "D" ou "G", couleur "True" ou "False"]

        self.signaux_droit = []
        self.signaux_gauche = []
        for signal in self.signaux:
            if signal[1] == "D":
                self.signaux_droit.append(signal)
            elif signal[1] == "G":
                self.signaux_gauche.append(signal)
            else: 
                pass
    
    def change_color(self, test) -> None:
        """Change la couleur du feu au passage du train"""

        # if test == 2:
        #     self.signaux_droit[0][2] = True
        #     self.signaux_droit[1][2] = True
        if test > 0: 
            if self.signaux_droit[test][2]:
                self.signaux_droit[test][2] = not self.signaux_droit[test][2]
                self.signaux_droit[test-1][2] = True
                pass


        elif test == 0:
            self.signaux_droit[test][2] = False
            pass

    

    def Afficher(self):
        """Affiche les feux de signalisation"""

        for signal in range(len(self.signaux_droit)):
            
            pygame.draw.rect(screen, Gris, (self.signaux_droit[signal][0], (22, 45)), 0, 5)
            if self.signaux_droit[signal][2] == True:
                pygame.draw.circle(screen, Vert_clair, (self.signaux_droit[signal][0][0]+11, self.signaux_droit[signal][0][1]+13), 8)
                pygame.draw.circle(screen, Rouge_fonce, (self.signaux_droit[signal][0][0]+11, self.signaux_droit[signal][0][1]+33), 8)
            elif self.signaux_droit[signal][2] == False:
                pygame.draw.circle(screen, Vert_fonce, (self.signaux_droit[signal][0][0]+11, self.signaux_droit[signal][0][1]+13), 8)
                pygame.draw.circle(screen, Rouge, (self.signaux_droit[signal][0][0]+11, self.signaux_droit[signal][0][1]+33), 8)
            else:
                pygame.draw.circle(screen, Rouge, (self.signaux_droit[signal][0][0]+10, self.signaux_droit[signal][0][1]+13), 8)
                pygame.draw.circle(screen, Rouge, (self.signaux_droit[signal][0][0]+10, self.signaux_droit[signal][0][1]+33), 8)

        for signal in range(len(self.signaux_gauche)):
            
            pygame.draw.rect(screen, Gris, (self.signaux_gauche[signal][0], (22, 45)), 0, 5)
            if self.signaux_gauche[signal][2] == True:
                pygame.draw.circle(screen, Vert_clair, (self.signaux_gauche[signal][0][0]+11, self.signaux_gauche[signal][0][1]+13), 8)
                pygame.draw.circle(screen, Rouge_fonce, (self.signaux_gauche[signal][0][0]+11, self.signaux_gauche[signal][0][1]+33), 8)
            elif self.signaux_gauche[signal][2] == False:
                pygame.draw.circle(screen, Vert_fonce, (self.signaux_gauche[signal][0][0]+11, self.signaux_gauche[signal][0][1]+13), 8)
                pygame.draw.circle(screen, Rouge, (self.signaux_gauche[signal][0][0]+11, self.signaux_gauche[signal][0][1]+33), 8)
            else:
                pygame.draw.circle(screen, Rouge, (self.signaux_gauche[signal][0][0]+10, self.signaux_gauche[signal][0][1]+13), 8)
                pygame.draw.circle(screen, Rouge, (self.signaux_gauche[signal][0][0]+10, self.signaux_gauche[signal][0][1]+33), 8)
        


class Ecran:
    """Affichage de l'interface sur l'écran"""

    def __init__(self) -> None:
        pass

    def Affiche(self) -> None:
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
    Signal = signalisation()
    
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

                if event.key == pygame.K_w:
                    Signal.change_color(0)

                if event.key == pygame.K_x:
                    Signal.change_color(1)
                
                if event.key == pygame.K_c:
                    Signal.change_color(2)

        if run:
            train.deplacer()  
            train2.deplacer() 
        if display:
            HUD.Affiche()
            train.Affiche()
            test = train.detect_signal()
            if test[0]:
                Signal.change_color(test[1])
            train2.Affiche()
            Signal.Afficher()
        
        pygame.display.flip()  # Affichage Final


if __name__ == '__main__':
    main()

