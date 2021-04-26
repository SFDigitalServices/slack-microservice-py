
# SFDS slack-microservice-py [![CircleCI](https://circleci.com/gh/SFDigitalServices/slack-microservice-py.svg?style=svg)](https://circleci.com/gh/SFDigitalServices/slack-microservice-py) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/slack-microservice-py/badge.svg?branch=main)](https://coveralls.io/github/SFDigitalServices/slack-microservice-py?branch=main)
SFDS slack-microservice-py was developed for CCSF to send Slack messages.

## Requirements
* please refer to [DS microservice template](https://github.com/SFDigitalServices/microservice-py) for instructions to future development of this project.

## Usage
The Slack Microservice takes in a JSON object, parses through the parameters and sends the messages to a DS Slack channel.

Please refer to [data-sample.json] (https://github.com/SFDigitalServices/slack-microservice-py/blob/main/data-sample.json) for sample request
* For file uploads to work, you will need to add the slack microservice bot to the channel you're posting to.

The response is also a JSON object that looks like this:
```
    {"status": "fail", "data": {"message": "Failed to post file, error: Failed to post file"}
```

Running it locally
```
curl --location --request POST 'http://127.0.0.1:8000/slack-notification' --header 'ACCESS_KEY: 123456' --header 'Content-Type: text/plain' -d @data-sample.json
```