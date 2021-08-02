
#define INPUT_PIN A0
#define LED_PIN 13
unsigned long start_time = 0;
unsigned long tmp_time = 0;
unsigned long prev_time = 0;
unsigned long rec_time = 0;
int helz = 100;
int T = 1000 / helz;
int data = 0;
bool send_flag = false;



void send_data() {
  data = analogRead(INPUT_PIN);
  String s = String(tmp_time-start_time);
  s += ",";
  s += String(data);
  s += '\n';
  Serial.print(s);
}

void test_mode() {
  String s = "0, 1023, ";
  s += String(analogRead(INPUT_PIN));
  Serial.println(s);
}
/*
int funcnum = 0;
typedef void (*processFunc)(void);
processFunc FuncList[] = 
{
  &send_data,
  &test_mode
};
*/

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(115200);
  Serial.print("arduino is avairable\n");
}

void(* resetFunc) (void) = 0;

void loop() {
  serialEvent(); // Arduino nano every needs this line.
  tmp_time = millis();
  rec_time = tmp_time - prev_time;
  if (rec_time >= T) {
    if (send_flag) {
      //(void)(*FuncList[funcnum])();
      //test_mode();
      send_data();
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
        //funcnum = 0;
        send_flag = true;
        start_time = millis();
        digitalWrite(LED_PIN, HIGH);
        break;
      case byte('2'): // test mode
        //funcnum = 1;
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
