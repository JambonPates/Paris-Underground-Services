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

attente_station = 5000
tempo_signalisation = 2000


# Création des polices d'écriture
font = pygame.font.Font(None, 15)
moyfont = pygame.font.Font(None, 30)
grandfont = pygame.font.Font(None, 45)
quitfont = pygame.font.Font(None, 55)
megafont = pygame.font.Font(None, 70)


# Définiton des couleurs 
Blanc = (255, 255, 255)
Blanc_light = (230, 230, 230)
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

class Gestion:
    """gestion de l'argent dans le jeu"""

    def __init__(self) -> None:
        self.solde = 1000
        self.nb_voyageur_tot = 0
        self.nb_voyageurs_droite = 30
        self.nb_voyageurs_gauche = 30
        pass


    def Ajouter(self, montant) -> None:
        """Ajoute le montant demandé au porte monnaie du joueur"""

        self.solde += montant


    def enlever(self, montant) -> None:
        """Enleve le montant demandé au porte monnaie du joueur"""

        self.solde -= montant

class Train:
    """gestion des trains dans le jeu"""

    def __init__(self, dir, signaux) -> None:
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

        # Definition liste des positions (en X) des signaux 
        self.signaux = []
        for signal in signaux:

            if signal[1] == dir:
                self.signaux.append(signal[0][0])
           

        # Self.train = (couleur, position, taille, nb de voyageurs, direction (jeu), direction (écran), bouge(Vrai ou faux))
        self.train = [Rouge_coquelicot, self.pos, self.taille, self.voyageurs, self.dir, dir, self.run]

        # Stationnement en gare 
        self.station = 515 # coordonnées en x arret station
        self.time_station = False
        self.depart = 0

        # Temporisation signalisation
        self.tempo = 0
        self.ajouter_tempo = True
        


    def deplacer(self) -> None:
        """Déplace le train"""

        # Si en station, le train s'arrete 
        if self.train[1][0] == self.station:
            self.train[6] = False
            self.depart = pygame.time.get_ticks() + attente_station
            self.time_station = True
            self.train[1][0] += 0.5
            

        # Si R.A.S le train avance  
        if self.train[6]:
            self.train[1][0] += 1
            pass

        # Attente du train en station
        if self.time_station:
            if self.depart <= pygame.time.get_ticks():
                self.train[1][0] += 0.5
                self.time_station = False
                self.train[6] = True
                pass
             
                

    def detect_signal(self):
        """Permet de dire au train quand il est au niveau d'un signal"""
        
        if self.train[5] == "D":

            for test in range(len(self.signaux)):
                if (self.train[1][0] + self.taille[0]) == self.signaux[test]:
                    # self.train[6] = False
                    return (True, test, "D")   
            return (False, 0, "D")
       

        elif self.train[5] == "G":

            for test in range(len(self.signaux)):
                if self.train[1][0] == test:
                    return (True, (len(self.signaux) - test), "G")
            return (False, 0, "G")


    def run_train(self, running): 
        """ Arrete ou démarre le train """

        if running and not self.time_station or self.train[6] == True: # feu vert
            self.train[6] = True
    
        if not running:
            self.train[6] = False
            if self.ajouter_tempo:
                self.tempo = pygame.time.get_ticks() + tempo_signalisation
                self.ajouter_tempo = False

        
    def Affiche(self) -> None:

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

    def liste_signaux(self):
        """ Retourne la liste des signaux pour le train (execution unique) """

        return self.signaux_gauche + self.signaux_droit
    

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
            if test < len(self.signaux_gauche)-1: 
                if self.signaux_gauche[test][2]:
                    self.signaux_gauche[test][2] = False
                    self.signaux_gauche[test+1][2] = True
                    pass
            
            elif test == 100:
                for i in range(len(self.signaux_gauche)):
                    self.signaux_gauche[i][2] = True
                self.time = pygame.time.get_ticks() + random.randint(900, 1500)

            elif test == len(self.signaux_gauche)-1:
                self.signaux_gauche[len(self.signaux_gauche)-1][2] = False
           

    def etat(self, infos) -> bool:
        """ Renvoie l'état actuel du signal (vert ou rouge) et change couleur lors du franchissement """
    
        if infos[0]: 
            if infos[2] == "D":
                if self.signaux_droit[infos[1]][2] == False: # Si rouge -> stop train
                    return False
                elif self.signaux_droit[infos[1]][2] == True: # Si vert -> train avance, change couleur
                    self.signaux_droit[infos[1]][2] = not self.signaux_droit[infos[1]][2]
                    self.signaux_droit[infos[1]-1][2] = True
                    self.signaux_droit[4][2] = True
                    return True
                # else:
                #     print("error")
                #     return False # Sinon considère comme rouge

            if infos[2] == "G":
                if self.signaux_gauche[infos[1]][2] == False: # Si rouge -> stop train
                    return False
                elif self.signaux_gauche[infos[1]][2] == True: # Si vert -> train avance, change couleur
                    self.signaux_gauche[infos[1]][2] = False
                    self.signaux_gauche[infos[1]+1][2] = True
                    return True
                else:
                    return False # Sinon considère comme rouge

        return True
    

    def Afficher(self) -> None:
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

    def interface(self) -> None:
        """dessine l'interface utilisable par le joueur"""

        pygame.draw.line(screen, Blanc_light, (0, 290), (tailleEcran[0],290), 5)
        pygame.draw.rect(screen, Gris_clair, ((20, 305), (tailleEcran[0] - 40, tailleEcran[1] - 325)), 0, 15)
        pygame.draw.line(screen, Gris, (250, 305), (250, tailleEcran[0] - 40), 3)
        pygame.draw.line(screen, Gris, (20, 425), (250, 425), 3)
        pygame.draw.line(screen, Gris, (20, 560), (250, 560), 3)

    def Affichage_infos(self, Money, nb_voyageurs):
        """Affiche les infoemations de la partie (heure, argent, nb de passagers)"""

        argent = grandfont.render("Argent", 1, Or)
        screen.blit(argent, (75, 325))
        solde = moyfont.render(str(Money) + "$", 1, Noir)
        screen.blit(solde, (((250-20)/2)-25, 375))
        voyageurs = grandfont.render("Voyageurs", 1, Or)
        screen.blit(voyageurs, (50, 450))
        voy = moyfont.render(str(nb_voyageurs), 1, Noir)
        screen.blit(voy, (((270-20)/2), 500))
        horloge = grandfont.render("Horloge", 1, Or)
        screen.blit(horloge, (72, 570))
        time = moyfont.render("--:--", 1, Noir)
        screen.blit(time, (((270-20)/2)-10, 630))
        



