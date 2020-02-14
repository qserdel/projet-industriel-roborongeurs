#include <WiFi101.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 7
#define NB_LED 15



WiFiServer server(80);
char ssid[] = "MKR1000_RATATOUILLE";
int status = WL_IDLE_STATUS;

bool alreadyConnected = false;

boolean newData = false;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NB_LED,LED_PIN);

const byte numChars = 100;
char receivedChars[numChars];

void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
  
  // if (Serial.available() > 0) {
  while (Serial.available() > 0 && newData == false) {
    //Serial.println("lecture");
    rc = Serial.read();
    
    if (rc != endMarker) {
    receivedChars[ndx] = rc;
    ndx++;
    if (ndx >= numChars) {
      ndx = numChars - 1;
      }
    }
    else {
      //Serial.print("lu :");
      //Serial .println(ndx);
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true;
    }
  }
}

bool ledOn = false;
void myHandler(){
  ledOn = !ledOn;

  if(ledOn){
    Serial.println("on");
  }
  else{
    Serial.println("off");
  }
}


void setup() {

  delay(1000);
  Serial.begin(9600);
  
  strip.begin();
  strip.show();

  
  Serial.print("Creating access point named: ");
  Serial.println(ssid);
  if (WiFi.beginAP(ssid) != WL_AP_LISTENING) {
    Serial.println("Creating access point failed");
    while (true);
  }
  server.begin();

  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  
}

void loop() {
  WiFiClient client = server.available();
  recvWithEndMarker();
  
  if(newData == true){
      server.println(receivedChars);
      Serial.println("serial: ");
      Serial.println(receivedChars);
      /*
      while (Serial.available()> 0) 
        Serial.read();
        */
      newData = false;
    }

  if (client) {
    //Serial.println("entre");
    
    if (!alreadyConnected) {
      // clear out the input buffer:
      client.flush();
      Serial.println("We have a new client");
      alreadyConnected = true;
    }
    if (client.available() > 0) {
      String msg = client.readStringUntil('\n');
      if(msg.charAt(0) == 'L'){
        int n, r, g, b;
        char id;
        n = msg.substring(2,3).toInt();
        r = msg.substring(4,7).toInt();
        g = msg.substring(8,11).toInt();
        b = msg.substring(12,15).toInt();
        
        strip.setPixelColor(n, r, g, b);
        strip.show();
        
        Serial.print("set ");
        Serial.print(n);
        Serial.print(" [");
        Serial.print(r);
        Serial.print(",");
        Serial.print(g);
        Serial.print(",");
        Serial.print(b);
        Serial.println("]");
        
      }
      
      Serial.print("message : ");
      Serial.println(msg);
    }
  }
}

