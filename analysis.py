#MBA and Asteroid Analysis

import numpy as np 
from pandas import DataFrame as DF
import pandas as pd
import sys

from astropy.io import ascii

file = open("Analysis.txt", "w")

Asteroids = np.genfromtxt("Objects_test_asteroids.txt" , comments='#', delimiter = " | ",dtype=None,invalid_raise=False,usecols=(1), encoding=None)

Class = np.genfromtxt("Objects_test_asteroids.txt" , comments='#', delimiter = " | ",dtype=None,invalid_raise=False,usecols=(4), encoding=None)

Magnitudes = np.genfromtxt("Objects_test_asteroids.txt" , comments='#', delimiter = " | ",dtype=None,invalid_raise=False,usecols=(5), encoding=None)

Unique_Asteroids , ind = np.unique(Asteroids, return_index = True)

file.write("Asteroid Analysis resulting from skybot script: " + "\n" + "\n")

file.write("Total Asteroids found: " + str(Unique_Asteroids.shape[0]) + "\n")

#This is repeated elements, ignore
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
