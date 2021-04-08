"""Mock objects for testing"""

SUBMISSION_POST_DATA = {
    "channel": "#slack_microservice_test",
    "message": "@henry Test message from slack microservice ",
    "file_path": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuGqps7ZafuzUsViFGIremEL2a3NR0KO0s0RTCMXmzmREJd5m4MA&s",
    "file_name": "image.png",
    "file_upload_text": "File title",
    "blocks":  [{
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ":check: The script has run successfully on the dev."
      }
    }]
}
