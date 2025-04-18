import json

import requests
#url="https://ipinfo.io/37.46.15.2/geo"
# url="https://qamardevops.atlassian.net/rest/api/2/user?accountId=712020%3A9bf5cd4a-1df3-4b01-8e42-f82e1a5f7b37"
url="https://qamardevops.atlassian.net/rest/api/2/issue"
jira_token=""
user="mirza.qamar68@gmail.com"
header={
    "Accept":"application/json",
    "content-type":"application/json"
}

issue_dict={
    "fields":{
        "project": {"key":"SKP"},
        "issuetype":{"name":"Task"},
        "summary":"New issue is created with API",
        "description":"new discription"
    }
}

print(issue_dict)
payload=json.dumps(issue_dict)
#response=requests.get(url,headers=header)
#response=requests.get(url,auth=(user,jira_token),headers=header)
response=requests.post(url,auth=(user,jira_token),headers=header,data=payload)

mydata=response.json()
# print(mydata)
# status_code=response.status_code
# if status_code ==200:
#     print("Status is :", status_code ,"\n" "Header" ,response.headers ,"\n" "Response" ,response.json())
# else:
#     print("Status is :", status_code ,"\n" "Header" ,response.headers ,"\n" "Response" ,response.json())

# for i,k in mydata.items():
#     if i == "emailAddress":
#         print(i,":",k)
print(mydata)
