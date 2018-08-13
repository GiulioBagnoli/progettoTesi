from math import fabs
from utility import *
from random import random
import copy

def baseLine1(ripetizioni, dim):

    partite = pickle.load(open("datiElaborati/partite_baseline_utili", "rb"))
    indice = pickle.load(open("datiElaborati/indici_utili", "rb"))

    errore = 0

    for i in range(ripetizioni):

        indiciPartite = []

        for i in range(dim):
            valore = int(random() * (len(partite)-1))
            indiciPartite.append(valore)


        perContare = copy.copy(partite)
        daContare = []

        for i in indiciPartite:
            daContare.append(perContare[i])

        numPartiteBuone = dim
        sumErroreRip = 0

        for partita in daContare:

            sumPercentualiRiempimenti = 0
            numPartiteVecchie = 0

            for i in range(len(indice)):
                if indice[i][0] == partita.casa:
                    indicePartitaInizio = indice[i][1]
                    if i == len(indice) - 1:
                        indicePartitaFine = len(perContare)
                    else:
                        indicePartitaFine = indice[i + 1][1]
                    break

            for j in range(indicePartitaInizio, indicePartitaFine):

                if partita.dataGara > perContare[j].dataGara:

                    if partita.impianto == perContare[j].impianto:

                        if perContare[j].spettatori >= perContare[j].impianto:
                            sumPercentualiRiempimenti += 1
                        else:
                            sumPercentualiRiempimenti += (float(perContare[j].spettatori) / perContare[j].impianto)
                        numPartiteVecchie += 1

            if numPartiteVecchie != 0:

                avgRiempimenti = sumPercentualiRiempimenti / numPartiteVecchie

                if partita.spettatori >= partita.impianto:
                    riempimentoEffettivo = 1
                else:
                    riempimentoEffettivo = float(partita.spettatori) / partita.impianto

                errorePartita = fabs(avgRiempimenti - riempimentoEffettivo) / riempimentoEffettivo

            else:
                numPartiteBuone -= 1
                errorePartita = 0

            sumErroreRip += errorePartita

        errore += (sumErroreRip / numPartiteBuone)

    return errore / ripetizioni


def baseLine2(ripetizioni, dim):

    partite = pickle.load(open("datiElaborati/partite_baseline_utili", "rb"))
    indice = pickle.load(open("datiElaborati/indici_utili", "rb"))

    errore = 0

    for i in range(ripetizioni):

        indiciPartite = []

        for i in range(dim):
            valore = int(random() * (len(partite)-1))
            indiciPartite.append(valore)


        perContare = copy.copy(partite)
        daContare = []

        for i in indiciPartite:
            daContare.append(perContare[i])

        numPartiteBuone = dim
        sumErroreRip = 0

        for partita in daContare:

            sumPercentualiRiempimenti = 0
            numPartiteVecchie = 0

            for i in range(len(indice)):
                if indice[i][0] == partita.casa:
                    indicePartitaInizio = indice[i][1]
                    if i == len(indice) - 1:
                        indicePartitaFine = len(perContare)
                    else:
                        indicePartitaFine = indice[i + 1][1]
                    break

            for j in range(indicePartitaInizio, indicePartitaFine):

                if partita.dataGara > perContare[j].dataGara and partita.fuori == perContare[j].fuori:

                    if partita.impianto == perContare[j].impianto:

                        if perContare[j].spettatori >= perContare[j].impianto:
                            sumPercentualiRiempimenti += 1
                        else:
                            sumPercentualiRiempimenti += (float(perContare[j].spettatori) / perContare[j].impianto)
                        numPartiteVecchie += 1

            if numPartiteVecchie != 0:

                avgRiempimenti = sumPercentualiRiempimenti / numPartiteVecchie

                if partita.spettatori >= partita.impianto:
                    riempimentoEffettivo = 1
                else:
                    riempimentoEffettivo = float(partita.spettatori) / partita.impianto

                errorePartita = fabs(avgRiempimenti - riempimentoEffettivo) / riempimentoEffettivo

            else:
                numPartiteBuone -= 1
                errorePartita = 0

            sumErroreRip += errorePartita

        errore += (sumErroreRip / numPartiteBuone)



    return errore / ripetizioni





