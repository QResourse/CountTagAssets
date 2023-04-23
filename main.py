import Config as Conf
import Lib.Functions as Func
import pandas as pd 
import json

BASE = Conf.base


BASE = Conf.base
GATEWAY = BASE.replace("qualysapi","gateway")
cleanPassword = Conf.PASSWORD.replace("%","%25")
safePassword = cleanPassword.replace("&","%26")
safePassword = safePassword.replace("#","%23")
payload = 'username='+Conf.USERNAME+"&password="+safePassword+"&token=true"
header = Func.getTokenHeader() 
REQUEST_URL = GATEWAY+"/auth"
response = Func.postRequest(REQUEST_URL,payload,header)
if (response.ok != True):
  print("Failed to get response from API")
  exit()

token = response.text



######Got the token ######

URL = "/rest/2.0/count/am/asset"

df = pd.read_xml('config.xml')
configList = df.iloc[0].to_list()
##header = Func.getXmlHeader(Conf.USERNAME,Conf.PASSWORD) 
header = Func.getHeaderBearer(token)
REQUEST_URL = GATEWAY + URL

df = pd.read_csv('tags.csv')

tagsList = df.values.tolist()



output = []
index = 0 
tagValue = tagsList[0]
for tagValue  in tagsList:
  assets= tagValue[1]
  tag = tagValue[0]
  payload = json.dumps(Func.getJsonTagPayload(tag))
  response = Func.postRequest(REQUEST_URL,payload,header)
  index+=1
  if (response.ok != True):
    print("Failed to get response from API")
    exit()

  data = response.json()

  numberOfHostsPerTag = data['count']
  if(int(numberOfHostsPerTag) == int(assets)):
    msg = "success: tag" + str(tag) + " expect result are "+ str(assets)+ " match actual result: " + str(numberOfHostsPerTag)
  else:
    msg = "failed: tag " + str(tag) + " expect result are "+ str(assets)+ " actual result: " + str(numberOfHostsPerTag)
    
    print(msg)
    output.append(msg)


  print(output)



