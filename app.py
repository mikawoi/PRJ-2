import requests, os
from flask import Flask, render_template, request
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv('API_KEY')
print(API_KEY)
