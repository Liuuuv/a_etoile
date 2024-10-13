import pygame as py
import math
import collections

py.init()
py.font.init()
py.display.set_caption("YAAAAAHOUUUUUUUUUUUUUU!")

font=py.font.SysFont('Comic Sans MS', 30)

liste_distances_possibles=["manhattan","euclidienne"]
distance="euclidienne"
deplacements_diagonaux=True


vert_clair=(150,255,150)
vert=(0,255,0)
bleu=(0,0,255)
bleu_clair=(100,100,255)
noir=(0,0,0)
blanc=(255,255,255)
rouge=(255,0,0)
gris=(180,180,180)
gris_fonce=(100,100,100)

inf=float('inf')


class Debut:
    def __init__(self,pos):
        self.pos=pos

class Fin:
    def __init__(self,pos):
        self.pos=pos

class Mur:
    def __init__(self,pos):
        self.pos=pos

class Affichage:
    def __init__(self,facteur,debut,fin):
        self.dimensions=(int(1920*facteur),int(1080*facteur))
        self.fenetre=py.display.set_mode(self.dimensions)
        self.debut=debut
        self.fin=fin
        self.taille_grille=16

        self.taille_case=self.dimensions[1]//self.taille_grille

        self.liste_murs=[]


    def dessiner_grille(self):
        UL=[0,0]
        UR=[self.taille_grille*self.taille_case,0]
        DR=[self.taille_grille*self.taille_case,self.taille_grille*self.taille_case]
        DL=[0,self.taille_grille*self.taille_case]
        py.draw.polygon(self.fenetre,gris,[UL,UR,DR,DL])
    
    def dessiner_distance(self):
        texte_surface=font.render("distance debut-fin : "+str(self.distance_totale),True,noir)
        self.fenetre.blit(texte_surface,(self.taille_grille*self.taille_case+20,0))
        
    
    def dessiner_contour_cases(self):
        epaisseur=2
        
        for j in range(self.taille_grille+1):
            
            y_debut=0
            y_fin=self.taille_case*self.taille_grille
            
            x=j*self.taille_case
            
            py.draw.line(self.fenetre,noir,[x,y_debut],[x,y_fin],epaisseur)
        
        for i in range(self.taille_grille+1):
            
            x_debut=0
            x_fin=self.taille_case*self.taille_grille
            
            y=i*self.taille_case
            
            py.draw.line(self.fenetre,noir,[x_debut,y],[x_fin,y],epaisseur)

    def dessiner_debut(self):
        UL=[debut.pos[0]*self.taille_case,debut.pos[1]*self.taille_case]
        UR=[(debut.pos[0]+1)*self.taille_case,debut.pos[1]*self.taille_case]
        DR=[(debut.pos[0]+1)*self.taille_case,(debut.pos[1]+1)*self.taille_case]
        DL=[debut.pos[0]*self.taille_case,(debut.pos[1]+1)*self.taille_case]
        py.draw.polygon(self.fenetre,vert,[UL,UR,DR,DL])

    def dessiner_fin(self):
        UL=[fin.pos[0]*self.taille_case,fin.pos[1]*self.taille_case]
        UR=[(fin.pos[0]+1)*self.taille_case,fin.pos[1]*self.taille_case]
        DR=[(fin.pos[0]+1)*self.taille_case,(fin.pos[1]+1)*self.taille_case]
        DL=[fin.pos[0]*self.taille_case,(fin.pos[1]+1)*self.taille_case]
        py.draw.polygon(self.fenetre,rouge,[UL,UR,DR,DL])

    def dessiner_murs(self):
        for pos in self.liste_murs:
            UL=[pos[0]*self.taille_case,pos[1]*self.taille_case]
            UR=[(pos[0]+1)*self.taille_case,pos[1]*self.taille_case]
            DR=[(pos[0]+1)*self.taille_case,(pos[1]+1)*self.taille_case]
            DL=[pos[0]*self.taille_case,(pos[1]+1)*self.taille_case]
            py.draw.polygon(self.fenetre,gris_fonce,[UL,UR,DR,DL])

    def dessiner_chemin(self,chemin):
        if chemin is None:
            return
        for pos in chemin:
            if pos!=debut.pos and pos!=fin.pos:
                UL=[pos[0]*self.taille_case,pos[1]*self.taille_case]
                UR=[(pos[0]+1)*self.taille_case,pos[1]*self.taille_case]
                DR=[(pos[0]+1)*self.taille_case,(pos[1]+1)*self.taille_case]
                DL=[pos[0]*self.taille_case,(pos[1]+1)*self.taille_case]
                py.draw.polygon(self.fenetre,bleu_clair,[UL,UR,DR,DL])
    
    def position_souris_grille(self):
        position_souris=py.mouse.get_pos()
        return [position_souris[0]//self.taille_case,position_souris[1]//self.taille_case]
    
    def mettre_a_jour_positions(self):
        
        # inputs clavier
        liste_clavier_pressees=py.key.get_pressed()
        
        if liste_clavier_pressees[py.K_m]:
        
            position_souris_grille=self.position_souris_grille()
            
            if not position_souris_grille in self.liste_murs:
                self.liste_murs.append(position_souris_grille)
            
        
        elif liste_clavier_pressees[py.K_l]:
            
            position_souris_grille=self.position_souris_grille()
            
            if position_souris_grille in self.liste_murs:
                self.liste_murs.remove(position_souris_grille)
                
        
        # flemme d'interpoler le mouvement de la souris pour rendre confortable les placements rapides
            
        
        
        # souris
        liste_souris_pressees=py.mouse.get_pressed()
        
        
        if liste_souris_pressees[0]:
            
            position_souris_grille=self.position_souris_grille()
            self.debut.pos=position_souris_grille
            

        if liste_souris_pressees[2]:
            
            position_souris_grille=self.position_souris_grille()
            self.fin.pos=position_souris_grille
            

    def voisins(self,pos):
        liste_voisins=[]
        for j in range(-1,2):
            for i in range(-1,2):
                if pos[0]+j>=0 and pos[0]+j<=self.taille_grille-1 and pos[1]+i>=0 and pos[1]+i<=self.taille_grille-1:
                    if deplacements_diagonaux:
                        liste_voisins.append([pos[0]+j,pos[1]+i])
                    else:
                        if i*j==0:
                            liste_voisins.append([pos[0]+j,pos[1]+i])
                    # liste_voisins.append([pos[0]+j,pos[1]+i])
        return(liste_voisins)

    def distance(self,pos1,pos2):
        
        if distance=="manhattan":
            return(math.fabs(pos1[0]-pos2[0])+math.fabs(pos1[1]-pos2[1]))
        
        elif distance=="euclidienne":
            return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)



    def a_star(self):
        cases_explorees=[]
        cases_accessibles=[debut.pos[:]]
        dico_couts={(debut.pos[0],debut.pos[1]):self.distance(debut.pos,fin.pos)}
        dico_poids={(debut.pos[0],debut.pos[1]):0}
        dico_parents={}

        while cases_accessibles!=[]:
            pos=min(cases_accessibles,key=lambda p:dico_couts[(p[0],p[1])])
            cases_accessibles.remove(pos)
            cases_explorees.append(pos[:])
            

            # si c'est fini
            if pos==fin.pos:
                chemin=[[pos[0],pos[1]]]
                while (chemin[-1][0],chemin[-1][1]) in dico_parents:
                    chemin.append(dico_parents[(chemin[-1][0],chemin[-1][1])])
                chemin.reverse()
                
                return chemin

            liste_voisins=self.voisins(pos)
            
            for voisin in liste_voisins:
                if voisin in self.liste_murs or voisin in cases_explorees:
                    continue
                    
                    
                    
                poids=dico_poids[(pos[0],pos[1])]+self.distance(pos,voisin)
                cout=poids+self.distance(voisin,self.fin.pos)
                
                if (voisin[0],voisin[1]) not in dico_poids.keys() or poids<dico_poids[(voisin[0],voisin[1])]:
                    dico_poids[(voisin[0],voisin[1])]=poids
                    dico_couts[(voisin[0],voisin[1])]=cout
                    
                    dico_parents[(voisin[0],voisin[1])]=pos[:]
                    
                    if not voisin in cases_accessibles:
                        cases_accessibles.append(voisin)


    def loop(self):
        horloge=py.time.Clock()


        # boucle de jeu
        continuer=True
        while continuer:
            for event in py.event.get():
                if event.type==py.QUIT:
                    continuer=False
                if event.type==py.KEYDOWN:
                    
                    # quitter
                    if event.key==py.K_ESCAPE:
                        continuer=False
                        
            horloge.tick(144)
            
            self.mettre_a_jour_positions()


            self.fenetre.fill(blanc)
            self.dessiner_grille()
            self.dessiner_debut()
            self.dessiner_fin()
            self.dessiner_murs()
            

            chemin=self.a_star()
            self.dessiner_chemin(chemin)
            
            # self.dessiner_distance()
            
            self.dessiner_contour_cases()
        

            py.display.flip()

        py.quit()

debut=Debut([0,3])
fin=Fin([8,4])
affichage=Affichage(0.7,debut,fin)
affichage.loop()


# faire que s'il y a deux chemin possibles, le serpent en choisit judicieusement un