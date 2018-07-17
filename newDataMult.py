
#Data grab from football-data.co.uk
#HH, 8.07.18

#--------------------------------------------------------#

#Imports
import subprocess
import sys

#Getting user parameters
minSes = int(sys.argv[1]) #Get data from this season and onwards
outName = sys.argv[2] #Get data from this season and onwards
url = sys.argv[3] #URL
special = int(sys.argv[4])
print("Speical", special)

#Getting data from football-data.co.uk
subprocess.call(['curl',url,'-onydata.txt'])

#Boolean to skip first line
forsteLinje = True

#Reading downloaded data file
turneringer = open('nydata.txt','r')
#Opening file for export of results
outfile = open(outName,"w")


#Looping through data file
for line in turneringer:

    if not forsteLinje:
        #Get line data
        linjeData = line.split(',')
        #Get variables
        if special == 1:
            sesong = int(linjeData[2]) #sesong
            dato = linjeData[3] #data
            home = linjeData[5] #home team
            away = linjeData[6] #away team
            hg = linjeData[7] # home goals
            ag = linjeData[8] #away goals
        else:
            dato = linjeData[1] #data
            home = linjeData[2] #home team
            away = linjeData[3] #away team
            hg = linjeData[4] # home goals
            ag = linjeData[5] #away goals

            dateInfo = dato.split('/')
            sesong = int("20"+dateInfo[2])

        #Adding data if correct season
        if sesong >= minSes:
            dataLine = str(sesong) + ';' + dato + ';' + home + ';' + away + ';' +str(hg) + ';' + str(ag) + '\n'
            outfile.write(dataLine)
    else:
        forsteLinje = False
        outfile.write("Season;Data;Home;Away;HG;AG\n")

outfile.close()
