from moviepy.editor import VideoFileClip, concatenate
import numpy as np
import os

def extract_high_volume(mypath, Accuracy):
	clip = VideoFileClip(mypath)
	cut = lambda i: clip.audio.subclip(i, i + 1).to_soundarray(fps=22000)
	volume = lambda array: np.sqrt(((1.0 * array) ** 2).mean())
	volumes = [volume(cut(i)) for i in range(0, int(clip.duration - 1))]
	averaged_volumes = np.array([sum(volumes[i:i + 10]) / 10 for i in range(len(volumes) - 10)])
	increases = np.diff(averaged_volumes)[:-1] >= 0
	decreases = np.diff(averaged_volumes)[1:] <= 0
	peaks_times = (increases * decreases).nonzero()[0]
	peaks_vols = averaged_volumes[peaks_times]
	peaks_times = peaks_times[peaks_vols > np.percentile(peaks_vols, 100 - Accuracy)]
	final_times = [peaks_times[0]]
	for t in peaks_times:
		if (t - final_times[-1]) < 60:
			if averaged_volumes[t] > averaged_volumes[final_times[-1]]:
				final_times[-1] = t
		else:
			final_times.append(t)
	return final_times

def Goals(mypath, Accuracy=10, ShotSize=10):
	clip = VideoFileClip(mypath)
	final_times = extract_high_volume(mypath, Accuracy)
	final = concatenate([clip.subclip(max(t - int(ShotSize / 2), 0), min(t + int(ShotSize / 2), clip.duration))
	                     for t in final_times])
	path = mypath[mypath.rindex("/"):]
	output_path = os.path.join('E:', 'Graduation Project', 'FinalTest', 'Output')
	os.makedirs(output_path, exist_ok=True)
	final_path = os.path.join(output_path, path)
	final.to_videofile(final_path)
	return final_path