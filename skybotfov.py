# Skybot FOV objects LCAM project


import requests 
import sys
import time
from datetime import datetime, date, time, timedelta
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


#Change the name of the txt file to whatever you want
file = open("Objects_test.txt", "w")

astr_file = open("Objects_test_asteroids.txt", "w")

comets_file = open("Objects_commets.txt", "w")

#FOV dimensions to arcsecs
TALL = 20 * 3600

WIDE = 24 * 3600

#Include path and name of the excel file
file_name = "J2000 Coordinates - LCAM Center FOV Visibility Sheet.xlsx"

#grabbing data from excel sheet
df = pd.read_excel(io=file_name)


#Turning declination from degrees and minutes into just degrees 
#Having them in an array
Declination = df["DEC (Deg)"] + (df["DEC (Min)"] / 60)

#Turning RA from hours and minutes into just degrees
#having them in an array
Right_Ascencion = (df["RA (Hours)"] * 15) + (df["RA (Min)"] / 60)

#9600 is the total number of timestamps from selected dates (change this depending on the excel file)
#In this case, its 200 days, measuring the FOV every 30 minutes, so 48 timeframes per day * 200 
#CHANGE THIS TO WHATEVER YOU NEED FOR THE TIME CHANGE IN DAYS
x = np.linspace(1,9601,len(Declination))

#interpolating data for declination 
dec_interp = interp1d(x, Declination)
ra_interp = interp1d(x, Right_Ascencion)

#generating array from 1 to 1960 to get the times in interpolation
new_x = np.arange(1,9601)

#Initial date 
date = datetime.strptime(df["DateandTime"][0], "%y:%m:%dT%H:%M:%S")

#establish the difference in times we want to see
#in this case we want 30 minutes
time_change = timedelta(minutes=30)

#substract 30 minutes so date starts normally in the loop
date = date - time_change

#extend interpolation objects so that they are an array of 1960 time frames
RA = ra_interp(new_x)
DEC = dec_interp(new_x)

i = 0

#Loop through all wanted generated points
while i < 9600:


	#Adding the minutes to date
	date = date + time_change

	print(date)


	#Load the parameters for the search query
	ploads = {"-ep":date.isoformat(), "-ra":RA[i], "-dec":DEC[i],"-mime":"text","-radius":str(TALL)+"x"+str(WIDE),"-objFilter":"100","-output":"object"}

	ploads_comets = {"-ep":date.isoformat(), "-ra":RA[i], "-dec":DEC[i],"-mime":"text","-radius":str(TALL)+"x"+str(WIDE),"-objFilter":"001","-output":"object"}

	#TEXT request for query, will write in a seperate text file all the objects
	receive_text = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads)

	receive_text_comets = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?", params=ploads_comets)

	file.write(date.isoformat())
	file.write(" RA: " + str(RA[i]))
	file.write(" DEC: " + str(DEC[i]))
	file.write(receive_text.text)
	file.write("\n")

	astr_file.write(receive_text.text)

	comets_file.write(receive_text_comets.text)



	#increment loop 
	i +=1

file.close()
astr_file.close()
comets_file.close()


#General Analysis

file = open("Analysis.txt", "w")

Asteroids = np.genfromtxt("Objects_test_asteroids.txt" , comments='#', delimiter = " | ",dtype=None,invalid_raise=False,usecols=(1), encoding=None)

Class = np.genfromtxt("Objects_test_asteroids.txt" , comments='#', delimiter = " | ",dtype=None,invalid_raise=False,usecols=(4), encoding=None)

Magnitudes = np.genfromtxt("Objects_test_asteroids.txt" , comments='#', delimiter = " | ",dtype=None,invalid_raise=False,usecols=(5), encoding=None)

Unique_Asteroids , ind = np.unique(Asteroids, return_index = True)

file.write("Asteroid Analysis resulting from skybot script: " + "\n" + "\n")

file.write("Total Asteroids found: " + str(Unique_Asteroids.shape[0]) + "\n")

#This are repeated elements, ignore
All_magnitudes = Magnitudes

Magnitudes = Magnitudes[ind]


