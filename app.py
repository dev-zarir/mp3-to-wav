from flask import Flask, request, redirect
from urllib.parse import unquote
from base64 import b64decode
import subprocess, random
from string import ascii_letters

app=Flask(__name__)
app.config['SECRET_KEY']='somerandomkey'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='GET':
        return 'Send a Post request to this url with "data=<base64 encoded mp3>"'
    
    data=b64decode(unquote(request.form.get('data')))
    name=''.join(random.choices(ascii_letters, k=20))
    with open(name+'.mp3', 'wb') as mp3:
        mp3.write(data)
        mp3.close()
    subprocess.call(['ffmpeg', '-y', '-i', name+'.mp3', name+'.wav'], stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT)
    return redirect('/'+name+'.wav')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
