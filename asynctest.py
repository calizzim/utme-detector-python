from requests import get
from time import sleep
from os import listdir
from requests import post
import csv
from pprint import pprint

#check wifi connection
def checkConnection():
  try:
    get("https://www.google.com")
    return True
  except:
    print("not connected to wifi")

#check if there are new datasets in the folder
def getDatasetsToUpload():
  datasets = set(listdir('./datasets'))
  with open('uploaded.txt') as uploadedFile:
    uploaded = set([s.strip() for s in uploadedFile.readlines()])
  return datasets.difference(uploaded)

#upload a dataset
def upload(filename):
  with open('datasets/'+filename,'r') as readfile:
    reader = csv.reader(readfile)
    dataset = ({ row[0]:(row[1:] if len(row)>2 else row[1]) for row in reader })
    #rename keys
    dataset["co2"] = dataset.pop("CO2")
    dataset["temperature"] = dataset.pop("T")
    dataset["humidity"] = dataset.pop("RH")
    dataset["tvoc"] = dataset.pop("TVOC")
    dataset["pm10"] = dataset.pop("PM1.0")
    dataset["pm25"] = dataset.pop("PM2.5")
    dataset["pm40"] = dataset.pop("PM4.0")
    dataset["pm100"] = dataset.pop("PM10.0")
    dataset["pmSize"] = dataset.pop("PMSize")
    del dataset["Timestamp"]
    pprint(dataset)

  result = post('http://localhost:3000/api/sensorData', json = dataset).status_code
  if(result == 200): print("upload successful")
  else: print("upload unsuccessful")

#main loop
while True:
  #check for wifi connection
  if(checkConnection()):
    print('connected')
    toUpload = getDatasetsToUpload()
    if(len(toUpload)):
      print('new datasets found')
      for dataset in toUpload:
        upload(dataset)
        with open('uploaded.txt','a') as uploadedFile:
          uploadedFile.write(dataset+'\n')
    else: print('no new datasets')
  else: print('not connected')
  sleep(5)