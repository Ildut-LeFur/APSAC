#importation des modules
import stat
import getTime
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

#fonction principale du module statistique
def statistique(nombre, listeDebut, listeFin):
  #variable compteur
  i = 0
  #création de liste pour stocker les résultats et ensuite les plot
  listeFreqClign = []
  listeDispersion = []
  listeMoyenneDiametrePupille = []
  listeMaxDiametrePupille = []
  listeMinDiametrePupille = []
  listeMouvementFixation = []
  #création de la ligne des noms de colonnes
  stat = pd.DataFrame(columns=['Debut/Fin','FrequenceClignement','MoyenneDispersion','MoyenneDiametrePupille','MaxDiametrePupille','MinDiametrePupille','InterQuantileMouvementFixation'])
  #boucle jusqua ce que le compteur atteigne la valeur du nombre d'intervalle que l'utilisateur veut analyser
  while i < nombre :
    #On ajoute chaque statistique une par une dans chaque liste
    listeFreqClign.append(freqClignement(listeDebut[i],listeFin[i]-listeDebut[i]))
    listeDispersion.append(dispersion(listeDebut[i],listeFin[i]-listeDebut[i]))
    listeMoyenneDiametrePupille.append(DiametrePupille(listeDebut[i],listeFin[i]-listeDebut[i])[0])
    listeMaxDiametrePupille.append(DiametrePupille(listeDebut[i],listeFin[i]-listeDebut[i])[1])
    listeMinDiametrePupille.append(DiametrePupille(listeDebut[i],listeFin[i]-listeDebut[i])[2])
    listeMouvementFixation.append(mouvementFixation(listeDebut[i],listeFin[i]-listeDebut[i]))
    #Quelque chose de plus jolie pour mieux représenter l'intervalle
    txt = str(listeDebut[i])+'/'+str(listeFin[i])
    #Création de la ligne à partir des autres listes
    newRow =  {'Debut/Fin':txt,'FrequenceClignement':str(listeFreqClign[i])+' Hz','MoyenneDispersion':str(listeDispersion[i])+' cm','MoyenneDiametrePupille':listeMoyenneDiametrePupille[i],'MaxDiametrePupille':listeMaxDiametrePupille[i],'MinDiametrePupille':listeMoyenneDiametrePupille[i],'InterQuantileMouvementFixation':listeMouvementFixation[i]}
    #On ajoute la ligne fraichement crée
    stat = stat.append(newRow, ignore_index=True)
    #incrémentation
    i += 1
  #création du csv
  stat.to_csv('../SortiePython/statistique.csv', index = False)

#calcul de tout les stats par rapport au diamètre de la pupille
def DiametrePupille(debut, duration):
  #lecture csv
  df = pd.read_csv('../SortiePython/pupil_positions_filtred_t_c.csv')
  #on récupère la valeur en seconde de quand à commencer l'enregistrement des données sur Pupil Player
  startTimeUnix = getTime.get_start_time_system_s()
  #On ne prends que les valeurs situées dans l'intervalle
  df = df[(df['pupil_timestamp']>=(debut+startTimeUnix)) & (df['pupil_timestamp']<=(debut+duration+startTimeUnix))]
  #calcul des valeurs intéressantes
  moyenneDiametrePupille = df['diameter'].mean()
  maxDiametrePupille = df['diameter'].max()
  minDiametrePupille = df['diameter'].min()
  #On arrondis les valeurs pour rendre ça plus beau
  moyenneDiametrePupille = np.around(moyenneDiametrePupille, decimals=1)
  maxDiametrePupille = np.around(maxDiametrePupille, decimals=1)
  minDiametrePupille = np.around(minDiametrePupille, decimals=1)
  #création de la liste regroupant les valeurs intéressantes
  diametrePupille = [moyenneDiametrePupille, maxDiametrePupille, minDiametrePupille]
  return(diametrePupille)


#fonction permettant de calculer la fréquence de clignement des yeux sur un intervalle donné
#debut : instant t ou commence l'analyse, duration : durée de l'analyse
def freqClignement(debut, duration):
  #lecture du csv voulu
  df =  pd.read_csv('../SortiePython/blinks_filtred_t_a.csv')
  #on récupère la valeur en seconde de quand à commencer l'enregistrement des données sur Pupil Player
  startTimeUnix = getTime.get_start_time_system_s()
  #on récupère chaque index correspondant à un clignement se situant entre le moment on l'on commence l'analyse jusque sa fin
  index = df[(df['start_timestamp'] > (debut+startTimeUnix)) & (df['start_timestamp'] < (debut+startTimeUnix+duration))].index.tolist()
  #Calcule de la fréquence
  fréquence = len(index)/duration
  fréquence = np.around(fréquence, decimals=1)
  print('Il a eu ' , len(index) , ' clignement(s) depuis la seconde ' , debut , ' pendant ' , duration , ' seconde(s)\nPour une fréquence de : ' , fréquence , ' Hz' )
  return(fréquence)

