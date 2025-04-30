import requests
import csv

'''
this script will allow you to add Multiple ip object on a Palo Alto
you will need to have a CSV file ready (in this case: 'object-sample_with_desc.csv'.
the csv file will inclued the values need for the REST API.

---/ sample of the file:
H-10.40.30.10,10.40.30.10/32,Test Rest API
H-10.40.30.11,10.40.30.11/32,Test Rest API
H-10.40.30.12,10.40.30.12/32,Test Rest API
H-10.40.30.13,10.40.30.13/32,Test Rest API
H-10.40.30.14,10.40.30.14/32,Test Rest API
---/ end csv sample /---

below you will have a response request like:
response = requests.post(.....etc..

this will POST the content of the CSV to the Palo
to delete: change the .post to .delete :
response = requests.delete(....etc...
'''

# Setting basic parameters for the url
firewall_ip = 'https://192.168.55.180'
api_key = '<api_key-genertated from the firewall>'
api_version = 'v10.2'


#setting keys for the values in CSV file
keys = ["name", "ip", "description"]

#set empty list to be populated in the next phase
address_objects = []

#Reading CSV and setting items to be added to list above (address_objects)
with open ('object-sample_with_desc.csv') as f:
    read = csv.reader(f)
    for i in read:
        address_objects.append(dict(zip(keys, i)))


# Set headers
headers = {
    'X-PAN-KEY': api_key,
    'Content-Type': 'application/json'
}


# Disable SSL warnings (optional)
requests.packages.urllib3.disable_warnings()

#create the empty address-group
grp_url = 'https://192.168.55.180/restapi/v10.2/Objects/AddressGroups?location=vsys&vsys=vsys1&name=rest-test-api'
grp_payload = {"entry": {"@name":"rest-test-api", "static": {},"tag": {}, "description": {}}}
requests.post(grp_url, headers=headers, json=grp_payload, verify=False)

#creating an empty list to have members added later
grp_members = []

# Add each address object
for obj in address_objects:
    payload = {
        "entry": {
            "@name": obj["name"],
            "ip-netmask": obj["ip"],
            "description": obj["description"]
        }
    }
    objname = payload.get('entry', {}).get('@name')
    #Setting REST API URL
    url = f"{firewall_ip}/restapi/v10.2/Objects/Addresses?location=vsys&vsys=vsys1&name={objname}"
    #Sending the URL and expecting a response
    response = requests.post(url, headers=headers, json=payload, verify=False)

    #adding members to a list above named:grp_members
    grp_members.append(objname)

    if response.status_code == 200:
        print(f"Adding object {obj['name']} was completed successfully.")
    else:
        print(f"Failed to add {obj['name']}: {response.text}")

#adding members that were created above to the address-group
grp_payload = {"entry": {"@name":"rest-test-api", "static": {"member": grp_members}}}
grp_add = requests.put(grp_url, headers=headers, json=grp_payload, verify=False)
if response.status_code == 200:
    print(f"All members were added successfully to the group.")
else:
    print(f"Failed to add {obj['name']}: {response.text}")
