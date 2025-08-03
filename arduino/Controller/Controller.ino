#include <IRremote.hpp>

#define IR_RECEIVE_PIN      2

uint32_t last_decodedRawData = 0;
IRrecv irrecv(IR_RECEIVE_PIN);

void setup() {
  Serial.begin(9600);
  irrecv.enableIRIn();
}

void translateIR() 
{
  if (irrecv.decodedIRData.flags)
  {
    //set the current decodedRawData to the last decodedRawData
    irrecv.decodedIRData.decodedRawData = last_decodedRawData;
  }
  else
  {
    Serial.print("IR code: 0x");
    Serial.println(irrecv.decodedIRData.decodedRawData, HEX);
  }

  switch (irrecv.decodedIRData.decodedRawData)
  {
    case 0xE718FF00:
      Serial.println("straight");
      Serial.println("forward");
      break;
    case 0xAD52FF00:
      Serial.println("straight");
      Serial.println("backward");
      break;
    case 0xA55AFF00:
      Serial.println("right");
      break;
    case 0xF708FF00:
      Serial.println("left");
      break;
    case 0xE31CFF00:
      Serial.println("stop");
      break;
    case 0xBA45FF00:
      Serial.println("rainbow");
      break;
    case 0xB946FF00:
      Serial.println("police");
      break;
  }
}

void loop()
{
  if (irrecv.decode())
  {
    translateIR();
    irrecv.resume();
  }
}
