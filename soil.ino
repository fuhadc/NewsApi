#define sensorPower 7
#define sensorPin A0
#define RELAY_ON 0
#define RELAY_OFF 1
#define RELAY_1 4

void setup() {
	pinMode(RELAY_1, OUTPUT);
	pinMode(sensorPower, OUTPUT);
    digitalWrite(sensorPower, LOW);
	Serial.begin(9600);
}

void loop() {
	Serial.print("Analog output: ");
	Serial.println(readSensor());
	int data =readSensor();
	if(data <= 500){
	digitalWrite(RELAY_1, RELAY_ON);
	Serial.println(“irrigation started.”);
}
	else if(data < 500){
	digitalWrite(RELAY_1, RELAY_OFF);
	Serial.println(“Bulb is now turned OFF.”);
}
	delay(1000);
}

int readSensor() {
	digitalWrite(sensorPower, HIGH);	
	delay(10);							
	int val = analogRead(sensorPin);	
	digitalWrite(sensorPower, LOW);		
	return val;							
}
