"""Mock objects for testing"""

SUBMISSION_POST_DATA = {
    "channel": "#slack_microservice_test",
    "message": "@henry Test message from slack microservice ",
    "file_path": "https://cdn4.iconfinder.com/data/icons/logos-and-brands-1/512/306_Slack_logo-512.png",
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
