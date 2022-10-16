import pandas as pd
import numpy as np
from datetime import timedelta
from cartopy.crs import PlateCarree


class Flight:
    # classe décrivant un avion.
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return (
            f"Flight {self.callsign} with aircraft {self.icao24} "
            f"on {self.min('timestamp'):%Y-%m-%d} "
        )

    def __lt__(self, other):
        return self.min("timestamp") <= other.min("timestamp")

    def max(self, feature):
        return self.data[feature].max()

    def min(self, feature):
        return self.data[feature].min()

    def mean(
        self, feature
    ):  # méthode renvoyant la valeur moyenne d'une donnée sur l'ensemble des mesures
        return self.data[feature].mean()

    @property
    def callsign(self):
        return self.min("callsign")

    @property
    def icao24(self):
        return self.min("icao24")

    @property
    def altitude(self):  # méthode renvoyant l'altitude minimale d'un avion
        return self.min("altitude")

    @property
    def vertical_rate_barometric(
        self,
    ):  # méthode renvoyant la vitesse verticale barométrique moyenne d'un avion
        return self.mean("vertical_rate_barometric")

    @property
    def vertical_rate_inertial(
        self,
    ):  # méthode renvoyant la vitesse verticale inertielle moyenne d'un avion
        return self.mean("vertical_rate_inertial")

    @property
    def is_landing(
        self,
    ):  # méthode renvoyant True si l'avion est en atterrissage, False sinon
        return self.altitude < 30000 and self.vertical_rate_barometric < 0

    # critère choisi pour identifier un atterrissage : altitude minimale < 30000m et vitesse verticale barométrique moyenne < 0

    @property
    def is_taking_off(
        self,
    ):  # méthode renvoyant True si l'avion est en décollage, False sinon
        return (
            self.altitude < 30000 and self.vertical_rate_barometric > 0
        )  # critère choisi pour identifier un décollage : altitude minimale < 30000m et vitesse verticale barométrique moyenne > 0

    def plot(self, ax, **kwargs):  # fonction pour tracer un vol
        self.data.query("latitude.notnull()").plot(
            ax=ax,
            x="longitude",
            y="latitude",
            legend=False,
            transform=PlateCarree(),
            **kwargs,
        )


def iterate_time(data, threshold):
    idx = np.where(data.timestamp.diff().dt.total_seconds() > threshold)[0]
    start = 0
    for stop in idx:
        yield data.iloc[start:stop]
        start = stop + 1
    yield data.iloc[start:]


def iterate_icao24_callsign(data):
    for _, chunk in data.groupby(["icao24", "callsign"]):
        yield chunk


class FlightCollection:
    # classe décrivant un ensemble de mesures
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"FlightCollection with {len(self)} flights"

    @classmethod
    def read_json(cls, filename):
        return cls(pd.read_json(filename))

    def __iter__(self):
        for group in iterate_icao24_callsign(self.data):
            for elt in iterate_time(group, 20000):
                yield Flight(elt)

    def __len__(self):
        return sum(1 for _ in self)

    def __getitem__(self, key):
        if isinstance(key, str):
            result = FlightCollection(
                self.data.query("callsign == @key or icao24 == @key")
            )
        if isinstance(key, pd.Timestamp):
            before = key
            after = key + timedelta(days=1)
            result = FlightCollection(
                self.data.query("@before < timestamp < @after")
            )

        if len(result) == 1:
            return Flight(result.data)
        else:
            return result
