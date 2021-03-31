## What it is?

Updated to run in docker via the vaccine spotter API. 

* Scans the vaccine spotter api for resutls
* Validates results are within your desired range based on your zip code
* Will send you a text message with the results


## How to use

* Create a twilio account and setup a phone number in which to send messages from
* Create a twilio auth token
* Fill out the settings.py with the appropriate twilio data as well as adding your zip code
* Run the bash script; which takes care of creating your docker image as well as running your container
* `./run.sh`


## Todo?
* Add exception handling
* Allow app to continue if users don't add twilio info - just skip the notification
* Locate twilio support articles and add them here
* Probably some other stuff I'm missing...