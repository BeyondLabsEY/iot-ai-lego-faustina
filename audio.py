import pyaudio
import wave
from subprocess import call, check_output, TimeoutExpired

def record():
    #call(["ffplay", "-nodisp", "-autoexit", "recordings/{}".format(file_name)])
    WAVE_OUTPUT_FILENAME = "file.wav"
    
    try:
        call(["arecord", "--device=hw:1,0", "--format", "S16_LE", "--rate", "16000", "-c1", "file.wav"], timeout=5)
    except TimeoutExpired as exc:    
        return WAVE_OUTPUT_FILENAME
    return "" 

'''
def record():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
 
    audio = pyaudio.PyAudio()
 
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
 
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    return WAVE_OUTPUT_FILENAME
'''