#fonction permettant de calculer le pourcentage de temps passé à regarder les surfaces enregistrées
def pourcentageSurface():
  #lecture du csv voulu
  df = pd.read_csv('../EyeTracker/exports/000/surfaces/surface_gaze_distribution.csv')
  #on récupère les colonnes du csv pour avoir le nombre total de regard récupéré par l'application
  columns = df.columns  
  #totalité : nombre total de regard récupéré par l'application, utile pour le calcul de la fréquence
  totalite = float(columns[1])
  #variable compteur
  count = 0
  #création des listes pour les noms des surfaces ainsi que toutes les fois correspondantes où l'on regarde cette surface.
  nomSurface = []
  nombreRegard = []
  #on parcours le csv
  for label, row in df.iterrows():
    #ne pas prendre la première ligne car ce ne sont pas ces données que nou voulons
    if count != 0 :
      #on récupère le nom de la surface
      nomSurface.append(row[0])
      #ainsi que le nombre d'instant récupéré lié à cette surface
      nombreRegard.append(float(row[1]))
    #incrémentation
    count += 1
  #encore une variable de compteur
  i = 0
  #on passe la liste en array pour pouvoir la manipuler plus facilement grace à numpy
  arrayNombreRegard = np.array(nombreRegard)
  #Calcule du pourcentage de temps passé à regarder la surface
  nombreRegard = (arrayNombreRegard * 100)/totalite
  #on arrondi les valeurs présentent dans la liste pour que ce soit plus visible
  nombreRegard = np.around(nombreRegard, decimals=1)
  #Affichage
  while i < len(nomSurface) :
    print('La surface '+nomSurface[i]+' a été regardé pendant ', nombreRegard[i],'pourcents du temps')
    i += 1

def dispersion(debut, duration):
  #lecture du csv
  df = pd.read_csv('../SortiePython/fixations_filtred_t_c.csv')
  #on récupère la valeur en seconde de quand à commencer l'enregistrement des données sur Pupil Player
  startTimeUnix = getTime.get_start_time_system_s()
  #On ne prends que les valeurs situées dans l'intervalle
  df = df[(df['start_timestamp']>=(debut+startTimeUnix)) & (df['start_timestamp']<=(debut+duration+startTimeUnix))]
  #calcul des valeurs intéressantes
  moyenneDispersion = df['dispersion'].mean()
  #on arrondie les valeurs précédentes
  moyenneDispersion = np.around(moyenneDispersion, decimals=1)
  print('La moyenne de la dispersion du regard est de' , moyenneDispersion, 'depuis la seconde ' , debut , ' pendant ' , duration , 'seconde(s)' )
  return(moyenneDispersion)

def mouvementFixation(debut, duration):
  df = pd.read_csv('../SortiePython/fixations_filtred_t_c.csv')
  startTimeUnix = getTime.get_start_time_system_s()
  df = df[(df['start_timestamp']>=(debut+startTimeUnix)) & (df['start_timestamp']<=(debut+duration+startTimeUnix))]
  listeNorme = []
  i = 0
  print('PLOOOOOOOOOP    ',df.loc[df.index[0],'norm_pos_x'])
  while i < len(df)-1 :
    deplacementX = abs(df.loc[df.index[i],'norm_pos_x']-df.loc[df.index[i+1],'norm_pos_x'])
    deplacementY = abs(df.loc[df.index[i],'norm_pos_y']-df.loc[df.index[i+1],'norm_pos_y'])
    norme = math.sqrt((deplacementX**2)+(deplacementY**2))
    listeNorme.append(norme)
    i += 1
  #On calcule le quantile représentant 25% de la probabilité
  q1 = np.quantile(listeNorme,.25)
  #On calcule le quantile représentant 75% de la probabilité
  q3 = np.quantile(listeNorme,.75)
  plt.boxplot(listeNorme)
  plt.show()
  iq_range = q3 - q1
  iq_range = np.around(iq_range, decimals=3)
  return(iq_range)