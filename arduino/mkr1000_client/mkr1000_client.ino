#include <WiFi101.h>

IPAddress server(192, 168, 1, 1);
WiFiClient client;

unsigned long last_time;
unsigned long time_to_wait;
String ans;

boolean newData = false;

const byte numChars = 100;
char receivedChars[numChars];

void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
  
  // if (Serial.available() > 0) {
  while (Serial.available() > 0 && newData == false) {
    Serial.println("lecture");
    rc = Serial.read();
    
    if (rc != endMarker) {
    receivedChars[ndx] = rc;
    ndx++;
    if (ndx >= numChars) {
      ndx = numChars - 1;
      }
    }
    else {
      Serial.print("lu :");
      Serial .println(ndx);
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true;
    }
  }
}

void setup() {
  Serial.begin(9600);

  

  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    while (true) ;
  }

  String fv = WiFi.firmwareVersion();
  Serial.print("Wifi Firmware version : ");
  Serial.println(fv);

  int status = WL_IDLE_STATUS;
  do {
    status = WiFi.begin("MKR1000_RATATOUILLE");
  } while (status != WL_CONNECTED);

  IPAddress ip = WiFi.localIP();
  Serial.print("Local IP: ");
  Serial.println(ip);

  if (client.connect(server, 80)) {
    Serial.println("Connected!");
  }
  else {
    Serial.println("Connection failed");
    while (true);
  }
  last_time = millis();
  time_to_wait = 100;
}

void loop() {

  recvWithEndMarker();
  if(newData == true){
    client.println(receivedChars);
    Serial.println("rec: ");
    Serial.println(receivedChars);
    while (Serial.available()> 0) 
      Serial.read();
    newData = false;
  }

  delay(50);
  
  if (client.available()) {
    ans = client.readStringUntil('\n');
    Serial.println("ans: ");
    Serial.println(ans);
  }

  
  delay(50);
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println(WiFi.status());
    setup();
  }
}
