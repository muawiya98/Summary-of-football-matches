# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response, redirect, url_for, session, jsonify
from ffpyplayer.player import MediaPlayer
from time import sleep
import cv2

from Codes.Goals.Goals import Goals
from Codes.GoalsWhistle.GoalsWhistle import GoleWhistle 
from Codes.Whistle.Whistle import Whistle


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ''

def gen_frames(cam):
    vid = cv2.VideoCapture(cam,)
    aud=MediaPlayer(cam)
    while True:
        sleep(0.0308)
        ret, frame = vid.read()
        aud_frame,val=aud.get_frame()
        if not ret:
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
