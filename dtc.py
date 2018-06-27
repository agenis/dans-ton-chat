# -*- coding: latin-1 -*-
"""
Created on 2018/03/18
Ce script permet de webscrapper le site danstonchat et faire des stats dessus.
@author: Marc.AGENIS-NEVERS
"""
# This is python 3.6 beware!
# environment path C:\Bib\Prod\Miniconda3-64

# packages import
import requests
#from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import os
import unicodedata
import statsmodels.formula.api as sm
import statsmodels
from numpy import *

os.chdir(r'C:\Users\user\Desktop\dtc')
#test = pd.DataFrame({"r":[10, 20], "b":[2, 3]})
#with open('test.json', 'w') as f:
#    f.write(test.to_json(orient='records', lines=True))
def see(id):
    if len(result[result.id_quote==id])==0:
        print("no such quote Id")
        return(None)
    print(result[result.id_quote==id].rtue.iloc[0])
    
def ExtractFromPage(page):
    r = requests.get("https://danstonchat.com/latest/" + str(page) + ".html")
    soup = BeautifulSoup(r.content, 'html.parser')
    res1 = soup.find_all('div', attrs={'class':'addthis_inline_share_toolbox'})
    res2 = soup.find_all("span", attrs={'class': "score"})
    res3 = soup.find_all("span", attrs={'class': "comments"})
    res4 = soup.find_all('div', attrs={'class':'item-content'})
    # texte brut sous forme de liste 1 element par ligne (attention encodage!)
    raw_texte = [i["data-description"].split("\n") for i in res1] # longueur 25 => attention ici on crée une liste avec un élement par ligne
    # score de la quote (2 entiers)
    score_pos = [int(re.findall(": ([0-9]+) /", i.text)[0]) for i in res2] # longueur 25
    score_neg = [int(re.findall("/ ([0-9]+)", i.text)[0]) for i in res2] # longueur 25
    # nombre de commentaires (entier)
    comments = [int(re.findall("[0-9]+ ", i.text)[0]) for i in res3] # longueur 25
    # nombre de lignes dans la quote
    nb_lignes = [len(i) for i in raw_texte] # longueur 25
    # numero de la quote
    id_quote = [int(i.find('a')['href'].split(".com/")[1].split(".")[0]) for i in res4] # longueur 25
    # transformer tout ca en PANDA
    temp = pd.DataFrame(
        {'id_quote': id_quote,
         'raw_texte': raw_texte,
         'nb_lignes': nb_lignes,
         'comments': comments,
         'score_pos': score_pos,
         'score_neg': score_neg
        })
    return(temp)
## MAKE THE LOOP
#result = ExtractFromPage(1)
#for page_num in np.r_[2:775]:
#    print("page_num", page_num)
#    temp = ExtractFromPage(page_num)
#    result = result.append(temp)
#    # integrer du code pour faire un sleep.time...

## creer le JSON exporte une fois fini
#with open('result.json', 'w') as f:
#	f.write(result.to_json(orient="records", lines=True))

############################################
# charger le panda/json 
result = pd.read_json("result.json", orient="records", lines=True)

# renommer en plus court..
result.rename(columns = {'raw_texte':'rt'}, inplace=True)
# le texte est stocké dans une colonne qui contient une liste par ligne, chaque liste contenant autant d'élements que de lignes de citation
# on va créer une colonne dédiée avec tout le texte en format string d'un seul tenant pour faciliter certaines recherches
result['rtu'] = ["\n".join(row) for row in result.rt]
# on va supprimer tous les caracteres accentues et les remplacer par des sans accents 
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
result['rtue'] = result.rtu.apply(strip_accents)
# on va chercher a compter combien d'interlocuteurs sont dans une quote
# on remarque que parfois le nom de l'interlocuteur est entre <..> parfois non et alors ca finit par des deux points ":"
# meme parfois le quote commence juste par une astérique (action utilisateur)
# parfois ya un espace dans le nom, parfois ya rien de spécial (nom brut) alors là c'est plus tendu donc on considère que c'est exclu.
# on peut vouloir signaler cet évènement ou le compter
# ca fait 4 possibilité s de regex pour récupérer le nom

