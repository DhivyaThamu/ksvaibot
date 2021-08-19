
import sounddevice as sd
#from playsound import playsound
from scipy.io.wavfile import read, write
import requests
from pathlib import Path
from pydub import AudioSegment
# import speech_recognition as sr



def enrollUser (BiometricID): 
  test_data = Record(BiometricID)
  print(test_data)
  enrollment_url = "http://34.231.177.128:8080/ksvvoiceservice/rest/service/enrollment/"+str(BiometricID)+"/AIBOT"
  try:
    result = requests.post(url = enrollment_url, files= test_data)
  except requests.exceptions.HTTPError as errh:
      print(errh)
      return ("Cannot connect to server now!. PLease try later")
  except requests.exceptions.ConnectionError as errc:
      print(errc)
      return ("Cannot connect to server now!. PLease try later")
  except requests.exceptions.Timeout as errt:
      print(errt)
      return ("Cannot connect to server now!. PLease try later")
  except requests.exceptions.RequestException as err:
      print(err)
      return ("Cannot connect to server now!. PLease try later")

  print (result)
  print(result.text)
  return(result.text)

def authenticateUser (BiometricID):
  test_data = Record(BiometricID)
  verification_url = 'http://34.231.177.128:8080/ksvvoiceservice/rest/service/verification/'+str(BiometricID) +"/AIBOT"
  try:
    result = requests.post(url = verification_url, files= test_data)
  except requests.exceptions.HTTPError as errh:
      print(errh)
      return ("Cannot connect to server now!. PLease try later")
  except requests.exceptions.ConnectionError as errc:
      print(errc)
      return ("Cannot connect to server now!. PLease try later")
  except requests.exceptions.Timeout as errt:
      print(errt)
      return ("Cannot connect to server now!. PLease try later")
  except requests.exceptions.RequestException as err:
      print(err)
      return ("Cannot connect to server now!. PLease try later")
  print (result)
  print(result.text)
  return(result.text)

def Record (BiometricID):
  fs = 16000  # Sample rate
  seconds = 22 # Duration of recording
  print("Recording Started....")
  myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
  sd.wait() 
  print("recording stopped.")
  fname = "output"+str(BiometricID)+".wav"
  write(fname, fs, myrecording)
  file_path = Path(r"C:/KSV_Banking_Bot/" + fname)
  sound = AudioSegment.from_wav(file_path)
  sound = sound.set_channels(1)
  file = str(BiometricID)+".wav"
  sound.export(file, format="wav")
  test_data =  {
    "file": open(r'C:/KSV_Banking_Bot/'+file, "rb")}
  return test_data


# authenticateUser(78183)