import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pandas as pd
from datetime import datetime, timedelta
import time
import random
from dataLoader import updatedData
import logging
from uptimeimage import imageGenerator
import numpy as np

logging.basicConfig(filename="dashBoard_log.log", level=logging.INFO)
templates = Jinja2Templates(directory="templates") 

# last hr time
last_hour_date_time = datetime.now() - timedelta(minutes= 1)
lh_time = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')

# app starting
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# about page rendering
@app.get("/about")
async def about():
    return "Need to link data"

# index page rendering
@app.get("/", response_class=HTMLResponse)
async def read_posts(request: Request):
    logging.info('User Refreshed At: '+str(datetime.now())+'Data Has been updated')
    uptime,LE,index,value = imageGenerator()
    # uptime,LE = imageGenerator()
    timestamp_obj = datetime.strptime(str(LE), '%Y-%m-%d %H:%M:%S.%f%z')
    LE = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
    return templates.TemplateResponse("blog.html", {"request": request, 
                                                    "mills" : pd.read_csv('new.csv'),#updatedData(),
                                                    "Uptime": uptime,
                                                    "le":  LE,
                                                    "lh_time" : lh_time})



# Performnce
@app.get("/performance", response_class=HTMLResponse)
async def read_performance(request: Request):
    logging.info('User Refreshed Performance At: '+str(datetime.now())+'Data Has been updated')
    return templates.TemplateResponse("performance.html", {"request": request})


# ModelAnalysis
@app.get("/modelanalysis", response_class=HTMLResponse)
async def read_modelanalysis(request: Request):
    logging.info('User Refreshed Performance At: '+str(datetime.now())+'Data Has been updated')
    return templates.TemplateResponse("modelanalysis.html", {"request": request})


# graph response
@app.get("/uptime/{item_id}", response_class=HTMLResponse)
def get_chart(item_id: str,request: Request):
    print("in loop of uptime")
    # labels = ['Category A', 'Category B', 'Category C']
    # data = [random.randint(1, 10) for _ in labels]
    uptime,LE,index,value = imageGenerator()
    print(type(index)," : ",type(value))
    labels = list(index)
    data = np.array(value).tolist()
    print(type(labels)," : ",type(data[0]))
    return templates.TemplateResponse("chart.html", {
        "request": request,
        "labels":labels,
        "data":data}) 


@app.get("/chart", response_class=HTMLResponse)
async def get_chart(request: Request):
    labels = ['Category A', 'Category B', 'Category C']
    data = [random.randint(1, 10) for _ in labels]
    return templates.TemplateResponse("chart.html", {"request": request,
                                                     "labels":labels,
        "data":data})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8088)

