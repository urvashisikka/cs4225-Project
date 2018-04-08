
"""
The script below extract the stock prices for the past 6 months using the Quandl API.
The data retrieved and the computed fluctuations are stored automatically into separte text file"""

import pandas as pd
import quandl
import numpy as np
import pickle
import os
import pyformat

quandl.ApiConfig.api_key = '4eneTCPvj2z6youDnQcb' 

def makeDirectory(folder_name1,sub_folder):
        directory = os.path.join(folder_name1 , sub_folder)
        if not os.path.exists(directory):
                os.makedirs(directory)
        return directory

# The function takes variable data which has the daily closing price of a stock.
#It computes the weekly means and the maximum price in a week.

def computeWeeklyChange(data):
    
    weeklyMeans = []
    weeklyMax = []
    i = 0
    while i < len(data):
        weeklySet = data[i:min(i+5, len(data))]
#        print(weeklySet)
	weekLen=len(weeklySet)
	weeklyMeans.append(sum(weeklySet)/weekLen)
        weeklyMax.append(max(weeklySet))
        i = i + 5
    fluctuations = []
    for i in range(len(weeklyMeans) - 1):
        val = (weeklyMax[i+1] - weeklyMeans[i])*100/weeklyMeans[i]
	#val ='{:2f%}'.format(val)
	fluctuations.append("%0.2f" % val)
    return fluctuations

def aggregateWeeklyFluctuations(allFluctuations,approved_companies):
	fluctuationText = []

	aggregatefluctuation_directory = makeDirectory(folder_name,"aggregateWeeklyfluctuations")

	for j in range(len(allFluctuations[0])):

    		string = ' '.join(('Week',str(j+1), ':'))

    		for i in range(len(allFluctuations)):
               		try:
                      		value =str(allFluctuations[i][j])
              	 	except:
                      		value = 'NA'
               		string = ' '.join((string, approved_companies[i], ':',value,','))

    		fluctuationText.append(string)

		# write the weekly fluctation to a text file

	aggFluctuation_filename = 'aggregateWeeklyFluctuation.txt'

	aggregateWeeklyFluctuation_filename = os.path.join(aggregatefluctuation_directory ,aggFluctuation_filename)

	aggregateWeeklyfluctuation_output_file=open(aggregateWeeklyFluctuation_filename,'w')
	for string in fluctuationText:
     		aggregateWeeklyfluctuation_output_file.write("%s" % string)
     		aggregateWeeklyfluctuation_output_file.write('\n')



companies =["AMNZ","AAPL","FB","GOOGL","TWTR","MU","PGR","NFLX",
"GS","JNJ","DAL","BAC","CSCO","INTC","F","WFC","KMI","CVS","CLX",
"ALB","MCHP","EQR","SPG","M","CF","KHC","MDLZ","PG","MSFT","TSLA",
"CHKP","HACK","ABX","BCS","MAC","ORCL","AAON",
"FOX","MAA","GG","DB","DIS","DLA","BGR","C","CRI","CS",
"GES","BPMX","BBK","BCS","FEYE","SPLK","CRI","BFY","BB"
,"ACP","LOGM","BB","CAH","QQQ", "V","UNH","KO","GS","WMT",
"MRK","VZ","UTX","TRV","DIS","BA","NKE","MCD","JPM","GE",
"CVX","CAT","AXP","IBM","ALKS","BK","CELG","CHTR","CTXS","COST",
"DLTR","DISH","EBAY","ESRX","HAS","MAR","MAT","PYPL","SIRI",
"SBUX","SYMC","TSCO","ULTA","VIAB","VOD","VRTX","WDC","WBA",
"XRAY","ORLY","STX","WYNN","XLNX","PCAR","IDXX","CBT","COG",
"CAMP","CRC","CWT","CALX","CPT","CCBG","COF","CAH","DDR","FFG",
"AGM","FDX","GPS","GLOG","IT","GD","GIS","GM","GGP","GIG","HALL",
"ISSC","IBP","ICE","ICPT","IGT","XON","JCP","JBL","JACK","KTWO",
"K","KEG","KNX","LADR","LSR","LVS","LTM","TREE","LSI","LECO","LNC",
"M","MRO","MPX","VAC","MA","MAT","MXWL","MDR","MED","MCC","MGM",
"KORS","MSTR","MSEX","MPO","MTX","MS","MORN","MUR","NANO","MC","P",
"PEI","PE","PWR","RRD","RDN","RL","RNR","SPGI"]


allFluctuations= []
approved_companies=[]

folder_name = "./stock_data"

companies_directory = makeDirectory(folder_name , "companies") 

fluctuation_directory = makeDirectory(folder_name , "fluctuations")

for company in companies:
	# fetch the company data
	data = quandl.get_table('WIKI/PRICES', ticker = company, 
                        qopts = { 'columns': ['date', 'open', 'close', 'volume'] }, 
                        date = { 'gte': '2014-10-04', 'lte': '2018-02-04' })

	if len(data) == 0:
		print 'Data for %s is not available'%company
	else:
		print 'Data for %s fetched'%company
		approved_companies.append(company)
		# computation of the weekly fluctuations
		weeklyFluctuations = computeWeeklyChange(data['close'])
		# add to the list of fluctuation of all companies
       		allFluctuations.append(weeklyFluctuations)
                #print(allFluctuations)
		# write the data to a text file
		companiesData_filename = os.path.join(companies_directory, company + ".txt")
		companiesData_output_file=open(companiesData_filename,'w')
		data.to_string(companiesData_output_file,index = False)

		fluctuationData_filename = os.path.join(fluctuation_directory , company + "_Fluctuation.txt")
		fluctuationData_output_file=open(fluctuationData_filename,'w')

		for item in weeklyFluctuations:
	       		fluctuationData_output_file.write(item)
                	fluctuationData_output_file.write('\n')

#print(approved_companies)
aggregateWeeklyFluctuations(allFluctuations,approved_companies)

