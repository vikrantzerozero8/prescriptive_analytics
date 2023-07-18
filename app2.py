#app.py
from flask import Flask, render_template, jsonify, request
import psycopg2 #pip install psycopg2 
import psycopg2.extras
      
app = Flask(__name__)
      
app.secret_key = "caircocoders-ednalan"
      
DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "admin"
          
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def main():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM carbrands ORDER BY brand_id")
    carbrands = cur.fetchall()
    return render_template('index.html', carbrands=carbrands)
  
@app.route("/carbrand",methods=["POST","GET"])
def carbrand():  
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)  
        cur.execute("SELECT * FROM carmodels WHERE brand_id = %s ORDER BY car_models ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'id': row['brand_id'],
                'name': row['car_models']}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)
 
if __name__ == "__main__":
    app.run(debug=True)
