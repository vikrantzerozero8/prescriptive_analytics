from flask import Flask, render_template
from github import Github
from github import InputGitTreeElement
app = Flask(__name__)
app1 = Flask(__name1__)

import pycaret
from pycaret.classification import *
#import pickle
import numpy as np
import pandas as pd

#import pickle

saved_final_rf = load_model('model')
g = Github("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")

user = g.get_user()

repository = user.get_repo('pres')

file_content = repository.get_contents('jun23.csv')

bytes_data=file_content.decoded_content

s=str(bytes_data,'utf-8')

file = open("data.txt","w")

file.write(s)

df = pd.read_csv('data.txt')
df.columns = df.columns.str.replace(' ', '')
df.rename(columns = {'CustomerName':"Party_Name","Plant":"Warehouse","TargetQuantity":"Net_Weight"},inplace = True)

@app.route('/')
def home1():	
    name1 = [x for x in df.Warehouse]
    return render_template('index2.html', name1=name1)

@app.route('/')
def home():	
    name = [x for x in df.Party_Name]
    return render_template('index2.html', name=name)

if __name__=='__main__':
    app.run(debug=True, use_reloader=False)

if __name1__=='__main__':
    app1.run(debug=True, use_reloader=False)
    
'''Total_rejected_WD=1&Nr_days_without_activity=2

from flask import Flask, render_template, json
app = Flask(__name__)

@app.route('/')
def index():    
    name = ['Red', 'Blue', 'Orange', 'Yellow', 'Green']
    return render_template('index2.html', name=name)

if __name__ == "__main__":
    app.run(debug=True)
'''
