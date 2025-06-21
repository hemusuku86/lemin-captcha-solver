import requests
import ua_generator
import hashlib
import random
import uuid
import numpy as np
import vsmutok
from PIL import Image
import io

def solve(cap_id, url="https://dashboard.leminnow.com"):
    s = requests.Session()
    ua = ua_generator.generate(browser="chrome",platform="ios")
    s.headers = {
        ua.text
    }
    js = s.get(f"https://api.leminnow.com/captcha/v1/cropped/{cap_id}/js")
    md5_uuid = js.text.split("['MD5']['calc'](")[1].split("+")[1].split(");")[0]
    md5_uuid = js.text.split(f"{md5_uuid}='")[1].split("'")[0]
    cap_uuid = str(uuid.uuid4())
    utc_offset = -540 # new Date()["getTimezoneOffset"], change for your/proxy's timezone
    screen_width = random.randint(360,399)
    screen_height = int(screen_width/9)*19
    img_url = f"https://api.leminnow.com/captcha/v1/cropped/{cap_id}/image/{cap_uuid}?screen_width={screen_width}&screen_height={screen_height}&utc_offset={utc_offset}&v=3&domain={url}&enc=SHA256"
    lsign = hashlib.md5((img_url+md5_uuid).encode()).hexdigest()
    img_url += f"&lsign={lsign}"
    img = s.get(img_url)
    img = s.get(img.text.split("|")[0])
    im = Image.open(io.BytesIO(img.content))
    im.crop((0,0,400,400)).save("lemin_cap_bg_aaaaa.png")
    im.crop((430,30,500,100)).save("lemin_cap_piece_aaaaaa.png")
    imgsolver = vsmutok.PuzzleCaptchaSolver(
        gap_image_path="lemin_cap_piece_aaaaaa.png",
        bg_image_path="lemin_cap_bg_aaaaa.png"
    )
    ans_result = imgsolver.discern()
    ans_result = [round((n-3)/10)*10-20 for n in ans_result]
    #ans_result = [int(v) for v in input("input manually:").split(",")]
    answer = ""
    a_x = 10
    a_y = 400
    while True:
        answer += "0x"
        answer += (np.base_repr(a_x, 32).lower() + "x")
        answer += (np.base_repr(a_y, 32).lower() + "x")
        if a_x == ans_result[0] and a_y == ans_result[1]:
            break
        if random.random() > 0.5:
            if a_x > ans_result[0]:
                a_x -= 10
            elif a_x < ans_result[0]:
                a_x += 10
            else:
                if random.random() > 0.7:
                    a_x += random.choice([10,-10])
        else:
            if a_y > ans_result[1]:
                a_y -= 10
            elif a_y < ans_result[1]:
                a_y += 10
            else:
                if random.random() > 0.7:
                    a_y += random.choice([10,-10])
    pre = s.post("https://api.leminnow.com/captcha/v1/cropped/pre-validate",json={
        "answer": answer,
        "challenge_id": cap_uuid
    })
    if pre.json()["success"] == False:
        return {"answer": "Failed", "challenge_id": cap_uuid}
    else:
        pv_token = pre.json()["data"]["pv_token"]
        return {"answer": f"{answer}_?_{pv_token}", "challenge_id": cap_uuid}
