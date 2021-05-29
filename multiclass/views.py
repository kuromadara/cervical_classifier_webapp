from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings 
import numpy as np
from cv2 import cv2
from PIL import Image
import datetime
import traceback
import os
from keras.preprocessing.image import load_img
from keras.applications.mobilenet import preprocess_input
from django.conf import settings
from keras.models import load_model
import base64
from .models import UserRegistrationForm
from django.contrib import messages
import time

model = load_model('static/models/model_sgd.h5')
model_binary = load_model('static/models/model.h5')

def login(request):
    msg = ''
    wrongemail = ''
    wrongpass = ''
    if request.session.get('err'):
        msg = request.session.get('err')
        del request.session['err']

    if (msg != ''):
        for key, value in msg.items():
            if key == 'email':
                wrongemail = value
                break
            else:
                wrongpass = value
                break
    context = {
            'wrongpass': wrongpass,
            'wrongemail' : wrongemail,
            }
    return render(request, "login.html", context)

def logout(request):
    if request.session.get('login'):
        del request.session['login']
    
    return redirect('/')

def validate_login(request):
    
    if request.method == "POST":
        errors = UserRegistrationForm.objects.login_validator(request.POST)
        if len(errors):
            for value in errors.items():
                messages.add_message(request, messages.ERROR, value, extra_tags='login')
            
            context = {
                'er ':errors
            }
            request.session['err'] = errors
            return redirect('/', context)
        else:
            # userr = UserRegistrationForm.objects.cur_user(request.POST)
            # print(userr)
            # context = {
            #     'userr' : userr
            # }
            # request.session['userrr'] = userr
            request.session['login'] = True
            return redirect("/home") #,context
        

def index(request):
    if request.session.get('login') == True:

        if request.method == "POST":

            start = time.time()
            
            f = request.FILES.get('sentFile')

            file_name = "static/media/pic.jpg"
            file_name_2 = default_storage.save(file_name,f)
            file_url = default_storage.url(file_name_2)[1:] # /static/media/pic_7f2JcAh.jpg => static/media/pic_7f2JcAh.jpg

            image_org = cv2.imread(file_url)
            img_resize = (cv2.resize(image_org, dsize=(224, 224),interpolation=cv2.INTER_LINEAR))/255.
            pred_img = img_resize[np.newaxis,...]

            r, enc = cv2.imencode('.jpg', image_org)
            encoded = base64.b64encode(enc).decode('ascii')
            mime = "image/jpg"
            mime = mime + ";" if mime else ";"
            input_image = "data:%sbase64,%s" % (mime, encoded)   

            '''
            batch images

            image_org = load_img(("." + file_url), target_size=(224,224))

            img_array = np.asarray(image_org)
            #img_resize = (cv2.resize(image, dsize=(224, 224),    interpolation=cv2.INTER_LINEAR))/255.
            
            img_pre = preprocess_input(img_array)
            img_exp = np.expand_dims(img_pre, axis=0)
            '''

            prediction = model.predict(pred_img)
            pred_binary = model_binary.predict(pred_img)

            #time.sleep(1)

            end = time.time()

            time_taken = round((end - start), 2)

            hsil = round((prediction[0][0] * 100), 2)
            lsil = round((prediction[0][1] * 100), 2)
            nl = round((prediction[0][2] * 100), 2)
            ascus = round((prediction[0][3] * 100), 2)

            max = hsil + lsil + nl + ascus

            abnormal = round((pred_binary[0][0] * 100), 2)
            normal = round((pred_binary[0][1] * 100), 2)

            max_binary = normal + abnormal

            
            
            context = { 
                'time' : time_taken,
                'hs':hsil, 
                'ls':lsil,
                'nl':nl,
                'as':ascus, 
                'img': input_image,
                'max':max,
                'normal' : normal,
                'abnormal' : abnormal,
                'max_binary' : max_binary
                }

            return render(request, 'home.html', context)
        else:
            return render(request, 'home.html')
    else:
        return redirect('/')