# matching patterns OR condition entre 5 possibilités:
#      (?<=^<)[\S]+(?=>)     type: <Pseudo 89>... ou <Pseudo89> ...    (utilisation du non-greedy match entre les <...>)
#      ^[^>< ]+(?=[ ]?:)       type: Pseudo89:... ou Pseudo89 :...     (ici on interdit les ><)
#      (?<=^\* )[\S]+        type: * Pseudo89...
#      (?<=^\()[\S ]+?(?=\))   type: (Pseudo89)...
#      (?<=^\[)[\S ]+?(?=\])   type: [Pseudo89]...
#      ^[^>< ]+(?= dit[ ]?:)   type: Pseudo89 dit:... ou Pseudo89 dit :...
def ComputeNumberSpeakers(string):    # [re.findall("^<[a-zA-Z0-9_]+>|^[a-zA-Z0-9_]+:|^\* [a-zA-Z0-9_]+", elmt) for elmt in result.rtue[0].splitlines()]
    temp = [re.findall("(?<=^<)[\S ]+?(?=>)|^[^>< ]+(?=[ ]?:)|(?<=^\* )[\S]+|(?<=^\()[\S ]+?(?=\))|(?<=^\[)[\S ]+?(?=\])", elmt) for elmt in string.splitlines()]
    return(len(list(np.unique(temp))))
def ComputeSpeakers(string):    # [re.findall("^<[a-zA-Z0-9_]+>|^[a-zA-Z0-9_]+:|^\* [a-zA-Z0-9_]+", elmt) for elmt in result.rtue[0].splitlines()]
    temp = [re.findall("(?<=^<)[\S ]+?(?=>)|^[^>< ]+(?=[ ]?:)|(?<=^\* )[\S]+|(?<=^\()[\S ]+?(?=\))|(?<=^\[)[\S ]+?(?=\])|^[^>< ]+(?= dit[ ]?:)", elmt) for elmt in string.splitlines()]
    return(list(np.unique(temp)))
result["speak"] = result.rtue.apply(ComputeSpeakers)
result["nb_speak"] = result.speak.apply(len)
# check the numbers
import matplotlib.pyplot as plt
n, bins, patches = plt.hist(result.nb_speak, 'auto', facecolor='blue', alpha=0.5)
plt.show()
result.nb_speak.value_counts()
# check quels cas ont été ratés par la détection de speaker
result.query('nb_speak==0').rtue
# on met en valuer manquante les comptes à zéro
result.nb_speak = result.nb_speak.apply(lambda x: np.nan if x == 0 else x)
import pylab
pylab.hist(result.nb_speak[~ np.isnan(result.nb_speak)], bins=15)
# analyse de correlations
result[['comments', 'nb_speak', 'score_pos', 'score_neg', 'nb_lignes', 'id_quote']].corr() # comments seem linked to time
import datetime
plt.plot(result.id_quote, result.comments)
# ou une anova
import statsmodels.api as sm
from statsmodels.formula.api import ols
fitted=ols('score_neg ~ comments + nb_lignes + nb_speak', data=result).fit() #Specify C for Categorical
print(sm.stats.anova_lm(fitted, typ=2))

######## special quotes
# le plus de commentaires
result.query('comments>=250')
result.query('nb_lignes>=50')
result.query('score_pos>=50000')
result.query('score_neg>=10000')
result.query('nb_speak>=15')
result.query('(score_neg/score_pos)>4')
# tendances de long terme (pas d'échelle temporelle malheuerusement)

# variable facteur sur le nombre d'interlocuteurs
result['nb_speak_factor'] = result.nb_speak.apply(lambda x: 'un' if x==1 else "deux" if x==2 else "plusieurs")
# petit modele lineaire
y=result.score_pos
X=result[["comments", "nb_lignes", "nb_speak"]].values
X=statsmodels.tools.tools.add_constant(X)
fit = sm.OLS(y, X)
fitted = fit.fit()
fitted.summary()

# DIRE QU'AVEC Tweeter on peut partiellement remonter la datation des quotes qui n'est pas accessible sinon.



# creer un facteur pour les quotes contenant un message offline
def ComputeOffline(string):    # [re.findall("^<[a-zA-Z0-9_]+>|^[a-zA-Z0-9_]+:|^\* [a-zA-Z0-9_]+", elmt) for elmt in result.rtue[0].splitlines()]
    temp = [len(re.findall("^\* ", elmt))>0 for elmt in string.splitlines()]
    return(any(temp))
