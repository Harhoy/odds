
#https://www.sbo.net/strategy/football-prediction-model-poisson-distribution/

#https://en.wikipedia.org/wiki/Kelly_criterion
#https://math.stackexchange.com/questions/662104/kelly-criterion-with-more-than-two-outcomes

import numpy as np
from scipy.stats import poisson


from os import listdir
from os.path import isfile, join
from os import getcwd


#-------------KLASSER--------------------#

class Kamp:
    def __init__(self, hjemmelag, bortelag, homeGoal, awayGoal,dato):
        self._hjemmelag = hjemmelag
        self._bortelag = bortelag
        self._homeGoal = int(homeGoal)
        self._awayGoal = int(awayGoal)
        self._dato = dato

    def skrivInfo(self):
        print("Hjemmelag:",self._hjemmelag,"Bortelag:",self._bortelag)

    def hentLag(self):
        return self._hjemmelag, self._bortelag

    def hentMaal(self):
        return self._homeGoal,self._awayGoal

class Lag:
    def __init__(self,navn):

        #Info
        self._navn = navn
        self._hjemmekamper = []
        self._bortekamper = []

        #Scoring
        self._hjemmeFor = 0
        self._hjemmeMot = 0
        self._borteFor = 0
        self._borteMot = 0

        #Snitt
        self._avgHjemmeFor = 0
        self._avgHjemmeMot = 0
        self._avgBorteFor = 0
        self._avgBorteMot = 0

        #Spilleparamtere
        self._homeAttack = 0.0
        self._homeDefense = 0.0
        self._awayAttack = 0.0
        self._awayDefense = 0.0

    def nyHjemmekamp(self,kamp):
        self._hjemmekamper.append(kamp)

    def skrivParametere(self):
        print("Lag:",self._navn)
        print("Angrep(H):","{:10.2f}".format(self._homeAttack))
        print("Forsvar(H):","{:10.2f}".format(self._homeDefense))
        print("Angrep(B):","{:10.2f}".format(self._awayAttack))
        print("Forsvar(B):","{:10.2f}".format(self._awayDefense))


    def hentParametere(self):
        return self._homeAttack,self._homeDefense,self._awayAttack,self._awayDefense

    def nyBortekamp(self,kamp):
        self._bortekamper.append(kamp)

    def skrivMaal(self):
        print("Hjemmemaal:",self._hjemmeFor)

    def hentNavn(self):
        return self._navn

    def hentKamper(self):
        return self._hjemmekamper,self._bortekamper

    def antallKamper(self):
        print("Kamper:",len(self._hjemmekamper))

    def beregnParametere(self,snitt):
        self._homeAttack = float(self._avgHjemmeFor/snitt[0])
        self._homeDefense = float(self._avgHjemmeMot/snitt[1])
        self._awayAttack = float(self._avgBorteFor/snitt[2])
        self._awayDefense = float(self._avgBorteMot/snitt[3])

    def beregnScore(self):

        #Summerer maal
        for kamp in self._hjemmekamper:
            hjemme,borte = kamp.hentMaal()
            self._hjemmeFor += hjemme
            self._hjemmeMot += borte

        for kamp in self._bortekamper:
            hjemme,borte = kamp.hentMaal()
            self._borteFor += borte
            self._borteMot += hjemme

        #Regner snitt
        self._avgHjemmeFor = float(self._hjemmeFor/len(self._hjemmekamper))
        self._avgHjemmeMot = float(self._hjemmeMot/len(self._hjemmekamper))
        self._avgBorteFor = float(self._borteFor/len(self._bortekamper))
        self._avgBorteMot = float(self._borteMot/len(self._bortekamper))

    def hentScore(self):
        return self._avgHjemmeFor,self._avgHjemmeMot,self._avgBorteFor,self._avgBorteMot


