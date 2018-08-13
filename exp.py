from partite import partite
from utility import *
import pickle
from operator import attrgetter

min = 9999
resultGood = []
for i in range(1, 10):
    print "estrazione numero :", i
    results = pickle.load(open("datiElaborati/result"+str(i)+"_utili", 'rb'))
    for result in results:
        if result.meanSquareError < min :
            resultGood = []
            resultGood.append(result)
            min = result.meanSquareError
            print "cambio minimo, il nuovo minimo e' : ", min
        elif result.meanSquareError == min :
            resultGood.append(result)

print "fine"