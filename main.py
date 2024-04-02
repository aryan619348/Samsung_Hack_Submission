from flask import Flask,request,Response
from flask_sock import Sock
import json
import base64
from twilio.twiml.voice_response import Gather, VoiceResponse, Say
from transcribe import TwilioTranscriber
import os
import time
PORT=5000
DEBUG= False
INCOMING_CALL_ROUTE="/"
WEBSOCKET_ROUTE="/realtime"

from transcribe import sessionid
app=Flask(__name__)
sock=Sock(app)


@app.route(INCOMING_CALL_ROUTE,methods=['GET','POST'])
def receive_call():
    if request.method=='POST':
        open("output_audio.ulaw", "wb").close()
        xml= f"""
            <Response>
                <Say>
                    Welcome to the Samsung hack submission, you can now interact with our AI agent for a clothing brand called zorbo.
                </Say>
                <Connect>
                    <Stream url='wss://{request.host}{WEBSOCKET_ROUTE}' />
                </Connect>
            </Response>
            """.strip()
        return Response(xml,mimetype="text/xml")
    else:
        return "Realtime transcribe"

# @app.route("/speak",methods=['GET', 'POST'])
# def talk():
#     data = request.get_json()
#     answer = data.get('answer')
#     if request.method=='POST':
#         xml= f"""
#             <Response>
#                 <Say>
#                     {answer}
#                 </Say>
#             </Response>
#             """.strip()
#         return Response(xml,mimetype="text/xml")
#     else:
#         return "call fail"

@sock.route(WEBSOCKET_ROUTE)
def transription_websocket(ws):
    last_modified_time = 0 
    check_mark=True
    while True:
        data =json.loads(ws.receive())
        match data['event']:
            case "connected":
                transcriber= TwilioTranscriber()
                transcriber.connect()
                print('twillo connected')
            case "start":
                print('twilio started')
            case "media": 
                payload_b64 = data['media']['payload']
                payload_mulaw=base64.b64decode(payload_b64)
                transcriber.stream(payload_mulaw)
                current_modified_time = os.path.getmtime("output_audio.ulaw")
                if current_modified_time != last_modified_time:
                    with open("output_audio.ulaw", 'rb') as f:
                        out_audio = f.read()
                    base64_encoded = base64.b64encode(out_audio).decode('utf-8')
                    media_message = {
                        'event': 'media',
                        'media': { # Specify the track as outbound
                            'payload': base64_encoded  # Use the same payload received from Twilio
                        },
                        'streamSid': data.get('streamSid')  # Use the streamSid received from Twilio
                    }
                    mark_message={ 
                        "event": "mark",
                        "streamSid": data.get('streamSid'),
                        "mark": {
                        "name": "my label"
                        }
                    }
                    ws.send(json.dumps(media_message))
                    ws.send(json.dumps(mark_message))
                    last_modified_time = current_modified_time
                    time.sleep(3)
                     
            case "stop":
                print('twilio stopped')
                transcriber.close()
                print("transcriber closed")
            


if __name__=='__main__':
    app.run(port=PORT,debug=DEBUG)
