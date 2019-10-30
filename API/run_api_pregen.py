# --------------------------------------REQUIREMENTS--------------------------------------
from flask import Flask, jsonify, request, abort, redirect, url_for, session
from flask_session import Session
from flask_dance.contrib.github import make_github_blueprint, github
import psycopg2
import sys
import os
import numpy as np
import pandas as pd
import credentials as creds
import pandas.io.sql as psql
import json
# --------------------------------------REQUIREMENTS--------------------------------------

"""
API important links explanation:
/refresh (GET)
-> Refreshes the session, removing the cookies and allowing you to start 
from the original create session again

/session/create (POST)
-> Generate session number, return the session number to user
-> Need key value for lat, long ,transport_mode, speed, quality
-> Generates lat, long, preferences and others and stores it in the database
-> Only for OAuth authenticated users

/session/<session_id> (PUT)
-> Insert details for each particular user
-> Need key value for lat, long ,transport_mode, speed, quality

/session/<session_id> (GET)
-> Get all session details
-> Requires OAuth

/session/<session_id>/calculate (GET)
-> If OAuth is provided, run the calculation
-> Redirect to results page

/session/<session_id>/results (GET)
-> Use this page for showing results to prevent lag
-> If OAuth is provided or IP address matches, show results

"""

app = Flask(__name__)

#The secret key is necessary for session to work
app.secret_key = 'super dsagbrjuyki64y5tg4fd key'


@app.route('/')
def index():
    #A placeholder to check if the website is working
    return 'Main Site Goes Here'


@app.route('/session/create', methods=['POST'])
def create_session(): 
    #Create the session if it does not exist
    if session.get('data') is None:
        # Here we create the session

        # Get session details from OAUTH
        username = 'username'

        # Extract the post json details
        content = request.get_json()

        # Generate Random Session ID:
        session_id = '123456'

        # Consolidate the session details
        host_user_details = {'username': username,
                            'lat': content.get('lat'),
                            'long': content.get('long'),
                            'transport_mode': content.get('transport_mode', 'public'),
                            'metrics': {
                                'speed': int(content.get('speed', 5)),
                                'quality': int(content.get('quality', 5))
                            }}

        session['data'] = {'users': [host_user_details]}

        return jsonify({"session_id":session_id})    
    else:
        return jsonify({"warning":'session already exists'})


#Create a function to refresh the data if necessary
@app.route('/refresh', methods=['GET'])
def refresh():
    #Remove the cookies
    session.clear()
    return "Session has been refreshed"

@app.route('/session/<session_id>', methods=['POST', 'GET'])
def manage_details(session_id):
    if request.method == 'POST':

        # Ensure that we have not yet received a message from this ip
        identifier = 'identifier'

        # Get the content of the PUT
        content = request.get_json()

        # Make sure the lat and long are provided and valid

        # Consolidate the session details
        new_user_details = {'identifier': identifier,
                            'lat': content.get('lat'),
                            'long': content.get('long'),
                            'transport_mode': content.get('transport_mode', 'public'),
                            'metrics': {
                                'speed': int(content.get('speed', 5)),
                                'quality': int(content.get('quality', 5))
                            }}

        #If the session does not yet exist
        if session.get('data') is not None:

            #append the users details to the session data
            data = session['data']
            data['users'].append(new_user_details)
            session['data'] = data

            return jsonify({'updated_info_for_session_id': session_id})
        else:
            return jsonify({'error': 'The specified session id does not yet exist'})

    elif request.method == 'GET':

        if session.get('data') is not None:
            #Return the session details if a get request is performed
            return jsonify(session['data'])
        else:
            return jsonify({'error': 'sesson_id or username is wrong'})


@app.route('/session/<session_id>/calculate', methods=['GET'])
def calculate(session_id):
    #Always return the result, for testing purposes
    return redirect("/session/"+session_id+"/results", code=302)


