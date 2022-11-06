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
        self.solde = 10000
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
        


    def deplacer(self) -> None:
        """Déplace le train"""

        if self.train[6]:
            if self.train[5] == "D":
                if self.train[1][0] != 515:
                    self.train[1][0] += 0.25
                else:
                    self.train[6] = False
                    self.train[1][0] += 0.25
                    self.tmps_arret = pygame.time.get_ticks() + random.randint(5000, 20000)
                
                
            elif self.train[5] == "G":
                if self.train[1][0] != 505:
                    self.train[1][0] -= 0.25
                else:
                    self.train[6] = False
                    self.train[1][0] -= 0.25
                    self.tmps_arret = pygame.time.get_ticks() + random.randint(5000, 15000)

        else:
            if self.tmps_arret <= pygame.time.get_ticks():
                self.train[6] = True


    def detect_signal(self):
        """Permet de dire au train quand il est au niveau d'un signal"""

        if self.train[5] == "D":
            if self.train[1][0] == (160 - self.taille[0]):
                return (True, 0)
            elif self.train[1][0] == (475 - self.taille[0]):
                return (True, 1)
            elif self.train[1][0] == (755 - self.taille[0]):
                return (True, 2)
            elif self.train[1][0] == (1140 - self.taille[0]):
                return (True, 3)
            else:
                return (False, 0)
        

        elif self.train[5] == "G":
            if self.train[1][0] == (1140):
                return (True, 3)
            if self.train[1][0] == (755):
                return (True, 2)
            elif self.train[1][0] == (475):
                return (True, 1)
            elif self.train[1][0] == (160):
                return (True, 0)

            else:
                return (False, 0)
        else:
                return (False, 0)


    def stop_train(self) -> None:
        """Arrete le train"""

        if self.train[6] == True:
            self.train[6] = False
            self.tmps_arret = pygame.time.get_ticks() + 60000
        else:
            pass

    def go_train(self) -> None:
        """démarre le train"""

        if self.train[6] == False:
            self.train[6] = True
        else:
            pass


    
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
           

    def etat(self, test, dir) -> bool:
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
    run1 = False
    run2 = False

    # Variable pour demande de nouveaux trains
    run_suivant_droit = True
    run_suivant_gauche = True

    # Active l'affichage des éléments de l'interface
    display = True

    HUD = Ecran()
    Signal = signalisation()
    gestion = Gestion()

    # train_droite = Train("D")
    # train_gauche = Train("G")

    # Variable pour temps de génération du prochain trains
    train_suivant_droit = pygame.time.get_ticks() + random.randint(3000, 12000)
    train_suivant_gauche = train_suivant_droit = pygame.time.get_ticks() + random.randint(9000, 21000)

    if dev:
        run_suivant_droit = False
        run_suivant_gauche = False
        train_droite = Train("D")
        train_gauche = Train("G")
        run1 = True
        run2 = True
    

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
                        run1 = not run1
                        run2 = not run2

                    if event.key == pygame.K_q:
                        train_droite.go_train()

                    if event.key == pygame.K_s:
                        train_droite.stop_train()
                    
                    if event.key == pygame.K_c:
                        Signal.change_color(random.randint(0, 3), "D")

                    if event.key == pygame.K_v:
                        Signal.change_color(1, "D")

                    if event.key == pygame.K_w:
                        Signal.change_color(-100, "D")

        if run_suivant_droit:
            if pygame.time.get_ticks() > train_suivant_droit:
                train_droite = Train("D")
                run1 = True
                run_suivant_droit = False

        if run_suivant_gauche:
            if pygame.time.get_ticks() > train_suivant_gauche:
                train_gauche = Train("G")
                run2 = True
                run_suivant_gauche = False

        if run1:
            test_droite = train_droite.detect_signal()
            if test_droite[0] == True:                  # Le train detect le signal
                if Signal.etat(test_droite[1], "D") == True:    # Si le signal est vert
                    if Signal.time < pygame.time.get_ticks():
                        train_droite.train[1][0] += 1
                        train_droite.go_train()
                        Signal.change_color(test_droite[1], "D")     # Change la couleur du signal
                elif Signal.etat(test_droite[1], "D") == False:
                    train_droite.stop_train()                       # Sinon il s'arrete et attend

            elif train_droite.train[1][0] == 514:   # Déchargement et chargement des passagers
                desc = random.randint(0, train_droite.voyageurs)
                mont = random.randint(0, gestion.nb_voyageurs_droite)
                train_droite.train[3] -= desc
                gestion.nb_voyageur_tot += desc
                gestion.nb_voyageurs_droite -= mont
                if train_droite.train[3] + mont <= 300:
                    train_droite.train[3]  += mont
                else: 
                    gestion.nb_voyageurs_droite = train_droite.train[3] + mont - 300
                    train_droite.train[3] = 300
                train_droite.train[1][0] += 0.5

            elif train_droite.train[1][0] == 1310: # Arret train actuel et appel du train suivant
                Signal.change_color(-100, "D")
                run1 = False
                run_suivant_droit = True
                train_suivant_droit = pygame.time.get_ticks() + random.randint(7000, 12000)

            else:
                train_droite.deplacer()  

        if run2: 
            test_gauche = train_gauche.detect_signal()
            if test_gauche[0] == True:
                if Signal.etat(test_gauche[1], "G") == True:
                    if Signal.time < pygame.time.get_ticks():
                        train_gauche.train[1][0] -= 1
                        train_gauche.go_train()
                        Signal.change_color(test_gauche[1], "G")
                elif Signal.etat(test_gauche[1], "G") == False:
                    train_gauche.stop_train()

                    505

            elif train_gauche.train[1][0] == (0 - train_gauche.taille[0]): # Arret train actuel et appel du train suivant
                Signal.change_color(100, "G")
                run2 = False
                run_suivant_gauche = True
                train_suivant_gauche = pygame.time.get_ticks() + random.randint(7000, 12000)

            else:
                train_gauche.deplacer()  
            

                
        if display:
            HUD.Affiche()
            HUD.interface()
            HUD.Affichage_infos(gestion.solde, gestion.nb_voyageur_tot)
            Signal.Afficher()
            if run1:
                train_droite.Affiche()
            if run2:
                train_gauche.Affiche()
            
        
        pygame.display.flip()  # Affichage Final


if __name__ == '__main__':
    main()

