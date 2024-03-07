from time import sleep

import cv2
from flask import Flask, render_template, request, Response, redirect, url_for, session, jsonify
from main import Goals,GoleWhistle,Whistle
from ffpyplayer.player import MediaPlayer
#
# def Goals(mypath, Accuracy=10, ShotSize=10):
#     clip = VideoFileClip(mypath)
#     final_times = proj(mypath, Accuracy)
#     final = concatenate([clip.subclip(max(t - int(ShotSize / 2), 0), min(t + int(ShotSize / 2), clip.duration))
#                          for t in final_times])
#     path = mypath[mypath.rindex("\\"):]
#     final.to_videofile('E:\\Graduation Project\\test2' + path)
#     return 'E:\\Graduation Project\\test2' + path
#
#
# def Whistle(mypath, ShotSize=10):
#     clip = VideoFileClip(mypath)
#     path = mypath[mypath.rindex("\\"):]
#     patha = path[:path.rindex(".")]
#     clip.audio.write_audiofile('E:\\Graduation Project\\test3' + patha + ".wav")
#     samples, sr = librosa.load('E:\\Graduation Project\\test3' + patha + ".wav", sr=16000)
#     TimesFromWhistle = get_all_seconds_with_whistle(samples)
#     acx = []
#     for t in range(0, len(TimesFromWhistle) - 2, 3):
#         if (TimesFromWhistle[t + 1] - TimesFromWhistle[t] <= (ShotSize / 3)) and (
#                 TimesFromWhistle[t + 2] - TimesFromWhistle[t + 1] <= (ShotSize / 2)):
#             acx.append(TimesFromWhistle[t + 1])
#         elif TimesFromWhistle[t + 1] - TimesFromWhistle[t] <= (ShotSize / 3):
#             acx.append(TimesFromWhistle[t + 1])
#             acx.append(TimesFromWhistle[t + 2])
#         elif TimesFromWhistle[t + 2] - TimesFromWhistle[t + 1] <= (ShotSize / 2):
#             acx.append(TimesFromWhistle[t])
#             acx.append(TimesFromWhistle[t + 1])
#         else:
#             acx.append(TimesFromWhistle[t])
#             acx.append(TimesFromWhistle[t + 1])
#             acx.append(TimesFromWhistle[t + 2])
#
#     final_list = filter_wistles(acx, 'E:\\Graduation Project\\test3' + patha + ".wav", 1)
#     final = concatenate([clip.subclip(max(t - int(ShotSize / 3), 0), min(t + int(ShotSize / 2), clip.duration))
#                          for t in final_list])
#     final.to_videofile('E:\\Graduation Project\\test3' + path)
#     return 'E:\\Graduation Project\\test3' + path
#
#
# def GoleWhistle(mypath, Accuracy=10, ShotSize=10):
#     clip = VideoFileClip(mypath)
#     path = mypath[mypath.rindex("\\"):]
#     patha = path[:path.rindex(".")]
#     clip.audio.write_audiofile('E:\\Graduation Project\\test4' + patha + ".wav")
#     samples, sr = librosa.load('E:\\Graduation Project\\test4' + patha + ".wav", sr=16000)
#     TimesFromWhistle = get_all_seconds_with_whistle(samples)
#     acx = []
#     for t in range(0, len(TimesFromWhistle) - 2, 3):
#         if (TimesFromWhistle[t + 1] - TimesFromWhistle[t] <= (ShotSize / 3)) and (
#                 TimesFromWhistle[t + 2] - TimesFromWhistle[t + 1] <= (ShotSize / 2)):
#             acx.append(TimesFromWhistle[t + 1])
#         elif TimesFromWhistle[t + 1] - TimesFromWhistle[t] <= (ShotSize / 3):
#             acx.append(TimesFromWhistle[t + 1])
#             acx.append(TimesFromWhistle[t + 2])
#         elif TimesFromWhistle[t + 2] - TimesFromWhistle[t + 1] <= (ShotSize / 2):
#             acx.append(TimesFromWhistle[t])
#             acx.append(TimesFromWhistle[t + 1])
#         else:
#             acx.append(TimesFromWhistle[t])
#             acx.append(TimesFromWhistle[t + 1])
#             acx.append(TimesFromWhistle[t + 2])
#     TimesFromWhistle = filter_wistles(acx, 'E:\\Graduation Project\\test4' + patha + ".wav", 1)
#     TimesFromGolesSum = proj(mypath, Accuracy)
#     alls = set(TimesFromGolesSum + TimesFromWhistle)
#     ALL = list(alls)
#     ALL.sort()
#     acx = []
#     for t in range(0, len(ALL) - 2, 3):
#         if (ALL[t + 1] - ALL[t] <= (ShotSize / 3)) and (ALL[t + 2] - ALL[t + 1] <= (ShotSize / 2)):
#             acx.append(ALL[t + 1])
#         elif ALL[t + 1] - ALL[t] <= (ShotSize / 3):
#             acx.append(ALL[t + 1])
#             acx.append(ALL[t + 2])
#         elif ALL[t + 2] - ALL[t + 1] <= (ShotSize / 2):
#             acx.append(ALL[t])
#             acx.append(ALL[t + 1])
#         else:
#             acx.append(ALL[t])
#             acx.append(ALL[t + 1])
#             acx.append(ALL[t + 2])
#     li = []
#     path = mypath[mypath.rindex("\\"):]
#     for t in acx:
#         if t in TimesFromGolesSum:
#             li.append(clip.subclip(max(t - int(ShotSize / 2), 0), min(t + int(ShotSize / 2), clip.duration)))
#         else:
#             li.append(clip.subclip(max(t - int(ShotSize / 3), 0), min(t + int(ShotSize / 2), clip.duration)))
#     final = concatenate(li)
#     final.to_videofile('E:\\Graduation Project\\test4' + path)
#     return 'E:\\Graduation Project\\test4' + path


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = ''