#The results come from here
@app.route('/session/<session_id>/results', methods=['GET'])
def results(session_id):

    # Make the fake results json
    results="""
    {
  "Coffeeshop": {
    "243213958": {
      "end_vid": "6135405004",
      "latitude": [
        1.2855896,
        1.2859143,
        1.2859143,
        1.2863548,
        1.2863548,
        1.2863548,
        1.2863433,
        1.2863433,
        1.2862659,
        1.2862243,
        1.2860071,
        1.2859992,
        1.2859992,
        1.2859305,
        1.2859305,
        1.2859419,
        1.2859419,
        1.2860635
      ],
      "longtitude": [
        103.8251266,
        103.8251707,
        103.8251707,
        103.8252231,
        103.8252231,
        103.8252231,
        103.8253817,
        103.8253817,
        103.8256776,
        103.8258736,
        103.8271872,
        103.8272698,
        103.8272698,
        103.8272579,
        103.8272579,
        103.8271775,
        103.8271775,
        103.8263959
      ],
      "restaurant_x": 103.826623485547,
      "restaurant_y": 1.28577109982105,
      "start_user": "243213958",
      "start_user_name": "identifier",
      "total_cost": "0.139279667031"
    },
    "4488019045": {
      "end_vid": "6135405004",
      "latitude": [
        1.3333416,
        1.3333416,
        1.3321144,
        1.331882,
        1.3317869,
        1.3317571,
        1.3313831,
        1.3313831,
        1.331297,
        1.3310123,
        1.3308219,
        1.3307604,
        1.3307604,
        1.330121,
        1.3296956,
        1.3296956,
        1.328818,
        1.328818,
        1.3285763,
        1.3285763,
        1.3284539,
        1.3284539,
        1.3279776,
        1.3279776,
        1.3281706,
        1.3287751,
        1.3288148,
        1.328866,
        1.3290304,
        1.3290304,
        1.3290419,
        1.3290083,
        1.328971,
        1.3286981,
        1.3278476,
        1.3252418,
        1.3249918,
        1.3239018,
        1.3237545,
        1.3236071,
        1.3233592,
        1.3217274,
        1.3217274,
        1.3215628,
        1.3205324,
        1.3197514,
        1.3195591,
        1.3193745,
        1.3193745,
        1.3186061,
        1.3180936,
        1.3178073,
        1.3170033,
        1.3154792,
        1.315076,
        1.3140528,
        1.313975,
        1.313975,
        1.3134631,
        1.3109121,
        1.3088208,
        1.3081959,
        1.3081959,
        1.3060809,
        1.3033909,
        1.3032144,
        1.3026463,
        1.3026463,
        1.3017053,
        1.2914753,
        1.2914753,
        1.2903631,
        1.2891176,
        1.2888334,
        1.2870683,
        1.2869844,
        1.2868783,
        1.2860255,
        1.2860255,
        1.2846382,
        1.2840873,
        1.2835123,
        1.2835123,
        1.2831535,
        1.2831535,
        1.2831077,
        1.2831077,
        1.2830322,
        1.2830322,
        1.283163,
        1.283163,
        1.2835354,
        1.2840488,
        1.2841165,
        1.2841165,
        1.2842149,
        1.2842149,
        1.2845578,
        1.2848746,
        1.2853782,
        1.2853782,
        1.2854086,
        1.2854086,
        1.2856372,
        1.285943,
        1.2858745,
        1.285869,
        1.285869,
        1.2858422,
        1.2858422,
        1.2858403,
        1.2858403,
        1.2858128,
        1.2857922,
        1.2857922,
        1.2858787,
        1.285899,
        1.285899,
        1.2859305,
        1.2859305,
        1.2859419,
        1.2859419,
        1.2860635
      ],
      "longtitude": [
        103.8652285,
        103.8652285,
        103.8654213,
        103.865756,
        103.8659139,
        103.8659713,
        103.8665797,
        103.8665797,
        103.8666429,
        103.8673693,
        103.868005,
        103.868217,
        103.868217,
        103.8680357,
        103.8679564,
        103.8679564,
        103.8677216,
        103.8677216,
        103.868267,
        103.868267,
        103.8684917,
        103.8684917,
        103.8679996,
        103.8679996,
        103.8677575,
        103.8658854,
        103.8657454,
        103.8655717,
        103.8650095,
        103.8650095,
        103.8642211,
        103.8641653,
        103.8640957,
        103.8636167,
        103.8620665,
        103.8599358,
        103.8596678,
        103.8585017,
        103.8583445,
        103.8581874,
        103.8579285,
        103.8565377,
        103.8565377,
        103.8563696,
        103.8552404,
        103.8541098,
        103.8538304,
        103.8535398,
        103.8535398,
        103.8518878,
        103.850824,
        103.8501455,
        103.8483712,
        103.8464109,
        103.846096,
        103.8455114,
        103.845481,
        103.845481,
        103.8452381,
        103.8445551,
        103.8428282,
        103.8418494,
        103.8418494,
        103.8402144,
        103.8407341,
        103.8408784,
        103.8415685,
        103.8415685,
        103.8426224,
        103.8433247,
        103.8433247,
        103.8427493,
        103.842053,
        103.841843,
        103.840124,
        103.839995,
        103.8398021,
        103.8384233,
        103.8384233,
        103.8373153,
        103.8370169,
        103.8365651,
        103.8365651,
        103.8361492,
        103.8361492,
        103.8360637,
        103.8360637,
        103.83594,
        103.83594,
        103.8358247,
        103.8358247,
        103.8355547,
        103.8349859,
        103.8347989,
        103.8347989,
        103.8345837,
        103.8345837,
        103.8343164,
        103.8340683,
        103.8336635,
        103.8336635,
        103.8336406,
        103.8336406,
        103.8334301,
        103.8320239,
        103.8302797,
        103.8301037,
        103.8301037,
        103.8294625,
        103.8294625,
        103.8294107,
        103.8294107,
        103.8289064,
        103.8283545,
        103.8283545,
        103.8275597,
        103.8274801,
        103.8274801,
        103.8272579,
        103.8272579,
        103.8271775,
        103.8271775,
        103.8263959
      ],
      "restaurant_x": 103.826623485547,
      "restaurant_y": 1.28577109982105,
      "start_user": "4488019045",
      "start_user_name": "username",
      "total_cost": "0.139279667031"
    }
  },
  "Coocaca": {
    "243213958": {
      "end_vid": "6438089513",
      "latitude": [
        1.2855896,
        1.2859143,
        1.2859143,
        1.2863548,
        1.2863548,
        1.2863548,
        1.2870809,
        1.2877204,
        1.2881006,
        1.2881006,
        1.2883592,
        1.288577,
        1.2887281,
        1.2893873,
        1.2897756,
        1.2900226,
        1.2900226,
        1.2905007,
        1.2905007,
        1.2906685,
        1.2906685,
        1.290908,
        1.291434,
        1.2916845,
        1.2921484,
        1.2921484,
        1.2922487,
        1.2925285,
        1.2928297,
        1.2928297,
        1.2930502,
        1.2931232,
        1.2932971,
        1.2934698,
        1.2935431,
        1.2937062,
        1.2940298,
        1.2940298,
        1.2944756,
        1.2944756,
        1.2947792,
        1.2948744,
        1.2949978,
        1.2952551,
        1.2952551,
        1.2954703,
        1.2956759,
        1.2956759,
        1.2966413,
        1.2981398,
        1.2985609,
        1.2985609,
        1.2991608,
        1.2991608,
        1.2992908,
        1.2992908,
        1.2993811,
        1.2993811,
        1.2996514,
        1.2996514,
        1.2998238,
        1.2998458,
        1.2998486,
        1.2998486,
        1.2999216,
        1.3001187,
        1.3004014,
        1.3004014,
        1.300887,
        1.3012867,
        1.3012867,
        1.3016603,
        1.3021341,
        1.302523,
        1.3025886,
        1.3025886,
        1.3026823,
        1.3019543,
        1.3019543,
        1.3019348
      ],
      "longtitude": [
        103.8251266,
        103.8251707,
        103.8251707,
        103.8252231,
        103.8252231,
        103.8252231,
        103.8253132,
        103.825406,
        103.8254653,
        103.8254653,
        103.8255127,
        103.8255526,
        103.8255808,
        103.8257669,
        103.8259062,
        103.8259981,
        103.8259981,
        103.8261203,
        103.8261203,
        103.8261398,
        103.8261398,
        103.8261301,
        103.8260275,
        103.8259647,
        103.8258769,
        103.8258769,
        103.8258734,
        103.8258803,
        103.8259697,
        103.8259697,
        103.8261008,
        103.8261897,
        103.8264267,
        103.8266666,
        103.8267828,
        103.8270099,
        103.8274605,
        103.8274605,
        103.828082,
        103.828082,
        103.8285208,
        103.8286489,
        103.8288285,
        103.829267,
        103.829267,
        103.8298237,
        103.8303113,
        103.8303113,
        103.8301592,
        103.8300249,
        103.8300216,
        103.8300216,
        103.8299545,
        103.8299545,
        103.8298928,
        103.8298928,
        103.8300709,
        103.8300709,
        103.8306146,
        103.8306146,
        103.8318944,
        103.8324509,
        103.8325361,
        103.8325361,
        103.8339409,
        103.8346343,
        103.8348306,
        103.8348306,
        103.8350842,
        103.8353291,
        103.8353291,
        103.8355127,
        103.8357454,
        103.8358968,
        103.835918,
        103.835918,
        103.8361705,
        103.8374552,
        103.8374552,
        103.8374982
      ],
      "restaurant_x": 103.837310485546,
      "restaurant_y": 1.30148389981886,
      "start_user": "243213958",
      "start_user_name": "identifier",
      "total_cost": "0.137905099871"
    },
    "4488019045": {
      "end_vid": "6438089513",
      "latitude": [
        1.3333416,
        1.3333416,
        1.3321144,
        1.331882,
        1.3317869,
        1.3317571,
        1.3313831,
        1.3313831,
        1.331297,
        1.3310123,
        1.3308219,
        1.3307604,
        1.3307604,
        1.330121,
        1.3296956,
        1.3296956,
        1.328818,
        1.328818,
        1.3285763,
        1.3285763,
        1.3284539,
        1.3284539,
        1.3279776,
        1.3279776,
        1.3281706,
        1.3287751,
        1.3288148,
        1.328866,
        1.3290304,
        1.3290304,
        1.3290419,
        1.3290083,
        1.328971,
        1.3286981,
        1.3278476,
        1.3252418,
        1.3249918,
        1.3239018,
        1.3237545,
        1.3236071,
        1.3233592,
        1.3217274,
        1.3217274,
        1.3215628,
        1.3205324,
        1.3197514,
        1.3195591,
        1.3193745,
        1.3193745,
        1.3186061,
        1.3180936,
        1.3178073,
        1.3170033,
        1.3154792,
        1.315076,
        1.3140528,
        1.313975,
        1.313975,
        1.3134631,
        1.3109121,
        1.3088208,
        1.3081959,
        1.3081959,
        1.3067676,
        1.3065167,
        1.3062127,
        1.3061169,
        1.3061093,
        1.3061005,
        1.3061005,
        1.3060528,
        1.3058534,
        1.305748,
        1.3056382,
        1.3051365,
        1.3051365,
        1.3044327,
        1.3035595,
        1.3035595,
        1.3032115,
        1.3032115,
        1.3028907,
        1.3023605,
        1.3023605,
        1.3021218,
        1.3019543,
        1.3019543,
        1.3019348
      ],
      "longtitude": [
        103.8652285,
        103.8652285,
        103.8654213,
        103.865756,
        103.8659139,
        103.8659713,
        103.8665797,
        103.8665797,
        103.8666429,
        103.8673693,
        103.868005,
        103.868217,
        103.868217,
        103.8680357,
        103.8679564,
        103.8679564,
        103.8677216,
        103.8677216,
        103.868267,
        103.868267,
        103.8684917,
        103.8684917,
        103.8679996,
        103.8679996,
        103.8677575,
        103.8658854,
        103.8657454,
        103.8655717,
        103.8650095,
        103.8650095,
        103.8642211,
        103.8641653,
        103.8640957,
        103.8636167,
        103.8620665,
        103.8599358,
        103.8596678,
        103.8585017,
        103.8583445,
        103.8581874,
        103.8579285,
        103.8565377,
        103.8565377,
        103.8563696,
        103.8552404,
        103.8541098,
        103.8538304,
        103.8535398,
        103.8535398,
        103.8518878,
        103.850824,
        103.8501455,
        103.8483712,
        103.8464109,
        103.846096,
        103.8455114,
        103.845481,
        103.845481,
        103.8452381,
        103.8445551,
        103.8428282,
        103.8418494,
        103.8418494,
        103.8407269,
        103.8404922,
        103.8395287,
        103.8388245,
        103.8387773,
        103.8387287,
        103.8387287,
        103.8385301,
        103.8380155,
        103.8377558,
        103.8374916,
        103.8370804,
        103.8370804,
        103.837232,
        103.8377633,
        103.8377633,
        103.8377823,
        103.8377823,
        103.8377907,
        103.8377054,
        103.8377054,
        103.837586,
        103.8374552,
        103.8374552,
        103.8374982
      ],
      "restaurant_x": 103.837310485546,
      "restaurant_y": 1.30148389981886,
      "start_user": "4488019045",
      "start_user_name": "username",
      "total_cost": "0.137905099871"
    }
  },
  "Food Paradise": {
    "243213958": {
      "end_vid": "4984756061",
      "latitude": [
        1.2855896,
        1.2859143,
        1.2859143,
        1.2863548,
        1.2863548,
        1.2863548,
        1.2863433,
        1.2863433,
        1.2862659,
        1.2862243,
        1.2860071,
        1.2859992,
        1.2859992,
        1.2858814,
        1.2858847,
        1.2858847,
        1.285918,
        1.2859206,
        1.2859206,
        1.2859469
      ],
      "longtitude": [
        103.8251266,
        103.8251707,
        103.8251707,
        103.8252231,
        103.8252231,
        103.8252231,
        103.8253817,
        103.8253817,
        103.8256776,
        103.8258736,
        103.8271872,
        103.8272698,
        103.8272698,
        103.8283134,
        103.8283616,
        103.8283616,
        103.829404,
        103.8294597,
        103.8294597,
        103.830104
      ],
      "restaurant_x": 103.829495185547,
      "restaurant_y": 1.28614999982099,
      "start_user": "243213958",
      "start_user_name": "identifier",
      "total_cost": "0.135387982991"
    },
    "4488019045": {
      "end_vid": "4984756061",
      "latitude": [
        1.3333416,
        1.3333416,
        1.3321144,
        1.331882,
        1.3317869,
        1.3317571,
        1.3313831,
        1.3313831,
        1.331297,
        1.3310123,
        1.3308219,
        1.3307604,
        1.3307604,
        1.330121,
        1.3296956,
        1.3296956,
        1.328818,
        1.328818,
        1.3285763,
        1.3285763,
        1.3284539,
        1.3284539,
        1.3279776,
        1.3279776,
        1.3281706,
        1.3287751,
        1.3288148,
        1.328866,
        1.3290304,
        1.3290304,
        1.3290419,
        1.3290083,
        1.328971,
        1.3286981,
        1.3278476,
        1.3252418,
        1.3249918,
        1.3239018,
        1.3237545,
        1.3236071,
        1.3233592,
        1.3217274,
        1.3217274,
        1.3215628,
        1.3205324,
        1.3197514,
        1.3195591,
        1.3193745,
        1.3193745,
        1.3186061,
        1.3180936,
        1.3178073,
        1.3170033,
        1.3154792,
        1.315076,
        1.3140528,
        1.313975,
        1.313975,
        1.3134631,
        1.3109121,
        1.3088208,
        1.3081959,
        1.3081959,
        1.3060809,
        1.3033909,
        1.3032144,
        1.3026463,
        1.3026463,
        1.3017053,
        1.2914753,
        1.2914753,
        1.2903631,
        1.2891176,
        1.2888334,
        1.2870683,
        1.2869844,
        1.2868783,
        1.2860255,
        1.2860255,
        1.2846382,
        1.2840873,
        1.2835123,
        1.2835123,
        1.2831535,
        1.2831535,
        1.2831077,
        1.2831077,
        1.2830322,
        1.2830322,
        1.283163,
        1.283163,
        1.2835354,
        1.2840488,
        1.2841165,
        1.2841165,
        1.2842149,
        1.2842149,
        1.2845578,
        1.2848746,
        1.2853782,
        1.2853782,
        1.2854086,
        1.2854086,
        1.2856372,
        1.285943,
        1.2858745,
        1.285869,
        1.285869,
        1.2859469
      ],
      "longtitude": [
        103.8652285,
        103.8652285,
        103.8654213,
        103.865756,
        103.8659139,
        103.8659713,
        103.8665797,
        103.8665797,
        103.8666429,
        103.8673693,
        103.868005,
        103.868217,
        103.868217,
        103.8680357,
        103.8679564,
        103.8679564,
        103.8677216,
        103.8677216,
        103.868267,
        103.868267,
        103.8684917,
        103.8684917,
        103.8679996,
        103.8679996,
        103.8677575,
        103.8658854,
        103.8657454,
        103.8655717,
        103.8650095,
        103.8650095,
        103.8642211,
        103.8641653,
        103.8640957,
        103.8636167,
        103.8620665,
        103.8599358,
        103.8596678,
        103.8585017,
        103.8583445,
        103.8581874,
        103.8579285,
        103.8565377,
        103.8565377,
        103.8563696,
        103.8552404,
        103.8541098,
        103.8538304,
        103.8535398,
        103.8535398,
        103.8518878,
        103.850824,
        103.8501455,
        103.8483712,
        103.8464109,
        103.846096,
        103.8455114,
        103.845481,
        103.845481,
        103.8452381,
        103.8445551,
        103.8428282,
        103.8418494,
        103.8418494,
        103.8402144,
        103.8407341,
        103.8408784,
        103.8415685,
        103.8415685,
        103.8426224,
        103.8433247,
        103.8433247,
        103.8427493,
        103.842053,
        103.841843,
        103.840124,
        103.839995,
        103.8398021,
        103.8384233,
        103.8384233,
        103.8373153,
        103.8370169,
        103.8365651,
        103.8365651,
        103.8361492,
        103.8361492,
        103.8360637,
        103.8360637,
        103.83594,
        103.83594,
        103.8358247,
        103.8358247,
        103.8355547,
        103.8349859,
        103.8347989,
        103.8347989,
        103.8345837,
        103.8345837,
        103.8343164,
        103.8340683,
        103.8336635,
        103.8336635,
        103.8336406,
        103.8336406,
        103.8334301,
        103.8320239,
        103.8302797,
        103.8301037,
        103.8301037,
        103.830104
      ],
      "restaurant_x": 103.829495185547,
      "restaurant_y": 1.28614999982099,
      "start_user": "4488019045",
      "start_user_name": "username",
      "total_cost": "0.135387982991"
    }
  },
  "La Villa": {
    "243213958": {
      "end_vid": "566964118",
      "latitude": [
        1.2855896,
        1.2859143,
        1.2859143,
        1.2863548,
        1.2863548,
        1.2863548,
        1.2870809,
        1.2877204,
        1.2881006,
        1.2881006,
        1.2883592,
        1.288577,
        1.2887281,
        1.2893873,
        1.2897756,
        1.2900226,
        1.2900226,
        1.2905007,
        1.2905007,
        1.2906685,
        1.2906685,
        1.290908,
        1.291434,
        1.2916845,
        1.2921484,
        1.2921484,
        1.2922487,
        1.2925285,
        1.2928297,
        1.2928297,
        1.2930502,
        1.2931232,
        1.2932971,
        1.2934698,
        1.2935431,
        1.2937062,
        1.2940298,
        1.2940298,
        1.2944756,
        1.2944756,
        1.2947792,
        1.2948744,
        1.2949978,
        1.2952551,
        1.2952551,
        1.2954703,
        1.2956759,
        1.2956759,
        1.2958652,
        1.2960978,
        1.2960978,
        1.2962024,
        1.2962589,
        1.2963046,
        1.2963192,
        1.2962563,
        1.2962288,
        1.2961394,
        1.2961338,
        1.2961596,
        1.2962287
      ],
      "longtitude": [
        103.8251266,
        103.8251707,
        103.8251707,
        103.8252231,
        103.8252231,
        103.8252231,
        103.8253132,
        103.825406,
        103.8254653,
        103.8254653,
        103.8255127,
        103.8255526,
        103.8255808,
        103.8257669,
        103.8259062,
        103.8259981,
        103.8259981,
        103.8261203,
        103.8261203,
        103.8261398,
        103.8261398,
        103.8261301,
        103.8260275,
        103.8259647,
        103.8258769,
        103.8258769,
        103.8258734,
        103.8258803,
        103.8259697,
        103.8259697,
        103.8261008,
        103.8261897,
        103.8264267,
        103.8266666,
        103.8267828,
        103.8270099,
        103.8274605,
        103.8274605,
        103.828082,
        103.828082,
        103.8285208,
        103.8286489,
        103.8288285,
        103.829267,
        103.829267,
        103.8298237,
        103.8303113,
        103.8303113,
        103.8308192,
        103.8314505,
        103.8314505,
        103.8318112,
        103.832201,
        103.8325359,
        103.8334738,
        103.8336666,
        103.8338018,
        103.833959,
        103.8338074,
        103.8336653,
        103.8334599
      ],
      "restaurant_x": 103.833560285546,
      "restaurant_y": 1.29560869981968,
      "start_user": "243213958",
      "start_user_name": "identifier",
      "total_cost": "0.139124727941"
    },
    "4488019045": {
      "end_vid": "566964118",
      "latitude": [
        1.3333416,
        1.3333416,
        1.3321144,
        1.331882,
        1.3317869,
        1.3317571,
        1.3313831,
        1.3313831,
        1.331297,
        1.3310123,
        1.3308219,
        1.3307604,
        1.3307604,
        1.330121,
        1.3296956,
        1.3296956,
        1.328818,
        1.328818,
        1.3285763,
        1.3285763,
        1.3284539,
        1.3284539,
        1.3279776,
        1.3279776,
        1.3281706,
        1.3287751,
        1.3288148,
        1.328866,
        1.3290304,
        1.3290304,
        1.3290419,
        1.3290083,
        1.328971,
        1.3286981,
        1.3278476,
        1.3252418,
        1.3249918,
        1.3239018,
        1.3237545,
        1.3236071,
        1.3233592,
        1.3217274,
        1.3217274,
        1.3215628,
        1.3205324,
        1.3197514,
        1.3195591,
        1.3193745,
        1.3193745,
        1.3186061,
        1.3180936,
        1.3178073,
        1.3170033,
        1.3154792,
        1.315076,
        1.3140528,
        1.313975,
        1.313975,
        1.3134631,
        1.3109121,
        1.3088208,
        1.3081959,
        1.3081959,
        1.3067676,
        1.3065167,
        1.3062127,
        1.3061169,
        1.3061093,
        1.3061005,
        1.3061005,
        1.3060528,
        1.3058534,
        1.305748,
        1.3056382,
        1.3051365,
        1.3051365,
        1.3044327,
        1.3035595,
        1.3035595,
        1.3032115,
        1.3032115,
        1.3028907,
        1.3023605,
        1.3023605,
        1.3021218,
        1.3019543,
        1.3019543,
        1.3015166,
        1.3011432,
        1.3009126,
        1.3006852,
        1.3004714,
        1.3004714,
        1.3002864,
        1.3001582,
        1.3003134,
        1.3003134,
        1.3000565,
        1.2998176,
        1.2998176,
        1.298896,
        1.2963192,
        1.2962563,
        1.2962288,
        1.2961394,
        1.2961338,
        1.2961596,
        1.2962287
      ],
      "longtitude": [
        103.8652285,
        103.8652285,
        103.8654213,
        103.865756,
        103.8659139,
        103.8659713,
        103.8665797,
        103.8665797,
        103.8666429,
        103.8673693,
        103.868005,
        103.868217,
        103.868217,
        103.8680357,
        103.8679564,
        103.8679564,
        103.8677216,
        103.8677216,
        103.868267,
        103.868267,
        103.8684917,
        103.8684917,
        103.8679996,
        103.8679996,
        103.8677575,
        103.8658854,
        103.8657454,
        103.8655717,
        103.8650095,
        103.8650095,
        103.8642211,
        103.8641653,
        103.8640957,
        103.8636167,
        103.8620665,
        103.8599358,
        103.8596678,
        103.8585017,
        103.8583445,
        103.8581874,
        103.8579285,
        103.8565377,
        103.8565377,
        103.8563696,
        103.8552404,
        103.8541098,
        103.8538304,
        103.8535398,
        103.8535398,
        103.8518878,
        103.850824,
        103.8501455,
        103.8483712,
        103.8464109,
        103.846096,
        103.8455114,
        103.845481,
        103.845481,
        103.8452381,
        103.8445551,
        103.8428282,
        103.8418494,
        103.8418494,
        103.8407269,
        103.8404922,
        103.8395287,
        103.8388245,
        103.8387773,
        103.8387287,
        103.8387287,
        103.8385301,
        103.8380155,
        103.8377558,
        103.8374916,
        103.8370804,
        103.8370804,
        103.837232,
        103.8377633,
        103.8377633,
        103.8377823,
        103.8377823,
        103.8377907,
        103.8377054,
        103.8377054,
        103.837586,
        103.8374552,
        103.8374552,
        103.8370648,
        103.8367471,
        103.8365556,
        103.8363421,
        103.8360928,
        103.8360928,
        103.8359432,
        103.8355448,
        103.8350774,
        103.8350774,
        103.8347036,
        103.8339078,
        103.8339078,
        103.8338792,
        103.8334738,
        103.8336666,
        103.8338018,
        103.833959,
        103.8338074,
        103.8336653,
        103.8334599
      ],
      "restaurant_x": 103.833560285546,
      "restaurant_y": 1.29560869981968,
      "start_user": "4488019045",
      "start_user_name": "username",
      "total_cost": "0.139124727941"
    }
  },
  "Tian Tian Seafood Restaurant": {
    "243213958": {
      "end_vid": "248009773",
      "latitude": [
        1.2855896,
        1.2859143,
        1.2859143,
        1.2863548,
        1.2863548,
        1.2863548,
        1.2863433,
        1.2863433,
        1.2862659,
        1.2862243,
        1.2860071,
        1.2859992,
        1.2859992,
        1.2858814,
        1.2858847,
        1.2858847,
        1.285918,
        1.2859206,
        1.2859206,
        1.2859469,
        1.2860051,
        1.2859819,
        1.2861355,
        1.2861355,
        1.2863221,
        1.2865863,
        1.2863225,
        1.2863225,
        1.2861469,
        1.2861469,
        1.2859086,
        1.2854136,
        1.2853299,
        1.2851485,
        1.2849139,
        1.2846245,
        1.2845059
      ],
      "longtitude": [
        103.8251266,
        103.8251707,
        103.8251707,
        103.8252231,
        103.8252231,
        103.8252231,
        103.8253817,
        103.8253817,
        103.8256776,
        103.8258736,
        103.8271872,
        103.8272698,
        103.8272698,
        103.8283134,
        103.8283616,
        103.8283616,
        103.829404,
        103.8294597,
        103.8294597,
        103.830104,
        103.8320239,
        103.8326539,
        103.8336476,
        103.8336476,
        103.8339437,
        103.8343492,
        103.8346713,
        103.8346713,
        103.8345444,
        103.8345444,
        103.834601,
        103.8347786,
        103.8348185,
        103.8348949,
        103.8349917,
        103.8351111,
        103.8351582
      ],
      "restaurant_x": 103.835005085546,
      "restaurant_y": 1.28458109982121,
      "start_user": "243213958",
      "start_user_name": "identifier",
      "total_cost": "0.139309687076"
    },
    "4488019045": {
      "end_vid": "248009773",
      "latitude": [
        1.3333416,
        1.3333416,
        1.3321144,
        1.331882,
        1.3317869,
        1.3317571,
        1.3313831,
        1.3313831,
        1.331297,
        1.3310123,
        1.3308219,
        1.3307604,
        1.3307604,
        1.330121,
        1.3296956,
        1.3296956,
        1.328818,
        1.328818,
        1.3285763,
        1.3285763,
        1.3284539,
        1.3284539,
        1.3279776,
        1.3279776,
        1.3281706,
        1.3287751,
        1.3288148,
        1.328866,
        1.3290304,
        1.3290304,
        1.3290419,
        1.3290083,
        1.328971,
        1.3286981,
        1.3278476,
        1.3252418,
        1.3249918,
        1.3239018,
        1.3237545,
        1.3236071,
        1.3233592,
        1.3217274,
        1.3217274,
        1.3215628,
        1.3205324,
        1.3197514,
        1.3195591,
        1.3193745,
        1.3193745,
        1.3186061,
        1.3180936,
        1.3178073,
        1.3170033,
        1.3154792,
        1.315076,
        1.3140528,
        1.313975,
        1.313975,
        1.3134631,
        1.3109121,
        1.3088208,
        1.3081959,
        1.3081959,
        1.3060809,
        1.3033909,
        1.3032144,
        1.3026463,
        1.3026463,
        1.3017053,
        1.2914753,
        1.2914753,
        1.2903631,
        1.2891176,
        1.2888334,
        1.2870683,
        1.2869844,
        1.2868783,
        1.2860255,
        1.2860255,
        1.2846382,
        1.2840873,
        1.2835123,
        1.2835123,
        1.2831535,
        1.2831535,
        1.2831077,
        1.2831077,
        1.2830322,
        1.2830322,
        1.283163,
        1.283163,
        1.2835354,
        1.2840488,
        1.2841165,
        1.2841165,
        1.2845059
      ],
      "longtitude": [
        103.8652285,
        103.8652285,
        103.8654213,
        103.865756,
        103.8659139,
        103.8659713,
        103.8665797,
        103.8665797,
        103.8666429,
        103.8673693,
        103.868005,
        103.868217,
        103.868217,
        103.8680357,
        103.8679564,
        103.8679564,
        103.8677216,
        103.8677216,
        103.868267,
        103.868267,
        103.8684917,
        103.8684917,
        103.8679996,
        103.8679996,
        103.8677575,
        103.8658854,
        103.8657454,
        103.8655717,
        103.8650095,
        103.8650095,
        103.8642211,
        103.8641653,
        103.8640957,
        103.8636167,
        103.8620665,
        103.8599358,
        103.8596678,
        103.8585017,
        103.8583445,
        103.8581874,
        103.8579285,
        103.8565377,
        103.8565377,
        103.8563696,
        103.8552404,
        103.8541098,
        103.8538304,
        103.8535398,
        103.8535398,
        103.8518878,
        103.850824,
        103.8501455,
        103.8483712,
        103.8464109,
        103.846096,
        103.8455114,
        103.845481,
        103.845481,
        103.8452381,
        103.8445551,
        103.8428282,
        103.8418494,
        103.8418494,
        103.8402144,
        103.8407341,
        103.8408784,
        103.8415685,
        103.8415685,
        103.8426224,
        103.8433247,
        103.8433247,
        103.8427493,
        103.842053,
        103.841843,
        103.840124,
        103.839995,
        103.8398021,
        103.8384233,
        103.8384233,
        103.8373153,
        103.8370169,
        103.8365651,
        103.8365651,
        103.8361492,
        103.8361492,
        103.8360637,
        103.8360637,
        103.83594,
        103.83594,
        103.8358247,
        103.8358247,
        103.8355547,
        103.8349859,
        103.8347989,
        103.8347989,
        103.8351582
      ],
      "restaurant_x": 103.835005085546,
      "restaurant_y": 1.28458109982121,
      "start_user": "4488019045",
      "start_user_name": "username",
      "total_cost": "0.139309687076"
    }
  },
  "possible_locations": [
    "Tian Tian Seafood Restaurant",
    "La Villa",
    "Food Paradise",
    "Coffeeshop",
    "Coocaca"
  ],
  "users": {
    "243213958": {
      "latitude": 1.2848664,
      "longtitude": 103.8244263
    },
    "4488019045": {
      "latitude": 1.333489,
      "longtitude": 103.865812
    }
  }
}
    """
    

    # return the results
    return results


if __name__ == '__main__':

    # Run the App
    app.run(host='0.0.0.0', debug=True, use_reloader=False, port=5000)

    #These settings are required for session to work
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANANT_SESSION_LIFETIME'] = True
    app.config.from_object(__name__)
    Session(app)

