from app import app
from flask import render_template, request, redirect, url_for
from predict_model import model_prediction
from followup_diabetes import weight_control, pressure_control, sugar_control
from config import mydb, mycursor


@app.route("/")
def index():

    global alert
    alert = 0

    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/prediction")
def diabetes_prediction():
    return render_template("diabetes-prediction.html")


@app.route("/prediction-result", methods=["get", "post"])
def diabetes_prediction_result():

    req = request.form

    age = float(req["age"])
    weight = float(req["weight"])
    height = float(req["height"])
    sugar = float(req["sugar"])
    pressure1 = float(req["pressure1"])
    pressure2 = float(req["pressure2"])
    family = float(req["family"])
    bmi = weight / ((height/100)**2)

    result = model_prediction(2.95, sugar, pressure2, 29.1, 141.8, bmi, family, age)

    return render_template("diabetes-prediction-result.html", result=result)


@app.route("/login")
def login():
    return render_template("login.html", alert=alert)


@app.route("/followup", methods=["get", "post"])
def diabetes_followup():

    req = request.form

    global username

    username = str(req["username"])
    password = req["password"]

    sql = "SELECT * FROM patient WHERE p_id = '" + username + "' AND p_password = '" + password + "'"

    mycursor.execute(sql)
    result = mycursor.fetchall()

    if len(result) == 1:

        global name

        sql = "SELECT (p_name) FROM patient WHERE p_id = '" + username + "'"
        mycursor.execute(sql)
        name = mycursor.fetchone()[0].split()[0]

        global height

        sql = "SELECT (p_height) FROM patient WHERE p_id = '" + username + "'"
        mycursor.execute(sql)
        height = mycursor.fetchone()[0]

        return render_template("diabetes-followup.html", name=name)
    else:

        global alert
        alert = 1

        return redirect("/login")


@app.route("/weight-control")
def control_weight():
    return render_template("weight-control.html")


@app.route("/weight-control-result", methods=["get", "post"])
def control_weight_result():

    req = request.form

    weight = float(req["weight"])

    result = weight_control(weight, height)

    t_name = "WT"
    t_notes = "BMI= " + str("%.1f" % (weight / ((height/100)**2)))

    sql = "INSERT INTO test (t_name, t_result, t_notes, p_id) VALUES (%s, %s, %s, %s)"
    val = (t_name, weight, t_notes, username)

    mycursor.execute(sql, val)
    mydb.commit()

    return render_template("weight-control-result.html", result=result)


@app.route("/pressure-control")
def control_pressure():
    return render_template("pressure-control.html")


@app.route("/pressure-control-result", methods=["get", "post"])
def control_pressure_result():

    req = request.form

    systolic = int(req["pressure1"])
    diastolic = int(req["pressure2"])

    result = pressure_control(systolic, diastolic)

    t_name = "BP"
    t_result = str(systolic) + "/" + str(diastolic)

    sql = "INSERT INTO test (t_name, t_result, p_id) VALUES (%s, %s, %s)"
    val = (t_name, t_result, username)

    mycursor.execute(sql, val)
    mydb.commit()

    return render_template("pressure-control-result.html", result=result)


@app.route("/sugar-control")
def control_sugar():
    return render_template("sugar-control.html")


@app.route("/sugar-control-result", methods=["get", "post"])
def control_sugar_result():

    req = request.form

    time = req["time"]
    sugar = float(req["sugar"])

    result = sugar_control(sugar, time)

    t_name = "BG"

    sql = "INSERT INTO test (t_name, t_result, t_notes, p_id) VALUES (%s, %s, %s, %s)"
    val = (t_name, sugar, time, username)

    mycursor.execute(sql, val)
    mydb.commit()

    return render_template("sugar-control-result.html", result=result)
