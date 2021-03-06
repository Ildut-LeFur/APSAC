import json
import time
import datetime
import glob
from os.path import basename, splitext

#là où se trouve le json
chemin = "../EyeTracker/info.player.json"
chemin2 = "../SimulateurIPG/Log"
#on ouvre le json
with open(chemin) as json_data:
  #pour lire ce qui a dedans et mettre le contenu dans un dictionnaire
	data_dict = json.load(json_data)

#récupération des données
#donnée propre à l'appareil utiliser, commencement du record en seconde dans le référentiel de l'appareil
def get_start_time_synced_s():
	return(data_dict["start_time_synced_s"])

#donnée représentant le commencement du début du record dans le référentiel du monde avec l'heure UNIX en seconde
def get_start_time_system_s():
	return(data_dict["start_time_system_s"])

#donnée représentant le commencement de la simulation du point de vue du simulateur de voiture
def get_start_time_simulateur_s():
  filepath = glob.glob('../SimulateurIPG/Log/*.txt')[0]
  filename = splitext(basename(filepath))[0]
  file = open('../SimulateurIPG/Log/'+filename+'.txt', "r")
  for line in file:
    if 'SIM_START' in line:
      listeTime = line[-20:-1]
      break
  file.close()

  année = ""
  str1 = listeTime[0:4]
  année = int(année.join(str1))
  mois = ""
  str1 = listeTime[5:7]
  mois = int(mois.join(str1))
  jour = ""
  str1 = listeTime[8:10]
  jour = int(jour.join(str1))
  heure = ""
  str1 = listeTime[11:13]
  heure = int(heure.join(str1))
  minute = ""
  str1 = listeTime[14:16]
  minute = int(minute.join(str1))
  seconde = ""
  str1 = listeTime[17:19]
  seconde = int(seconde.join(str1))

  dt = datetime.datetime(année, mois, jour, heure, minute, seconde)
  timestamp = dt.replace(tzinfo=datetime.timezone.utc).timestamp()
  return(timestamp)