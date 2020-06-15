# (c) 2019 Samujjwaal Dey, Ashish Joshi, Gurpreet Singh Nagpal

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import urllib.request
import json
import requests
import pyodbc
import folium
from math import sin, cos, sqrt, atan2, radians
import numpy as np
from werkzeug import secure_filename
from numpy import genfromtxt

R = 6373.0
UPLOAD_FOLDER = '.\\uploaded_csvs'
# UPLOAD_FOLDER = r'C:\Users\sag\Desktop\CatchmentPredictionUI\uploaded_csvs'

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def api_call(lat,long,rainwater,groundwater,soil_score,elevation):
    lat1=radians(float(lat))
    lon1=radians(float(long))
    return_array =[]
    return_array.append([float(lat),float(long)])

    #flash(lat+" "+long+" "+rainwater+" "+groundwater+" "+elevation+" "+soil_score)

    data = {
            "Inputs": {
                    "Catchment_Input":
                    [
                        {
                                'LAT': lat,
                                'LON': long,
                                'RAINFALL': rainwater,
                                'GRDWTR': groundwater,
                                'Soil_Score': soil_score,
                                'Elevation': elevation,
                        }
                    ],
            },
        "GlobalParameters":  {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/e8133a8b3c3e4e70be72cffb0e45a85c/services/95b227a3833042df9afeb7abe8cbd71b/execute?api-version=2.0&format=swagger'
    api_key = 'LQ0Tb4vX0P7Fbb/zuGmNSauhlKrJv7WcKJps70psDo+8f1vKrV7GyX/XQCD5pJ4CUG/pNeQc/xZX+XK/T5RQkw==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = json.loads(response.read().decode("utf8"))["Results"]["Catchment_Output"][0]["Scored Labels"]
        return_array.append(int(result))

        if int(result) == 1 :
            #flash("Conditions are suitable for catchment...")
            connection = pyodbc.connect(driver="{SQL Server}",server='sagdb.database.windows.net',database='sag',uid='sag',pwd='db@12345678')
            cursor = connection.cursor()
            #cursor1 = connection.cursor()
            cursor.execute("SELECT * from UniqueLatLong ")
            row_set = cursor.fetchall()
            g=0
            for row in row_set :
                lat2=radians(row[1])
                lon2=radians(row[2])
                dlon = lon2 - lon1
                dlat = lat2 - lat1

                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                if distance<=35:

                    #print(distance," ",row[1]," ",row[2])


                    cursor.execute("SELECT SUM(catchment2) AS SUM_CATCHMENT FROM VariedRainfall WHERE LAT=(?) AND LON =(?) GROUP BY LAT,LON;",row[1],row[2]  )
                    row1_set=cursor.fetchall()


                    for row1 in row1_set :
                        if row1[0]<2 :
                            return_array.append([float(row[1]),float(row[2]),float(distance)])
                            #print("LAT : ",row[1],"LONG : ",row[2],"Catchment_sum : ",row1[0],"distance : ",distance)
                            #flash("LAT : "+str(row[1])+" LONG : "+str(row[2])+" Catchment_sum : "+str(row1[0])+" distance : "+str(distance))
                            g=g+1

            print("Count : ",g)

        else :
            #flash("Conditions are not suitable for catchment...")
            connection = pyodbc.connect(driver="{SQL Server}",server='sagdb.database.windows.net',database='sag',uid='sag',pwd='db@12345678')
            cursor = connection.cursor()
            #cursor1 = connection.cursor()
            cursor.execute("SELECT * from UniqueLatLong ")
            row_set = cursor.fetchall()
            g=0
            for row in row_set :
                lat2=radians(row[1])
                lon2=radians(row[2])
                dlon = lon2 - lon1
                dlat = lat2 - lat1

                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                if distance<=50:

                    #print(distance," ",row[1]," ",row[2])


                    cursor.execute("SELECT SUM(catchment2) AS SUM_CATCHMENT FROM VariedRainfall WHERE YEAR_OBS>=2013 AND LAT=(?) AND LON =(?) GROUP BY LAT,LON;",row[1],row[2]  )
                    row1_set=cursor.fetchall()


                    for row1 in row1_set :
                        if row1[0] > 0 :
                            return_array.append([float(row[1]),float(row[2]),float(distance)])
                            #print("LAT : ",row[1],"LONG : ",row[2],"Catchment_sum : ",row1[0],"distance : ",distance)
                            #flash("LAT : "+str(row[1])+" LONG : "+str(row[2])+"  Catchment_sum : "+str(row1[0])+" distance : "+str(distance))
                            g=g+1

            #flash("Count : "+str(g))


    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

    print(return_array)
    return return_array


@app.route("/show_basic_input_map")
def show_basic_input_map():
    return render_template('show_basic_input_map.html')

class ReusableForm(Form):
##    name = TextField('Name:', validators=[validators.required()])
##    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
##    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

    @app.route("/batch_input", methods=['GET', 'POST'])
    def batch_ip():
        form = ReusableForm(request.form)
        print(form.errors)
        return render_template('batch_input.html',form=form)

    @app.route("/", methods=['GET', 'POST'])
    def index():
        start_coords = (19.663280, 75.300293)
        folium_map = folium.Map(location=start_coords, zoom_start=7)
        folium.LatLngPopup().add_to(folium_map)
        folium_map.save('templates/basic_input_map.html')
        form = ReusableForm(request.form)
        print(form.errors)
        return render_template('index.html',form=form)

    @app.route("/show_map", methods=['GET', 'POST'])
    def show_map():
##        start_coords = (46.9540700, 142.7360300)
##        folium_map = folium.Map(location=start_coords, zoom_start=14)
##        folium_map.save('templates/current_map.html')
        form = ReusableForm(request.form)
        if request.method == 'POST':
            return redirect (request.path)
        return render_template('show_map.html',form=form)

    @app.route("/show_batch_map", methods=['GET', 'POST'])
    def show_batch_map():
##        start_coords = (46.9540700, 142.7360300)
##        folium_map = folium.Map(location=start_coords, zoom_start=14)
##        folium_map.save('templates/current_map.html')
        form = ReusableForm(request.form)
        if request.method == 'POST':
            return redirect (request.path)
        return render_template('show_batch_map.html',form=form)

    @app.route("/batch_result", methods=['GET', 'POST'])
    def batch_result():
        return_matrix=[]
        form = ReusableForm(request.form)
        print(form.errors)
        if request.method == 'POST':
            f = request.files['csv_file']
            f.save(secure_filename(f.filename))
            my_data = genfromtxt(f.filename , delimiter=',')
            for row in my_data:
                return_matrix.append(api_call(row[0],row[1],row[2],row[3],row[4],row[5]))
                #flash("call is made..!")
        for k in range(len(return_matrix)):
            flash("Result for LAT : "+str(return_matrix[k][0][0])+",  LON : "+str(return_matrix[k][0][1])+"  :")
            if(int(return_matrix[k][1]) == 1):
                flash("Suitable for catchment..!")
            else:
                flash("Not suitable for catchment..!")
        print(return_matrix)
        mapit = folium.Map( location=[19.663280, 75.300293], zoom_start=8 )
        for j in range(len(return_matrix)):
            if int(return_matrix[j][1])== 1 :
                folium.Marker(
                        location=[return_matrix[j][0][0], return_matrix[j][0][1]],
                        popup='Potential catchment',
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(mapit)
                for i in range(2,len(return_matrix[j])):
                    #mapit = folium.Map( location=[ return_array[i][0], return_array[i][1] ] )
                    #folium.Marker( location=[ return_array[i][0], return_array[i][1] ], fill_color='#43d9de', radius=8 ).add_to( mapit )
                    folium.Marker(
                        location=[return_matrix[j][i][0], return_matrix[j][i][1]],
                        popup='Drought prone region',
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(mapit)
                    folium.PolyLine([return_matrix[j][0],return_matrix[j][i]], color="blue", weight=2.5, opacity=1).add_to(mapit)
            else :
                folium.Marker(
                        location=[return_matrix[j][0][0], return_matrix[j][0][1]],
                        popup='Drought prone region',
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(mapit)
                for i in range(2,len(return_matrix[j])):
                    #mapit = folium.Map( location=[ return_array[i][0], return_array[i][1] ] )
                    #folium.Marker( location=[ return_array[i][0], return_array[i][1] ], fill_color='#43d9de', radius=8 ).add_to( mapit )
                    folium.Marker(
                        location=[return_matrix[j][i][0], return_matrix[j][i][1]],
                        popup='Potential catchment',
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(mapit)
                    folium.PolyLine([return_matrix[j][0],return_matrix[j][i]], color="blue", weight=2.5, opacity=1).add_to(mapit)


            mapit.save('templates/current_batch_map.html')
        return render_template('batch_result.html',form=form)

    @app.route("/Results", methods=['GET', 'POST'])
    def show_result():
        form = ReusableForm(request.form)

        print(form.errors)
        if request.method == 'POST':
    ##        name=request.form['name']
    ##        password=request.form['password']
    ##        email=request.form['email']
    ##        print(name, " ", email, " ", password)
            lat = request.form['lat']
            long = request.form['long']
            rainwater = request.form['rainwater']
            groundwater = request.form['groundwater']
            elevation = request.form['elevation']
            soil_score = request.form['soil_score']

            return_array = api_call(lat,long,rainwater,groundwater,soil_score,elevation)
            print(return_array)

            if int(return_array[1]) == 1 :
                mapit = folium.Map( location=[return_array[0][0], return_array[0][1]], zoom_start=10 )
                folium.Marker(
                        location=[return_array[0][0], return_array[0][1]],
                        popup='Potential catchment location',
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(mapit)
                for i in range(2,len(return_array)):
                    #mapit = folium.Map( location=[ return_array[i][0], return_array[i][1] ] )
                    #folium.Marker( location=[ return_array[i][0], return_array[i][1] ], fill_color='#43d9de', radius=8 ).add_to( mapit )
                    folium.Marker(
                        location=[return_array[i][0], return_array[i][1]],
                        popup='Drought prone location',
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(mapit)
                    folium.PolyLine([return_array[0],return_array[i]], color="blue", weight=2.5, opacity=1).add_to(mapit)


                mapit.save('templates/current_map.html')
            else :
                mapit = folium.Map( location=[return_array[0][0], return_array[0][1]], zoom_start=10 )
                folium.Marker(
                        location=[return_array[0][0], return_array[0][1]],
                        popup='Drought prone region',
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(mapit)
                for i in range(2,len(return_array)):
                    #mapit = folium.Map( location=[ return_array[i][0], return_array[i][1] ] )
                    #folium.Marker( location=[ return_array[i][0], return_array[i][1] ], fill_color='#43d9de', radius=8 ).add_to( mapit )
                    folium.Marker(
                        location=[return_array[i][0], return_array[i][1]],
                        popup='Potential catchment region',
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(mapit)
                    folium.PolyLine([return_array[0],return_array[i]], color="blue", weight=2.5, opacity=1).add_to(mapit)


                mapit.save('templates/current_map.html')


            if(return_array[0]==1):
                flash("Conditions are suitable for catchment..!")
                flash("This cordinate can provide water to following coordinates :")
                for i in range(2,len(return_array)):
                    flash("LAT : "+str(return_array[i][0])+"  LON : "+str(return_array[i][1])+"  Distance : "+str(return_array[i][2]))
            else :
                flash("Conditions are not suitable for catchment..!")
                flash("This cordinate can take water from following coordinates :")
                for i in range(2,len(return_array)):
                    flash("LAT : "+str(return_array[i][0])+"  LON : "+str(return_array[i][1])+"  Distance : "+str(return_array[i][2]))


        return render_template('single_result.html', form=form)

if __name__ == "__main__":
    app.run()
