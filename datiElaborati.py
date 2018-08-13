from utility import *
import copy
from features import makeFeatures
from partite import partite


def createAll():

    newCampionati()
    newGiornateCampionato()
    newPartiteClassifiche()
    newPartite()
    newSquadre()
    newClassifiche()
    newTitoli()
    newPartiteBaseLine()
    newFeatures()


"""Funzione per creare una nuova lista di campionati contenenti solo quelli utili all'analisi."""

def newCampionati():
    campionati = readFile('dataset/Campionati.txt')
    aux = []

    for campionato in campionati:
        campionato[1] = int(campionato[1])
        if campionato[1] < 2000 or campionato[2] != 'RS' or campionato[3] != '1':
            aux.append(campionato)
    for i in aux:
        campionati.remove(i)

    pickle.dump(campionati, open("DatiElaborati/campionati_utili", "wb"))


"""Funzione per creare una nuova lista di GiornateCampionato, contenenti solo quelle utili all'analisi.
    Ciclo fatto male, rimettere a modino."""

def newGiornateCampionato():
    giornate = readFile('dataset/GiornateCampionato.txt')
    campionati = pickle.load(open("datiElaborati/campionati_utili", "rb"))
    aux = []

    for giornata in giornate:
        nonTrovata = True
        for campionato in campionati:
            if giornata[1] == campionato[0]:

                nonTrovata = False

                campionato[1] = int(campionato[1])
                giornataMax = 13  # valore che servira' per capire se la giornata potra' essere usata o meno.
                if campionato[1] == 2009:
                    giornataMax = 14
                elif campionato[1] == 2014:
                    giornataMax = 12
                elif campionato[1] == 2012 or campionato[1] == 2013 or campionato[1] == 2015:
                    giornataMax = 11
                giornata.append(giornataMax)

        if nonTrovata:
            aux.append(giornata)

    for i in aux:
        giornate.remove(i)

    pickle.dump(giornate, open("DatiElaborati/giornate_utili", "wb"))


"""Funzione che crea una nuova lista contenente solo i club di A1 che hanno giocato negli ultimi 18 anni."""

def newSquadre():
    partite = pickle.load(open("datiElaborati/partite_classifica_utili", "rb"))
    squadre = readFile('dataset/Squadre.txt')

    squadreBuone = []

    for partita in partite:
        for squadra in squadre:
            if partita.casa == squadra[0] and not (squadra in squadreBuone):
                squadreBuone.append(squadra)

    pickle.dump(squadreBuone, open("DatiElaborati/squadre_utili", "wb"))


"""Funzione che crea una nuova lista per le partite da usare per creare la classifica."""

def newPartiteClassifiche():
    aux = readFile("dataset/GareCampionato.txt")
    partiteBuone = []
    for p in aux:
        partita = partite(p)
        if partita.isGoodClassifiche():
            partiteBuone.append(partita)
    pickle.dump(partiteBuone, open("DatiElaborati/partite_classifica_utili", "wb"))


"""Funzione che crea una nuova lista per le partite da usare l'analisi."""

def newPartite():
    aux = readFile("dataset/GareCampionato.txt")
    partiteBuone = []
    for p in aux:
        partita = partite(p)
        if partita.isVeryGood():
            partiteBuone.append(partita)
    pickle.dump(partiteBuone, open("DatiElaborati/partite_utili", "wb"))


"""Funzione che crea le classifiche."""

