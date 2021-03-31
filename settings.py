# Url for vaccine spotter api
VACCINE_SPOTTER_URL="https://www.vaccinespotter.org/api/v0/states/MN.json"

# Amount of time to wait between runs when at least one result is found
RESULT_FOUND_SLEEP_TIME=60

# Amount of tiem to wait between runs when no results are found
RESULT_NOT_FOUND_SLEEP_TIME=3

# Your twilio account sid
TWILIO_ACCOUNT_SID=""

# Your twilio auth token
TWILIO_TOKEN=""

# The twilio phone number you'll use to send messages
# NOTE: must start with +1
TWILIO_PHONE_NUMBER=""

# The phone number you want to receive messages with
# NOTE: must start with +1
PHONE_NUMBER_TO_RECEIVE_NOTIFICATIONS=""

# Your zip code - used to messure distance
ZIP_CODE=""

# The desirecd distance in which to include results
DESIRED_DISTANCE=25