result["has_offline"] = result.rtue.apply(ComputeOffline)
fitted=ols('score_pos ~ nb_lignes + C(nb_speak_factor) + has_offline + id_quote', data=result).fit()
print(sm.stats.anova_lm(fitted, typ=2))


# certains mots
def ComputeString(string, match):    # [re.findall("^<[a-zA-Z0-9_]+>|^[a-zA-Z0-9_]+:|^\* [a-zA-Z0-9_]+", elmt) for elmt in result.rtue[0].splitlines()]
    temp = [len(re.findall(match, elmt))>0 for elmt in string.splitlines()]
    return(any(temp))
result["w_bite"] = result.rtue.apply(ComputeString, match="bite")
result["w_pr0n"] = result.rtue.apply(ComputeString, match="pr0n")
result["w_cours"] = result.rtue.apply(ComputeString, match="cours")
result["w_cours"] = result.rtue.apply(ComputeString, match="cours")

ols('score_pos ~ nb_lignes + C(nb_speak_factor) + has_offline + id_quote + w_bite + w_pr0n + w_cours', data=result).fit().summary()
# qq bonnes quotes selon le modèle linéaire:
result.query('nb_speak==2 & has_offline==True & w_pr0n==True')

#¼ idées
# faire une colonne avec que les quotes sans les pseudos
# faire une ACP
# etudier les smileys, etudier les oooo
# etudier certains mots: pr0n, cours, etc.
# palmares des speakers
# toutes les orthographes possibles de tel mot...
# faire un modèle logistique sur les quotes à votes positif ou négatif (ou un arbre de régression)


# Politique
result["Hollande"] = result.rtue.apply(ComputeString, match="[Hh]ollande")

def seeword(pattern, maxnum=10, full=True):
    temp = result[["rtue", "id_quote", "comments", "score_neg", "score_pos"]].copy()
    temp["pattern"] = temp.rtue.apply(ComputeString, match=pattern)
    print("nombre de matches:", temp.pattern.value_counts())
    temp = temp.query("pattern==True")
    if full==True:
        print("first full quotes:")
        for i in range(min(maxnum, len(temp))):
            print(temp.rtue.iloc[i])
            print("")
    return(temp.head(maxnum))


# la politique est très peu présente sur DTC, pour des raisons éditoriales ou 
# bien purement intrinsèques (moins fun, moins le sujet de préoccupation des jeunes des forums, etC.)
# pas facile de prévoir les fautes de frappe!
seeword("[Hh]oll?ande?", full=False)   #8 (dont 3FP)
seeword("[Hh]oll?ande", full=False)   #5 (mais il en manque au moins 1)
seeword("[sS]ocialiste")    # 5
seeword("[sS]arko|[sS]arkozy") # 17
seeword("UMP|[' ]ump", 10)   #4
seeword("les ecolos?|EELV", 10) #1
seeword("[cC]hirac ", 10) #2
seeword("[rR][eé]publicains?", 10) # 2 dont 1FP
seeword("[lL]e [pP]en[^a-zA-Z]", 10) # 6
seeword(" FN[^a-zA-Z]") # 3
seeword("[Mm]odem ", 10) # 3 dont 2FP
seeword("[Mm]erkel", 10) #2
seeword("[oO]bama", 10) #8
seeword("[bB]ush", 10) #3 dont 1FP
seeword("[kK]en?nedy", 10) #2
seeword("[' ][Eeé]l[éel]ction", 10) # 9 dont 1FP
# et les nuls:
seeword("[mM]acron", 10)   #0
seeword("[Cc]linton", 10) #0
seeword("[bB]erlusconi", 10) #0
seeword(" [aA]ignan", 10) #0
seeword("[' ]UPR[^a-zA-Z]|ass?elineau") # 0
seeword("[vV]all?s[^a-zA-Z]", 10) #0
seeword("[pP]remier [mM]inistre") #0
seeword("[fF]ront [nN]ational") #0
seeword(" LR", 10) # 0
seeword("les verts", 10) #0 
seeword("[fF]illon ", 10) #0
seeword("[vV]alls", 10) #0
seeword("[tT]rump|TRUMP", 10) # 1FP
# est-ce que ca fait plus ou moins de succès qu'en moyenne? (ou commentaires)
# RBIND de tous les résultats (ou simplement on concatene les recherches?)

