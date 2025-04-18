import requests
ip=["37.46.105.2","37.40.225.99"]
# url=f"https://ipinfo.io/{ip}/geo"
# response=requests.get(url)
#
# print(response.status_code)
# mydata=response.json()

# print(mydata)
# print(type(mydata))
# for i,k in mydata.items():
#     print(k)
# for i in mydata.items():
#     print(i)

# for i,k in mydata.items():
#     if i=="city":
#         print(i,k)

for i in ip:
    url=f"https://ipinfo.io/{i}/geo"
    response = requests.get(url)
    mydata = response.json()
    print(mydata)

