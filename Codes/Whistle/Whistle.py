# -*- coding: utf-8 -*-
from moviepy.editor import VideoFileClip, concatenate
import speech_recognition as sr1
from pydub import AudioSegment
from scipy import signal
import librosa
import shutil
import os

important_words = "  افتتاحيه صافره الفار انطلاق تدخل بطاقه البطاقه تسلل التسلل حارس الحارس مرمى المرمى منطقه المنطفه خطيره الخطيره خطير الخطير عرضيه العرضيه عارضه العارضه قائم القائم ركنيه الركنيه خطا الخطا خطوره الخطوره تسديده التسديده يسدد سدد بدايه نهايه فرصه الفرصه رايه الرايه شباك الشباك ضربه تحذير جزاء"
very_important_words = "بطاقه البطاقه تسلل التسلل حارس الحارس  منطقه المنطفه خطيره الخطيره عرضيه العرضيه عارضه العارضه قائم القائم ركنيه الركنيه خطوره الخطوره تسديده التسديده فرصه الفرصه رايه الرايه شباك الشباك ضربه جزاء"

def list_to_wav(list_of_seconds, path):
	list_of_paths = []
	mypath = path[:path.rindex("\\")]
	os.mkdir(mypath + '/chunks')
	fullAudio = AudioSegment.from_wav(path)
	for index, second in enumerate(list_of_seconds):
		newAudio = fullAudio[(second - 3) * 1000:(second + 5) * 1000]
		newAudio.export(mypath + '/chunks\\' + str(index) + '.wav', format="wav")
		list_of_paths.append(mypath + '/chunks/' + str(index) + '.wav')
	return list_of_paths

def wav_to_text(list_of_paths, recoganizer):
	list_of_texts = []
	for path in list_of_paths:
		with sr1.AudioFile(path) as source:
			audio_data = recoganizer.record(source)
			try:text = recoganizer.recognize_google(audio_data, language='ar-IL')
			except:text = "no thing"
		list_of_texts.append(text)
	return list_of_texts

def is_important_event(text, important_words):
	if text == "no thing":
		return False
	for word in important_words.split():
		if word in text:
			return True
	return False

def filter_wistles(list_of_seconds, path, type_of_words):
	important_events = []
	recoganizer = sr1.Recognizer()
	list_of_paths = list_to_wav(list_of_seconds, path)
	texts = wav_to_text(list_of_paths, recoganizer)
	if type_of_words == 1:
		for index, text in enumerate(texts):
			if is_important_event(text, important_words):
				important_events.append(index)
	else:
		for index, text in enumerate(texts):
			if is_important_event(text, very_important_words):
				important_events.append(index)
	mypath = path[:path.rindex("\\")]
	shutil.rmtree(mypath + '\\chunks')
	return [list_of_seconds[x] for x in important_events]

def is_second_with_whisle(psds_of_second, thre1, thre2):
	for i in range(0, len(psds_of_second) - thre2):
		temp_range = psds_of_second[i:i + thre2]
		if all(temp >= thre1 for temp in temp_range):
			return True
		i += 1
	return False

# Power Spectral Density (psd)
def get_psd_for_all_windows_for_all_seconds(samples, sample_rate):
	results = []
	for i in range(0, len(samples) // sample_rate):
		start_of_current_window = i * sample_rate
		end_of_current_window = i * sample_rate + 640
		result = []
		for j in range(0, 50):
			freqs, psd = signal.welch(samples[start_of_current_window:end_of_current_window])
			freqs = freqs * sample_rate
			list_of_whistle_range = [i for i in range(len(freqs)) if ((freqs[i] >= 3500) and (freqs[i] <= 4500))]
			psd_whistle_range = psd[list_of_whistle_range]
			result.append(sum(psd_whistle_range))
			start_of_current_window += 320
			end_of_current_window += 320
		results.append(result)
	return results

def get_all_seconds_with_whistle(samples, sample_rate=16000, thre1=0.01, thre2=12):
	accpeted_seconds = []
	results = get_psd_for_all_windows_for_all_seconds(samples, sample_rate)
	for i in range(len(results)):
		if is_second_with_whisle(results[i], thre1, thre2):
			accpeted_seconds.append(i + 1)
	return accpeted_seconds

def Whistle(mypath, ShotSize=10):
	clip = VideoFileClip(mypath)
	path = mypath[mypath.rindex("/"):]
	patha = path[:path.rindex(".")]
	clip.audio.write_audiofile('E:/Graduation Project/test3' + patha + ".wav")
	samples, sr = librosa.load('E:/Graduation Project/test3' + patha + ".wav", sr=16000)
	TimesFromWhistle = get_all_seconds_with_whistle(samples)
	acx = []
	for t in range(0, len(TimesFromWhistle) - 2, 3):
		if (TimesFromWhistle[t + 1] - TimesFromWhistle[t] <= (ShotSize / 3)) and (
				TimesFromWhistle[t + 2] - TimesFromWhistle[t + 1] <= (ShotSize / 2)):
			acx.append(TimesFromWhistle[t + 1])
		elif TimesFromWhistle[t + 1] - TimesFromWhistle[t] <= (ShotSize / 3):
			acx.append(TimesFromWhistle[t + 1])
			acx.append(TimesFromWhistle[t + 2])
		elif TimesFromWhistle[t + 2] - TimesFromWhistle[t + 1] <= (ShotSize / 2):
			acx.append(TimesFromWhistle[t])
			acx.append(TimesFromWhistle[t + 1])
		else:
			acx.append(TimesFromWhistle[t])
			acx.append(TimesFromWhistle[t + 1])
			acx.append(TimesFromWhistle[t + 2])

	final_list = filter_wistles(acx, 'E:/Graduation Project/test3' + patha + ".wav", 1)
	final = concatenate([clip.subclip(max(t - int(ShotSize / 3), 0), min(t + int(ShotSize / 2), clip.duration))
	                     for t in final_list])
	final.to_videofile("E:\\Graduation Project\\FinalTest\\Output" + path)
	return "E:\\Graduation Project\\FinalTest\\Output" + path