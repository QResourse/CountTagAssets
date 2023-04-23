import requests
import xml.etree.ElementTree as Xet
import base64
from datetime import timedelta, date
import os as _os
import pandas as pd 



#collecting data from XML 
def tryToGetAttribute(Object,inputString):
    try:
        output = Object.find(inputString).text
    except:
        output = "Null"
    
    return output

#collecting data from XML 
def tryToGetObj(Object,inputString):
    try:
        output = Object.find(inputString)
    except:
        output = "Null"
    
    return output


#used to get the access token
def getToken(USERNAME,PASSWORD):
    AuthStringRaw = USERNAME+":"+PASSWORD
    base64_bytes = AuthStringRaw.encode("ascii")
    authtoken = base64.b64encode(base64_bytes)
    base64_authtoken = authtoken.decode("ascii")
    return base64_authtoken

#calculate time delta
def getSearchTime(delta):
    today = date.today()
    lastweek_date = today - timedelta(days=delta)
    DateForSearch=lastweek_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return DateForSearch
#return timestemp 
def getStempTime():
    today = date.today()
    dt_string = today.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt_string



#Creates the XML to be used as payload 
def getXmlTagPayload(tag):
    ##payload = "<ServiceRequest> \r\n <preferences>\r\n <limitResults> 10000 </limitResults>\r\n<</preferences>\r\n<filters> \r\n <Criteria field=\"tagName\" operator=\"EQUALS\">"+str(tag)+"</Criteria> \r\n </filters> \r\n</ServiceRequest>"
    payload = "<ServiceRequest>\n\t<preferences>\n\t\t<limitResults>10</limitResults>\n\t</preferences>\n\t<filters>\n    \t<Criteria field=\"tagName\" operator=\"EQUALS\">"+str(tag)+"</Criteria>\n\t</filters>\n</ServiceRequest>"
    return payload


#Creates the XML to be used as payload 
def getJsonTagPayload(tag):
    ##payload = "<ServiceRequest> \r\n <preferences>\r\n <limitResults> 10000 </limitResults>\r\n<</preferences>\r\n<filters> \r\n <Criteria field=\"tagName\" operator=\"EQUALS\">"+str(tag)+"</Criteria> \r\n </filters> \r\n</ServiceRequest>"
    #payload = "<ServiceRequest>\n\t<preferences>\n\t\t<limitResults>10</limitResults>\n\t</preferences>\n\t<filters>\n    \t<Criteria field=\"tagName\" operator=\"EQUALS\">"+str(tag)+"</Criteria>\n\t</filters>\n</ServiceRequest>"
    payload = {
    "filters": [
        {
            "field": "tags.name",
            "operator": "CONTAINS",
            "value": tag
        }
    ]
    }
    return payload

#will be used by host API to get host based on time critira 
def getXmlPayload(id,delta):
    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\r\n<ServiceRequest>\r\n <preferences>\r\n <limitResults>10000</limitResults></preferences>\r\n   <filters>\r\n        <Criteria field=\"lastVulnScan\" operator=\"GREATER\">"+str(getSearchTime(delta))+"</Criteria>\r\n <Criteria field=\"id\" operator=\"GREATER\">"+str(id)+"</Criteria>\r\n    </filters>\r\n</ServiceRequest>"
    return payload

##Override - Delete - remove the False=True option
def getXmlHeader(USERNAME={},PASSWORD={}):
    headers = {
    "Content-Type": "application/xml",
    "Accept": "application/xml",
    "X-Requested-With": "QualysPostman",
    "Authorization": "Basic "+getToken(USERNAME,PASSWORD)
    }
    return headers


#Used to get the header of the request
def getHeader(USERNAME,PASSWORD):
    headers = {
    "X-Requested-With": "QualysPostman",
    "Authorization": "Basic "+getToken(USERNAME,PASSWORD)
    }
    return headers


#Used to Post requests
def postRequest(URL,payload,headers,files=[]):
    print("POSTING to "+ URL)
    #print("Payload: "+ str(payload))
    try:
        response = requests.request("POST", URL, headers=headers, data=payload, files=files)
    except:
        print("Failed to send request to API")
        return str(response.status_code)
    
    if (response.ok != True):
        print("Failed to get response from API")
        return {"Error"}
    else:
        return  response


