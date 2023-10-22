# Concevoir un CryptoBot avec Binance

# Participants

- Laurent BOSCHET
- Harilala RAKOTOARIVONINA
- Audrey ROUSSEAUX

# Introduction

De nos jours, le monde des crypto-monnaies commence à prendre une place importante et grossi. Il s’agit tout simplement de marchés financiers assez volatiles et instables se basant sur la technologie de la Blockchain.
Le but principal de ce projet est de créer un bot de trading basé sur un modèle de Machine Learning et qui investira sur des marchés crypto.

Pour réaliser ce projet, nous allons nous appuyer sur les données mises à disposition par le site Binance : <https://www.binance.com/fr>

Un descriptif détaillé des étapes nécessaires à la conception du CryptoBot est disponible ci-après.

# 1. Récolte des données

La toute première étape du projet consiste à définir les données que nous allons traiter dans notre projet et à en définir les méthodes d'extraction.

## 1.1. Origine des données

Les données sont extraites depuis le site de Binance : <https://www.binance.com/fr>

Binance est une plateforme de trading en ligne qui permet d’acheter et d’échanger des crypto monnaies. Cette plateforme a été fondée en 2017 et son nom est issu de la combinaison des mots bitcoin et finance. A ce jour, on y retrouve plus de 500 crypto-monnaies.

## 1.2. Périmètre des données à extraire

Notre choix s’est porté sur le Top 10 des crypto monnaies répertoriées par le site <http://coinmarketcap.com> hors crypto monnaie stable (stablecoin) puisque celles-ci sont indexées sur une monnaie fiduciaire comme le dollar ou l'euro.

En effet, ce type de crypto-monnaie tente d’apporter de la stabilité au marché volatile qu’est le marché des crypto monnaies mais n’a pas un grand intérêt à être analyser.

Les crypto-monnaies retenues dans notre projet sont disponibles dans le tableau ci-dessous :
| Nom  | Symbole |
| :---------------  |:-----------------|
| Bitcoin | BTCUSDT |
| Ethereum | ETHUSDT |
| BNB | BNBUSDT |
| XRP | XRPUSDT |
| Cardano | ADAUSDT |
| Dogecoin | DOGEUSDT |
| Polygon | MATICUSDT |
| Solana | SOLUSDT          |
| TRON | TRXUSDT          |
| Litecoin | LTCUSDT          |

Pour chacune des crypto-monnaie citée ci-dessus, nous allons extraire 2 types de données :

- les données en temps réel
- les données historiques

## 1.3. Les méthodes de récupération des données

La plateforme Binance fournit des API afin de permettre, à des développeurs, d’accéder aux fonctionnalités et aux données de la plateforme en se connectant sur les serveurs de Binance.

- L’**API REST** est un ensemble de fonctionnalités permettant d'interagir avec la plateforme Binance via des requêtes HTTP.
- L’**API WebSocket** permet une communication bidirectionnelle en temps réel entre le client et le serveur Binance. Nous allons donc l’utiliser pour la récupération des données en temps réel.

### _1.3.1. Les données temps réel_

Pour récupérer les données en temps réel, sur les 10 crypto-monnaies retenues, nous avons fait le choix d’utiliser l’API WebSocket au travers du endpoint « Individual Symbol Ticker Streams ».

Ce endpoint est en charge, à intervalles de 1 000 ms, de la récupération des données d’une seule crypto-monnaie dont le symbole est passé en paramètre sur une fenêtre de 24 heures.

La description des données échangées entre le serveur Binance et le client est fournie ci-dessous :

```
{
  "e": "24hrTicker",  // Event type
  "E": 1672515782136, // Event time
  "s": "BNBBTC",      // Symbol
  "p": "0.0015",      // Price change
  "P": "250.00",      // Price change percent
  "w": "0.0018",      // Weighted average price
  "x": "0.0009",      // First trade(F)-1 price (first trade before the 24hr rolling window)
  "c": "0.0025",      // Last price
  "Q": "10",          // Last quantity
  "b": "0.0024",      // Best bid price
  "B": "10",          // Best bid quantity
  "a": "0.0026",      // Best ask price
  "A": "100",         // Best ask quantity
  "o": "0.0010",      // Open price
  "h": "0.0025",      // High price
  "l": "0.0010",      // Low price
  "v": "10000",       // Total traded base asset volume
  "q": "18",          // Total traded quote asset volume
  "O": 0,             // Statistics open time
  "C": 86400000,      // Statistics close time
  "F": 0,             // First trade ID
  "L": 18150,         // Last trade Id
  "n": 18151          // Total number of trades
}
```

### _1.3.2. Les données historiques_

Pour chaque crypto-monnaie, Binance met à disposition des fichiers au format .csv contenant une historisation quotidienne des données selon différents intervalles de récupération de la donnée.
Par exemple, pour une crypto-monnaie donnée, dans un fichier .csv relatif à une date d, je vais pouvoir disposer des données à intervalle de 12 heures, 1 heure, 15 minutes, 1 minute, 1 seconde, ...

Les données historiques sur les 10 crypto-monnaies que nous avons retenues sont donc extraites grâce à ces fichiers .csv quotidiens. Ils sont disponibles à l’adresse <https://data.binance.vision/?prefix=data/spot/daily/klines/>

Dans le cadre de notre projet, nous avons fait le choix de récupérer les données à compter du 01/01/2020 pour couvrir un période de 3 ans minimum.
Après une série de tests, l'extraction des données de l'historique s'effectue sur la fréquence de 1 minute.

