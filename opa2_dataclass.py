from dataclasses import dataclass
from typing import Optional
from enum import Enum
from datetime import datetime
import json
import csv


"""
Enumerations des types d'event
"""


class EventType(str, Enum):
    KLINE: str = "kline"
    TICKER: str = "24hrTicker"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


"""
Enumerations des intervalles Kline/Candlestick
"""


class ChartInterval(str, Enum):
    ONE_SECOND: str = "1s"
    ONE_MINUTE: str = "1m"
    THREE_MINUTE: str = "3m"
    FIVE_MINUTE: str = "5m"
    FIFTEEN_MINUTE: str = "15m"
    THIRTEEN_MINUTE: str = "30m"
    ONE_HOUR: str = "1h"
    TWO_HOUR: str = "2h"
    FOUR_HOUR: str = "4h"
    SIX_HOUR: str = "6h"
    EIGHT_HOUR: str = "8h"
    TWELVE_HOUR: str = "12h"
    ONE_DAY: str = "1d"
    THREE_DAY: str = "3d"
    ONE_WEEK: str = "1w"
    ONE_MONTH: str = "1M"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


"""
Dataclass BasicPayload
__repr__ redéfinie pour afficher la date au format iso à la place du timestamp
"""


@dataclass(init=True)
class BasicPayload:
    eventType: EventType
    eventTime: int
    lastPrice: float
    symbol: str

    def __repr__(self):
        simple = self.__dict__.copy()
        simple["eventTime"] = datetime.fromtimestamp(
            self.eventTime/1000).isoformat()
        return str(simple)

    def basic(self):
        return (BasicPayload(self.eventType, self.eventTime, self.lastPrice, self.symbol))

    def to_json(self):
        return self.__dict__


"""
Dataclass ticker
__repr__ redéfinie pour afficher la date au format iso à la place du timestamp
"""


@dataclass(init=True)
class Ticker(BasicPayload):
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

    """
    affichage de l'objet avec la date lisible
    """

    def __repr__(self) -> str:
        simple = self.__dict__.copy()
        simple["eventTime"] = datetime.fromtimestamp(
            self.eventTime/1000).isoformat()
        return str(simple)

    """
    deserialisation du message e
    """

    @classmethod
    def from_json(cls, json_payload):
        payload = json.loads(json_payload)
        return cls(eventType=EventType.TICKER,
                   eventTime=payload["E"],
                   lastPrice=payload["c"],
                   symbol=payload["s"],
                   priceChange=payload["p"],
                   priceChangePercent=payload["P"],
                   weightedAveragePrice=payload["w"],
                   firstTrade=payload["x"],
                   lastQuantity=payload["Q"],
                   bestBidPrice=payload["b"],
                   bestBidQuantity=payload["B"],
                   bestAskPrice=payload["a"],
                   bestAskQuantity=payload["A"],
                   openPrice=payload["o"],
                   highPrice=payload["h"],
                   lowPrice=payload["l"],
                   totalTradedBaseAsset=payload["v"],
                   totalTradedQuoteAsset=payload["q"],
                   statisticsOpenTime=payload["O"],
                   statisticsCloseTime=payload["C"],
                   lastTradeId=payload["L"],
                   firstTradeID=payload["F"],
                   totalNumberOfTrades=payload["n"])


"""
dataclass pour manipuler les données kline historique
"""


@dataclass(init=True)
class Kline(BasicPayload):
    interval: ChartInterval
    openTime: Optional[int] = None
    openPrice: Optional[float] = None
    highPrice: Optional[float] = None
    lowPrice: Optional[float] = None
    closePrice: Optional[float] = None
    volume: Optional[float] = None
    closeTime: Optional[int] = None
    quoteAssetVolume: Optional[int] = None
    numberOfTrades: Optional[int] = None
    takerBuyBaseAssetVolume: Optional[float] = None
    takerBuyQuoteAssetVolume: Optional[float] = None
    """
    crée une liste d'objet kline à partir d'un csv historique.
    csv_file_path -> doit etre le nom du fichier original. on extrait le symbol et l'interval à partir de cette dernière.
    """

    @classmethod
    def from_csv(cls, csv_file_path: str):
        klines = []
        with open(csv_file_path, 'r') as f_csv:
            reader = csv.reader(f_csv)
            for csv_row in reader:
                clazz = cls(
                    eventType=EventType.KLINE,
                    eventTime=int(csv_row[0]),
                    lastPrice=float(csv_row[1]),
                    symbol=csv_file_path.split("-")[0].split("/")[-1],
                    interval=ChartInterval(csv_file_path.split("-")[1]),
                    openTime=int(csv_row[0]),
                    openPrice=float(csv_row[1]),
                    highPrice=float(csv_row[2]),
                    lowPrice=float(csv_row[3]),
                    closePrice=float(csv_row[4]),
                    volume=float(csv_row[5]),
                    closeTime=int(csv_row[6]),
                    quoteAssetVolume=float(csv_row[7]),
                    numberOfTrades=int(csv_row[8]),
                    takerBuyBaseAssetVolume=float(csv_row[9]),
                    takerBuyQuoteAssetVolume=float(csv_row[10]))
                klines.append(clazz)

        return klines

    """
    affichage de l'objet avec la date lisible
    """

    def __repr__(self) -> str:
        simple = self.__dict__.copy()
        simple["eventTime"] = datetime.fromtimestamp(
            self.eventTime/1000).isoformat()
        simple["openTime"] = datetime.fromtimestamp(
            self.openTime/1000).isoformat()
        simple["closeTime"] = datetime.fromtimestamp(
            self.closeTime/1000).isoformat()

        return str(simple)
