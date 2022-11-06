import pygame
import math
import sys
import time
import random
import collections
import csv

# Initialisation des éléments pygame
tailleEcran = (1300, 700)
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

        # Self.train = (couleur, position, taille, nb de voyageurs, direction (jeu), direction (écran), bouge(Vrai ou faux))
        self.train = [Rouge_coquelicot, self.pos, self.taille, self.voyageurs, self.dir, dir, self.run]
        


    def deplacer(self):
        """Déplace le train"""

        if self.train[6]:
            if self.train[5] == "D":
                if self.train[1][0] != 515:
                    self.train[1][0] += 0.5
                else:
                    self.train[6] = False
                    self.train[1][0] += 0.5
                    self.tmps_arret = pygame.time.get_ticks() + random.randint(5000, 20000)
                
                
            elif self.train[5] == "G":
                if self.train[1][0] != 505:
                    self.train[1][0] -= 0.5
                else:
                    self.train[6] = False
                    self.train[1][0] -= 0.5
                    self.tmps_arret = pygame.time.get_ticks() + random.randint(5000, 15000)

        else:
            if self.tmps_arret <= pygame.time.get_ticks():
                self.train[6] = True


    def detect_signal(self):
        """Permet de dire au train quand il est au niveau d'un signal"""

        if self.train[5] == "D":
            if self.train[1][0] == (475 - self.taille[0]):
                # self.train[1][0] += 0.25
                return (True, 0)
            elif self.train[1][0] == (755 - self.taille[0]):
                # self.train[1][0] += 0.25
                return (True, 1)
            elif self.train[1][0] == (1080 - self.taille[0]):
                # self.train[1][0] += 0.25
                return (True, 2)
            else:
                return (False, 0)
        

        elif self.train[5] == "G":
            if self.train[1][0] == (755):
                # self.train[1][0] += 0.25
                return (True, 1)
            elif self.train[1][0] == (475):
                # self.train[1][0] += 0.25
                return (True, 0)
            # elif self.train[1][0] == (1080):
            #     # self.train[1][0] += 0.25
            #     return (True, 2)

            else:
                return (False, 0)
        else:
                return (False, 0)


    def stop_train(self):
        """Arrete le train"""

        if self.train[6] == True:
            self.train[6] = False
            self.tmps_arret = pygame.time.get_ticks() + 60000
        else:
            pass

    def go_train(self):
        """démarre le train"""

        if self.train[6] == False:
            self.train[6] = True
        else:
            pass


    
    def Affiche(self):

        # Affichage du train
        pygame.draw.rect(screen, self.train[0], (self.train[1], self.train[2]), 0, 5)

class signalisation():
    """gestion et affichage du systèpme de signalisation dans le jeu"""

    def __init__(self) -> None:
        """constructeur"""
        
        self.signaux = []
        self.time = pygame.time.get_ticks()

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
    
    def change_color(self, test, dir) -> None:
        """Change la couleur du feu au passage du train"""

        if dir == "D":
            if test > 0: 
                if self.signaux_droit[test][2]:
                    self.signaux_droit[test][2] = not self.signaux_droit[test][2]
                    self.signaux_droit[test-1][2] = True
                    self.time = pygame.time.get_ticks() + random.randint(700, 1500)
                    pass

            elif test == -1:
                self.signaux_droit[0][2] = False
            elif test == -2:
                self.signaux_droit[0][2] = True
                self.time = pygame.time.get_ticks() + random.randint(700, 1500)
            elif test == 0:
                self.signaux_droit[test][2] = False
                pass

            elif test == -100:
                for i in range(len(self.signaux_droit)):
                    self.signaux_droit[i][2] = True
                self.time = pygame.time.get_ticks() + random.randint(700, 1500)

        elif dir == "G":
            if test < 1: 
                if self.signaux_gauche[test][2]:
                    self.signaux_gauche[test][2] = False
                    self.signaux_gauche[test+1][2] = True
                    self.time = pygame.time.get_ticks() + random.randint(700, 1500)
                    pass

            elif test == 1:
                self.signaux_gauche[1][2] = False
            # elif test == -2:
            #     self.signaux_gauche[0][2] = True
            #     self.time = pygame.time.get_ticks() + random.randint(700, 1500)
            # elif test == 0:
            #     self.signaux_gauche[test][2] = False

            # elif test == -100:
            #     for i in range(len(self.signaux_gauche)):
            #         self.signaux_gauche[i][2] = True
            #     self.time = pygame.time.get_ticks() + random.randint(700, 1500)


    def etat(self, test, dir):
        """renvoie l'état actuel du signal (vert ou rouge)"""

        if dir == "D":
            if self.signaux_droit[test][2] == False:
                return False
            elif self.signaux_droit[test][2] == True:
                return True
            else:
                return False

        if dir == "G":
            if self.signaux_gauche[test][2] == False:
                return False
            elif self.signaux_gauche[test][2] == True:
                return True
            else:
                return False

    

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
    train_droite = Train("D")
    train_gauche = Train("G")
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

                if event.key == pygame.K_q:
                    train_droite.go_train()

                if event.key == pygame.K_s:
                    train_droite.stop_train()
                
                if event.key == pygame.K_c:
                    Signal.change_color(-1, "D")

                if event.key == pygame.K_v:
                    Signal.change_color(1, "D")

                if event.key == pygame.K_w:
                    Signal.change_color(-100, "D")

        if run:
            test_droite = train_droite.detect_signal()
            if test_droite[0] == True:                  # Le train detect le signal
                if Signal.etat(test_droite[1], "D") == True:    # Si le signal est vert
                    if Signal.time < pygame.time.get_ticks():
                        train_droite.train[1][0] += 1
                        train_droite.go_train()
                        Signal.change_color(test_droite[1], "D")     # Change la couleur du signal
                elif Signal.etat(test_droite[1], "D") == False:
                    train_droite.stop_train()                       # Sinon il s'arrete et attend
            else:
                train_droite.deplacer()  

        if run: 
            test_gauche = train_gauche.detect_signal()
            if test_gauche[0] == True:
                if Signal.etat(test_gauche[1], "G") == True:
                    if Signal.time < pygame.time.get_ticks():
                        train_gauche.train[1][0] -= 1
                        train_gauche.go_train()
                        Signal.change_color(test_gauche[1], "G")
                elif Signal.etat(test_gauche[1], "G") == False:
                    train_gauche.stop_train()
            else:
                train_gauche.deplacer()  

                
        if display:
            HUD.Affiche()
            train_droite.Affiche()
            train_gauche.Affiche()
            Signal.Afficher()
        
        pygame.display.flip()  # Affichage Final


if __name__ == '__main__':
    main()