L'url type pour récupérer les données est donc une chaine avec le pattern suivant :
```"https://data.binance.vision/data/spot/daily/klines/"" + symbol + "/" + interval + "/" + symbol + "-" + interval + "-" + current_day + ".zip"```
où ```symbol```, ```interval``` et ```current_day``` sont respectivement le symbole de la crypto_monnaie, l'intervalle de récupération des données et la date du jour pour lequel on souhaite avoir les données historiques.

## 1.4. Explications du script de récupération des données

### _1.4.1. Les données temps réel_

Les données en temps réel sont extraites par le biais de l'API WebSocket comme expliqué précédemment.
Pour cela, nous nous connectons sur le point d'entrée :
```"wss://stream.binance.com:443/ws/"+symbol+"@ticker"``` où ```symbol``` est le symbole de la crypto_monnaie pour laquelle pour souhaitons streamer les données.

### _1.4.2. Les données historiques_

L'extraction des données historiques s'effectue par le biais de fichiers .csv mis à disposition par Binance.

L'extraction de fichiers quotidiens sur la période d'analyse s'effectue à partir de l'url définie dans le paragraphe 1.3.2. Les fichiers sont ensuite sauvegardés dans un répertoire temporaire local _binance_datas_

Chaque symbole analysé donne lieu à la création d'un répertoire du nom du symbole dans le répertoire _binance_datas_. S'en suis un parcours récursif du répertoire temporaire local afin d'extraire les données de chaque fichier .csv.

## 1.5. Explications du script de pré-processing

De manière à avoir un maximum d'indépendance au niveau du code de notre application, nous avons décidé de créer des abstractions sous forme de classes d'objet python qui permettront de stocker les données 'temps réel' ou 'historiques'. Cette manière de procéder permet de s'affranchir des méthodes de récupération des données et de les adapter facilement si elles étaient amenées à changer (= changer uniquement la méthode de récupération sans avoir à modifier la structure des données).

Classes de données :
  - Enumérations des types d'event : KLINE (Candlestick pour les données historiques) ou TICKER (pour les données temps réel)
  - Intervalles Kline/Candlestick : 1s à 1M (1 mois)
   - Basic payload : informations basiques des données (symbol, Last Price)
   - Ticker payload : information des données TICKER (temps réel)
   - Kline payload : information des données KLINE (historiques)

   Exemple de la classe Ticker :

   ```
   Class Ticker(BasicPayload):
    priceChange: Optional[float] = None
    priceChangePercent: Optional[float] = None
    weightedAveragePrice: Optional[float] = None
    firstTrade: Optional[float] = None
    lastQuantity: Optional[int] = None
    bestBidPrice: Optional[float] = None
    bestBidQuantity: Optional[int] = None
    bestAskPrice: Optional[int] = None
    bestAskQuantity: Optional[int] = None
    openPrice: Optional[float] = None
    highPrice: Optional[float] = None
    lowPrice: Optional[float] = None
    totalTradedBaseAsset: Optional[int] = None
    totalTradedQuoteAsset: Optional[int] = None
    statisticsOpenTime: Optional[int] = None
    statisticsCloseTime: Optional[int] = None
    firstTradeID: Optional[int] = None
    lastTradeId: Optional[int] = None
    totalNumberOfTrades: Optional[int] = None
```

Les 2 dernières classes incluent chacune leur méthode de récupération :
   - TICKER: Récupération des données en JSON depuis le websocket (temps réel)
   - KLINE : Récupération des données depuis les .csv disponibles sur le site binance.com sur un intervalle de temps donné : tuple(début, fin)

Le pré-processing de ces données se fait par appel de la méthode associée à chaque type : TICKER ou KLINE.
Les données sont stockées dans des instances de la classe correspondante et sont directement envoyées dans un index Elastic Search (base de données clef/valeur choisie qui correspond bien aux objectifs de notre projet pour le traitement des données horodatées).

Les données temps réel seront directement envoyées dans un index Elsatic Search avec le bon mapping (typage) afin de pouvoir être traitées par la suite (algorithme de prédiction).

La notion de timestamp est très importante pour les projets de données financières. Tous les timestamp seront stockés au format natif (Unix Time Stamp)
https://en.wikipedia.org/wiki/Unix_time


## 1.6. Exemples de fichiers de données

Voici un exemple de fichier .csv du site binance.com pour les données historiques pour le bitcoin BTCUSDT sur 1s (journée du 13 Mai) :

BTCUSDT-1s-2023-05-13
1683936000000,26795.01000000,26795.01000000,26795.01000000,26795.01000000,1.05071000,1683936000999,28153.78495710,17,1.05071000,28153.78495710,0
1683936001000,26795.01000000,26795.01000000,26795.00000000,26795.00000000,0.70857000,1683936001999,18986.13364750,30,0.04975000,1333.05174750,0
1683936002000,26795.01000000,26795.01000000,26795.00000000,26795.00000000,0.66888000,1683936002999,17922.64186750,71,0.22675000,6075.76851750,0
1683936003000,26795.00000000,26795.01000000,26795.00000000,26795.00000000,0.46129000,1683936003999,12360.26770680,40,0.21568000,5779.14775680,0
[...]

### _1.6.1. Les données temps réel_

Les données sont renvoyées dans un fichier json dont vous trouverez un exemple ci-après : [json_ETHUSDT](ETHUSDT-Data.json)

### _1.6.1. Les données historiques_

Les données sont renvoyées dans un fichier json dont vous trouverez un exemple ci-après : [csv_ETHUSDT](ETHUSDT-1m-2023-05-23.csv)