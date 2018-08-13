import pickle
# from svm.svmutil import *
from svmutil_prova import *

from result import result
import itertools
from utility import *

results = []
classificazioni = [' -s 3', ' -s 4']
kernel = [' -t 0', ' -t 2']
scalati = [True, False]
features = ['punti_squadre', 'livello_squadre', 'giorna_partita', 'differenza_classifiche', 'vittorie_consegutive',
            'probabilita_nuova_fascia', 'posizione_classifica_vecchia', 'premi_club', 'numero_emittenti', 'derby']
count = 1

for s in scalati:
    print "--> inizio ciclo con dati scalati : ", s
    for dim in range(10, 40, 10):
        print "----> inizio ciclo con dimensione set : ", dim, "%"
        for i in range(7, len(features)):
            partialFeatures = list(itertools.combinations(features, i))
            for pf in partialFeatures:
                print "---- --> inizio ciclo con le seguenti features : "
                for p in pf:
                    print "---- ---- >", p
                y, x = prepareData(pf, s)
                dimensione = len(x) / 100 * dim
                prob = svm_problem(y[:dimensione], x[:dimensione])
                x = x[dimensione:]
                y = y[dimensione:]

                for classificazione in classificazioni:
                    print "---- ---- --> inizio ciclo su classificazione : ", classificazione
                    for k in kernel:

                        if k == ' -t 2':
                            print "\n---- ---- ----> inizio ciclo su kernel : ", k
                        else:
                            print "---- ---- ----> inizio ciclo su kernel : ", k

                        r = result(classificazione, k, s, dim, pf, prob, x, y)
                        if k == ' -t 2':
                            print ""
                        results.append(r)

                if len(results) % 500 == 0:
                    pickle.dump(results, open("DatiElaborati/result" + str(count) + "_utili", "wb"))
                    print ""
                    print "---- ---- ----> salvataggio <---- ---- ---- ", len(results)
                    print ""
                    count += 1
                    results = []

pickle.dump(results, open("DatiElaborati/result" + str(count) + "_utili", "wb"))