def getRequest(URL,payload,headers,files=[]):
    print("POSTING to "+ URL)
    #print("Payload: "+ str(payload))
    try:
        response = requests.request("GET", URL, headers=headers, data=payload, files=files)
    except:
        print("Failed to send request to API")
    
    if (response.ok != True):
        print("Failed to get response from API")
        return {"Error"}
    else:
        return  response



def checkNumberOfHosts(RESPONSEXML):
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()
    count = root.find("count")
    #hostlist = response.find('HOST_LIST')
    #hosts = hostlist.findall('HOST')
    if(int(count.text) > 0):  
        return int(count.text)
    else:
        return 0

#Used to get the header of the request
def getHeaderBearer(token):
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'pageSize': '30',
    #'X-Requested-With': 'QualysPostman',
    'Authorization': 'Bearer '+ token
    }
    return headers

#Used to get the header of the request
def getTokenHeader():
    headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "X-Requested-With": "QualysPostman",
    }
    return headers

# #This method is used to ensure all the inforation is gathered from the host API
# def pocessHostRequests(response,RESPONSEXML,URL,payload,header,delta):
#     RESPONSE_FILEARRAY = []
#     index = 1
#     while(checkForMoreRecords(RESPONSEXML) == 'true'):
#         filename = "Response_" + str(index)+".xml"
#         newFile =_os.path.join("Requests",filename)
#         RESPONSE_FILEARRAY.append(newFile)
#         with open(newFile, "w") as f:
#             f.write(response.text.encode("utf8").decode("ascii", "ignore"))
#             f.close()
#         lastId = getLastRecord(RESPONSEXML)
#         payload = getXmlPayload(lastId,delta)
#         response = postRequest(URL,payload,header)
#         with open(RESPONSEXML, "w") as f:
#             f.write(response.text.encode("utf8").decode("ascii", "ignore"))
#             f.close()
#         index+=1
#         print(lastId)
#     filename = "Response_" + str(index)+".xml"
#     newFile =_os.path.join("Requests",filename)
#     RESPONSE_FILEARRAY.append(newFile)
#     with open(newFile, "w") as f:
#         f.write(response.text.encode("utf8").decode("ascii", "ignore"))
#         f.close()
#     print(RESPONSE_FILEARRAY)
#     return RESPONSE_FILEARRAY


# def MergeHostAndTags(HOSTS,TAGS):
#     df1 = pd.read_csv(HOSTS)
#     df2 = pd.read_csv(TAGS)
#     #list of hosts from _host file
#     listOfHosts= df1.HOST_ID.unique().tolist()
#     for host in listOfHosts:
#         #all the indexes of tags relevent to host
#         tagIndexList = df2.index[df2['HOST_ID']==host].tolist()
#         print("Host ID: "+ str(host) + "Tag list: "+str(tagIndexList))
#         for index in tagIndexList:
#             TagName =  df2.iloc[index][3]
#             hostIndex = df1.index[df1['HOST_ID']==host].tolist()
#             df1.at[int(hostIndex[0]),TagName] = 1
#     df1.to_csv(HOSTS)


def deleteTempFiles(files):
    for file in files:
        if _os.path.exists(file):
            _os.remove(file)



#Used to process multiple requests
def checkForMoreRecords(RESPONSEXML):
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()   
    Data = root.find("hasMoreRecords")
    return str(Data.text)

#Used to check if this is the last record during multiple requests
def getLastRecord(RESPONSEXML):
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()   
    Data = root.find("lastId")
    return str(Data.text)

#get list of hosts
def getHostAssets(RESPONSEXML):
    index = 0
    rows = []
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()
    Data = root.find("data")
    HostAssets  = Data.findall("HostAsset")
    for host in HostAssets:
        print("procecing host ",str(index))
        id = tryToGetAttribute(host,"id")
        rows.append({"HOST_ID": id})
        index+=1
    return rows

# #Returns a list of host matching a tag
# def GetAssetInfo(RESPONSE_FILEARRAY,HOSTS):

#     cols = ["HOST_ID"]
#     rows=[]
#     for filename in RESPONSE_FILEARRAY:
#         print("Processing file name: " + filename)
#         rowsData= getHostAssets(filename)
#         print("length of rows data: "+ str(len(rows)))
#         rows = rows + rowsData

#     print("length of rows: "+ str(len(rows)))
#     df = pd.DataFrame(rows, columns=cols)
#     df.to_csv(HOSTS,index=False, encoding="utf-8")
