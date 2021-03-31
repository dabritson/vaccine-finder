import requests
import json
import settings
import time
import argparse
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from twilio.rest import Client

class Location():
    def __init__(self, name, address, city, state, zipCode, url, latitude, longitude):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.url = url
        self.latitude = latitude
        self.longitude = longitude
        self.distance = 0
        self.appointments = []

    def getName(self):
        return self.name

    def setDistanceFromLocation(self, zipCode):
        geolocator = Nominatim(user_agent="VaccineFinderV2")
        location = geolocator.geocode({"postalcode": zipCode}).raw
        latitude = location["lat"]
        longitude = location["lon"]
        location1 = (self.latitude, self.longitude)
        location2 = (latitude, longitude)
        self.distance = format(geodesic(location1, location2).mi, '.0f')

    def getDistanceFromLocation(self):
        return self.distance

    def addAppointment(self, time, vaccineType):
        newAppointment = Appointment(time, vaccineType)
        self.appointments.append(newAppointment)

    def getAppointmentCount(self):
        return len(self.appointments)

    def getAppointments(self):
        return self.appointments

    def getUrl(self):
        return self.url

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
        message = self.client.messages.create(
            body =  body,
            from_ = self.sendingPhoneNumber,
            to =    self.receivingPhoneNumber
        )
        message.sid

class VaccineSpotter():
    def __init__(self, websiteUrl, myZipCode):
        self.websiteUrl = websiteUrl
        self.myZipCode = myZipCode
        self.locations = []

    def __getWebsiteJson(self):
        response = requests.get(self.websiteUrl)
        return json.loads(response.text)

    def __extractLocationsAndAppointments(self, jsonData):
        for locationData in jsonData["features"]:
            latitude = locationData["geometry"]["coordinates"][1]
            longitude = locationData["geometry"]["coordinates"][0]
            providerBrandName = locationData["properties"]["provider_brand_name"]
            name = locationData["properties"]["name"]
            address = locationData["properties"]["address"]
            city = locationData["properties"]["city"]
            state = locationData["properties"]["state"]
            zipCode = locationData["properties"]["postal_code"]
            locationUrl = locationData["properties"]["url"]
            locationName = providerBrandName + " - " + name
            appointments = locationData["properties"]["appointments"]
            
            appointmentCount = len(appointments) if appointments else 0
            if appointmentCount > 0:
                newLocation = Location(locationName, address, city, state, zipCode, locationUrl, latitude, longitude)
                newLocation.setDistanceFromLocation(self.myZipCode)
                for appointment in appointments:
                    appointmentTime = appointment["time"]
                    appointmentVaccineType = appointment["type"]
                    newLocation.addAppointment(appointmentTime, appointmentVaccineType)
                self.locations.append(newLocation)

    def createLocationList(self):
        jsonData = self.__getWebsiteJson()
        self.__extractLocationsAndAppointments(jsonData)
        return self.locations

def main():
    url = settings.VACCINE_SPOTTER_URL
    myZipCode = settings.ZIP_CODE
    resultFoundSleep = settings.RESULT_FOUND_SLEEP_TIME
    resultNotFoundSleep = settings.RESULT_NOT_FOUND_SLEEP_TIME
    twilioAccountSid = settings.TWILIO_ACCOUNT_SID
    twilioToken = settings.TWILIO_TOKEN
    twilioPhoneNumber = settings.TWILIO_PHONE_NUMBER
    phoneNumberToReceiveNotifications = settings.PHONE_NUMBER_TO_RECEIVE_NOTIFICATIONS
    desiredDistance = settings.DESIRED_DISTANCE
    locations = []

    def deleteLocationsIfOutsideOfDesiredRange():
        for location in locations:
            if int(location.getDistanceFromLocation()) > desiredDistance:
                locations.remove(location)

    notification = Notification(twilioAccountSid, twilioToken, twilioPhoneNumber, phoneNumberToReceiveNotifications)

    while True:
        countLocationsOutOfRange = 0
        locations = VaccineSpotter(url, myZipCode).createLocationList()
        notificatonBody = ""
        notificationHeader = ""
        notificatonMessage = ""
        print(f"Found {len(locations)} locations with appointments\n")
        
        if len(locations) > 0:
            for location in locations:
                if not int(location.getDistanceFromLocation()) > desiredDistance:
                    if location.getAppointmentCount() > 0:
                        notificatonBody += (f"{location.toString()}\n")
                        notificatonBody += (f"{location.getAppointmentCount()} appointments\n")
                        notificatonBody += (f"{location.getDistanceFromLocation()} miles\n")
                        notificatonBody += (f"{location.getUrl()}\n\n")
                        print(location.toString())
                        print(f"Distance: {location.getDistanceFromLocation()} miles")
                        print("Appointments:")
                        for appointment in location.getAppointments():
                            print(f"\t{appointment.toString()}")
                        print("")
                else:
                    countLocationsOutOfRange += 1
                if countLocationsOutOfRange > 0:
                    print(f"Skipped {countLocationsOutOfRange} locations that were out of your desired range")
            notificationHeader = f"Found {len(locations)} locations with appointments."
            notificationHeader += f" {len(locations) - countLocationsOutOfRange} within your desired range and {countLocationsOutOfRange} outside of your desired range\n\n"
            notificatonMessage += notificationHeader
            notificatonMessage += notificatonBody
            notification.sendNotificaiton(notificatonMessage)
            print(f"Waiting for {resultFoundSleep} minutes....")
            time.sleep(resultFoundSleep * 60)
        else:
            print(f"Waiting for {resultNotFoundSleep} minutes....")
            time.sleep(resultNotFoundSleep * 60)

if __name__ == '__main__':
    main()
