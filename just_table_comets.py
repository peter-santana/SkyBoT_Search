#Same skybotfov but done for comets and for efficiency


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
file = open("Objects_commets.txt", "w")

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
while i < 9600:


	#Adding the minutes to date
	date = date + time_change

	print(date)


	#Load the parameters for the search query
	ploads = {"-ep":date.isoformat(), "-ra":RA[i], "-dec":DEC[i],"-mime":"text","-radius":str(TALL)+"x"+str(WIDE),"-objFilter":"001","-output":"object"}


	#TEXT request for query, will write in a seperate text file all the objects
	receive_text = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads)

	file.write(receive_text.text)



	i +=1

file.close()