Less_than_6 = Magnitudes[Magnitudes < 6]
Less_than_7 = Magnitudes[Magnitudes < 7]
Less_than_8 = Magnitudes[Magnitudes < 8]
Less_than_9 = Magnitudes[Magnitudes < 9]
Less_than_10 = Magnitudes[Magnitudes < 10]
Less_than_11 = Magnitudes[Magnitudes < 11]
Less_than_12 = Magnitudes[Magnitudes < 12]
Less_than_13 = Magnitudes[Magnitudes < 13]
Less_than_14 = Magnitudes[Magnitudes < 14]
Less_than_15 = Magnitudes[Magnitudes < 15]
Less_than_16 = Magnitudes[Magnitudes < 16]
Less_than_17 = Magnitudes[Magnitudes < 17]
Less_than_18 = Magnitudes[Magnitudes < 18]
Less_than_19 = Magnitudes[Magnitudes < 19]
Less_than_20 = Magnitudes[Magnitudes < 20]
Less_than_21 = Magnitudes[Magnitudes < 21]
Less_than_22 = Magnitudes[Magnitudes < 22]
Less_than_23 = Magnitudes[Magnitudes < 23]
Less_than_24 = Magnitudes[Magnitudes < 24]
Less_than_25 = Magnitudes[Magnitudes < 25]
Less_than_26 = Magnitudes[Magnitudes < 26]
Less_than_27 = Magnitudes[Magnitudes < 27]
Less_than_28 = Magnitudes[Magnitudes < 28]
Less_than_29 = Magnitudes[Magnitudes < 29]
Less_than_30 = Magnitudes[Magnitudes < 30]

