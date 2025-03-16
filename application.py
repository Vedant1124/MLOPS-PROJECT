from flask import Flask , render_template , request
import joblib
from config.paths_config import *

app = Flask(__name__) # FLASK app started below this everything comes under FLASK

model = joblib.load(MODEL_SAVE_PATH)

@app.route("/",methods = ["GET","POST"]) # Flask se ham Website se data lerahe hai using GET aur POST k ar rahe hai apne output ko website pe but Website mai keval POST hi kar rahe hai...website se jo bhi data aega usko Flask ke andar bhejenge using POST
def home():
    if request.method=="POST":
        try:
            departure_delay = float(request.form["Departure Delay"])
            arrival_delay = float(request.form["Arrival Delay"])

            flight_distance = float(request.form["Flight Distance"])

            delay_ratio = (departure_delay+arrival_delay) / (flight_distance+1)



            data = [
                int(request.form["Online Boarding"]),
                delay_ratio,
                int(request.form["Inflight wifi service"]),
                int(request.form["Class"]),
                int(request.form["Type of Travel"]),
                int(request.form["Inflight entertainment"]),
                flight_distance,
                int(request.form["Seat comfort"]),
                int(request.form["Leg room service"]),
                int(request.form["On-board service"]),
                int(request.form["Cleanliness"]),
                int(request.form["Ease of Online Booking"]),
            ]


            prediction = model.predict([data])
            output = prediction[0]
            print(output)

            return render_template("index.html" , prediction = output ) # Output ko index.html par bhejna hai isliye ye wala render_template use aaega
        
        except Exception as e:
            return render_template("index.html" , error = str(e))
        

    return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0" , port=5000)

            
