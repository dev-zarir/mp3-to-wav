from flask import Flask, request, jsonify
from urllib.parse import unquote
from base64 import b64decode
import subprocess, random
from string import ascii_letters
import os
from time import sleep
from threading import Thread

app=Flask(__name__)
app.config['SECRET_KEY']='somerandomkey'

try:
    os.mkdir('static')
except: pass

def del_func(mp3_path, wav_path):
    sleep(60*10)
    os.remove(mp3_path)
    os.remove(wav_path)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='GET':
        return 'Send a Post request to this url with "data=<base64 encoded mp3>"'
    
    data=b64decode(unquote(request.form.get('data')))
    name=''.join(random.choices(ascii_letters, k=20))
    with open('static/'+name+'.mp3', 'wb') as mp3:
        mp3.write(data)
        mp3.close()
    subprocess.call(['ffmpeg', '-y', '-i', 'static/'+name+'.mp3', 'static/'+name+'.wav'], stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT)
    t=Thread(target=lambda: del_func('static/'+name+'.mp3', 'static/'+name+'.wav'))
    t.setDaemon(True)
    t.start()
    return jsonify({'link': (request.base_url+'/static/'+name+'.wav').replace('//','/').replace(':/','://')})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