def newClassifiche():

    partite = pickle.load(open("datiElaborati/partite_classifica_utili", 'rb'))
    giornateCampionato = pickle.load(open("datiElaborati/giornate_utili", 'rb'))

    """Ciclo che sostituisce le date effettive con quelle relative alle giornate per permettere l'ordinamento."""

    for partita in partite:

        for giornata in giornateCampionato:

            if partita.idGiornata == giornata[0]:
                partita.dataGara = giornata[5]
                break

    """Ciclo per vedere quanti sono i campionati e per la creazione delle liste per ogni campionato."""

    auxCampinati = []
    for p in partite:
        if p.idCampionato not in auxCampinati:
            auxCampinati.append(p.idCampionato)

    campionati = []
    classifiche = []

    for i in range(len(auxCampinati)):
        campionati.append([auxCampinati[i]])
        classifiche.append([auxCampinati[i]])

    """Creazione sottoliste per le giornate."""

    auxGiornate = []

    for i in range(len(campionati)):
        for p in partite:
            if p.idGiornata not in auxGiornate and p.idCampionato == campionati[i][0]:
                auxGiornate.append(p.idGiornata)
                campionati[i].append([p.idGiornata])
                classifiche[i].append([p.idGiornata])

    for i in range(len(campionati)):
        d = campionati[i][1:]
        f = classifiche[i][1:]
        campionati[i] = [campionati[i][0]]
        classifiche[i] = [classifiche[i][0]]
        d.sort(key=lambda a: a[0])
        f.sort(key=lambda a: a[0])
        for e in d:
            campionati[i].append(e)
        for e in f:
            classifiche[i].append(e)

    """Inserimento partite nei campionati e nelle giornate giusti."""

    for partita in partite:
        for c in campionati:
            for g in range(1, len(c)):
                if partita.idCampionato == c[0] and partita.idGiornata == c[g][0]:
                    c[g].append(partita)

    """Creazione delle classifiche."""

    for i in range(len(campionati)):
        """Determinazione del numero di squadre presenti in un campionato, si deve tener conto di due giornate poiche' 
        vi sono campionati con un numero di squadre dispari."""
        numSquadre = []
        for index in range(1, 4):
            for k in range(1, len(campionati[i][index])):
                if campionati[i][index][k].casa not in numSquadre:
                    numSquadre.append(campionati[i][index][k].casa)
                elif campionati[i][index][k].fuori not in numSquadre:
                    numSquadre.append(campionati[i][index][k].fuori)

        classificaOld = []

        for squadra in numSquadre:
            classificaOld.append([squadra, 0, 0, 0])  # [squadra, punti tot, posizione, punti relativi]
        numSquadre = len(numSquadre)

        for j in range(1, len(campionati[i])):  # scorrole giornate
            for h in range(1, len(campionati[i][j])):  # scorro le partite
                if j == 1:  # se e' la prima giornata
                    for index in range(numSquadre):
                        if classificaOld[index][0] == campionati[i][j][h].casa:
                            classificaOld[index][3] = campionati[i][j][h].puntiCasa
                        elif classificaOld[index][0] == campionati[i][j][h].fuori:
                            classificaOld[index][3] = campionati[i][j][h].puntiFuori
                else:
                    for index in range(numSquadre):
                        if classificaOld[index][0] == campionati[i][j - 1][h].casa:
                            classificaOld[index][1] += campionati[i][j - 1][h].puntiCasa
                        elif classificaOld[index][0] == campionati[i][j - 1][h].fuori:
                            classificaOld[index][1] += campionati[i][j - 1][h].puntiFuori
                        for g in range(1, len(campionati[i][j])):
                            if classificaOld[index][0] == campionati[i][j][g].casa:
                                classificaOld[index][3] = campionati[i][j][g].puntiCasa

                            if classificaOld[index][0] == campionati[i][j][g].fuori:
                                classificaOld[index][3] = campionati[i][j][g].puntiFuori

            classificaGiornata = []
            for k in range(len(classificaOld)):
                classificaGiornata.append(copy.copy(classificaOld[k]))
            classificaGiornata.sort(key=lambda a: a[1], reverse=True)

            """Determiniamo la posizione in classifica."""
            firstTime = True
            posizione = 1
            count = 0
            for k in range(len(classificaGiornata)):
                if firstTime:
                    firstTime = False
                    classificaGiornata[k][2] = posizione
                elif classificaGiornata[k][1] != classificaGiornata[k - 1][1]:
                    posizione += 1
                    posizione += count
                    classificaGiornata[k][2] = posizione
                    count = 0
                else:
                    classificaGiornata[k][2] = posizione
                    count += 1

            for c in classificaGiornata:
                classifiche[i][j].append(c)

    """Convertiamo idSquadra con idClub in modo da poter trovare dati di anni precedenti."""
    for classifica in classifiche:
        for giornata in range(1, len(classifica)):
            for squadra in range(1, len(classifica[giornata])):
                classifica[giornata][squadra][0] = fromSquadraToCLub(classifica[giornata][squadra][0])

    pickle.dump(classifiche, open("DatiElaborati/classifiche_utili", "wb"))


"""Funzione che crea una lista contenente i premi dellevarie squadre."""

def newTitoli():
    aux = readFile("dataset/Titoli.txt")
    titoli = []

    for titolo in aux:
        if titolo[0] == "SQU":
            titoli.append(titolo)

    pickle.dump(titoli, open("DatiElaborati/titoli_utili", "wb"))


"""Funzione che crea una nuova lista per le partite da usare per la Base Line."""

def newPartiteBaseLine():

    partiteBuone = pickle.load(open("datiElaborati/partite_utili", 'rb'))

    listaPartite = []

    for partita in partiteBuone:
        partita.casa = fromSquadraToCLub(partita.casa)
        partita.fuori = fromSquadraToCLub(partita.fuori)
        aux = [partita.casa, partita]
        listaPartite.append(aux)

    listaPartite.sort(key=lambda lista: lista[0])

    for i in range(len(listaPartite)):
        listaPartite[i] = listaPartite[i][1]

    indice = []
    vecchioClub = None

    for j in range(len(listaPartite)):
        if vecchioClub != listaPartite[j].casa:
            vecchioClub = listaPartite[j].casa
            indice.append([vecchioClub, j])


    pickle.dump(partiteBuone, open("DatiElaborati/partite_baseline_utili", "wb"))
    pickle.dump(indice, open("DatiElaborati/indici_utili", "wb"))


"""Funzione che crea una nuova lista contenenti le features utili per l'analisi."""

def newFeatures():

    partite = pickle.load(open("datiElaborati/partite_utili", 'rb'))

    features = []
    count = 0
    for partita in partite:
        count += 1
        features.append([partita.id, makeFeatures(partita)])

        if count % 5 == 0:
            pickle.dump(features, open("DatiElaborati/features_utili", "wb"))
            print "ultima partita salvata ---> ", count

    pickle.dump(features, open("DatiElaborati/features_utili", "wb"))