def main():

    # DEV
    dev = True

    # Variables controle déplacement des trains sur une voie
    run = False

    # Active l'affichage des éléments de l'interface
    display = True

    # Liste contenant toutes les instances de trains
    liste_train = []

    HUD = Ecran()
    Signal = signalisation()
    gestion = Gestion()

    if dev:
        liste_train.append(Train("D", Signal.liste_signaux()))
        run = True
    

    while True:

        screen.fill(Noir)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if dev:
                    if event.key == pygame.K_d:
                        # tmps = pygame.time.get_ticks()
                        run = not run

                    # if event.key == pygame.K_q:
                    #     train_droite.run_train(False)

                    # if event.key == pygame.K_s:
                    #     train_droite.train[1][0] += 0.5
                    #     train_droite.run_train(True)
                    
                    if event.key == pygame.K_b:
                        print("ok")
                        train_droite = Train("G", Signal.liste_signaux())
                        liste_train.append(train_droite)

                    if event.key == pygame.K_v:
                        Signal.change_color(0, "D")

                    if event.key == pygame.K_w:
                        Signal.change_color(-100, "D")
                    
                    if event.key == pygame.K_n:
                        run = True
                        train_droite = Train("D", Signal.liste_signaux())
                        liste_train.append(train_droite)

        
        if not bool(liste_train):
            run = False

        if run: 
            for train in liste_train:         
                train.run_train(Signal.etat(train.detect_signal()))
                train.deplacer() 
            
        if display:
            HUD.Affiche()
            HUD.interface()
            HUD.Affichage_infos(gestion.solde, gestion.nb_voyageur_tot)
            Signal.Afficher()
            if run:
                for train in liste_train:
                    train.Affiche()
            
        
        pygame.display.flip()  # Affichage Final


if __name__ == '__main__':
    main()

