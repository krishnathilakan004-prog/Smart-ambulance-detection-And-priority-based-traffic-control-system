
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

// blynk
#define BLYNK_PRINT Serial
#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

#define BLYNK_TEMPLATE_ID "TMPL3HtWBWtXV"
#define BLYNK_TEMPLATE_NAME "SMART AMBULANCE"
#define BLYNK_AUTH_TOKEN "5gZk8tjdIMuGYvgbmQNUTeAf_gJ5Fg3M"

// gps pin
const int GPS_RX=32;
const int GPS_TX=33;

// traffic light - pins conneced
int red[] = {15, 14, 25};
int yellow[] = {2, 12, 26};
int green[] = {0, 13, 27};

String ambulance="";
int i;

float  latitude;   
 float  longitude;



 
#define GPS_BAUD 9600


TinyGPSPlus gps;


SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
         

// Blynk
char auth[] = "5gZk8tjdIMuGYvgbmQNUTeAf_gJ5Fg3M";          
char ssid[] = "KNJ";                               
char pass[] = "karthi2004";


void setup() {
Serial.begin(115200);

  gpsSerial.begin(GPS_BAUD);
 
  Blynk.begin(auth, ssid, pass,"blynk.cloud",80);

  latitude = 0;   
  longitude = 0;

  Blynk.virtualWrite(V1, 0);
  Blynk.virtualWrite(V0, 0);
  
  Serial.println("Software Serial started at 9600 baud rate");
for (i=0;i<=2;i++)
{
  pinMode(red[i],OUTPUT);
  pinMode(yellow[i],OUTPUT);
  pinMode(green[i],OUTPUT);
}
}

void loop()
{
  Blynk.run();
// gps
unsigned long start = millis();

  while (millis() - start < 1000) {
    while (gpsSerial.available() > 0) {
      
    char c = gpsSerial.read();
   // Serial.print(c);  
    gps.encode(c);
    }
    if (gps.location.isUpdated()) 
    {
      latitude = (gps.location.lat());    
  longitude = (gps.location.lng()); 
    
    Serial.print("LAT:  ");
    Serial.println(latitude, 6); 
    Serial.print("LONG: ");
    Serial.println(longitude, 6);

    Blynk.virtualWrite(V1, latitude);    
    Blynk.virtualWrite(V0, longitude);          
    }
  }
  
 // traffic light
 for(i=0;i<3;i++)
{      
 emergency();

   // normal traffic operation
   for (int j = 0; j < 3; j++)
{
    if (j != i) 
    {  // If it's not the current traffic light
        digitalWrite(red[j], HIGH);
        digitalWrite(yellow[j], LOW);
        digitalWrite(green[j], LOW);
    }
}

emergency();

// Red light
    digitalWrite(red[i], HIGH);
    digitalWrite(yellow[i], LOW);
    digitalWrite(green[i], LOW);
    delay(3000);  // Red for 3 seconds

   if (emergency()==1) 
    continue;

// Green light
    digitalWrite(red[i], LOW);
    digitalWrite(yellow[i], LOW);
    digitalWrite(green[i], HIGH);
    delay(3000);  // Green for 3 seconds

    if (emergency()==1) 
    continue;

// Orange (Yellow) light
    digitalWrite(red[i], LOW);
    digitalWrite(yellow[i], HIGH);
    digitalWrite(green[i], LOW);
    delay(2000);  // Yellow for 2 second

   
 if (emergency()==1) 
    continue;
    // Red light
    digitalWrite(red[i], HIGH);
    digitalWrite(yellow[i], LOW);
    digitalWrite(green[i], LOW);
    delay(1000);  // Red for 1 seconds

     emergency();

}

}



int emergency()
{
   if (Serial.available() > 0) 
{
    ambulance = Serial.readStringUntil('#'); 
 }

  if (ambulance == "k") 
{ 
  Serial.println("Ambulance Detected! Giving Priority...");

//  Turn all other signals RED
    for (int j = 1; j < 3; j++)
    { 
     // Turn signals 2 and 3 red only if they are NOT already red
       
            if (digitalRead(red[j]) == LOW)
            {  // If not already red
                digitalWrite(green[j], LOW);
                digitalWrite(yellow[j], HIGH);
                delay(500);
                digitalWrite(yellow[j], LOW);
                digitalWrite(red[j], HIGH);
                delay(1000);
            }
        }
    
    

 // Check if the first traffic light is already green
        if (digitalRead(green[0]) == LOW) 
        {  
           digitalWrite(red[0], LOW);
            digitalWrite(yellow[0], LOW);
            digitalWrite(green[0], HIGH);
            delay(5000);  // Green for 5 seconds
           
        }
        else
        {
         digitalWrite(red[i], LOW);
         digitalWrite(yellow[i], LOW);
         digitalWrite(green[i], HIGH);
         delay(5000);  // Green for 5 seconds
          
        }

      ambulance="";
      return 1; 
      
}
     return 0; 
}
