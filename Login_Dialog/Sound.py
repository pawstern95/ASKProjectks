import wave
import pyaudio

class Sound:
    def __init__(self):
        f = wave.open('alarm.wav', 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
                        rate = f.getframerate(),
                        output = True)
        data = f.readframes(1024)
        while data:
            stream.write(data)
            data = f.readframes(1024)
        stream.stop_stream()
        stream.close()
        p.terminate()