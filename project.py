from pydub import AudioSegment
from gtts import gTTS
import speech_recognition as sr
from twilio.rest import Client
import pyaudio
import time
import sys
import wave
import os
import webbrowser


#amount of data used at a time
CHUNK = 1024
#input and output to .wav file
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
#amont of seconds to record at a time
RECORD_SECONDS = 4

#function to convert speech to text
def recognizespeech():
   #r has the speech recognizer class
   r =sr.Recognizer()
   #takes the audio from the output 
   audiosource = sr.AudioFile('output.wav')
   with audiosource as source:
       audio = r.record(source)
   #Prints the recognized data

   try:
       data = r.recognize_google(audio)
       return data
   except sr.UnknownValueError:
       return ("Google Speech Recognition could not understand audio")
   except sr.RequestError as e:
       return ("Could not request results from Google Speech Recognition service; {0}".format(e))

def readwavfile():
   #opens a wav file
   wf = wave.open('tts.wav','rb')
   p = pyaudio.PyAudio()
   stream = p.open(format=FORMAT,
               channels=CHANNELS,
               rate=12700,
               output=True)
  
   #takes data chunks at a time
   data = wf.readframes(CHUNK)

   #reads out data from wav file
   while len(data) > 0:
       stream.write(data)
       data = wf.readframes(CHUNK)
      
   stream.stop_stream()
   stream.close()

   p.terminate()

def makewavfile():
   p = pyaudio.PyAudio()
   #records from microphone and outputs it to output.wav file
   WAVE_OUTPUT_FILENAME = "output.wav"

   stream = p.open(format=FORMAT,
               channels=CHANNELS,
               rate=RATE,
               input=True,
               frames_per_buffer=CHUNK)

   print("* recording")

   frames = []

   #gets frame chunks one at a time and appends it
  
   for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
       data = stream.read(CHUNK)
       frames.append(data)

   print("* done recording")

   stream.stop_stream()
   stream.close()
   p.terminate()

   wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
   wf.setnchannels(CHANNELS)
   wf.setsampwidth(p.get_sample_size(FORMAT))
   wf.setframerate(RATE)
   wf.writeframes(b''.join(frames))
   wf.close()

def recordAudio():
   all = []
   p = pyaudio.PyAudio()
   WAVE_OUTPUT_FILENAME = "output.wav"
   stream = p.open(format=FORMAT,
               channels=CHANNELS,
               rate=RATE,
               input=True,
               frames_per_buffer=CHUNK)

   try:
       while True:
           data = stream.read(CHUNK)
           all.append(data)
   except KeyboardInterrupt:
       stream.stop_stream()
       stream.close()
       p.terminate()
       wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
       wf.setnchannels(CHANNELS)
       wf.setsampwidth(p.get_sample_size(FORMAT))
       wf.setframerate(RATE)
       wf.writeframes(b''.join(all))
       wf.close()
   print ("* done recording")

def saytts(content):
   tts = gTTS(text=content, lang='en')
   tts.save("tts.mp3")
   sound = AudioSegment.from_mp3("tts.mp3")
   sound.export("tts.wav", format="wav")
   readwavfile()

def displaymenu():   
   print("------------------------------------------------------------------------------------------------------")
   print("                                            S-H-E-L-L")
   print("-------------------------------------------------------------------------------------------------------")
   print("Options")
   print("[0] Help")
   print("[1] Make Directory")
   print("[2] Delete Directory")
   print("[3] Create File")
   print("[4] Delete File")
   print("[5] Rename File")
   print("[6] Display File Content")
   print("[7] Edit File")
   print("[8] Switch Between Speech and Keyboard")
   print("[9] List files")
   print("[10] Change Directory")
   print("[11] Current directory")
   print("[12] Find my phone")
   print("[13] Where am I")
   print("[14] Exit")


def keyboardinput():       
   displaymenu()
   n= int(input('Choose Command>>:  '))
  
   if n==0:
       displaymenu()
   elif(n==1):
       x=input('Enter dir name:   ')
       os.mkdir(x)
       #saytts("directory added succesfully")
  
   elif(n==2):
       x=input('Enter dir name to be deleted:   ')
       try:
           os.rmdir(x)
       except:
           print("Directory doesnt exist")
  
   elif(n==3):
       x=input('Enter file-name:   ')
       file=open(x,'w')
  
   elif(n==4):
       x=input('Enter file-name to be deleted:   ')
       try:
           os.remove(x)
       except:
           print("File doesnt exist")
  
   elif(n==5):
       x=input('Enter old file-name :   ')
       y=input('Enter new file-name       :   ')
       try:
           os.rename(x,y)
       except:
           print("File doesnt exist")
  
   elif(n==6):
       x=input('Enter file-name  :   ')
       file=open(x,'r')
       content=file.read()
       print(content)

   elif(n==7):
       x=input('Enter file-name    :   ')
       print('\n'*2)
       print("______________________________________________________________________________________")
       print('\n'*2)
       file=open(x,'w')
       y=input('>')
       file.write(y)
       file.close()
  
   elif(n==8):
       speechinput()

   elif (n==10):
       x = input("Enter directory name: ")
       txt = os.getcwd()
       directory = txt + "\\" + x
       print(directory)
       os.chdir(directory)
       print(os.getcwd())
  
   elif(n==11):
       os.getcwd()

   elif(n==12):
       exit()

