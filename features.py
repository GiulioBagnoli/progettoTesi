from utility import *
from datetime import datetime






def makeFeatures(partita):

    features = []

    features.append(partita.spettatori / partita.impianto)

    """Inseriamo i punti delle due squadre."""
    punti = puntiSquadre_differenzaInClassifica(partita)
    features.append(punti[0])
    features.append(punti[2])

    """Inseriamo il livello delle due squadre basato sulla posizione dell'anno precedente."""
    livello = livSquadre(partita)
    features.append(livello[0])
    features.append(livello[1])

    """Differenziamo il giorno in cui e' stata svolta la gara."""
    features.append(giornoSett(partita))

    """Inseriamo la differenza in classifica delle due squadre, un valore positivo indica che la squadra in casa ha una 
    posizione superiore mentre un valore negativo indica che ha una posizione inferiore."""
    features.append(punti[3] - punti[1])

    """Inseriamo il numero di vittorie consecutive per le due squadre."""
    numVittorie = vittorieConsecutive(partita)
    features.append(numVittorie[0])
    features.append(numVittorie[1])

    """Inseriamo il numero di anni complessivi trascorsi in superLega per le due squadre"""
    anni = anniComplessivi(partita)
    features.append(anni[0])
    features.append(anni[1])

    """Inseriamo la possibilita' di accedere a una fascia superiore della classifica per le due squadre
    e la posizione in classifica rispetto alla stessa giornata dell'anno precedente per le due squadre"""
    fasce = nuovaFascia_posAnnoPrec(partita)
    features.append(fasce[0])
    features.append(fasce[1])
    features.append(fasce[2])
    features.append(fasce[3])

    """Inseriamo il numero di premi vinti dai due club negli anni precedenti."""
    premi = palmares(partita)
    features.append(premi[0])
    features.append(premi[1])

    """Inseriamo il numero di emittenti che possono aver pubblicizzato la partita. """

    pubblicita = numPubblicita(partita)
    features.append(pubblicita[0])
    features.append(pubblicita[1])

    """Verifichiamo se e' un derby."""

    features.append(derby(partita))

    return features


def puntiSquadre_differenzaInClassifica(partita):

    classifiche = pickle.load(open("datiElaborati/classifiche_utili", "rb"))

    for classifica in classifiche:
        if partita.idCampionato == classifica[0]:
            for i in range(1, len(classifica)):
                # l'ultima giornata viene esclusa dall'analisi, non dovrebbe dare errore
                if partita.idGiornata == classifica[i][0]:
                    aux = [None, None, None, None]
                    for j in range(1, len(classifica[i])):  # ciclo sulle partite
                        squadra = classifica[i][j]
                        clubCasa = fromSquadraToCLub(partita.casa)
                        clubFuori = fromSquadraToCLub(partita.fuori)
                        if clubCasa == squadra[0]:
                            aux[0] = squadra[1]
                            aux[1] = squadra[2]
                        elif clubFuori == squadra[0]:
                            aux[2] = squadra[1]
                            aux[3] = squadra[2]
                    return aux