res_pol = seeword("[Hh]oll?ande|[sS]ocialiste|[sS]arko|[sS]arkozy|UMP|[' ]ump|les ecolos?|EELV|[cC]hirac |[rR][eé]publicains?|[lL]e [pP]en[^a-zA-Z]| FN[^a-zA-Z]|[Mm]odem |[Mm]erkel|[oO]bama|[bB]ush|[kK]en?nedy|[' ][Eeé]l[éel]ction", 1000)
res_pol.score_pos.apply(["median", "mean"])
result.score_pos.apply(["median", "mean"])
# score positif bien pourri comparé a la médiane?
res_pol.score_neg.apply(["median", "mean"])
result.score_neg.apply(["median", "mean"])
res_pol.comments.apply(["median", "mean"])
result.comments.apply(["median", "mean"])
# 

#  BASE DE DONNEES TEMPORELLES. la plus récente 19705
d = {'19699': '2018-04-23',
     '19689': '2018-04-23',
     '19646': '2018-03-29',
     '19604': '2018-03-01',
     '19531': '2018-01-29',
     '19449': '2017-23-12',
     '19346': '2017-11-27',
     '19273': '2017-10-30',
     '19166': '2017-10-02',
     '19075': '2017-09-02',
     '18990': '2017-08-25',
     '18892': '2017-07-23',
     '18844': '2017-06-26'}
     # 9 juin 2009: 10 000 quotes..


# creer le JSON exporte une fois fini
with open('result_traite.json', 'w') as f:
	f.write(result.to_json(orient="records", lines=True))
result.to_csv("result_traite.csv")

    
# ET LES SMILEYS???

len(seeword("\:\-\)", maxnum=1000, full=False).rtue) # :-)
len(seeword("\:\)", maxnum=1000, full=False).rtue) # :-)

len(seeword("\;\-\)", maxnum=1000, full=False).rtue) # ;-)
len(seeword("\;\)", maxnum=1000, full=False).rtue) # ;-)

len(seeword("\:\-\(", maxnum=1000, full=False).rtue) # :-(
len(seeword("\:\(", maxnum=1000, full=False).rtue) # :(

len(seeword("\:\[", maxnum=1000, full=False).rtue) # :[
      
len(seeword("\:\/", maxnum=1000, full=False).rtue) # :/

len(seeword("\>\<", maxnum=1000, full=False).rtue) # ><

len(seeword("oO|Oo", maxnum=1000, full=False).rtue) # oO
len(seeword("Oo", maxnum=1000, full=False).rtue) # oO
len(seeword("O_o|o_O", maxnum=1000, full=False).rtue) # o_O
len(seeword("O[_]+o", maxnum=1000, full=False).rtue) # o_...O

len(seeword("\:[oO]", maxnum=1000, full=False).rtue) # :O

len(seeword("[xX]D", maxnum=1000, full=False).rtue) # xD
len(seeword("[xX]\)", maxnum=1000, full=False).rtue) # x)

len(seeword(":D", maxnum=1000, full=False).rtue) # :D
len(seeword("=D", maxnum=1000, full=False).rtue) # =D

len(seeword(":p", maxnum=1000, full=False).rtue) # :p
len(seeword(":-p", maxnum=1000, full=False).rtue) # :-p

len(seeword("\^\^", maxnum=1000, full=False).rtue) # ^^

len(seeword("-_-", maxnum=1000, full=False).rtue) # 
len(seeword("-__-", maxnum=1000, full=False).rtue) # 
len(seeword("-___-", maxnum=1000, full=False).rtue) # 
len(seeword("-____-", maxnum=1000, full=False).rtue) # 
len(seeword("-_____-", maxnum=1000, full=False).rtue) # 
len(seeword("-______-", maxnum=1000, full=False).rtue) #
 
len(seeword("\.\_\.", maxnum=1000, full=False).rtue) #  ._.

len(seeword("\\\[oO]/", maxnum=1000, full=False).rtue) # \o/

