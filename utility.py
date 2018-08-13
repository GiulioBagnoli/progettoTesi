import pickle


'''Funzione per la lettura delle tabelle. 

Inputs : -> fileName : nome del file da leggere.
        -> noParametres : parametro opzionale per rimuovere la prima riga.
Output : lista contenente le tabelle.
'''
def readFile(fileName, noParametres=True):

    aux = []
    file_object = open(fileName, 'r')
    for line in file_object:
        aux.append(line.strip().split(','))
    if noParametres:
        aux.remove(aux[0])
    return aux



"""Funzione utilizzata per il calcolo delle classfiche parziali."""
def puntiClassifica(partita, gare):
    puntiSquadraCasa = 0
    puntiSquadraFuori = 0
    for g in gare:
        if partita.idGiornata >= g.idGiornata:
            if partita.idCampionato == g.idCampionato:

                if partita.casa == g.casa:
                    puntiSquadraCasa += g.puntiCasa
                elif partita.casa == g.fuori:
                    puntiSquadraCasa += g.puntiFuori

                if partita.fuori == g.casa:
                    puntiSquadraFuori += g.puntiCasa
                elif partita.fuori == g.fuori:
                    puntiSquadraFuori += g.puntiFuori

    return [fromSquadraToCLub(partita.casa), puntiSquadraCasa, fromSquadraToCLub(partita.fuori), puntiSquadraFuori]


"""Funzione che data l'idSquadra rende il corrispondente idClub."""
def fromSquadraToCLub(squadra):

    squadre = pickle.load(open("datiElaborati/squadre_utili", "rb"))
    notFind = True
    index = 0
    while (notFind and index < len(squadre)-1):
        if squadra == squadre[index][0]:
            notFind = False
        else:
            index += 1

    return squadre[index][1]


"""Funzione che serve per preparare i dati per i test."""


def prepareData(partialFeatures, scalati, dimensioneTest = False):
    features = pickle.load(open("datiElaborati/features_utili", "rb"))
    y = []
    x = []
    if dimensioneTest == False:
        dimensioneTest = len(features)
    for i in range(dimensioneTest):
        y.append(features[i][1][0])
        aux = []
        if "punti_squadre" in partialFeatures:
            aux.append(features[i][1][1])
            aux.append(features[i][1][2])
        if "livello_squadre" in partialFeatures:
            aux.append(features[i][1][3])
            aux.append(features[i][1][4])
        if "giorno_partita" in partialFeatures:
            aux.append(features[i][1][5])
        if "differenza_classifica" in partialFeatures:
            aux.append(features[i][1][6])
        if "vittorie_consegutive" in partialFeatures:
            aux.append(features[i][1][7])
            aux.append(features[i][1][8])
        if "anni_in_A1" in partialFeatures:
            aux.append(features[i][1][9])
            aux.append(features[i][1][10])
        if "probabilita_nuova_fascia" in partialFeatures:
            aux.append(features[i][1][11])
            aux.append(features[i][1][12])
        if "posizione_classifica_vecchia" in partialFeatures:
            aux.append(features[i][1][13])
            aux.append(features[i][1][14])
        if "premi_club" in partialFeatures:
            aux.append(features[i][1][15])
            aux.append(features[i][1][16])
        if "numero_emittenti" in partialFeatures:
            aux.append(features[i][1][17])
            aux.append(features[i][1][18])
        if "derby" in partialFeatures:
            aux.append(features[i][1][19])
        x.append(aux)

        if scalati:
            for i in range(len(x[0])):
                aux = []
                for j in range(len(x)):
                    aux.append(x[j][i])
                max1 = max(aux)
                if max1 != 0:
                    for h in range(len(x)):
                        x[h][i] = float(x[h][i] / max1)

    return y, x