def speechinput():   
   displaymenu()
   while True:   
       time.sleep(2)
       makewavfile()
       cspeech = recognizespeech()
       print(cspeech)
      
       if(cspeech=="0" or cspeech=="zero" or cspeech=="hello"):
           displaymenu()

       elif(cspeech == "make directory" or cspeech=="one" or cspeech=="1"):
           print("say  directory name")
           #saytts("say  directory name")           
           makewavfile()
           x=recognizespeech()
           os.mkdir(x)
           #saytts("Directory added successfully")
           print("Directory Added successfully!")

       elif(cspeech=="delete directory" or cspeech=="two" or cspeech=="2"):
           print("say directory name")
           #saytts("say directory name")  
           makewavfile()
           x=recognizespeech()
           try:
               os.rmdir(x)
           except:
               #saytts("Directory does not exist")
               print("Directory doesnt exist")

       elif (cspeech=="create file" or cspeech == "3"):
           print("say file name")
           #saytts("say file name") 
           makewavfile()  
           x=recognizespeech() + ".txt"
           file=open(x,'w')

       elif (cspeech=="delete file" or cspeech == "4"):
           print("say file name")
           #saytts("say file name")
           makewavfile()
           x=recognizespeech() + ".txt"
           try:
               os.remove(x)
           except:
               #saytts("File does not exist")
               print("File doesnt exist")

       elif (cspeech=="rename file" or cspeech =="5"):
           print("say file name")
           #saytts("say file name")
           makewavfile()
           x=recognizespeech() + ".txt"
           try:
               os.remove(x)
           except:
               #saytts("File does not exist")
               print("File doesnt exist")

       elif(cspeech=="read file" or cspeech == "6"):
           print("say file name")
           #saytts("say file name")
           makewavfile()
           x=recognizespeech() + ".txt"
           file=open(x,'r')
           content=file.read()
           print(content)

       elif(cspeech=="edit file" or cspeech == "7"):
           print("say file name")
           #saytts("say file name")
           makewavfile()
           x=recognizespeech() + ".txt"
           print('\n'*2)
           print("______________________________________________________________________________________")
           print('\n'*2)
           file=open(x,'w')
           print('Press Crtl+C to stop edititng')
           recordAudio()
           y=recognizespeech()
           file.write(y)
           file.close()

       elif (cspeech=="keyboard" or cspeech=="8"):
           keyboardinput()

       elif(cspeech=="list files" or cspeech=="9" or cspeech=="LS" or cspeech=="list file"):
           print(os.listdir())
      
       elif(cspeech=="change directory" or cspeech=="10" or cspeech=="CD"):
           print("say directory name")
           #saytts("say directory name")
           makewavfile()
           x=recognizespeech()
           txt = os.getcwd()
           directory = txt + "\\" + x
           print(directory)
           os.chdir(directory)
           print(os.getcwd())
      
       elif(cspeech=="current directory" or cspeech=="11" or cspeech=="PWD"):
           print(os.getcwd)
      
       elif(cspeech=="stop" or cspeech=="exit" or cspeech=="14"):
           exit()
      
       elif(cspeech=="find my phone" or cspeech=="12"):
           account_sid = "AC94929f51f689771ba18eecdfe0232779"
           auth_token = "8001b259d14de0ac3924c8b275adfd06"
           client = Client(account_sid, auth_token)
           call= client.calls.create(
                   to="+917338996054",
                   from_="+16505427384",
                   url="http://demo.twilio.com/docs/voice.xml"
           )
           print(call.sid)
           time.sleep(3)
       elif(cspeech=="location" or cspeech=="where am I" or cspeech=="13"):
           url="map.html"
           webbrowser.open(url,new=2)
       else:
           #saytts("command not found")
           print("command not found")

def main():
   speechinput()

if __name__ == "__main__":
   main()

