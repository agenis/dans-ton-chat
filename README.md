DansTonChat est un site qui fonctionne un peu comme "Vie de Merde", sauf qu'il recense les meilleures citations et échanges les plus drôles qui ont eu lieu sur des forums de discussion (chats).

https://danstonchat.com/

Très réputé chez les ados, ce site est doublé d'une application smartphone. Pour donner une idée de la popularité, il est classé 2900^ème site français le plus consulté par l'outil Alexa Ranking ([source](https://www.alexa.com/siteinfo/danstonchat.com)), a titre de comparaison le site de l'[Elysée](http://www.elysee.fr/) est 3 fois moins fréquenté (8500^ème). Bref.

Les citations ou "quotes" sont soumises par les utilisateurs puis sélectionnées. Un système de likes/dislikes et de commentaires permet d'interagir. Le site recense (au 1er mai 2018) 19 327 quotes, ce qui est important et permet de faire des statistiques. L'ensemble de ces quotes constituent un **corpus de texte** particulièrement intéressant à la fois sur le language utilisé sur ces forums, les facteurs qui font le succès d'une citation ou anecdote, et plus généralement sur la culture "geek". La population concernée a probablement entre 12 et 30 ans, est assez connectée à l'informatique et aux jeux vidéos (mais pas nécessairement, la preuve j'ai une [quote perso](https://danstonchat.com/13296.html) qui y est publiée :-)), enfin le sujet des relations amoureuses qui revient souvent. 

Ma demande d'accès à la base de donnée n'ayant pas eu de suites, j'ai décidé de passer par du **webscrapping**. Pour des raisons légales donc, je ne publie pas cette base de données qui ne m'appartient pas, mais uniquement des analyses statistiques réalisées sur ce site en accès libre.

1. Webscrapping

Toute la partie webscrapping et construction de la base est réalisé sous Python 3.0 à l'aide du package BeautifulSoup (très pratique pour scrapper). L'enjeu de cette méthode est de trouver les tags HTML où sont stockées les information qui nous intéressent, ici la quote, les likes, les commentaires, etc. Premier problème, chaque ligne de la quote contient le pseudo de la personne qui écrit, et pas de aisé de le retirer... On peut faire appel à du "regex" (expressions régulières) pour créer des patterns de caractères qui vont "matcher" le pseudo. Ainsi quand j'exécute:

`findall("(?<=^<)[\S]+(?=>)", quote)`

Il ne s'agit pas de rechercher un *juron du capitaine Haddock*, mais bien un code très subtil pour faire comprendre à la fonction qu'on cherche à isoler le premier (`^`) bloc de texte de la ligne ne contenant aucun espace (`[\S]+`), et qu'on veut récupérer tout ce qui est situé entre un `<` et un `>`. Exemple:

![exemple quote 1](quote_exemple_1.png)

Pour plus d'infos sur ces techniques de regex, voir [ici](https://docs.python.org/2/library/re.html). Parfois les pseudos ne sont pas isolés par des caractères spéciaux, on ne peut pas deviner..

2. Aperçus...

Avant d'entrer dans des analyses compliquées, quelques exemples amusants. D'abord, la quote avec le plus de likes:

![exemple quote 2](quote_toplikes.png)

Mais aussi:

[La quote la moins likée](https://danstonchat.com/11364.html) (qui est pas si mal en fait!)

[La quote avec le plus de commentaires](https://danstonchat.com/19524.html)

[La quote avec le plus d'interlocuteurs](https://danstonchat.com/18250.html)

[La quote la plus longue](https://danstonchat.com/17812.html)

Pour revenir aw webscrapping, une particularité est l'absence totale d'horodatage des quotes. On peut retrouver manuellement les dates de certaines quotes via le compte tweeter DTC, mais impossible de remonter au delà de 2500 tweets (limite max). Bref, on sera embêté pour estimer l'effet de trend temporel sur le taux de like ou autre, il faudra faire l'hypothèse d'un rythme de publication constant, ce qui est faux. Enfin, des problèmes d'encodage de caractères spéciaux qui m'ont obligé à supprimer tous les accents.

3. Quelques statistiques

La première statistique est le rapport entre les likes et les dislikes. Il faut savoir que le site a ajouté le bouton *dislike* il y a 2 ou 3 ans, avant seul le like était possible, ce qui peut expliquer la chute soudaine autour de la 13000^ème (celles d'avant bénéficient d'un stock de likes plus élevé). On voit toutefois une remontée progressive sur les dernières, peut-être due à une évolution du comportement des utilisateurs. Mais ce sont toujours les quotes anciennes qui récoltent le plus d'interactions likes/dislikes, contrairement aux commentaires, qui sont plus fournis sur les quotes récentes (on peut imaginer qu'ils ont été autorisés via l'application smartphone?). Une explication pourrait être l'instauration d'un controle des IPs qui empeche de voter plusieurs fois.

![plot 1](plot_evolution_ratio.png)


- 

2. 




