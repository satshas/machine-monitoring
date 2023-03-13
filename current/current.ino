#include <WiFi.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.

const char* ssid = "Hamburger";
const char* password = "Hamburger";
const char* mqtt_server = "pi-mqtt-server";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;
#define BUTTON_PIN 0

const int ACPin = 35;         //set arduino signal read pin
#define ACTectionRange 0.5;    //set Non-invasive AC Current Sensor tection range (5A,10A,20A)
// VREF: Analog reference
// For Arduino UNO, Leonardo and mega2560, etc. change VREF to 5
// For Arduino Zero, Due, MKR Family, ESP32, etc. 3V3 controllers, change VREF to 3.3
#define VREF 3.3

float readACCurrentValue()
{
  float ACCurrtntValue = 0;
  float peakVoltage = 0;  
  float voltageVirtualValue = 0;  //Vrms
  for (int i = 0; i < 5; i++)
  {
    peakVoltage += analogRead(ACPin);   //read peak voltage
    delay(1);
  }
  peakVoltage = peakVoltage / 5;   
  voltageVirtualValue = peakVoltage * 0.707;    //change the peak voltage to the Virtual Value of voltage

  /*The circuit is amplified by 2 times, so it is divided by 2.*/
  voltageVirtualValue = (voltageVirtualValue / 1024 * VREF ) / 2;  

  ACCurrtntValue = voltageVirtualValue * ACTectionRange;

  return ACCurrtntValue;
}


void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(BUTTON_PIN, INPUT);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float ACCurrentValue = readACCurrentValue(); //read AC Current Value
  Serial.print(ACCurrentValue);
  Serial.println(" A");

  char result[8]; // Buffer big enough for 7-character float
  dtostrf(ACCurrentValue, 6, 2, result); // Leave room for too large numbers
  
  
  client.publish("inmachines/lasercutter/power", result);

  delay(100);

}
