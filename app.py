#app.py
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
from github import Github
from github import InputGitTreeElement
app = Flask(__name__)

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
def main():
    carbrands = df
    return render_template('index.html', carbrands=carbrands)
  
@app.route("/carbrand",methods=["POST","GET"])
def carbrand():  
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)  
        
        carmodel = df
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'id': row['Party_Name'],
                'name': row['Warehouse']}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)
 
if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0")
