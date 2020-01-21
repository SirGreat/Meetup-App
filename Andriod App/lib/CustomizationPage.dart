import 'main.dart';
import 'MapPage.dart';
import 'ShareLinkPage.dart';
import 'Meetingtype.dart';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'dart:async';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:esys_flutter_share/esys_flutter_share.dart';
import 'package:location/location.dart';
import 'package:geolocator/geolocator.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:connectivity/connectivity.dart';
import 'color_loader.dart';

class CustomizationPage extends StatelessWidget {
  final PrefData data;
  CustomizationPage({this.data});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Choose Your Preferences"),
//        backgroundColor: Colors.black,
      ),
      body: CustomizationPageWidget(data: data,),
    );
  }

}

class CustomizationPageWidget extends StatefulWidget {
  final PrefData data;
  CustomizationPageWidget({this.data});
  @override
  CustomizationPageState createState() => CustomizationPageState(data: data);
}

class CustomizationPageState extends State<CustomizationPageWidget> {
  final PrefData data;
  CustomizationPageState({this.data});

  String value2 = "Select...";
  String value3 = "Select...";
  String value4 = "Select...";
  double value5 = 0;
  //Method for the labels on the slider
  String labels() {
    switch (value5.floor()) {
      case 0:
        return "No Pref.";
      case 1:
        return "\$";
      case 2:
        return "\$\$";
      case 3:
        return "\$\$\$";
      case 4:
        return "\$\$\$\$";
    }
    return "";
  }