def gen_frames(cam):
    vid = cv2.VideoCapture(cam,)
    aud=MediaPlayer(cam)
    while True:
        sleep(0.0308)
        ret, frame = vid.read()
        aud_frame,val=aud.get_frame()
        if not ret :
            print("End of video")
            break
        if val != 'eof' and aud_frame is not None:
            img,t=aud_frame
        frame = cv2.resize(frame, (370, 220))
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def home():
    return render_template('home.html')


video = ''


@app.route('/proprieties', methods=['GET', 'POST'])
def proprieties():
    global video
    print(request.form)
    path = request.form['path']
    print(path)
    typeS = request.form['character']
    if typeS == 'g':
        print('g')
        if request.form['path'] != '' or request.form['accuracy'] != '' or request.form['size'] != '':
            video = Goals("E:/Graduation Project/FinalTest/Input/"+request.form['path'], int(request.form['accuracy']), int(request.form['size']))
            return render_template('result.html', video=video)
        else:
            return render_template('home.html', msg='you have to fill the chosen fileds')
    elif typeS == 'w':
        print('w')
        if request.form['path'] != '' or request.form['size2'] != '':
            video = Whistle("E:/Graduation Project/FinalTest/Input/"+request.form['path'], int(request.form['size2']))
            return render_template('result.html', video=video)
        else:
            return render_template('home.html', msg='you have to fill the chosen fileds')
    elif typeS == 'gw':
        print('gw')
        if request.form['path'] != '' or request.form['accuracy2'] != '' or request.form['size3'] != '':
            video = GoleWhistle("E:/Graduation Project/FinalTest/Input/"+request.form['path'], int(request.form['accuracy2']), int(request.form['size3']))
            return render_template('result.html', video=video)
        else:
            return render_template('home.html', msg='you have to fill the chosen fileds')
    return render_template('home.html', msg='you have to fill the filed')


@app.route('/video_feed_for_output')
def video_feed_for_output():
    return Response(gen_frames(video), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(port=8001, host='localhost')
