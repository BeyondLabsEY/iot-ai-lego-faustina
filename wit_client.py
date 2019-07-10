from wit import Wit


def get_response(speech_file):
    access_token = "<access_token>"
    client = Wit(access_token)
    resp = None
    with open(speech_file, 'rb') as f:
        resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
    return resp
