
#define INPUT_PIN A0
#define LED_PIN 13
unsigned long start_time = 0;
unsigned long tmp_time = 0;
unsigned long prev_time = 0;
int helz = 50;
int T = 1000 / helz;
int data = 0;
bool send_flag = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(115200);
  Serial.print("arduino is avairable\n");
}

void send_data(unsigned long t) {
  data = analogRead(INPUT_PIN);
  String s = String(t-start_time);
  s += ",";
  s += String(data);
  s += '\n';
  Serial.print(s);
}

void(* resetFunc) (void) = 0;

void loop() {
  tmp_time = millis();
  if (tmp_time - prev_time >= T) {
    if (send_flag) {
      send_data(tmp_time);
    }
    prev_time = tmp_time;
  }
}

void serialEvent() {
  if(Serial.available() > 0) { // 内部でloop毎にSerial.available()>0の時呼ばれる関数なはずだから要らないのかもしれない．
    char c = Serial.read();
    switch (c) {
      case byte('0'):
        send_flag = false;
        digitalWrite(LED_PIN, LOW);
        break;
      case byte('1'):
        send_flag = true;
        start_time = millis();
        digitalWrite(LED_PIN, HIGH);
        break;
      // default:
      case byte('9'):
        resetFunc();
        break;
    }
  }
}
