#include <WiFi101.h>

#define LED_POWER 2
#define LED_CONNECTED 3
#define LED_SYNC 4

#define BUTTON_RIGHT 7
#define BUTTON_LEFT 6

IPAddress server(192, 168, 1, 1);
WiFiClient client;

unsigned long last_time;
unsigned long time_to_wait;
String last_cmd;
String ans;

void setup() {
  pinMode(LED_POWER, OUTPUT);
  pinMode(LED_CONNECTED, OUTPUT);
  pinMode(LED_SYNC, OUTPUT);

  pinMode(BUTTON_LEFT, INPUT_PULLUP);
  pinMode(BUTTON_RIGHT, INPUT_PULLUP);

  digitalWrite(LED_POWER, HIGH);
  digitalWrite(LED_CONNECTED, LOW);
  digitalWrite(LED_SYNC, LOW);

  delay(1000);
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
    digitalWrite(LED_CONNECTED, HIGH);
  }
  else {
    Serial.println("Connection failed");
    while (true);
  }

  last_cmd = "none";
  last_time = millis();
  time_to_wait = 100;
}

void loop() {
  if ((millis() - last_time) > time_to_wait) {
    if (digitalRead(BUTTON_LEFT) == LOW) {
      time_to_wait = 5000;
      last_cmd = "left";
    }
    else if (digitalRead(BUTTON_RIGHT) == LOW) {
      time_to_wait = 5000;
      last_cmd = "right";
    }
    else {
      time_to_wait = 100;
      last_cmd = "none";
    }

    Serial.println(last_cmd);
    client.println(last_cmd);
    last_time = millis();
  }

  if (client.available()) {
    ans = client.readStringUntil('\n');
    if (ans.compareTo("ack\r") == 0) { // && last_cmd.compareTo("none") != 0) {
      digitalWrite(LED_SYNC, HIGH);
    }
    else {
      digitalWrite(LED_SYNC, LOW);
    }
  }

  delay(50);

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println(WiFi.status());
    setup();
  }
}
