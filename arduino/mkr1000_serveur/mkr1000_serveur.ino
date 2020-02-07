#include <WiFi101.h>

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
    }
  }
}
