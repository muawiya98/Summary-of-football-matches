from moviepy.editor import VideoFileClip, concatenate
import librosa

from Codes.Goals.Goals import extract_high_volume
from Codes.Whistle.Whistle import get_all_seconds_with_whistle, filter_wistles

def GoleWhistle(mypath, Accuracy=10, ShotSize=10):
	#     p = mypath
	#     mypath = "E:\\Graduation Project\\FinalTest\\Input\\"+mypath
	clip = VideoFileClip(mypath)
	path = mypath[mypath.rindex("/"):]
	patha = path[:path.rindex(".")]
	clip.audio.write_audiofile('E:/Graduation Project/test4' + patha + ".wav")
	samples, sr = librosa.load('E:/Graduation Project/test4' + patha + ".wav", sr=16000)
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
	TimesFromWhistle = filter_wistles(acx, 'E:/Graduation Project/test4' + patha + ".wav", 1)
	TimesFromGolesSum = extract_high_volume(mypath, Accuracy)
	alls = set(TimesFromGolesSum + TimesFromWhistle)
	ALL = list(alls)
	ALL.sort()
	acx = []
	for t in range(0, len(ALL) - 2, 3):
		if (ALL[t + 1] - ALL[t] <= (ShotSize / 3)) and (ALL[t + 2] - ALL[t + 1] <= (ShotSize / 2)):
			acx.append(ALL[t + 1])
		elif ALL[t + 1] - ALL[t] <= (ShotSize / 3):
			acx.append(ALL[t + 1])
			acx.append(ALL[t + 2])
		elif ALL[t + 2] - ALL[t + 1] <= (ShotSize / 2):
			acx.append(ALL[t])
			acx.append(ALL[t + 1])
		else:
			acx.append(ALL[t])
			acx.append(ALL[t + 1])
			acx.append(ALL[t + 2])
	li = []
	path = mypath[mypath.rindex("/"):]
	for t in acx:
		if t in TimesFromGolesSum:
			li.append(clip.subclip(max(t - int(ShotSize / 2), 0), min(t + int(ShotSize / 2), clip.duration)))
		else:
			li.append(clip.subclip(max(t - int(ShotSize / 3), 0), min(t + int(ShotSize / 2), clip.duration)))
	final = concatenate(li)
	final.to_videofile("E:/Graduation Project/FinalTest/Output" + path)
	return "E:/Graduation Project/FinalTest/Output" + path