"""
LIVELLO DELLE SQUADRE: alto = 0 | medio = 1 | basso = 2
"""
def livSquadre(partita):
    classifiche = pickle.load(open("datiElaborati/classifiche_utili", "rb"))
    if partita.idCampionato == 2000:
        return [1, 1]
    score = []
    for classifica in classifiche:
        if partita.idCampionato - 1 == classifica[0]:
            numUltimaGiornata = len(classifica) - 1
            clubFuori = fromSquadraToCLub(partita.fuori)
            clubCasa = fromSquadraToCLub(partita.casa)
            newClassifica = []
            for i in range(1, len(classifica[numUltimaGiornata])):
                puntiFinali = classifica[numUltimaGiornata][i][1] + classifica[numUltimaGiornata][i][3]
                newClassifica.append([classifica[numUltimaGiornata][i][0], puntiFinali])
            newClassifica.sort(key=lambda a: a[1], reverse=True)

            """Determiniamo la posizione in classifica."""
            firstTime = True
            posizione = 1
            count = 0
            for k in range(len(newClassifica)):
                if firstTime:
                    firstTime = False
                    newClassifica[k].append(posizione)
                elif newClassifica[k][1] != newClassifica[k - 1][1]:
                    posizione += 1
                    posizione += count
                    newClassifica[k].append(posizione)
                    count = 0
                else:
                    newClassifica[k].append(posizione)
                    count += 1
            for squadra in newClassifica:
                if clubCasa == squadra[0]:
                    if squadra[2] < 5:
                        livello = 0
                    elif squadra[2] < 9:
                        livello = 1
                    else:
                        livello = 2
                    score.append(livello)
                    break
            if len(score) != 1:
                score.append(2)
            for squadra in newClassifica:
                if clubFuori == squadra[0]:
                    if squadra[2] < 5:
                        livello = 0
                    elif squadra[2] < 9:
                        livello = 1
                    else:
                        livello = 2
                    score.append(livello)
                    break
            if len(score) != 2:
                score.append(2)
            return score


"""Metodo che assegna un valore a una data.
Inputs : -> data : oggetto di tipo data.
Output : valore intero. """
def giornoSett(partita):
    if partita.dataGara.weekday() > 4:
        return 1  # fineSettimana
    else:
        return 0  # infraSettimana


"""Rende il numero di vittorie consegutive."""
def vittorieConsecutive(partita):
    classifiche = pickle.load(open("datiElaborati/classifiche_utili", "rb"))
    clubFuori = fromSquadraToCLub(partita.fuori)
    clubCasa = fromSquadraToCLub(partita.casa)
    for classifica in classifiche:
        if partita.idCampionato == classifica[0]:
            notFound = True
            count = 1
            while (notFound):

                if partita.idGiornata == classifica[count][0]:
                    notFound = False
                else:
                    count += 1
            numWinsC = 0
            numWinsF = 0
            sconfittaCasa = False
            sconfittaFuori = False
            for i in range(count - 1, 0, -1):
                if sconfittaCasa and sconfittaFuori:
                    break
                for squadra in range(1, len(classifica[i])):
                    if sconfittaCasa == False and classifica[i][squadra][0] == clubCasa:
                        if classifica[i][squadra][3] > 1:
                            numWinsC += 1
                        else:
                            sconfittaCasa = True
                    if sconfittaFuori == False and classifica[i][squadra][0] == clubFuori:
                        if classifica[i][squadra][3] > 1:
                            numWinsF += 1
                        else:
                            sconfittaFuori = True
            return [numWinsC, numWinsF]


def anniComplessivi(partita):
    classifiche = pickle.load(open("datiElaborati/classifiche_utili", "rb"))
    anniCasa = 0
    anniFuori = 0
    casa = fromSquadraToCLub(partita.casa)
    fuori = fromSquadraToCLub(partita.fuori)
    for classifica in classifiche:
        if classifica[0] <= partita.idCampionato:
            squadre = []
            for j in range(1, len(classifica[1])):
                if classifica[1][j][0] not in squadre:
                    squadre.append(classifica[1][j][0])
            if casa in squadre:
                anniCasa += 1
            if fuori in squadre:
                anniFuori += 1
    return [anniCasa, anniFuori]


""" Rende una 4-tupla in cui i primi due elementi indicano la possibilita' della squadra di casa e della squadra
 ospite di entrare in una nuova fascia di diclassifica, dove le fasce sono:
 
 I --> 1 posizione.
 II --> 2 posizione.
 III --> 3 posizione.
 IV --> 4/8 posizione.
 V --> >8 posizione.
 
 Gli ultimi due elementi se la posizione dell'anno corrente e':
 
 -> migliore di almeno due posizioni o se la squadra non era presente in A1 l'anno precedente, valore 2.
 -> peggiore di almeno due posizioni, valore 0.
 -> altrimenti valore 1. 
 
 """
