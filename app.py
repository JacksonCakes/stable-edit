from flask import Flask, render_template , request , jsonify, make_response
import numpy as np
from PIL import Image
from io import BytesIO
from utils.preprocessing import get_mask, remove_transparent, resize_and_crop
from stable_edit.sd_model import Inpainting_Model
import base64
import json
import re
import io
import sys
app = Flask(__name__)

access_token = None

@app.route('/')
def home():
	return render_template('./index.html')

@app.route('/imgEditing' , methods=['POST'])
def get_img():
    # print(request.files , file=sys.stderr)
    prompt = request.form['prompt']
    neg_prompt = request.form['neg-prompt']
    img_data = re.sub('^data:image/.+;base64,', '', request.form['imageBase64'])
    mask_data = re.sub('^data:image/.+;base64,', '', request.form['maskBase64'])
    steps = int(request.form['step'])
    guidance = float(request.form['guidance'])
    img = Image.open(BytesIO(base64.b64decode(img_data)))
    img = remove_transparent(img)
    mask = Image.open(BytesIO(base64.b64decode(mask_data)))
    mask = get_mask(mask)
    if img.width % 8 != 0 or img.height % 8 != 0:
        img = resize_and_crop(img)
        mask = resize_and_crop(mask)
    
    inpaint_model = Inpainting_Model(access_token=access_token)
    print("Enter inpainting...")
    out_imgs = inpaint_model(prompt=prompt,image=img,mask=mask,steps=steps,guidance_scale=guidance,neg_prompt=neg_prompt)
    out_img = out_imgs[0]
    rawBytes = io.BytesIO()
    out_img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    print(f"Run success!-{prompt}-{steps}-{guidance}-{neg_prompt}" , file=sys.stderr)

    return jsonify({'status': True, 'image': str(img_base64)})

if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser()		
    config.read("config.ini")
    config = configparser.ConfigParser()
    if not config.has_section("AUTH"):
        config.add_section("AUTH")
        access_token = input("Enter your huggingface access token: ") 
        config.set("AUTH", "token", access_token)

    else:
        access_token = config['token']
    app.run(debug = True,use_reloader=False)