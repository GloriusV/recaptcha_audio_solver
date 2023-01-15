from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import ffmpeg
import pydub
import urllib
import speech_recognition as sr
import time

driver = webdriver.Chrome("C:/chromedriver.exe")

driver.get("https://www.google.com/recaptcha/api2/demo")
driver.implicitly_wait(10)

frames = driver.find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(frames[0])
driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()

driver.switch_to.default_content()
frames = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]").find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(frames[0])
driver.find_element(By.ID, "recaptcha-audio-button").click()
time.sleep(2)

driver.switch_to.default_content()
frames = driver.find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(frames[-1])
driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/button").click()

src = driver.find_element(By.ID, "audio-source").get_attribute("src")

urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
sound.export(os.getcwd()+"\\sample.wav", format="wav")
sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")

r = sr.Recognizer()
with sample_audio as source:
    audio = r.record(source)

key = r.recognize_google(audio)
print(key)
driver.find_element(By.ID, "audio-response").send_keys(key.lower())
driver.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)
os.system('del /f sample.mp3')
os.system('del /f sample.wav')

time.sleep(444)

