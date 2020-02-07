#include <WiFi101.h>


#define PULSE_PIN 6
#define DIR_PIN 7

WiFiServer server(80);
char ssid[] = "MKR1000_RATATOUILLE";
int status = WL_IDLE_STATUS;

bool alreadyConnected = false;


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
  pwm(9, 512, 20000);
  pinMode(PULSE_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);

  delay(1000);
  Serial.begin(9600);
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

  if (client) {
    if (!alreadyConnected) {
      // clear out the input buffer:
      client.flush();
      Serial.println("We have a new client");
      alreadyConnected = true;
    }

    Serial.println("===\nloop\n===");
    if (client.available() > 0) {
      String msg = client.readStringUntil('\n');
      Serial.print("message : ");
      Serial.println(msg);
      if (msg.compareTo("left\r") == 0) {
        digitalWrite(DIR_PIN, LOW);
        delay(20);
        analogWrite(PULSE_PIN, 127);
        Serial.println("PulseUP");
      }
      else if (msg.compareTo("right\r") == 0) {
        digitalWrite(DIR_PIN, HIGH);
        delay(20);
        analogWrite(PULSE_PIN, 127);
        Serial.println("PulseUP");
      }
      else {
        analogWrite(PULSE_PIN, 0);
        Serial.println("PulseDown");
      }
    }
    Serial.println("ack");
    client.println("ack");
  }
}
