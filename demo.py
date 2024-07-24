from freeswitch import *
import json

def input_callback(session, what, obj):
    consoleLog("info", "Input callback triggered: %s\n" % what)
    return "pause"

def bridge_command(session):
    original_called_number = session.getVariable("destination_number")
    original_caller_number = session.getVariable("caller_id_number")
    consoleLog("info", "Original called number: %s\n" % original_called_number)
    session.execute("bridge", "{sip_route_uri=sip:10.10.22.10,absolute_codec_string=OPUS\,G729\,PCMU\,PCMA}sofia/internal/%s@dev.io" % original_called_number)
    consoleLog("info", "Original Caller ID Number: %s\n" % original_caller_number)

def check_bridge_status(uuid):
    session = freeswitch.Session(uuid)
    consoleLog("error", "UUID: %s\n" % uuid)
    # Now perform further actions with UUID

def handler(session, args):
    consoleLog("info", "<< {} >> {} <<\n".format(session, args))

    # Answer the call
    session.answer()

    # Execute uuid_dump API
    uuid = session.get_uuid()

    api = API()

    status_result = api.execute("status")
    consoleLog("info", "Status: %s\n" % status_result)
    action  = "start"
    wss_url = "ws://10.10.10.30:10090"
    audio_params = "stereo 8k"
    json_params = {
        "chunk_size": [5, 10, 5],
        "wav_name": "h5",
        "is_speaking": True,
        "chunk_interval": 10,
        "itn": True,
        "mode": "2pass",
        "hotwords": None
    }
    json_str = json.dumps(json_params)
    cmd_str = " {} {} {} {} {}".format(uuid, action, wss_url, audio_params, json_str)
    asr_result = api.execute("uuid_funasr", cmd_str)
    consoleLog("info", "UUID FUNASR Result: %s\t%s\n" % (asr_result, cmd_str))

    # Execute bridge command
    bridge_command(session)

    # Schedule a timer to check bridge status after a delay
    consoleLog("info", "Scheduling check_bridge_status for UUID: %s\n" % uuid)
    session.execute("sched_api", "+5 python check_bridge_status %s" % uuid)
