#include <WiFi101.h>
#include <Adafruit_NeoPixel.h>
#include <Ramp.h>

#define STOP1 0
#define STOP2 5

#define BV 1
#define BJ 2
#define BR1 3
#define BR2 4

#define LED_PIN 7

#define PULSE_PIN 8
#define DIR_PIN 9


#define NB_LED 30

#define PULSE_PAR_REV 400



WiFiServer server(80);
char ssid[] = "MKR1000_RATATOUILLE";
int status = WL_IDLE_STATUS;

bool alreadyConnected = false;

boolean newData = false;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NB_LED, LED_PIN);
unsigned long lastT;

const byte numChars = 100;
char receivedChars[numChars];


rampDouble myRamp;



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

bool pulsehigh = false;
void pulseHandler() {
  pulsehigh = !pulsehigh;

  if (pulsehigh) {
    digitalWrite(PULSE_PIN, HIGH);
  }
  else {
    digitalWrite(PULSE_PIN, LOW);
  }
}

void turnTable() {

}

double v_to_dm(double v) {
  if ( v == 0 ) return -1;
  return 1. / (v * 2 * PULSE_PAR_REV / 360.);

}


void setup() {

  delay(1000);
  Serial.begin(9600);

  strip.begin();
  strip.fill(strip.Color(255, 10, 100), 0, NB_LED);
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

  pinMode(PULSE_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  pinMode(STOP1, INPUT);
  pinMode(STOP2, INPUT);

  pinMode(BV, INPUT);
  pinMode(BJ, INPUT);
  pinMode(BR1, INPUT);
  pinMode(BR2, INPUT);

  lastT = millis();


}

void loop() {
  WiFiClient client = server.available();

  recvWithEndMarker();
  if (newData == true) {
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
      if (msg.charAt(0) == 'L') {
        int n, r, g, b;
        char id;
        n = msg.substring(2, 3).toInt();
        r = msg.substring(4, 7).toInt();
        g = msg.substring(8, 11).toInt();
        b = msg.substring(12, 15).toInt();

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

      if (msg.charAt(0) == 'R') {
        int dir, t;
        char id;
        dir = msg.substring(2, 3).toInt();
        t = msg.substring(4, 5).toInt();


        Serial.print("turn dir = ");
        Serial.print(dir);
        Serial.print("  for ");
        Serial.print(t);
        Serial.println(" seconds");


        if (dir == 1) {
          digitalWrite(DIR_PIN, HIGH);
          Serial.println("high");
        }
        else {
          digitalWrite(DIR_PIN, LOW);
          Serial.println("Low");
        }
        delay(20);

        unsigned long start_time = millis();
        while (millis() - start_time < t * 1000) {
          analogWrite(PULSE_PIN, 127);
        }
        analogWrite(PULSE_PIN, 0);


      }

      Serial.print("message : ");
      Serial.println(msg);
    }
  }

  if (digitalRead(BV) == HIGH && millis() - lastT > 200) {
    server.println("T");
    lastT = millis();
  }

  if (digitalRead(BJ) == HIGH) {
    Serial.println("lu BJ");
  }

  if (digitalRead(BR1) == HIGH) {
    Serial.println("lu BR1");

    float tacc = 1000;//Temps d'acceleration en ms
    float vmin = 10000;
    float vmax = 1000000;//vitesse en °/ks
    float thold = 3000;//temps de maintient a la vitesse max en ms
    double vreel; //vitesse en °/s
    myRamp.go(vmin);
    int phase = 1;

    unsigned long rotstart = millis();
    myRamp.go(vmax, tacc, LINEAR);

    while (digitalRead(STOP1) == LOW) {
      //Serial.println("c'est dedans");
      pulseHandler();
      vreel = myRamp.update() / 1000.;
      Serial.println(v_to_dm(vreel)* 1000000);
      Serial.println(myRamp.update());
      delayMicroseconds(v_to_dm(vreel) * 1000000);



      if ((millis() - rotstart > tacc + thold) and (phase == 1)) {
        phase = 2;
        myRamp.go(vmin, tacc, LINEAR, ONCEFORWARD);
      }
    }
  }


  if (digitalRead(BR2) == HIGH) {
    Serial.println("lu BR2");
    
    float tacc = 1000;//Temps d'acceleration en ms
    float vmin = 10000;
    float vmax = 1000000;//vitesse en °/ks
    float thold = 3000;//temps de maintient a la vitesse max en ms
    double vreel; //vitesse en °/s
    myRamp.go(vmin);
    int phase = 1;
    
    unsigned long rotstart = millis();
    myRamp.go(vmax,tacc,LINEAR);
    
    while(digitalRead(STOP1) == LOW){
      //Serial.println("c'est dedans");
      pulseHandler();
      vreel = myRamp.update()/1000.;
      //Serial.println(v_to_dm(vreel));
      //Serial.println(myRamp.update());
      delayMicroseconds(2500);
      
      
      
      if((millis()-rotstart > tacc + thold) and (phase == 1)){
        phase = 2;
        myRamp.go(vmin,tacc,LINEAR,ONCEFORWARD);
      }
    }
  }
  

}

