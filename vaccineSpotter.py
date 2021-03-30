import requests
import json
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

class Location():
    def __init__(self, name, address, city, state, zipCode, latitude, longitude):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.latitude = latitude
        self.longitude = longitude
        self.appointments = []

    def getName(self):
        return self.name

    def getDistanceFromLocation(self, zipCode):
        geolocator = Nominatim(user_agent="VaccineFinderV2")
        location = geolocator.geocode({"postalcode": zipCode}).raw
        latitude = location["lat"]
        longitude = location["lon"]
        location1 = (self.latitude, self.longitude)
        location2 = (latitude, longitude)
        return format(geodesic(location1, location2).mi, '.2f')

    def addAppointment(self, time, vaccineType):
        newAppointment = Appointment(time, vaccineType)
        self.appointments.append(newAppointment)

    def getAppointmentCount(self):
        return len(self.appointments)

    def getAppointments(self):
        return self.appointments

    def toString(self):
        return f"{self.name}\n{self.address}\n{self.city}, {self.state} {self.zipCode}"

class Appointment():
    def __init__(self, time, vaccineType):
        self.time = time
        self.vaccineType = vaccineType

    def getAppointmentTime(self):
        return time

    def getVaccineType(self):
        return self.vaccineType

    def toString(self):
        return f"Time: {self.time} - Type: {self.vaccineType}"

class Notification():
    def __init__(self, accountSid, authToken, sendingPhoneNumber, receivingPhoneNumber):
        self.client = Client(accountSid, authToken)
        self.sendingPhoneNumber = sendingPhoneNumber
        self.receivingPhoneNumber = receivingPhoneNumber
        
    def sendNotificaiton(self, body):
        message = client.messages .create(
            body =  body,
            from_ = self.sendingPhoneNumber,
            to =    self.receivingPhoneNumber
        )
        message.sid

class VaccineSpotter():
    def __init__(self, websiteUrl):
        self.websiteUrl = websiteUrl

    def __getWebsiteJson(self):
        response = requests.get(self.websiteUrl)
        return json.loads(response.text)

    def __extractLocationsAndAppointments(self, jsonData):
        locations = []

        for locationData in jsonData["features"]:
            latitude = locationData["geometry"]["coordinates"][1]
            longitude = locationData["geometry"]["coordinates"][0]
            providerBrandName = locationData["properties"]["provider_brand_name"]
            name = locationData["properties"]["name"]
            address = locationData["properties"]["address"]
            city = locationData["properties"]["city"]
            state = locationData["properties"]["state"]
            zipCode = locationData["properties"]["postal_code"]
            locationName = providerBrandName + " - " + name
            appointments = locationData["properties"]["appointments"]

            newLocation = Location(locationName, address, city, state, zipCode, latitude, longitude)
            
            appointmentCount = len(appointments) if appointments else 0
            if appointmentCount > 0:
                for appointment in appointments:
                    appointmentTime = appointment["time"]
                    appointmentVaccineType = appointment["type"]
                    newLocation.addAppointment(appointmentTime, appointmentVaccineType)

            locations.append(newLocation)
        
        return locations

    def createLocationList(self):
        jsonData = self.__getWebsiteJson()
        locations = self.__extractLocationsAndAppointments(jsonData)
        return locations    

def main():
    url = "https://www.vaccinespotter.org/api/v0/states/MN.json"
    myZipCode = "55306"

    locations = VaccineSpotter(url).createLocationList()

    for location in locations:
        if location.getAppointmentCount() > 0:
            storeDistance = location.getDistanceFromLocation(myZipCode)
            print(location.toString())
            print(f"Distance: {storeDistance} miles")
            print("Appointments:")
            for appointment in location.getAppointments():
                print(f"\t{appointment.toString()}")
            print("")

if __name__ == '__main__':
    main()
