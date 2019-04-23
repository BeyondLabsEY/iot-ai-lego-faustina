import wit_client
import audio
import json
from gtts import gTTS
from io import BytesIO
from subprocess import call, check_output
import time
from pylgbst.movehub import MoveHub, EncodedMotor, COLORS, COLOR_NONE, COLOR_RED, COLOR_BLACK, COLOR_PINK, \
    COLOR_PURPLE, COLOR_BLUE, COLOR_LIGHTBLUE, COLOR_CYAN, COLOR_GREEN, COLOR_WHITE, COLOR_YELLOW
import os
from subprocess import Popen
import threading
import glob
import soundfile as sf
import math
import wave
import contextlib
from scipy.io.wavfile import read
from datetime import datetime


def play_wave_file(file_name):
    call(["ffplay", "-nodisp", "-autoexit", "recordings/{}".format(file_name)])


def load_knowledge_base():
    """Loads knowledge base to memory"""
    knowledge_base = {}
    with open('knowledge_base.json') as f:
        knowledge_base = json.load(f)
    return knowledge_base


def get_answer(response):
    """Finds an answer on our knowledge base"""
    knowledge_base = load_knowledge_base()

    answer = {}
    intents, entities = [], []
    for k, v in response["entities"].items():
        if k == "intent":
            print(v)
            intents.append(v[0]["value"])
        else:
            print(v)
            entities.append(v[0]["value"])

    intent = intents[0] if len(intents) > 0 else ""
    entity = entities[0] if len(entities) > 0 else ""

    for answer_object in knowledge_base["answers"]:
        if answer_object["intent"] == intent and answer_object["entity"] == entity:
            print("Answer found:", str(answer_object))
            answer = answer_object
    return answer


def act(answer={}, hub={}, recording_seconds_size=0):
    """Do an action"""
    if answer["legoAction"] == "right":
        hub.motor_A.timed(2, 0.8)
    elif answer["legoAction"] == "left":
        hub.motor_B.timed(2, 0.8)
    elif answer["legoAction"] == "forward":
        hub.motor_AB.timed(2, 0.8, 0.8)
    elif answer["legoAction"] == "back":
        hub.motor_AB.timed(2, -0.8, -0.8)
    elif answer["legoAction"] == "headRight":
        hub.motor_external.timed(1.5, -0.1, -0.1)
    elif answer["legoAction"] == "headLeft":
        hub.motor_external.timed(1.5, 0.1, 0.1)
    elif answer["legoAction"] == "headCentered":
        hub.motor_external.angled(-61, 0.08)
    elif answer["legoAction"] == "colorRed":
        hub.led.set_color(COLOR_RED)
    elif answer["legoAction"] == "colorBlack":
        hub.led.set_color(COLOR_BLACK)
    elif answer["legoAction"] == "colorPink":
        hub.led.set_color(COLOR_PINK)
    elif answer["legoAction"] == "colorPurple":
        hub.led.set_color(COLOR_PURPLE)
    elif answer["legoAction"] == "colorBlue":
        hub.led.set_color(COLOR_BLUE)
    elif answer["legoAction"] == "colorLightBlue":
        hub.led.set_color(COLOR_LIGHTBLUE)
    elif answer["legoAction"] == "colorCyan":
        hub.led.set_color(COLOR_CYAN)
    elif answer["legoAction"] == "colorGreen":
        hub.led.set_color(COLOR_GREEN)
    elif answer["legoAction"] == "colorRed":
        hub.led.set_color(COLOR_RED)
    elif answer["legoAction"] == "colorWhite":
        hub.led.set_color(COLOR_WHITE)
    elif answer["legoAction"] == "colorYellow":
        hub.led.set_color(COLOR_YELLOW)