def nuovaFascia_posAnnoPrec(partita):

    classifiche = pickle.load(open("datiElaborati/classifiche_utili", "rb"))
    parziale = []
    vecchiaCasa = 1
    vecchiaFuori = 1
    changeCasa = False
    changeFuori = False

    for c in range(len(classifiche) - 1, -1, -1):
        if classifiche[c][0] == partita.idCampionato:

            for i in range(1, len(classifiche[c])):
                if classifiche[c][i][0] == partita.idGiornata:
                    indexGiornata = i
                    parziale = classifiche[c][i][1:]
                    break

            for j in range(1, len(classifiche[c][indexGiornata])):
                if classifiche[c][indexGiornata][j][0] == fromSquadraToCLub(partita.casa):
                    tuplaCasa = classifiche[c][indexGiornata][j]
                if classifiche[c][indexGiornata][j][0] == fromSquadraToCLub(partita.fuori):
                    tuplaFuori = classifiche[c][indexGiornata][j]

        if classifiche[c][0] == (partita.idCampionato - 1):

            if indexGiornata <= (len(classifiche[c]) - 1):

                for j in range(1, len(classifiche[c][indexGiornata])):

                    if classifiche[c][indexGiornata][j][0] == fromSquadraToCLub(partita.casa):
                        changeCasa = True
                        if classifiche[c][indexGiornata][j][2] - tuplaCasa[2] > 2:
                            vecchiaCasa = 2
                        elif tuplaCasa[2] - classifiche[c][indexGiornata][j][2] > 2:
                            vecchiaCasa = 0
                    if classifiche[c][indexGiornata][j][0] == fromSquadraToCLub(partita.fuori):
                        changeFuori = True
                        if classifiche[c][indexGiornata][j][2] - tuplaFuori[2] > 2:
                            vecchiaFuori = 2
                        elif tuplaFuori[2] - classifiche[c][indexGiornata][j][2] > 2:
                            vecchiaFuori = 0

            else:  # caso in cui il campionato precedente abbia meno giornate del campionato attuale
                # in questo caso se una partita sfora si fa riferimento all'ultima del campionato precedente

                indexGiornata = len(classifiche[c]) - 1 # il c qui indica gia' l'anno vecchio

                for j in range(1, len(classifiche[c][indexGiornata])):
                #if j < len(classifiche[c - 1][indexGiornata]) - 1:
                    #print "entro nell'if stronzo nell'anno ---> ", classifiche[c][0]
                    if classifiche[c][indexGiornata][j][0] == fromSquadraToCLub(partita.casa):
                        changeCasa = True
                        if classifiche[c][indexGiornata][j][2] - tuplaCasa[2] > 2:
                            vecchiaCasa = 2
                        elif tuplaCasa[2] - classifiche[c][indexGiornata][j][2] > 2:
                            vecchiaCasa = 0
                    if classifiche[c][indexGiornata][j][0] == fromSquadraToCLub(partita.fuori):
                        changeFuori = True
                        if classifiche[c][indexGiornata][j][2] - tuplaFuori[2] > 2:
                            vecchiaFuori = 2
                        elif tuplaFuori[2] - classifiche[c][indexGiornata][j][2] > 2:
                            vecchiaFuori = 0

            if not changeCasa:
                vecchiaCasa = 2
            if not changeFuori:
                vecchiaFuori = 2


    fasciaCasa = 0
    fasciaFuori = 0
    if tuplaCasa[2] == 2:
        if parziale[0][1] <= tuplaCasa[1] + 3:
            fasciaCasa = 1
    elif tuplaCasa[2] == 3:
        if parziale[1][1] <= tuplaCasa[1] + 3:
            fasciaCasa = 1
    elif tuplaCasa[2] > 3 and tuplaCasa[2] < 9:
        if parziale[2][1] <= tuplaCasa[1] + 3:
            fasciaCasa = 1
    elif tuplaCasa[2] >= 9:
        if parziale[7][1] <= tuplaCasa[1] + 3:
            fasciaCasa = 1
    if tuplaFuori[2] == 2:
        if parziale[0][1] <= tuplaFuori[1] + 3:
            fasciaFuori = 1
    elif tuplaFuori[2] == 3:
        if parziale[1][1] <= tuplaFuori[1] + 3:
            fasciaFuori = 1
    elif tuplaFuori[2] > 3 and tuplaFuori[2] < 9:
        if parziale[2][1] <= tuplaFuori[1] + 3:
            fasciaFuori = 1
    elif tuplaFuori[2] >= 9:
        if parziale[7][1] <= tuplaFuori[1] + 3:
            fasciaFuori = 1
    return [fasciaCasa, fasciaFuori, vecchiaCasa, vecchiaFuori]


