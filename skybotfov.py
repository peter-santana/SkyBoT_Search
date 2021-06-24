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



#USER MODE!!!! THE FIRST MODE HERE IS FOR USING THE PROGRAM WITH USER INPUT AND LOOPING
#SKIP UNTIL LINE 74



#EPOCH is the requested epoch, type "now" for now
#RA is the right ascencion of the FOV center
#DEC is the declination of the FOV center
#TALL is how tall in degrees the FOV is
#WIDE is how wide in degrees the FOV is
#END is the END EPOCH, meaning until what date and time do you want results
#MIN is the amount of time in minutes you want to update the timescale


# if len(sys.argv) > 6:
# 	EPOCH = sys.argv[1]
# 	RA = sys.argv[2]
# 	DEC = sys.argv[3]
# 	TALL = sys.argv[4]
# 	WIDE = sys.argv[5]
# 	END = sys.argv[6]
# 	MIN = sys.argv[7]
# else:
# 	print("missing parameter")
# 	sys.exit()

# #Turning degrees into arcsecs
# TAll = TALL * 3600
# WIDE = WIDE * 3600

# #Turning EPOCH string into datetime format
# date = datetime.strptime(EPOCH, "%Y-%m-%dT%H:%M:%S")

# file = open("resp_text.txt", "w")

# #Processing the data and recieving it
# while date.isoformat() != END:

# 	date = date + timedelta(minutes = int(MIN))

# ploads = {"-ep":date.isoformat(), "-ra":RA, "-dec":DEC,"-mime":"text","radius":str(TALL)+"x"+str(WIDE),"objfilter":"100"}

# 	receive = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads)

# 	print("EPOCH is: "+date.isoformat()+"\nRight Ascencion is: "+RA+"°"+"\nDeclination is: "+DEC+"°")
# 	print(receive.text)

# 	file.write(date.isoformat())
# 	file.write(receive.text)
# 	file.write("\n")



# file.close()

final_data = np.array([[1,2,3,4,5,6,7,8,9,10,11]])



file = open("resp_text.txt", "w")


TALL = 20 * 3600

WIDE = 24 * 3600

#Include path and name of the excel file
file_name = "J2000 Coordinates - LCAM Center FOV Visibility Sheet.xlsx"

df =  pd.read_excel(io=file_name)

i = 1

#Loop through all the excel file
while i <= 3:

	#Grab date from excel file
	date = datetime.strptime(df["DateandTime"][i], "%y:%m:%dT%H:%M:%S")

	#Turn RA from Hours and minutes to degrees
	RA = float(df["RA (Hours)"][i]) + float(df["RA (Min)"][i])

	#Turn DEC from degree and minutes to just degrees
	DEC = float(df["DEC (Deg)"][i] + float(df["DEC (Min)"][i]))


	#Load the parameters for the search query
	ploads = {"-ep":date.isoformat(), "-ra":RA, "-dec":DEC,"-mime":"text","-radius":str(TALL)+"x"+str(WIDE),"-objFilter":"100","-output":"object"}


	#TEXT request for query, will write in a seperate text file all the objects
	receive_text = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads)

	file.write(date.isoformat())
	file.write(receive_text.text)
	file.write("\n")

	#Same parameters but for the votable format(The one that lets you turn into array)
	ploads_vot = {"-ep":date.isoformat(), "-ra":RA, "-dec":DEC,"-mime":"votable","-radius":str(TALL)+"x"+str(WIDE),"-objFilter":"100","-output":"object"}

	#Same request but for VOTABLES
	receive_votables = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads_vot)


	#Turning into xml so parse from astropy can parse the data (idk why it works like that but it does lmao)
	root = ET.fromstring(receive_votables.text)

	tree = ET.ElementTree(root)

	#TODO: Error exception for astropy to not read empty xml, looking at how to do that
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
				print(almost_final)
				

			final_data = np.concatenate((final_data,almost_final))
				


		
		pass
			



	#increment loop 
	i +=1



	#TODO: ANALYSIS OF ARRAYS AND RESULTS