def shake_head(hub, recording_seconds_size):
    """Shakes robot's head to right and left"""
    # Side movements

    loops_count = math.ceil(recording_seconds_size /
                            4) if recording_seconds_size > 4 else 1
    print("Loops count:", str(loops_count))

    # Center head
    act({"legoAction": "headCentered"}, hub)

    for loop in range(loops_count):
        print("Loop count:", str(loop))
        t1 = datetime.now()

        # Move head right
        act({"legoAction": "headRight"}, hub)

        # Move head left
        act({"legoAction": "headLeft"}, hub)

        t2 = datetime.now()
        delta = t2 - t1

        print("Loop took:", str(delta.total_seconds()))

    # Center head
    act({"legoAction": "headCentered"}, hub)


def connect():
    """Connnects to Lego boost"""
    count = 0
    hub = None
    while count < 10:
        try:
            hub = MoveHub()
            break
        except:
            print(
                "Please, make sure that your Lego Boost device is turned on and connected")
            count += 1
    return hub


def get_recording_size(file_name):
    """Get recording's size in seconds"""
    recording_size = check_output(
        ["mp3info", "-p", "%m:%s\n", "{}".format(file_name)]).decode("utf-8")
    print("Recording size:", str(recording_size))

    minutes_seconds = (int(recording_size.split(":")[0]) * 60)
    seconds = int(recording_size.split(":")[1].replace("\n", ""))
    recording_seconds_size = minutes_seconds + seconds
    print("Recording seconds size:", str(recording_seconds_size))

    return recording_seconds_size


def query_text_to_speech(text, file_name):
    """Queries TTS service"""
    mp3_fp = BytesIO()
    tts = gTTS(text, 'pt-br')
    tts.save(file_name)
    tts.write_to_fp(mp3_fp)


def download_voice(text, answer):
    """Downloads voice"""
    file_name, recording_size_seconds = "mensagem_inicial.mp3", 0
    if "recordings" not in glob.glob("*"):
        os.mkdir("recordings")

    os.chdir("recordings")
    if answer:
        file_name = answer["intent"] + "_" + answer["entity"] + ".mp3"
        audio_files = glob.glob("*")
        print("Audio files:", str(audio_files))
        if file_name not in audio_files:
            print("baixando arquivo de áudio...")
            query_text_to_speech(text, file_name)
    else:
        print("baixando arquivo de áudio...")
        query_text_to_speech(text, file_name)

    recording_size_seconds = get_recording_size(file_name)
    os.chdir("..")

    return file_name, recording_size_seconds


def speech(text, hub, answer):
    """Performs speech"""
    file_name, recording_seconds_size = download_voice(text, answer)

    print("File name:", str(file_name))
    print("File structure:", str(glob.glob("*")))

    t1 = threading.Thread(target=shake_head, args=(
        hub, recording_seconds_size))
    t2 = threading.Thread(target=play_wave_file, args=(file_name,))

    t2.start()
    t1.start()

    t2.join()  # Waits until t1 ends
    t1.join()  # Waits until t2 ends


def main():
    """Integrates all the code"""

    # Play start sound
    play_wave_file("start.wav")

    # Connect to Lego Boost
    hub = connect()

    # If hub works, starts the main app flow
    if hub:
        speech(
            "Olá, bem-vindo ao centro de inovação da I UAI. Em que posso te ajudar?", hub, {})
        while True:
            try:
                act({"legoAction": "colorGreen"}, hub)

                recorded_file = audio.record()

                act({"legoAction": "colorRed"}, hub)

                wit_response = wit_client.get_response(recorded_file)

                if wit_response["_text"]:
                    #act({"legoAction": "colorRed"}, hub)
                    print(wit_response)
                    answer = get_answer(wit_response)
                    text = answer["text"] if answer else "Desculpa, nao entendi o que voce quis dizer"
                    speech(text, hub, answer)
                    if answer:
                        act(answer, hub)
                else:
                    act({"legoAction": "colorYellow"}, hub)
                    print("No sound detected")
                    time.sleep(2)
            except Exception as exception:
                print(exception)

        time.sleep(2)
        hub.motor_external.stop()


if __name__ == "__main__":
    main()