file.write("Asteroids with visual magnitude less than 6: " + str(Less_than_6.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 7: " + str(Less_than_7.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 8: " + str(Less_than_8.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 9: " + str(Less_than_9.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 10: " + str(Less_than_10.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 11: " + str(Less_than_11.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 12: " + str(Less_than_12.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 13: " + str(Less_than_13.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 14: " + str(Less_than_14.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 15: " + str(Less_than_15.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 16: " + str(Less_than_16.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 17: " + str(Less_than_17.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 18: " + str(Less_than_18.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 19: " + str(Less_than_19.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 20: " + str(Less_than_20.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 21: " + str(Less_than_21.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 22: " + str(Less_than_22.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 23: " + str(Less_than_23.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 24: " + str(Less_than_24.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 25: " + str(Less_than_25.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 26: " + str(Less_than_26.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 27: " + str(Less_than_27.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 28: " + str(Less_than_28.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 29: " + str(Less_than_29.shape[0]) + "\n")
file.write("Asteroids with visual magnitude less than 30: " + str(Less_than_30.shape[0]) + "\n")

file.write("\n" + "The average magnitude for all asteroids is: " + str(np.average(Magnitudes)) + "\n")

Main_Belt_indexer = np.char.count(Class, "MB>") != 0

Main_Belt_ocurrences = Asteroids[Main_Belt_indexer]

Main_Belt_Asteroids = np.unique(Main_Belt_ocurrences)

file.write("\n" + "There are " + str(Main_Belt_Asteroids.shape[0]) + " main belt asteroids" + "\n")

Comets = np.genfromtxt("Objects_commets.txt" , comments="#", delimiter = " | ",dtype=None,invalid_raise=False,usecols=(1), encoding=None)

Comets = np.unique(Comets)

file.write("\n" + "Over " + str(Comets.shape[0]) + " comets can be seen, these are: " + "\n")
np.savetxt(file, Comets, fmt='%s')

Near_earth_indexer = np.char.count(Class, "NEA>") != 0

Near_earth_ocurrences = Asteroids[Near_earth_indexer]

Near_earth_Asteroids = np.unique(Near_earth_ocurrences)

file.write("\n" + "There are " + str(Near_earth_Asteroids.shape[0]) + " Near earth asteroids")
file.write("\n" + "The average magnitude of these NEA's is: " + str(np.average(All_magnitudes[Near_earth_indexer])) + "\n")


Hungaria_indexer = np.char.count(Class, "Hungaria") != 0

Hungaria_ocurrences = Asteroids[Hungaria_indexer]

Hungaria_asteroids = np.unique(Hungaria_ocurrences)

file.write("\n" + "There are " + str(Hungaria_asteroids.shape[0]) + " Hungaria type asteroids")
file.write("\n" + "The average magnitude of Hungaria type asteroids is: " + str(np.average(All_magnitudes[Hungaria_indexer])) + "\n")

np.savetxt("Hungaria_asteroids.txt" , Hungaria_asteroids, fmt='%s')

Trojan_indexer = np.char.count(Class, "Trojan") != 0

Trojan_ocurrences = Asteroids[Trojan_indexer]

Trojan_asteroids = np.unique(Trojan_ocurrences)

file.write("\n" + str(Trojan_asteroids.shape[0]) + " Trojan Asteroids can be seen" + "\n")
file.write("The average magnitude of the Trojan Asteroids that can be seen is: " + str(np.average(All_magnitudes[Trojan_indexer])) + "\n")
np.savetxt("Trojan_asteroids.txt", Trojan_asteroids, fmt="%s")

Mars_Crosser_indexer = np.char.count(Class, "Mars-Crosser") != 0

Mars_Crosser_ocurrences = Asteroids[Mars_Crosser_indexer]

Mars_Crosser_asteroids = np.unique(Mars_Crosser_ocurrences)

file.write("\n" + str(Mars_Crosser_asteroids.shape[0]) + " Mars-crosser asteroids can be seen" + "\n")
file.write("The average magnitude of Mars-crosser asteroids that can be seen is: " + str(np.average(All_magnitudes[Mars_Crosser_indexer])) + "\n")

np.savetxt("Mars_crossers.txt", Mars_Crosser_asteroids, fmt="%s")




file.close()



nea_atira = open("NEA_Atira.txt","w")

Nea_atira_indexer = np.char.count(Class, "NEA>Atira") != 0

Nea_atira_ocurrences = Asteroids[Nea_atira_indexer]

Nea_atira_asteroids = np.unique(Nea_atira_ocurrences)

nea_atira.write("ATIRA NEA quantity: " + str(Nea_atira_asteroids.shape[0])  + "\n")
nea_atira.write("ATIRA NEAs: " + "\n" )
np.savetxt(nea_atira, Nea_atira_asteroids, fmt='%s')
nea_atira.write("\n" + "All NEA data: " + "\n")
np.savetxt(nea_atira,Nea_atira_ocurrences,fmt='%s')
nea_atira.close()


nea_aten = open("NEA_Aten.txt","w")

Nea_aten_indexer = np.char.count(Class, "NEA>Aten") != 0

Nea_aten_ocurrences = Asteroids[Nea_aten_indexer]

Nea_aten_asteroids = np.unique(Nea_aten_ocurrences)

nea_aten.write("ATEN NEA quantity: " + str(Nea_aten_asteroids.shape[0])  + "\n")
nea_aten.write("ATEN NEAs: " + "\n" )
np.savetxt(nea_aten, Nea_aten_asteroids, fmt='%s')
nea_aten.write("\n" + "All NEA data: " + "\n")
np.savetxt(nea_aten, Nea_aten_ocurrences, fmt='%s')
nea_aten.close()


nea_apollo = open("NEA_Apollo.txt","w")

Nea_apollo_indexer = np.char.count(Class, "NEA>Apollo") != 0

Nea_apollo_ocurrences = Asteroids[Nea_apollo_indexer]

Nea_apollo_asteroids = np.unique(Nea_apollo_ocurrences)

nea_apollo.write("APOLLO NEA quantity: " + str(Nea_apollo_asteroids.shape[0])  + "\n")
nea_apollo.write("APOLLO NEAs: " + "\n" )
np.savetxt(nea_apollo, Nea_apollo_asteroids, fmt='%s')
nea_apollo.write("\n" + "All NEA data: " + "\n")
np.savetxt(nea_apollo, Nea_apollo_ocurrences, fmt='%s')
nea_apollo.close()



nea_amor = open("NEA_Amor.txt","w")
Nea_amor_indexer = np.char.count(Class, "NEA>Amor") != 0

Nea_amor_ocurrences = Asteroids[Nea_amor_indexer]

Nea_amor_asteroids = np.unique(Nea_amor_ocurrences)

nea_amor.write("AMOR NEA quantity: " + str(Nea_amor_asteroids.shape[0])  + "\n")
nea_amor.write("AMOR NEAs: " + "\n" )
np.savetxt(nea_amor, Nea_amor_asteroids, fmt='%s')
nea_amor.write("\n" + "All NEA data: " + "\n")
np.savetxt(nea_amor, Nea_amor_ocurrences, fmt='%s')
nea_amor.close()





