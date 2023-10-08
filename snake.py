import pygame
import math
import random

NOIR    = (0, 0, 0)
BLANC   = (255, 255, 255)
GRIS    = (110, 113, 127)
ROUGE   = (255, 0, 0)
BLEU    = (10, 147, 228)
JAUNE   = (235, 235, 0)
VERT    = (75, 195, 0)
VERT_MANGE = (150, 195, 0)

LARGEUR_SERPENT = 60

FENETRE_HAUTEUR = 1800//3
FENETRE_LARGEUR = 2400//3

VITESSE = 10
POSITION_INIT = [FENETRE_LARGEUR//2, FENETRE_HAUTEUR//2]
TAILLE_INIT = 3
TAILLE_BORDURE = 60
NOURRITURE_RAYON = 30


fini = False
gameover = False
compteur = 0
enPause = False

#---Initialisation---#

def nouveauSerpent():
    return{
    'position': [POSITION_INIT[0], POSITION_INIT[1]],
    'vitesse': VITESSE,
    'taille': TAILLE_INIT,
    'corps': [],
    'direction': 'right',
    'direction_precedente': 'right',
    'position_grandir':[0, 0]
    }

def initialisationCompteur():
    global compteur
    compteur = 0

def nouvellePartieCorps(position):
    return{
    'position': position
    }

def initialisationCorps():
    global serpent
    serpent['corps'].append(nouvellePartieCorps(POSITION_INIT))
    serpent['corps'].append(nouvellePartieCorps([POSITION_INIT[0]-LARGEUR_SERPENT, POSITION_INIT[1]]))
    serpent['corps'].append(nouvellePartieCorps([POSITION_INIT[0]-2*LARGEUR_SERPENT, POSITION_INIT[1]]))

def nouvelleNourriture():
    return{
    'position': [-1, -1],
    'visible': True
    }

def emplacementNourriture(serpent):
    recherche = True
    position = [-1, -1]
    while recherche:
        position[0] = random.randint(0, 37)*60 + 60
        position[1] = random.randint(0, 27)*60 + 60
        for i in range(0, serpent['taille']):
            if not position[0]==serpent['corps'][i]['position'][0] and not position[1]==serpent['corps'][i]['position'][1]:
                recherche=False
                i=serpent['taille']
    return position

#---Fin Initialisation Serpent

#---Affichage---#

def affichageSerpent():
    global serpent
    pygame.draw.rect(fenetre, NOIR, (serpent['position'][0], serpent['position'][1], LARGEUR_SERPENT, LARGEUR_SERPENT))
    for i in range(1, serpent['taille']):
        pygame.draw.rect(fenetre, VERT, (serpent['corps'][i]['position'][0], serpent['corps'][i]['position'][1], LARGEUR_SERPENT, LARGEUR_SERPENT))
        if serpent['corps'][i]['position']==serpent['position_grandir']:
            pygame.draw.rect(fenetre, VERT_MANGE, (serpent['corps'][i]['position'][0], serpent['corps'][i]['position'][1], LARGEUR_SERPENT, LARGEUR_SERPENT))

def affichageBordures():
    pygame.draw.rect(fenetre, BLANC, (0, 0, TAILLE_BORDURE, FENETRE_HAUTEUR))
    pygame.draw.rect(fenetre, BLANC, (TAILLE_BORDURE, 0, FENETRE_LARGEUR-TAILLE_BORDURE, TAILLE_BORDURE))
    pygame.draw.rect(fenetre, BLANC, (FENETRE_LARGEUR-TAILLE_BORDURE, TAILLE_BORDURE, TAILLE_BORDURE, FENETRE_HAUTEUR - TAILLE_BORDURE))
    pygame.draw.rect(fenetre, BLANC, (TAILLE_BORDURE, FENETRE_HAUTEUR - TAILLE_BORDURE, FENETRE_LARGEUR-2*TAILLE_BORDURE, TAILLE_BORDURE))

def affichageNourriture(nourriture):
    pygame.draw.circle(fenetre, ROUGE, (nourriture['position'][0] + NOURRITURE_RAYON, nourriture['position'][1] + NOURRITURE_RAYON), NOURRITURE_RAYON )

def affichage(nourriture, serpent):
    global enPause
    affichageBordures()
    affichageNourriture(nourriture)
    affichageSerpent()
    if enPause:
        police = pygame.font.Font("Ailerons-Typeface.otf", FENETRE_LARGEUR // 17)
        texte = police.render("Pause", True, NOIR)
        texteL, texteH = police.size("Pause")
        position_texte = [(FENETRE_LARGEUR - texteL) // 2, (FENETRE_HAUTEUR - texteH) // 6]
        fenetre.blit(texte, position_texte)
    elif gameover:
        police = pygame.font.Font("Ailerons-Typeface.otf", FENETRE_LARGEUR // 17)
        texte = police.render("Game Over", True, NOIR)
        texteL, texteH = police.size("Gamge Over")
        position_texte = [(FENETRE_LARGEUR - texteL) // 2, (FENETRE_HAUTEUR - texteH) // 6]
        fenetre.blit(texte, position_texte)

#---FIN Affichage---#

#---Gestion Mouvements---#

def miseAJourSerpent():
    global compteur, serpent, gameover
    tuple_intermediaire = [0, 0]
    testgrandir = 0
    direction=serpent['direction']
    if not compteur%serpent['vitesse']:
        compteur = 0
        serpent['direction_precedente']=direction
        if verifGrandir():
            testgrandir = 1
        for i in range(serpent['taille']-1, 0, -1):
            tuple_intermediaire[0] = serpent['corps'][i-1]['position'][0]
            tuple_intermediaire[1] = serpent['corps'][i-1]['position'][1]
            serpent['corps'][i]['position'][0]=tuple_intermediaire[0]
            serpent['corps'][i]['position'][1]=tuple_intermediaire[1]

        if serpent['direction']=='up':
            serpent['position'][1]-=LARGEUR_SERPENT
            serpent['corps'][0]['position'][1]-=LARGEUR_SERPENT
        elif serpent['direction']=='down':
            serpent['position'][1]+=LARGEUR_SERPENT
            serpent['corps'][0]['position'][1]+=LARGEUR_SERPENT
        elif serpent['direction']=='right':
            serpent['position'][0]+=LARGEUR_SERPENT
            serpent['corps'][0]['position'][0]+=LARGEUR_SERPENT
        elif serpent['direction']=='left':
            serpent['position'][0]-=LARGEUR_SERPENT
            serpent['corps'][0]['position'][0]-=LARGEUR_SERPENT
        if testgrandir==1:
            grandir()
            serpent['position_grandir']=[-1, -1]

        for i in range(1, serpent['taille']):
            if serpent['corps'][0]['position']==serpent['corps'][i]['position']:
                gameover = True
        verificationSortieEcran()

def verificationSortieEcran():
    global gameover, serpent
    if serpent['position'][0]>=FENETRE_LARGEUR-TAILLE_BORDURE:
        gameover=True
    elif serpent['position'][1]>=FENETRE_HAUTEUR-TAILLE_BORDURE:
        gameover=True
    elif serpent['position'][0]<=0:
        gameover=True
    elif serpent['position'][1]<=0:
        gameover=True

#---FIN Gestion Mouvements---#

def gestionEntree():
    global fini, serpent, enPause
    for evenement in pygame.event.get():
        if evenement.type==pygame.QUIT:
            fini=True
        elif evenement.type==pygame.KEYDOWN:
            gestionDirection(evenement)
            if evenement.key==pygame.K_ESCAPE:
                if not gameover:
                    if enPause:
                        enPause = False
                    else:
                        enPause = True

def gestionDirection(evenement):
    global serpent
    if evenement.key==pygame.K_UP and not serpent['direction_precedente']=='down':
        serpent['direction']='up'
    elif evenement.key==pygame.K_DOWN and not serpent['direction_precedente']=='up':
        serpent['direction']='down'
    elif evenement.key==pygame.K_RIGHT and not serpent['direction_precedente']=='left':
        serpent['direction']='right'
    elif evenement.key==pygame.K_LEFT and not serpent['direction_precedente']=='right':
        serpent['direction']='left'

#---Nourriture/Score---#

def mangerNourriture():
    global nourriture, serpent
    if serpent['position'][0]==nourriture['position'][0] and serpent['position'][1]==nourriture['position'][1]:
        nourriture['visible']=False
        serpent['position_grandir']=nourriture['position']

def verifGrandir():
    global serpent
    taille = serpent['taille']
    if serpent['corps'][taille-1]['position'][0]==serpent['position_grandir'][0]:
        if serpent['corps'][taille-1]['position'][1]==serpent['position_grandir'][1]:
            return True
    return False

def grandir():
    global serpent
    serpent['corps'].append(nouvellePartieCorps(serpent['position_grandir']))
    serpent['taille']+=1

#---FIN Nourriture/Score---#


pygame.init()

temps = pygame.time.Clock()

fenetre_taille = [FENETRE_LARGEUR, FENETRE_HAUTEUR]
fenetre = pygame.display.set_mode(fenetre_taille)
pygame.display.set_caption('Snake')

serpent = nouveauSerpent()
initialisationCorps()
nourriture = nouvelleNourriture()
nourriture['position'] = emplacementNourriture(serpent)

while not fini:
    compteur+=1

    fenetre.fill(GRIS)

    gestionEntree()
    if not enPause and not gameover:
        miseAJourSerpent()

    mangerNourriture()
    if nourriture['visible'] == False:
        nourriture['visible'] = True
        nourriture['position'] = emplacementNourriture(serpent)
    affichage(nourriture, serpent)

    pygame.display.flip()
    temps.tick(60)

pygame.display.quit()
pygame.quit()
exit()
