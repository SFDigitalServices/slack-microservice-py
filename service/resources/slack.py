""" Twilio SMS """
import os
import json
import falcon
import jsend
import requests
import urllib.request
from .hooks import validate_access

@falcon.before(validate_access)
class SlackService():
    """ Slack service """
    def on_post(self, req, resp):
        """ Implement POST """
        request_body = req.bounded_stream.read()
        json_params = json.loads(request_body)
        message = json_params.get('message', '')
        slack_channel = json_params.get('channel', os.environ.get('SLACK_CHANNEL'))
        #blocks = json_params.get('blocks', None)
        blocks = None
        slack_token = json_params.get('SLACK_API_TOKEN', os.environ.get('SLACK_API_TOKEN'))

        if slack_token and slack_channel:
            response = self.post_message_to_slack(message, slack_token, slack_channel, blocks)

            if response["ok"]:
                print("Message sent to {}".format(slack_channel))
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(jsend.success({
                    'message': 'Slack message sent to ' + slack_channel
                }))
            else:
                print("Message failed to sent, error {}".format(response["error"]))
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(jsend.fail({
                    'message': 'Failed to send Slack message, error: ' + response["error"]
                }))

            #post a file
            file_path = json_params.get('file_path', '')
            if file_path != '':
                response = urllib.request.urlopen(file_path)
                data = response.read()
                file_upload_text = json_params.get('file_upload_text', 'file upload')
                file_name = json_params.get('file_name', '_file_name')

                posted_file = self.post_file_to_slack(
                    file_upload_text,
                    slack_token,
                    slack_channel,
                    file_name,
                    data
                )
                if posted_file["ok"]:
                    print("File uploaded to {}".format(slack_channel))
                    resp.status = falcon.HTTP_200
                    resp.body = json.dumps(jsend.success({
                        'message': 'File posted to ' + slack_channel
                    }))
                else:
                    print("File failed to upload, error: {}".format(posted_file["error"]))
                    resp.status = falcon.HTTP_400
                    resp.body = json.dumps(jsend.fail({
                        'message': 'Failed to post file, error: ' + posted_file['error']
                    }))

    @staticmethod
    def post_message_to_slack(message, slack_token, slack_channel, blocks=None):
        """ post a message to slack channel """
        url = os.environ.get('SLACK_API_URL', 'https://slack.com/api/')
        try:
            return requests.post(url+'chat.postMessage', {
                'token': slack_token,
                'channel': slack_channel,
                'text': message,
                'link_names': 1,
                'icon_url': os.environ.get('SLACK_ICON_URL', ''),
                'username': os.environ.get('SLACK_USER_NAME', ''),
                'blocks': json.dumps(blocks) if blocks else None
            }).json()
        except Exception: #pylint: disable=broad-except
            return {"ok": False, "error": "Failed to send"}

    @staticmethod
    #pylint: disable=too-many-arguments
    def post_file_to_slack(
            text, slack_token, slack_channel, file_name, file_bytes,
            file_type=None, title=None
    ):
        """ post a file to slack channel """
        try:
            return requests.post(
                'https://slack.com/api/files.upload',
                {
                    'token': slack_token,
                    'filename': file_name,
                    'channels': slack_channel,
                    'filetype': file_type,
                    'initial_comment': text,
                    'title': title
                },
                files={'file': file_bytes}).json()
        except Exception: #pylint: disable=broad-except
            return {"ok": False, "error": "Failed to post file"}
