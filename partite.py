from datetime import datetime
import pickle



"""Claase partite, contiene gli attributi utili della tabella gareCampionato per svolgere l'analisi"""


class partite:
    def __init__(self, list):
        self.id = list[0]
        self.idGiornata = int(list[1])
        self.idCampionato = self.fromCampionatoToDate(list[2])
        self.garaStagione = int(list[3])  # non so che sia, messo nel dubbio.
        self.numGara = int(list[4])  # serve veramente?
        self.dataGara = datetime.strptime(list[5], '%d/%m/%Y')
        self.casa = list[6]
        self.fuori = list[7]
        self.setVintiCasa = int(list[10])  # serve veramente?
        self.setVintiFuori = int(list[11])  # serve veramente?
        self.impianto = list[22]  # se e' presente la capienza del palazzatto successivamente alla chamata al metodo
        # isGoodImpianto contiene questa.
        self.spettatori = int(list[23])
        self.puntiCasa = int(list[25])
        self.puntiFuori = int(list[26])
        self.paganti = int(list[28])
        self.omaggio = int(list[29])
        self.abbonati = int(list[30])
        self.tessere = int(list[31])
        self.tessereSIAE = int(list[32])

        def __repr__(self):
            return repr((self.name, self.grade, self.age))

    """Metodo che stabilisce se la partita si e' disputata in serie A1 in Regolar Season dalla stagione 2000/2001
     alla stagione 2017/2018."""

    def isGoodCampionato(self):

        campionati = pickle.load(open("datiElaborati/campionati_utili", "rb"))

        for campionato in campionati:
            if campionato[1] == self.idCampionato:
                return True

        return False

    """Metodo che stabilisce se e' presente il numero di spettatori, qual ora questo sia calcolabile solo come somma dei
     vari gruppi l'attributo spettatori viene settato a questo valore. """

    def isGoodSpettatori(self):

        spettatori = self.paganti
        spettatori += self.omaggio
        spettatori += self.abbonati
        spettatori += self.tessere
        spettatori += self.tessereSIAE

        if self.spettatori < spettatori:
            self.spettatori = spettatori

        if self.spettatori > 0:
            return True

        return False

    """Metodo che stabilisce se la partita e' stata giocata in un data festiva."""

    def isGoodDate(self):

        specialDates = ["01/01/2000", "01/01/2001", "01/01/2002", "01/01/2003", "01/01/2004", "01/01/2005",
                        "01/01/2006",
                        "01/01/2007", "01/01/2008", "01/01/2009", "01/01/2010", "01/01/2011", "01/01/2012",
                        "01/01/2013",
                        "01/01/2014", "01/01/2015", "01/01/2016", "01/01/2017", "01/01/2018",
                        "06/01/2000", "06/01/2001", "06/01/2002", "06/01/2003", "06/01/2004", "06/01/2005",
                        "06/01/2006",
                        "06/01/2007", "06/01/2008", "06/01/2009", "06/01/2010", "06/01/2011", "06/01/2012",
                        "06/01/2013",
                        "06/01/2014", "06/01/2015", "06/01/2016", "06/01/2017", "06/01/2018",
                        "25/04/2000", "25/04/2001", "25/04/2002", "25/04/2003", "25/04/2004", "25/04/2005",
                        "25/04/2006",
                        "25/04/2007", "25/04/2008", "25/04/2009", "25/04/2010", "25/04/2011", "25/04/2012",
                        "25/04/2013",
                        "25/04/2014", "25/04/2015", "25/04/2016", "25/04/2017", "25/04/2018",
                        "01/05/2000", "01/05/2001", "01/05/2002", "01/05/2003", "01/05/2004", "01/05/2005",
                        "01/05/2006",
                        "01/05/2007", "01/05/2008", "01/05/2009", "01/05/2010", "01/05/2011", "01/05/2012",
                        "01/05/2013",
                        "01/05/2014", "01/05/2015", "01/05/2016", "01/05/2017", "01/05/2018",
                        "02/06/2000", "02/06/2001", "02/06/2002", "02/06/2003", "02/06/2004", "02/06/2005",
                        "02/06/2006",
                        "02/06/2007", "02/06/2008", "02/06/2009", "02/06/2010", "02/06/2011", "02/06/2012",
                        "02/06/2013",
                        "02/06/2014", "02/06/2015", "02/06/2016", "02/06/2017", "02/06/2018",
                        "01/11/2000", "01/11/2001", "01/11/2002", "01/11/2003", "01/11/2004", "01/11/2005",
                        "01/11/2006",
                        "01/11/2007", "01/11/2008", "01/11/2009", "01/11/2010", "01/11/2011", "01/11/2012",
                        "01/11/2013",
                        "01/11/2014", "01/11/2015", "01/11/2016", "01/11/2017",
                        "08/12/2000", "08/12/2001", "08/12/2002", "08/12/2003", "08/12/2004", "08/12/2005",
                        "08/12/2006",
                        "08/12/2007", "08/12/2008", "08/12/2009", "08/12/2010", "08/12/2011", "08/12/2012",
                        "08/12/2013",
                        "08/12/2014", "08/12/2015", "08/12/2016", "08/12/2017",
                        "25/12/2000", "25/12/2001", "25/12/2002", "25/12/2003", "25/12/2004", "25/12/2005",
                        "25/12/2006",
                        "25/12/2007", "25/12/2008", "25/12/2009", "25/12/2010", "25/12/2011", "25/12/2012",
                        "25/12/2013",
                        "25/12/2014", "25/12/2015", "25/12/2016", "25/12/2017",
                        "26/12/2000", "26/12/2001", "26/12/2002", "26/12/2003", "26/12/2004", "26/12/2005",
                        "26/12/2006",
                        "26/12/2007", "26/12/2008", "26/12/2009", "26/12/2010", "26/12/2011", "26/12/2012",
                        "26/12/2013",
                        "26/12/2014", "26/12/2015", "26/12/2016", "26/12/2017",
                        "23/04/2000", "15/04/2001", "31/03/2002", "20/04/2003", "11/04/2004", "27/03/2005",
                        "16/04/2006",
                        "08/04/2007", "23/03/2008", "12/04/2009", "04/04/2010", "24/04/2011", "08/04/2012",
                        "31/03/2013",
                        "20/04/2014", "05/04/2015", "27/03/2016", "16/04/2017", "01/04/2018",
                        "24/04/2000", "16/04/2001", "01/04/2002", "21/04/2003", "12/04/2004", "28/03/2005",
                        "17/04/2006",
                        "09/04/2007", "24/03/2008", "13/04/2009", "05/04/2010", "25/04/2011", "09/04/2012",
                        "01/04/2013",
                        "21/04/2014", "06/04/2015", "28/03/2016", "17/04/2017", "02/04/2018"]

        for date in specialDates:
            if date == self.dataGara:
                return False

        return True

    """Metodo che verifica la presenza della capienza del palazzetto in cui si e' disputata la partita, se presente
     questo valore viene salvato nell'attributo impianto dell'oggetto partita."""

    def isGoodPalazzetto(self):

        impianti = []
        file_object = open('dataset/Impianti.txt', 'r')
        for line in file_object:
            impianti.append(line.strip().split(','))

        impianti.remove(impianti[0])

        for impianto in impianti:
            if impianto[0] == self.impianto:
                impianto[1] = int(impianto[1])
                if impianto[1] != 0:
                    self.impianto = impianto[1]
                    return True
                return False
        return False

    """ Metodo che stabilisce se la partita si e' disputata in serie A1 in Regolar Season dalla stagione 2000/2001
    alla stagione 2017/2018 e che verifica che la partita sia fra quelle centrali del campionatono, escludendo quindi
    le prime tre e le ultime tre."""

    def isGoodGiornata(self):

        giornate = pickle.load(open("datiElaborati/giornate_utili", "rb"))

        for giornata in giornate:

            if self.idGiornata == int(giornata[0]):  # seleziono la giornata della partita.

                if giornata[2] == '1':  # caso girone di andata.
                    if int(giornata[3]) < 4:
                        return False
                    return True

                else:  # caso girone di ritorno, dipende dal numero di squadre nei vari campionati,
                    #  non vi dovrebbero essere altri casi
                    if int(giornata[3]) >= giornata[6]:
                        return False
                    return True

    """Metodo che stabilisce, rendendo un valore booleano, se la partita e' utile ai fini dell'analisi."""

    def isVeryGood(self):
        if self.isGoodGiornata():
            if self.isGoodPalazzetto():
                if self.isGoodSpettatori():
                    if self.isGoodDate():
                        return True
        return False

    """Metodo che stabilisce, rendendo un valore booleano, se la partita e' utile ai fini della costruzione della 
    classifica."""

    def isGoodClassifiche(self):

        if self.isGoodCampionato():
            return True
        return False

    def printPartita(self):

        attributi = []

        attributi.append(self.id)
        attributi.append(self.idGiornata)
        attributi.append(self.idCampionato)
        attributi.append(self.garaStagione)
        attributi.append(self.numGara)
        attributi.append(self.dataGara)
        attributi.append(self.casa)
        attributi.append(self.fuori)
        attributi.append(self.setVintiCasa)
        attributi.append(self.setVintiFuori)
        attributi.append(self.impianto)
        attributi.append(self.spettatori)
        attributi.append(self.puntiCasa)
        attributi.append(self.puntiFuori)
        attributi.append(self.paganti)
        attributi.append(self.omaggio)
        attributi.append(self.abbonati)
        attributi.append(self.tessere)
        attributi.append(self.tessereSIAE)

        print attributi

    def fromCampionatoToDate(self, idCampionato):

        """Sostiuire idCampionato con l'anno iniziale del campionato. """

        campionatiUtili = pickle.load(open("datiElaborati/campionati_utili", 'rb'))

        for c in campionatiUtili:
            if idCampionato == c[0]:
                return c[1]


