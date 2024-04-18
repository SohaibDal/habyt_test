
## Import the required Libraries
import requests
from datetime import datetime
import csv

print("Import requests, datetime, csv Libraries")


# ## Retrive Data

## Data source URL
url = "https://www.common.com/cmn-api/listings/common"

## Retrive the data from the Data source
try:
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()
        # Now you can work with the data
        print('Data was successfully retrived')
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
except requests.exceptions.RequestException as e:
    print("Error:", e)


# ## Schema Design

# Property class definition
class Property:
    def __init__(self, data):
        self.id = data['propertyId']
        self.propertyName = data['propertyName']
        self.marketingName = data['marketingName']
        self.neighborhood = data['neighborhood']
        self.description = data['description']
        self.neighborhoodDescription = data['neighborhoodDescription']
        self.currencyCode = data['currencyCode']

# Address class definition
class Address:
    def __init__(self, data):
        self.id = f"{data['id']}-{data['propertyId']}"  ## Concatination of id and propertyID to create a unique addressID.
        address_data = data['address'] 
        self.fullAddress = address_data['fullAddress']
        self.roomNumber = address_data['roomNumber']
        self.streetAddress = address_data['streetAddress']
        self.city = address_data['city']
        self.stateCode = address_data['stateCode']
        self.postalCode = address_data['postalCode']
        self.countryCode = address_data['countryCode']
        self.latitude = address_data['latitude']
        self.longitude = address_data['longitude']
        self.belongedCity = address_data['belongedCity']

# Unit class definition
class Unit:
    def __init__(self, data):
        self.id = data['id']
        self.propertyId = data['propertyId']
        self.addressId = f"{data['id']}-{data['propertyId']}" ## Concatination of id and propertyID to create a unique addressID.
        self.bedrooms = data['bedrooms']
        self.listingSqft = data['listingSqft']
        self.unitSqft = data['unitSqft']
        self.occupancyType = data['occupancyType']
        self.availableDate = datetime.strptime(data['availableDate'], '%Y-%m-%d')

# Pricing class definition
class Pricing:
    def __init__(self, data):
        self.id = f"{data['id']}-{data['months']}"  ## Concatination of id and months to create a unique PricingID.
        self.unitId = data['id']
        self.name = data['name']
        self.durationMonths = data['months']
        self.amount = data['amount']
        self.concessionsApplied = ', '.join(data['concessionsApplied']) ## get the list of concessionsApplied in the form of text as there can be multiple concessions.
        self.minimumPrice = data['pricing']['minimumPrice']  ## minimumPrice for each unit
        self.maximumPrice = data['pricing']['maximumPrice']  ## maximumPrice for each unit
        self.minimumStay = data['pricing']['minimumStay']    ## minimumStay for each unit

# Fee class definition
class Fee:
    def __init__(self, data):
        self.id = f"{data['id']}-{data['name']}" ## Concatination of id and name to create a unique FeeID.
        self.unitId = data['id']
        self.name = data['name']
        self.description = data['description']
        self.amount = data['amount']
        self.isMandatory = data['isMandatory']
        self.isRefundable = data['isRefundable']

# Image class definition
class Image:
    def __init__(self, data):
        self.unitId = data['id']
        self.url = data['url']
        self.tag = data['tag']

print ("Created the Schema")


# ## Transform JSON data into object models

## Properties, Addresses, and Units: Each item in the JSON data corresponds directly to an object of these types.
properties = [Property(item) for item in data]
addresses = [Address(item) for item in data]
units = [Unit(item) for item in data]

## Pricings, Fees, and Images: Each item in the JSON data contains multiple entries for pricing, fees, and images respectively.
## Therefore, we iterate over these entries separately to create objects for each of them.
pricings = []
for item in data:
    for each_item in item['pricing']['monthlyPricing']:
        pricings.append(Pricing({**item, **each_item}))

fees = []
for item in data:
    for each_item in item['fees']:
        fees.append(Fee({**item, **each_item}))

images = []
for item in data:
    for each_item in item['images']:
        images.append(Image({**item, **each_item}))

print("Transformed Json data into Objects")


# ## Function to create CSV file

# Function to Create CSV files from objects
# Also make sure to drop duplicate rows (eg. Propertties file was getting duplicated rows)

def generate_csv(objects, filename):
    unique_rows = set()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=objects[0].__dict__.keys(), delimiter=';')
        writer.writeheader()
        for obj in objects:
              obj_row = tuple(obj.__dict__.values())
              if obj_row not in unique_rows:
                  writer.writerow(obj.__dict__)
                  unique_rows.add(obj_row)
    print(f"Created CSV file called '{filename}'")


# ## Create CSV files

## Using the created function. Generate the respective CSV files

generate_csv(properties, 'properties.csv')
generate_csv(addresses, 'addresses.csv')
generate_csv(units, 'units.csv')
generate_csv(pricings, 'pricings.csv')
generate_csv(fees, 'fees.csv')
generate_csv(images, 'images.csv')
