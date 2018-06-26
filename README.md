DansTonChat est un site qui fonctionne un peu comme "Vie de Merde", sauf qu'il recense les meilleures citations et échanges les plus drôles qui ont eu lieu sur des forums de discussion (chats).

https://danstonchat.com/

Très réputé chez les ados, ce site est doublé d'une application smartphone. Pour donner une idée de la popularité, il est classé 2900ième site français le plus consulté par l'outil Alexa Ranking (source: https://www.alexa.com/siteinfo/danstonchat.com), a titre de comparaison le site de l'Elysée http://www.elysee.fr/ est 3 fois moins fréquenté (8500ème). Bref.

Les citations ou "quotes" sont soumises par les utilisateurs puis sélectionnées. Un système de likes/dislikes et de commentaires permet d'interagir. Le site recense (au 1er mai 2018) 19 327 quotes, ce qui est important et permet de faire des statistiques. L'ensemble de ces quotes constituent un **corpus de texte** particulièrement intéressant à la fois sur le language utilisé sur ces forums, les facteurs qui font le succès d'une citation ou anecdote, et plus généralement sur la culture "geek". La population concernée a probablement entre 12 et 30 ans, est assez connectée à l'informatique et aux jeux vidéos (mais pas nécessairement, la preuve j'ai une [quote perso](https://danstonchat.com/13296.html) qui y est publiée :-)), enfin le sujet des relations amoureuses qui revient souvent. 

Ma demande d'accès à la base de donnée n'ayant pas eu de suites, j'ai décidé de passer par du **webscrapping**. Pour des raisons légales donc, je ne publie pas cette base de données qui ne m'appartient pas, mais uniquement des analyses statistiques réalisées sur ce site en accès libre.

1. Webscrapping

Toute la partie webscrapping et construction de la base est réalisé sous Python 3.0 à l'aide du package BeautifulSoup (très pratique pour scrapper). L'enjeu de cette méthode est de trouver les tags HTML où sont stockées les information qui nous intéressent, ici la quote, les likes, les commentaires, etc. Premier problème, chaque ligne de la quote contient le pseudo de la personne qui écrit, et aucun moyen aisé de le retirer... On peut faire appel à du "regex" (expressions régulières) pour créer des patterns de caractères qui vont "matcher" le pseudo. Ainsi quand j'exécute:

`findall("(?<=^<)[\S]+(?=>)", quote)`

Il ne s'agit pas de rechercher un juron du capitaine Haddock, mais bien un code très subtil pour faire comprendre à la fonction qu'on cherche à isoler le premier (`^`) bloc de texte de la ligne ne contenant aucun espace (`[\S]+`), et qu'on veut récupérer tout ce qui est situé entre un `<` et un `>`. Exemple:

![exemple quote 1](quote_exemple_1.png)

Pour plus d'infos sur ces techniques de regex, voir [ici](https://docs.python.org/2/library/re.html).



- 

2. 