"""Funzione che rende il nuemro di premi vinti dalle squadre prima della stagione della partita."""
def palmares(partita):
    clubCasa = fromSquadraToCLub(partita.casa)
    clubFuori = fromSquadraToCLub(partita.fuori)

    numPremiCasa = 0
    numPremiFuori = 0

    stagionePartita = partita.idCampionato

    titoli = pickle.load(open("datiElaborati/titoli_utili", 'rb'))

    for titolo in titoli:
        if stagionePartita > int(titolo[2]):
            if clubCasa == titolo[1]:
                numPremiCasa += 1
            elif clubFuori == titolo[1]:
                numPremiFuori += 1

    return [numPremiCasa, numPremiFuori]


"""Funzione che rende il numero di emittenti collegati alle due squadre nel periodo in cui si e' svolta la partita. """
def numPubblicita(partita):
    televisioni = readFile('dataset/TelevisioneClub.txt')
    radio = readFile('dataset/RadioClub.txt')
    giornalisti = readFile('dataset/GiornalistiClub.txt')

    clubCasa = fromSquadraToCLub(partita.casa)
    clubFuori = fromSquadraToCLub(partita.fuori)

    pubblicitaCasa = 0
    pubblicitaFuori = 0

    for tv in televisioni:
        # print datetime.strptime(tv[1], '%d/%m/%Y'), "---", partita.dataGara, "---", datetime.strptime(tv[2], '%d/%m/%Y')
        if datetime.strptime(tv[1], '%d/%m/%Y') < partita.dataGara and partita.dataGara < datetime.strptime(tv[2],
                                                                                                            '%d/%m/%Y'):

            if tv[0] == clubCasa:
                pubblicitaCasa += 1
            elif tv[0] == clubFuori:
                pubblicitaFuori += 1

    for rad in radio:
        if datetime.strptime(rad[1], '%d/%m/%Y') < partita.dataGara and partita.dataGara < datetime.strptime(rad[2],
                                                                                                             '%d/%m/%Y'):
            if rad[0] == clubCasa:
                pubblicitaCasa += 1
            elif rad[0] == clubFuori:
                pubblicitaFuori += 1

    for gio in giornalisti:
        if datetime.strptime(gio[1], '%d/%m/%Y') < partita.dataGara and partita.dataGara < datetime.strptime(gio[2],
                                                                                                             '%d/%m/%Y'):
            if gio[0] == clubCasa:
                pubblicitaCasa += 1
            elif gio[0] == clubFuori:
                pubblicitaFuori += 1

    return [pubblicitaCasa, pubblicitaFuori]


"""Funzione che rende un valore booleano, asserito a True se entrambe le squadre sono della stessa regione, 
False altrimenti."""
def derby(partita):
    clubCasa = fromSquadraToCLub(partita.casa)
    clubFuori = fromSquadraToCLub(partita.fuori)

    club = readFile('dataset/Club.txt')

    for c in club:
        if clubCasa == c[0]:
            regioneCasa = c[2]
        elif clubFuori == c[0]:
            regioneFuori = c[2]

    if regioneCasa == regioneFuori:
        return 1
    return 0
