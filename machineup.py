import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import numpy as np


# last hr time
last_hour_date_time = datetime.now() - timedelta(minutes= 1)
lh_time = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')

print(lh_time)

df = pd.read_csv('new.csv')

for index,row in df.iterrows():
    print(row['lastuv_inspectionOn'])