  Future<String> postDataGetID() async {

    //extract data from PrefData to add to json package
    double lat = data.lat;
    double long = data.long;
    int quality = data.quality;
    int speed = data.speed;
    String transportmode = data.transportMode;
    int price  = data.price;

    //send json package to server as POST
    Map<String, String> headers = {"Content-type": "application/json"};
    String address = globalurl();

    String url = '$address/session/create';

//    String jsonpackage = '{"lat":$lat,   "long":$long,   "quality":$quality,   "speed":$speed,    "transport_mode":"$transportmode"}';
    String jsonpackage = '{"lat":$lat,   "long":$long,   "quality":$quality,   "speed":$speed,    "transport_mode":"$transportmode", "price_level":"$price"}';
    print("jsonpackage $jsonpackage");
    try{

      http.Response response = await http.post(url, headers:headers, body:jsonpackage);
      int statusCode = response.statusCode;

      if (statusCode != 200){
        Scaffold.of(context).showSnackBar(
            SnackBar(
              content: Text("Oops! Server Error 404! Can"),
              duration: Duration(seconds: 2),
            ));
      }

      else{

        String body = response.body; //store returned string-map "{sessionid: XXX}"" into String body
        print("POST REQUEST SUCCESSFUL/FAILED WITH STATUSCODE: $statusCode");
        print("SERVER SAYS: $body");

        //decode the string-map
        Map<String, dynamic> sessionidjsonversion = jsonDecode(body);
        var sessionid = sessionidjsonversion['session_id'];
        data.sessionid = sessionid;
        print("Transport Mode:$transportmode");
        print("Quality:$quality");
        print("Speed:$speed");
        print("Price: $price");
        data.link = "$address/session/$sessionid/get_details";
        String theLink = data.link;
        print('Link Created--> $theLink');
        return theLink;

      }
    }

    catch(e){print("Session Create Failed with Error: $e");}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            mainAxisSize: MainAxisSize.max,
            children: <Widget>[
              Expanded(
                flex: 5,
                child: Container(
                  padding: const EdgeInsets.only(left: 10.0, top: 8.0, right: 30.0, bottom: 8.0),
                  child: Row(
                    children: <Widget>[
                      Icon(Icons.directions_car, color: Colors.black),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text("Transport", style: TextStyle(
                            color: Colors.black,
                            fontWeight: FontWeight.bold,
                            fontSize: 20.0
                        ),),
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                flex: 5,
                child: Container(
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: value2,
                      onChanged: (String newValue) {
                        setState(() {
                          value2 = newValue;
                          data.transportMode = newValue; //ADD TO DATABASE
                        });
                      },
                      items: <String>["Select...", "Driving", "Public Transit", "Walk", "Riding"].map<DropdownMenuItem<String>>((String value) {
                        return DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        );
                      }).toList(),
                    ),
                  ),
                ),
              )
            ],
          ),//for transport
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            mainAxisSize: MainAxisSize.max,
            children: <Widget>[
              Expanded(
                flex: 5,
                child: Container(
                  padding: const EdgeInsets.only(left: 10.0, top: 8.0, right: 30.0, bottom: 8.0),
                  child: Row(
                    children: <Widget>[
                      Icon(Icons.timer, color: Colors.black),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text("Speed", style: TextStyle(
                            color: Colors.black,
                            fontWeight: FontWeight.bold,
                            fontSize: 20.0
                        ),),
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                flex: 5,
                child: Container(
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: value3,
                      onChanged: (String newValue) {
                        setState(() {
                          value3 = newValue;
                          if (value3=="Fast"){data.speed = 3;}
                          else if (value3=="Regular"){data.speed=2;}
                          else if (value3=="No Preference"){data.speed=1;}  //ADD TO DATABASE
                          else {data.speed=0;}
                        });
                      },
                      items: <String>["Select...", "No Preference", "Regular", "Fast"].map<DropdownMenuItem<String>>((String value) {
                        return DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        );
                      }).toList(),
                    ),
                  ),
                ),
              )
            ],
          ),//for speed
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            mainAxisSize: MainAxisSize.max,
            children: <Widget>[
              Expanded(
                flex: 5,
                child: Container(
                  padding: const EdgeInsets.only(left: 10.0, top: 8.0, right: 30.0, bottom: 8.0),
                  child: Row(
                    children: <Widget>[
                      Icon(Icons.star, color: Colors.black),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text("Ratings", style: TextStyle(
                            color: Colors.black,
                            fontWeight: FontWeight.bold,
                            fontSize: 20.0
                        ),),
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                flex: 5,
                child: Container(
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: value4,
                      onChanged: (String newValue) {
                        setState(() {
                          value4 = newValue;
                          if (value4=="Best"){data.quality=3;}
                          else if (value4=="Regular"){data.quality=2;}
                          else if (value4=="No Preference"){data.quality=1;}  //ADD TO DATABASE
                          else{data.quality=0;}
                        });
                      },
                      items: <String>["Select...", "No Preference", "Regular", "Best"]
                          .map<DropdownMenuItem<String>>((String value) {
                        return DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        );
                      }).toList(),
                    ),
                  ),
                ),
              )
            ],
          ),//for ratings
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            mainAxisSize: MainAxisSize.max,
            children: <Widget>[
              Expanded(
                flex: 5,
                child: Container(
                  padding: const EdgeInsets.only(left: 10.0, top: 8.0, right: 30.0, bottom: 8.0),
                  child: Row(
                    children: <Widget>[
                      Icon(Icons.attach_money, color: Colors.black),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text("Price", style: TextStyle(
                            color: Colors.black,
                            fontWeight: FontWeight.bold,
                            fontSize: 20.0
                        ),),
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                flex: 6,
                child: Container(
                    child: Slider(
                      value: value5,
                      onChanged: (newValue) => setState(() {
                        value5 = newValue;
                        if (value5==1){data.price=1;}
                        else if (value5==2){data.price=2;}
                        else if (value5==3){data.price=3;}  //ADD TO DATABASE
                        else{data.price=0;}
                      }),
                      max: 4,
                      min: 0,
                      divisions: 4,
                      label: labels(),
                    )
                ),
              )
            ],
          ),

        ], //children of ListView
      ),
      bottomNavigationBar: BottomAppBar(
        child: FlatButton(
            child: Text('Confirm', style: TextStyle(fontWeight: FontWeight.bold)),
            onPressed: () async {
              if (value2 != "Select..." && value3 != "Select..." && value4 != "Select...") {
                postDataGetID();
                await Future.delayed(Duration(milliseconds: 2000));
                Navigator.push(context,MaterialPageRoute(builder: (context) => ShareLinkPage(data:data)),);
              } else {
                Scaffold.of(context).showSnackBar(
                    SnackBar(
                      content: Text("Please select preferences!"),
                      duration: Duration(seconds: 2),
                    ));
              }
            }
        ),
      ),
    );
  }
}