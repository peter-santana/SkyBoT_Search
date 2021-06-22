# Skybot FOV objects LCAM project


import requests 
import sys
import time
from datetime import datetime, date, time, timedelta
import pandas as pd
from astropy.io.votable import parse
from astropy.io.votable import parse_single_table
import xml.etree.ElementTree as ET



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





file = open("resp_text.txt", "w")


TALL = 20

WIDE = 24

#Include path and name of the excel file
file_name = "J2000 Coordinates - LCAM Center FOV Visibility Sheet.xlsx"

df =  pd.read_excel(io=file_name)

i = 1

#Loop through all the excel file
while i <= 10:

	#Grab date from excel file
	date = datetime.strptime(df["DateandTime"][i], "%y:%m:%dT%H:%M:%S")

	#Turn RA from Hours and minutes to degrees
	RA = float(df["RA (Hours)"][i]) + float(df["RA (Min)"][i])

	#Turn DEC from degree and minutes to just degrees
	DEC = float(df["DEC (Deg)"][i] + float(df["DEC (Min)"][i]))


	#Load the parameters for the search query
	ploads = {"-ep":date.isoformat(), "-ra":RA, "-dec":DEC,"-mime":"text","-radius":str(TALL)+"x"+str(WIDE)}


	#TEXT request for query, will write in a seperate text file all the objects
	receive_text = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads)

	file.write(date.isoformat())
	file.write(receive_text.text)
	file.write("\n")

	#Same parameters but for the votable format(The one that lets you turn into array)
	ploads = {"-ep":date.isoformat(), "-ra":RA, "-dec":DEC,"-mime":"votable","-radius":str(TALL)+"x"+str(WIDE)}

	#Same request but for VOTABLES
	receive_votables = requests.get("http://vo.imcce.fr/webservices/skybot/skybotconesearch_query.php?",params=ploads)


	#Turning into xml so parse from astropy can parse the data (idk why it works like that but it does lmao)
	root = ET.fromstring(receive_votables.text)

	tree = ET.ElementTree(root)

	#TODO: Error exception for astropy to not read empty xml, looking at how to do that
	tree.write("file.xml")

	votable = parse("file.xml")

	#TODO:
	#get the first table (will change this after bc I intend to get all, Testing rn)
	table = votable.get_first_table()

	#Turn data into an array
	data = table.array

	#Testing this lmao
	print(data)

	#increment loop 
	i+=1

	# print(receive_text.url)

	# table = parse_single_table(receive_votables.text)

	# data = table.array

	# print(data)


	#TODO: ANALYSIS OF ARRAYS AND RESULTS





