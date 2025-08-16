from argparse import Namespace
from math import e
from os import name
from re import S
from socket import fromshare
import time
from turtle import st
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import psycopg2
from psycopg2.extensions import cursor


canUse = False

app = FastAPI()

templates = Jinja2Templates(directory="/")

app.mount("/static", StaticFiles(directory="/"), name="static")

@app.get("/", response_class=HTMLResponse)
def loginPage(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
@app.get("/register", response_class=HTMLResponse)
def loginPage(request:Request):
    return templates.TemplateResponse("kayit.html", {"request": request})



@app.post("/submitregister")
def submitregister (request: Request, nameSurname: str = Form(...), email: str = Form(...), password: str = Form(...),passwordAgain: str = Form(...)):
    con = psycopg2.connect("postgresql://neondb_owner:npg_bYafxhy1Jr0R@ep-jolly-king-aexq52y1-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    con.close()
    print(data)

    for i in range(data.__len__()):
        if nameSurname == data[i][1]:
            return templates.TemplateResponse("kayit.html", {"request": request, "msg": "Bu kullanıcı hali hazırda var. lütfen hesabınıza giriş yapın veya farklı kullanıcı adı kullanın."})
        else:
            for j in range(data.__len__()):
                if email == data[j][3]:
                    return templates.TemplateResponse("kayit.html", {"request": request, "msg": "Bu E-Mail, hali hazırda kullanılıyor. Lütfen hesabınız ile oturum açın yada farklı bir mail adresi kullanın."})
                else:
                    if password == passwordAgain:
                        con = psycopg2.connect("postgresql://neondb_owner:npg_bYafxhy1Jr0R@ep-jolly-king-aexq52y1-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
                        cur = con.cursor()
                        cur.execute("INSERT INTO users (username, password, email) VALUES(%s,%s,%s)",(nameSurname,password,email))
                        con.commit()
                        con.close()
                        return templates.TemplateResponse("kayit.html", {"request": request, "msg": "Kayıt başarılı! sizi giriş sayfasına yönlendiriyorum.", "canRequest":"yes"})
                        

                    else:
                        return templates.TemplateResponse("kayit.html", {"request": request, "msg": "Lütfen şifrenizi doğru bir şekilde tekrar giriniz."}) 

    