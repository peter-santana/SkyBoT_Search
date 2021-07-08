# Skybot FOV objects LCAM project


import requests 
import sys
import time
from datetime import datetime, date, time, timedelta
import pandas as pd
from astropy.io.votable import parse
from astropy.io.votable import parse_single_table, is_votable, validate
import xml.etree.ElementTree as ET
import numpy as np
from scipy.interpolate import interp1d

#Number of columns for the data we recieve, numbers are honestly just placeholders
final_data = np.array([[1,2,3,4,5,6,7,8,9,10,11]])

#Change the name of the txt file to whatever you want
file = open("Objects_test.txt", "w")

#FOV dimensions to arcsecs
TALL = 20 * 3600

WIDE = 24 * 3600

#Include path and name of the excel file
file_name = "J2000 Coordinates - LCAM Center FOV Visibility Sheet.xlsx"

#grabbing data from excel sheet
df =  pd.read_excel(io=file_name)




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
while i < 10:


	#Adding the minutes to date
	date = date + time_change

	print(date)


	#Load the parameters for the search query
	ploads = {"-ep":date.isoformat(), "-ra":RA[i], "-dec":DEC[i],"-mime":"text","-radius":str(TALL)+"x"+str(WIDE),"-objFilter":"100","-output":"object"}


	#TEXT request for query, will write in a seperate text file all the objects
	receive_text = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads)

	file.write(date.isoformat())
	file.write(" RA: " + str(RA[i]))
	file.write(" DEC: " + str(DEC[i]))
	file.write(receive_text.text)
	file.write("\n")

	ploads_comets = {"-ep":date.isoformat(), "-ra":RA[i], "-dec":DEC[i],"-mime":"text","-radius":str(TALL)+"x"+str(WIDE),"-objFilter":"001","-output":"object"}

	receive_text_comets = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads)

	file.write("Comets: " + "\n")
	file.write(receive_text_comets.text)
	file.write("\n")

	#Same parameters but for the votable format(The one that lets you turn into array)
	ploads_vot = {"-ep":date.isoformat(), "-ra":RA[i], "-dec":DEC[i],"-mime":"votable","-radius":str(TALL)+"x"+str(WIDE),"-objFilter":"100","-output":"object"}

	#Same request but for VOTABLES
	receive_votables = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads_vot)


	#Turning into xml so parse from astropy can parse the data (idk why it works like that but it does lmao)
	root = ET.fromstring(receive_votables.text)
	tree = ET.ElementTree(root)
	tree.write("file.xml")

	votable = parse("file.xml")

	#Loop to get the tables and the data
	for resource in votable.resources:

		for table in resource.tables:
			tmp = table.array
			almost_final = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]])

			for table_lists in tmp:
				tmp_elementcreator = np.array([])

				for elem in table_lists:

					tmp_elementcreator = np.append(tmp_elementcreator,elem)
					# print(tmp_elementcreator)
					
				almost_final = np.append(almost_final,[tmp_elementcreator],axis=0)

			final_data = np.concatenate((final_data,almost_final))
				
		pass


	#increment loop 
	i +=1

file.close()


#Specific data analysis for NEAs, etc


nea_atira = open("NEA_Atira.txt","w")

a = np.where(final_data == b'NEA>Atira')


nea_atira.write("ATIRA NEA quantity: " + str(len(a[0])) + " (how many times we can actually see NEA asteroids)" + "\n")
unique_atira = final_data[a[0]]
nea_atira.write("ATIRA NEA Unique quantity: " +str(len(np.unique(unique_atira[:,1])))+ "\n")
nea_atira.write("ATIRA NEAs: " + "\n" )
np.savetxt(nea_atira, np.unique(unique_atira[:,1]), fmt='%s')
nea_atira.write("\n" + "All NEA data: " + "\n")
np.savetxt(nea_atira,final_data[a[0]],fmt='%s')
nea_atira.close()


nea_aten = open("NEA_Aten.txt","w")

b = np.where(final_data == b'NEA>Aten')

nea_aten.write("Aten NEA quantity: " + str(len(b[0])) + " (how many times we can actually see NEA asteroids)" + "\n")
unique_aten = final_data[b[0]]
nea_aten.write("Aten NEA Unique quantity: " +str(len(np.unique(unique_aten[:,1]))) + "\n")
nea_aten.write("Aten NEAs: " + "\n")
np.savetxt(nea_aten, np.unique(unique_aten[:,1]), fmt='%s')
nea_aten.write("\n" + "All NEA data: " + "\n")
np.savetxt(nea_aten,final_data[b[0]],fmt='%s')

nea_aten.close()


nea_apollo = open("NEA_Apollo.txt","w")

c = np.where(final_data == b'NEA>Apollo')

nea_apollo.write("Apollo NEA quantity: " + str(len(c[0])) + " (how many times we can actually see NEA asteroids)" + "\n")
unique_apollo = final_data[c[0]]
nea_apollo.write("Apollo NEA Unique quantity: " +str(len(np.unique(unique_apollo[:,1]))) + "\n")
nea_apollo.write("Apollo NEAs: " + "\n")
np.savetxt(nea_apollo,np.unique(unique_apollo[:,1]),fmt='%s')
nea_apollo.write("\n" + "All NEA data: " + "\n")
np.savetxt(nea_apollo,final_data[c[0]],fmt='%s')

nea_apollo.close()

nea_amor = open("NEA_Amor.txt","w")

d = np.where(final_data == b'NEA>Amor')

nea_amor.write("Amor NEA quantity: " + str(len(d[0])) + " (how many times we can actually see NEA asteroids)" + "\n")
unique_amor = final_data[d[0]]
nea_amor.write("Amor NEA Unique quantity: " +str(len(np.unique(unique_amor[:,1]))) + "\n")
nea_amor.write("Amor NEAs: " + "\n")
np.savetxt(nea_amor,np.unique(unique_amor[:,1]), fmt='%s')
nea_amor.write("\n" + "All NEA data: " + "\n")
np.savetxt(nea_amor,final_data[d[0]],fmt='%s')

nea_amor.close()

magnitudes = final_data[2:,6].astype(float)

magnitudes_less_than_7 = magnitudes < 7

magnitudes_less_than_9 = magnitudes < 9

magnitudes_less_than_10 = magnitudes < 10

magnitudes_less_than_11 = magnitudes < 11

magnitudes_less_than_12 = magnitudes < 12

magnitude_analysis = open("Magnitudes_Analysis.txt" , "w")

magnitude_analysis.write("Objects with Magnitude less than 7: "  + str(len(magnitudes_less_than_7)) + "\n")

magnitude_analysis.write("Objects with Magnitude less than 9: "  + str(len(magnitudes_less_than_9)) + "\n")

magnitude_analysis.write("Objects with Magnitude less than 10: "  + str(len(magnitudes_less_than_10)) + "\n")

magnitude_analysis.write("Objects with Magnitude less than 11: "  + str(len(magnitudes_less_than_11)) + "\n")

magnitude_analysis.write("Objects with Magnitude less than 12: "  + str(len(magnitudes_less_than_12)) + "\n")

magnitude_analysis.close()






# TODO: data analysis 

#how many MBI, MBII, etf…
# how many NEA, PHA, etc…
# how many comets …




