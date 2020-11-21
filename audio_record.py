
# -*- coding: utf-8 -*-
"""
Created on 11.21.2020
@author: yuming 
"""
 
import os 
import pyaudio
import time
import threading
import wave

class Recorder():
    def __init__(self, chunk=160, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    def start(self):
        threading._start_new_thread(self.__recording, ())

    def stop(self):
        self._running = False
        self.save('test.wav')

    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while(self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def save(self, filename):
        p = pyaudio.PyAudio()            
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        filename = os.path.join(os.getcwd(), filename)       
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        print("Saved")


    def record(self):
        print('请按下回车键开始录音：')
        
        print("Enter start:")
        x = input()
        if x == 'start':        
            begin = time.time()
            print("Start recording")
            self.start()
            print('请按下回车键结束录音：')
            x = input()
            if x == 'end':
                print("Stop recording")
                self.stop()
                fina = time.time()
                t = fina - begin
                print('录音时间为%ds'%t)


if __name__ == "__main__":
    rec = Recorder()
    rec.record()