class Liga:

    def __init__(self,kamper):
        self._lag = []
        self._kamper = kamper

        self._homeFor = 0.0
        self._homeAgainst = 0.0
        self._awayFor = 0.0
        self._awayAgainst = 0


    def leggTilLag(self,nyttLag):
        funnet = False
        for lag in self._lag:
            if lag.hentNavn()== nyttLag:
                funnet = True

        if not funnet:
            self._lag.append(Lag(nyttLag))

    def skrivUtAlleLag(self):
        for lag in self._lag:
            print(lag.hentNavn())

    def hentAlleLag(self):
        return self._lag

    def finnLag(self,lagnavn):
        for lag in self._lag:

            if str(lag.hentNavn())==str(lagnavn):
                print(lagnavn,lag.hentNavn())
                return lag
        return None

    def hentLag(self,i):
        return self._lag[i]

    def beregnSnitt(self):
        for lag in self._lag:
            lag.beregnScore()

        #Beregner lagstyrk

        #Beregner snitt
        for lag in self._lag:
            score = lag.hentScore()
            self._homeFor += score[0]
            self._homeAgainst += score[1]
            self._awayFor += score[2]
            self._awayAgainst += score[3]

        #Snittberegning
        self._homeFor = float(self._homeFor/len(self._lag))
        self._homeAgainst = float(self._homeAgainst/len(self._lag))
        self._awayFor = float(self._awayFor/len(self._lag))
        self._awayAgainst = float(self._awayAgainst/len(self._lag))


        #Snittvektor
        snitt = [self._homeFor,self._homeAgainst,self._awayFor,self._awayAgainst]

        for lag in self._lag:
            lag.beregnParametere(snitt)

    def snitt(self):
        print(self._homeFor,self._homeAgainst,self._awayFor,self._awayAgainst)

    def prob_mat(self,home_team,away_team):

        size = 7
        table = np.zeros((size, size))
        scoreA = home_team.hentParametere()
        scoreB = away_team.hentParametere()

        for i in range(0,size):
            hjemmemaal = scoreA[0]*scoreB[3]*self._homeFor
            lambda_1 = (hjemmemaal)
            x_1 = poisson.pmf(i, lambda_1)

            for j in range(0,size):
                bortemaal = scoreA[1]*scoreB[2]*self._awayFor
                lambda_2 = (bortemaal)
                x_2 = poisson.pmf(j,lambda_2)
                table[i][j] = x_1*x_2


        away = np.sum(np.triu(table, k=1))
        tie = np.sum(np.diagonal(table))
        home = np.sum(np.tril(table, k=-1))

        resultsProb = {home_team.hentNavn():"{:10.2f}".format(home),'Tie':"{:10.2f}".format(tie), away_team.hentNavn():"{:10.2f}".format(away)}

        resultsMaal = {home_team.hentNavn():"{:10.2f}".format(hjemmemaal), away_team.hentNavn():"{:10.2f}".format(bortemaal)}

        return resultsProb


class BetKamp:

    def __init__(self,hjemmelag,bortelag,oddsH,oddsU,oddsB,liga):
        self._hjemmelag = hjemmelag
        self._bortelag = bortelag
        self._oddsH = float(oddsH)
        self._oddsU = float(oddsU)
        self._oddsB = float(oddsB)
        self._liga = liga

        self._return ={'H':0,'U':0,'B':0}

    def kampInfo(self):
        print("")
        print("Hjemmelag:",self._hjemmelag.hentNavn(),"Bortelag:",self._bortelag.hentNavn())
        print("Odds")
        print("H:",self._oddsH,"U:",self._oddsU,"B:",self._oddsB)

    def hentLag(self):
        return self._hjemmelag, self._bortelag

    def skrivInfo(self):
        streng = self._hjemmelag.hentNavn()+';'+self._bortelag.hentNavn()+';'+str(oddsH)+';'+str(oddsU)+';'+str(oddsB)
        return streng

    def calcReturn(self):
        prob = self._liga.prob_mat(self._hjemmelag,self._bortelag)
        self._return['H'] = self._oddsH*float(prob[self._hjemmelag.hentNavn()])-1.0
        self._return['U'] = self._oddsU*float(prob['Tie'])-1.0
        self._return['B'] = self._oddsB*float(prob[self._bortelag.hentNavn()])-1.0

        return self._return

def factorial(n):
    if n==0:
        return 1
    else:
        return n*factorial(n-1)

#def poisson(m,x):
#    return 2.71**(-m)*m**x/factorial(x)

#-------------MAIN--------------------#

