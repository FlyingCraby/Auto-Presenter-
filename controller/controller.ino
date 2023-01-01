#include "Adafruit_GFX.h"
#include "Adafruit_ILI9341.h"
#include "URTouch.h"

#define TFT_DC 9
#define TFT_CS 10
#define TFT_RST 8
#define TFT_MISO 12
#define TFT_MOSI 11
#define TFT_CLK 13

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_MOSI, TFT_CLK, TFT_RST, TFT_MISO);

#define t_SCK 3
#define t_CS 4
#define t_MOSI 5
#define t_MISO 6
#define t_IRQ 7 
#define trigpin A2
#define echopin A3

URTouch ts(t_SCK, t_CS, t_MOSI, t_MISO, t_IRQ);

int gpin = A0;
int opin = A1;
int x;
int y;
int ostatus = 2;
int gstatus = 2;

int getd() {
  digitalWrite(trigpin, LOW);
  delayMicroseconds(100);
  digitalWrite(trigpin, HIGH);
  delayMicroseconds(100);
  long duration = pulseIn(echopin, HIGH);
  int distance = duration * 0.034 / 2;
  return distance;
}

void getouch() {
  while (!ts.dataAvailable()){
    
  }
  ts.read();
  x = ts.getX();
  y = ts.getY();
  //    Serial.print("X: ");
  //    Serial.println(x);
  //    Serial.print("Y: ");
  //    Serial.println(y);
  if ((x != -1) && (y != -1)) {
    x = 320 - x;
    y = 240 - y;
  }
}


void setup() {
  Serial.begin(9600);
  pinMode(gpin, OUTPUT);
  pinMode(opin, OUTPUT);
  pinMode(trigpin, OUTPUT);
  pinMode(echopin, INPUT);
  tft.begin();
  tft.setRotation(1);
  delay(1000);
  tft.fillScreen(ILI9341_BLACK);
  ts.InitTouch();
  ts.setPrecision(PREC_EXTREME);
}

void loop(){
  if (gstatus == 1){
    digitalWrite(gpin, HIGH);
  }
  else if (gstatus == 2){
    digitalWrite(gpin, LOW);
  }
  else{
    digitalWrite(gpin, HIGH);
    delay(500);
    digitalWrite(gpin, LOW);
    delay(500);
  }
  if (ostatus == 1){
    digitalWrite(opin, HIGH);
  }
  else if (ostatus == 2){
    digitalWrite(opin, LOW);
  }
  else{
    digitalWrite(opin, HIGH);
    delay(500);
    digitalWrite(opin, LOW);
    delay(500);
  }
  x = NULL;
  y = NULL;
  if (Serial.available() > 0){
    String command = Serial.readString();
    char commandtype = command[0];
    if (commandtype == 'd'){
      Serial.println(getd());
    }
    else if (commandtype == 's'){
      char value = command[2];
      if (value == '0'){
        tft.fillScreen(ILI9341_BLACK);
      }
      else if (value == '1'){
        tft.setCursor(50,20);
        tft.setTextSize(2);
        tft.fillRect(15,150, 115, 40, ILI9341_GREEN);
        tft.fillRect(170,150, 115, 40, ILI9341_RED);
        tft.write("Choose an option.");
        tft.setTextSize(2);
        tft.setCursor(20, 150);
        tft.write("Answer");
        tft.setCursor(20, 170);
        tft.write("Questions");
        tft.setCursor(170, 150);
        tft.write("Chat with");
        tft.setCursor(220, 170);
        tft.write("Me");
        while (true){
          getouch();
          Serial.println(y);
          if (x>15 && x<130 && y>150 && y<190){ 
            Serial.println("a");
            tft.fillScreen(ILI9341_BLACK);
            break; 
          }
          if (x>170 && x<285 && y>150 && y<190){ 
            Serial.println("b");
            tft.fillScreen(ILI9341_BLACK);
            break; 
          }
        }       
      }
    }
    else if (commandtype == 'l'){
      gstatus = String (command[3]).toInt();
      ostatus = String (command[5]).toInt();
    }
  }
}
