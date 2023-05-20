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
tagItem = tagsList[0]

for tagItem  in tagsList:
  TagName = tagItem[0]
  AwsTagName = tagItem[1]
  AwsTagValue = tagItem[2]
  payload = json.dumps(Func.getJsonTagPayload(TagName))
  response = Func.postRequest(REQUEST_URL,payload,header)

  if (response.ok != True):
    print("Failed to get response from API")
    exit()

  data = response.json()

  numberOfHostsPerTag = data['count']

  payload = json.dumps(Func.getJsonAwsTagPayload(AwsTagName,AwsTagValue))
  response = Func.postRequest(REQUEST_URL,payload,header)
  if (response.ok != True):
    print("Failed to get response from API")
    exit()

  data = response.json()
  numberOfHostsPerAwsTag = data['count']
  if(int(numberOfHostsPerTag) == int(numberOfHostsPerAwsTag)):
    msg = "success: tag" + str(TagName) + " expect result are "+ str(numberOfHostsPerTag)+ " match actual result: " + str(numberOfHostsPerAwsTag)
  else:
    msg = "failed: tag " + str(TagName) + " expect result are "+ str(numberOfHostsPerTag)+ " actual result: " + str(numberOfHostsPerAwsTag)
  print(msg)
  output.append(msg)

print("-----------------------------------------------------------------------------")
print(output)



