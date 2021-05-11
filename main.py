import requests
from datetime import datetime,timedelta
import json
from pprint import pprint
import time

requiredFeeType='Any' #CASE SENSITIVE - can be 'Free' or 'Paid' or 'Any'
requiredminAge= 46
maxWeeks=3 #or set float("inf") for all dates
minCapacity=1 #minimum 1 slot should be available
delayAfterEachRun=120 #Seconds

searchByPincode=True

pincodes=['125104']
districts={
  'Central Delhi':141,
  'East Delhi':145,
  'New Delhi':140,
  'North Delhi':146,
  'North East Delhi':147,
  'North West Delhi':143,
  'Shahdara':148,
  'South Delhi':149,
  'South East Delhi':144,
  'South West Delhi':150,
  'West Delhi':142,
  'Faridabad' :199,
  'Gurgaon' :188,
  'Gautam Buddha Nagar':650,
  'Ghaziabad' :651,
  # 'Bathinda' :493
}




#################################################################################################3
if(searchByPincode):
  searchIDs=pincodes #District picodes
else:
  searchIDs=list(districts.values()) #District ids of delhi

while(True):
  for searchID in searchIDs:

    today= datetime.now()
    curdate=today
    weeksdone=0
    while(weeksdone<maxWeeks): #for dates

      curdateString= curdate.strftime(r"%d-%m-%Y")
      # print('searchID - {} ::: Checking for week starting - {}'.format(str(searchID),curdateString))
      if(searchByPincode):
        URL='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}'.format(searchID,curdateString)
      else:
        URL='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}'.format(searchID,curdateString)
      
      
      headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
      responseJson = requests.get(URL,headers=headers).json()
      if(len(responseJson['centers'])==0):
        break

      for center in responseJson['centers']:
        
        #Check fee type
        if(requiredFeeType!='Any' and center['fee_type']!=requiredFeeType):
          continue

        for session in center['sessions']:
          if(requiredminAge>=session['min_age_limit'] and session['available_capacity']>=minCapacity):
            if(searchByPincode):
              print('Pincode - {} ::: Name - {} ::: Date - {} ::: VaccineInfo - {} ::: Capacity - {} ::: FeeType - {}'.format(searchID,center['name'],session['date'],session['vaccine'],str(session['available_capacity']),center['fee_type']))
            else:
              print('District - {} ::: Name - {} ::: Date - {} ::: VaccineInfo - {} ::: Capacity - {} ::: FeeType - {}'.format(center['district_name'],center['name'],session['date'],session['vaccine'],str(session['available_capacity']),center['fee_type']))

      curdate=curdate + timedelta(days=7)
      weeksdone+=1
      time.sleep(0.1)
  
  print('______________________________________________________________________________________________')
  # break
  time.sleep(delayAfterEachRun)
