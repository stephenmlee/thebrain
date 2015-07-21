import copy
import glob
import json
import os
import math
import datetime
import numpy as np
from CommandBunker.ControlPanel import AGE_DROPOFF_THRESHOLD
from Cranium import NeuralNetwork
from Cranium.NeuralNetwork import UnstableNetworkError
from EvolutionChamber.Population import Population
import numpy

__author__ = 'stephen'


def decode(genome_file):
    f = open(genome_file, 'r')
    g = json.load(f)
    f.close()
    return g


def generate():
    n = 0
    while True:
        n += 1
        yield "." if n % 2 == 0 else "+"


def std_normalize(timeseries):
    timeseries = copy.copy(timeseries)
    timeseries -= np.mean(timeseries, axis=0)
    timeseries /= np.std(timeseries, axis=0)
    return timeseries


def min_max_normalize(timeseries):
    result = []
    for value in timeseries:
        result.append((value - min(timeseries)) / (max(timeseries) - min(timeseries)))
    return result


def balance(m, s, f):
    return m if m > 0 else s * f


def load_data():

    vault_files = glob.glob("Experiments/Vault/ftse100-*.json")
    quotes = []
    for ftse100_file in vault_files:
        ftse100_data = decode(ftse100_file)
        for quote in ftse100_data["query"]["results"]["quote"]:
            quotes.append(quote)

    quotes = sorted(quotes, key=lambda q: q["Date"])

    ftse100 = []
    volume = []
    dates = []

    for quote in quotes:
        ftse100.append(float(quote["Close"]))
        volume.append(float(quote["Volume"]))
        dates.append(quote["Date"])

    ftse100_pct = []

    for i, value in enumerate(ftse100):
        if i == 0:
            ftse100_pct.append(0)
        else:
            ftse100_pct.append((ftse100[i] - ftse100[i - 1]) / ftse100[i - 1])

    ftse100_t1, ftse100_t2, ftse100_t3, volume_t1 = normalise_all(ftse100, volume)

    return ftse100, dates, ftse100_t1, ftse100_t2, ftse100_t3, volume_t1


def normalise_all(ftse_series, volume_series):
    ftse100_n = min_max_normalize(ftse_series)
    volume_n = min_max_normalize(volume_series)
    ftse100_t1 = [ftse100_n[0]]
    ftse100_t1.extend(ftse100_n[:len(ftse100_n) - 1])
    ftse100_t2 = [ftse100_n[0], ftse100_n[0]]
    ftse100_t2.extend(ftse100_n[:len(ftse100_n) - 2])
    ftse100_t2_p = [ftse_series[0], ftse_series[0]]
    ftse100_t2_p.extend(ftse_series[:len(ftse_series) - 2])
    ftse100_t3 = [ftse100_n[0], ftse100_n[0], ftse100_n[0]]
    ftse100_t3.extend(ftse100_n[:len(ftse100_n) - 3])
    volume_t1 = [volume_n[0]]
    volume_t1.extend(volume_n[:len(ftse100_n) - 1])

    return ftse100_t1, ftse100_t2, ftse100_t3, volume_t1


if __name__ == "__main__":
    fund_manager = decode('Experiments/CryogenicStorage/prophet_fund_manager.json')

    ftse100, dates, ftse100_t1, ftse100_t2, ftse100_t3, volume_t1 = load_data()

    money = 1000
    shares = 0

    for index, quote in enumerate(ftse100):
        today = quote
        tomorrow = ftse100[min(index + 1, len(ftse100) - 1)]

        if tomorrow > today:
            if money > 0:
                shares = money / ftse100[index]
                money = 0
        else:
            if shares > 0:
                money = shares * ftse100[index]
                shares = 0

    print "Buy and hold: %s" % ((1000 / ftse100[0]) * ftse100[len(ftse100) - 1])

    print "Best possible result: %s" % money if money > 0 else shares * ftse100[len(ftse100) - 1]

    brain = NeuralNetwork.expressed_from(fund_manager)

    money = 1000
    shares = 0

    print "date,ftse100,prediction,balance,cash,shares"

    for index, quote in enumerate(ftse100):
        brain.stimulate([("S1", ftse100_t1[index]),
                         ("S2", ftse100_t2[index]),
                         ("S3", ftse100_t3[index]),
                         ("S4", volume_t1[index])
                         ])
        brain.electrify()
        prediction = brain.outputs()["O1"].activation()

        if prediction > 0.75:
            if money > 0:
                # shares = money / ftse100[max(0, index - 2)]  # cheat!
                shares = money * 0.995 / ftse100[index]
                money = 0
        elif prediction < 0.25:
            if shares > 0:
                # money = shares * ftse100[max(0, index - 2)]  # cheat!
                money = shares * 0.995 * ftse100[index]
                shares = 0

        print "%s,%.4f,%.4f,%.4f,%.4f,%.4f" % (
            dates[index], ftse100[index], prediction, balance(money, shares, ftse100[index]),
            money * (ftse100[0] / 1000), shares * ftse100[index] * (ftse100[0] / 1000))

    ending_balance = balance(money, shares, ftse100[len(ftse100) - 1])

    print ending_balance