len(seeword("[oO]h", maxnum=1000, full=False).rtue) # oh



# les exclamations

questionmark = [len(seeword(i, maxnum=20000, full=False).rtue)  for i in [re.escape("?") * i for i in range(1, 100)]]
exclamation  = [len(seeword(i, maxnum=20000, full=False).rtue)  for i in [re.escape("!") * i for i in range(1, 100)]]

# classement des top pseudos
flat_list = [item for sublist in result.speak for item in sublist]
flat_list = list(filter(None, flat_list))
flat_list2 = []
for item in flat_list:
    if type(item)!=list:
        flat_list2.append(item)
from collections import Counter
allspeak = dict(Counter(flat_list2))
sorted(allspeak.items(), key=operator.itemgetter(1), reverse=True)[:50]
dict(Counter(flat_list2).most_common(50))

## nombre d'interlocuteurs et nombre de likes
result.groupby("nb_speak_factor").agg({"score_pos":"median"})









































from matplotlib.dates import strpdate2num
lon, lat, time = np.loadtxt('data.txt', skiprows=1,
        converters={2:strpdate2num('%H:%M:%S')}, unpack=True)     
dd=pd.DataFrame(d.items(), columns=['id_quote', 'date'])
result.merge(dd, left_on='id_quote', right_on='id_quote', how='left')
dd.id_quote = dd.id_quote.astype(float)
pd.to_numeric(d)

[i[0] for i in result.rt.head()]

# on convertir la colonne de texte en strings
result['rts'] = result.raw_texte.astype(str)
    
# sauvegarder objets
s.to_pickle("save_DTC.pkl")
import pickle
s=pickle.loads("save_DTC.pkl")
pickle.Unpickler("save_DTC.pkl").load()


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

brower = webdriver.Firefox()
brower = webdriver.Chrome()
# si pb telecharger
# https://github.com/mozilla/geckodriver/releases
brower.get('http://www.danstonchat.com')
# tester site /robots.txt

item = brower.find_elements_by_class_name('items')
# si on met un point devant la classname ca donne un css element pratique
# item contient toute la colonne.
# si on met un .text global il concatene tout.
# attention la fonction find_elementSSS renvoie une oliste contrairemnet a findeemenT 
items = item[0].find_elements_by_class_name("item-content")
items[0].text
# question comment exclure un span
spans = items[0].find_elements_by_class_name("decoration")
# question: pkoi encodage OK ici?
[print(i.text) for i in spans]
[set(i.text) for i in spans]
personnes=[i.text for i in spans]
list(set(personnes)) # bizarre format set...

for j in items:
    spans = 
    
[k.text for k in [j.find_elements_by_class_name("decoration") for j in items]]

# technique de string pour remplacer:
derf search(dep, arr):
    "je m'appelle %s et j'ai %d ans" %("marc", 18)
# copier xpath
    busbouton = brower.find_element_by_xpath("/html/body/section/div/div/div/div/div[2]/div[2]/div[2]/div[1]/a/span[10]")
   # attendre un chargement...
    time.sleep(1)
    busbouton.click()
# on peut envoyer des commandes de clavier
brower.send_keys(KEYS.######) # ou un truc du genre
# attention on ne peut avoir qu'un onglet ouvert (il blqoue sur le premier)

res['y'] = res.score_pos/res.score_neg

import sklearn



import statsmodels.formula.api as sm

fit = sm.ols(formula=y~comments+nb_lignes, data=res).fit()
y=res['score_neg'].values
X=res[["comments", "nb_lignes", "id_quote"]].values
X=add_constant(X)
fit = sm.OLS(y, X)
fitted = fit.fit()
fitted.summary()

fit = sm.ols(formula=y~comments+nb_lignes, data=res).fit()
y=res['score_pos'].values
X=res[["comments", "nb_lignes", "id_quote"]].values
X=add_constant(X)
fit = sm.OLS(y, X)
fitted = fit.fit()
fitted.summary()

result['y'] = result.score_pos/result.score_neg
fit = sm.ols(formula=y~comments+nb_lignes, data=result).fit()
y=result['y'].values
X=result[["comments", "nb_lignes"]].values
X=add_constant(X)
fit = sm.OLS(y, X)
fitted = fit.fit()
fitted.summary()