def importKamper(fil):
    data = open(fil)
    for line in data:
        linjedata = line.split(';')
        hjemmelag = liga.finnLag(linjedata[0])
        bortelag = liga.finnLag(linjedata[1])
        h = linjedata[2]
        u = linjedata[3]
        b = linjedata[4]
        if hjemmelag != None and bortelag != None:
            nyeKamper.append(BetKamp(hjemmelag,bortelag,h,u,b,liga))

#Oppretter lister
lag = []
kamper = []
nyeKamper = []
liga = Liga(kamper)

#Leser inn data
file = open('Bundesliga.csv')
forsteLinje = True
#Legger til kamper
for line in file:
    if not forsteLinje:
        kampdata = line.split(';')
        dato = kampdata[1]
        hjemmelag = kampdata[2]
        bortelag = kampdata[3]
        homeGoal = kampdata[4]
        awayGoal = kampdata[5]
        kamper.append(Kamp(hjemmelag, bortelag,homeGoal,awayGoal,dato))
    else:
        forsteLinje = False

#Legger til lag
for kamp in kamper:
    lagA,lagB = kamp.hentLag()
    liga.leggTilLag(lagA)
    liga.leggTilLag(lagB)


#Legger kamper til lag
for lag in liga.hentAlleLag():
    for kamp in kamper:
        lagA,lagB = kamp.hentLag()
        if lag.hentNavn()==lagA:
            lag.nyHjemmekamp(kamp)
        elif lag.hentNavn()==lagB:
            lag.nyBortekamp(kamp)
        else:
            pass

#Regner ut parametere
liga.beregnSnitt()

'''
for lag in liga.hentAlleLag():
    lag.skrivParametere()
    lag.skrivMaal()
    lag.antallKamper()
    print("")
'''


#Neste fase:
#Lese inn Odds og beregne gevinst per spill
#Leser inn og lager BetKamp-objekter
#Går så gjennom disse og bereger
#Beregne fordelning (Kelly)

nummer = 0
fortsett = True

while fortsett:
    print("")
    print("#_________________________________#")
    print("Meny")
    print("#_________________________________#")
    print("0: Avslutt")
    print("1: Legg til ny kamp")
    print("2: Skriv ut alle kamper")
    print("3: Beregn sannsynligheter")
    print("4: Lagre kamper til fil")
    print("5: Hente kamper fra fil")

    svar = int(input("Tast inn ønsket valg: "))

    if svar == 0:
        fortsett = False

    elif svar == 1:
        print("")
        print("#_________________________________#")
        print("Lag i ligaen")
        print("#_________________________________#")
        i = 0
        for lag in liga.hentAlleLag():
            print(i,":",lag.hentNavn())
            i += 1

        print("")
        hjemmelag = int(input("Hjemmelag: "))
        bortelag = int(input("Bortelag: "))
        oddsH = float(input("OddsH: "))
        oddsU = float(input("OddsU: "))
        oddsB = float(input("OddsB: "))

        print(liga.hentLag(hjemmelag))

        nyeKamper.append(BetKamp(liga.hentLag(hjemmelag),liga.hentLag(bortelag),oddsH,oddsU,oddsB,liga))
    elif svar == 2:
        for kamp in nyeKamper:
            kamp.kampInfo()

    elif svar == 3:
        print("Informasjon om kamper")
        i= 0
        for kamp in nyeKamper:
            lag = kamp.hentLag()
            res = kamp.calcReturn()
            print("")
            print("Kamp:"+str(i))
            print(lag[0].hentNavn(),res['H'])
            print("U:",res['U'])
            print(lag[1].hentNavn(),res['B'])
            print("Sannsynligheter")
            print(liga.prob_mat(lag[0],lag[1]))


            i += 1

    elif svar == 4:
        filnavn = input("Oppgi filnavn: ")
        fil = open(filnavn+".csv",'w')
        tekst = ""
        for kamp in nyeKamper:
            fil.write(kamp.skrivInfo() + '\n')
        fil.close()

    elif svar == 5:
        mypath = getcwd()
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print("")
        print("Tilgjengelige filer")
        for i in range(len(onlyfiles)):
            print("Fil: ",i," ",onlyfiles[i])
        fil = int(input("Velg fil: "))
        importKamper(onlyfiles[fil])
