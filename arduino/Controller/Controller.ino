#include <IRremote.hpp>

#define IR_RECEIVE_PIN      2

uint32_t last_decodedRawData = 0;

void setup() {
  Serial.begin(9600);
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);
}

void translateIR() 
{
  if (IrReceiver.decodedIRData.flags)
  {
    //set the current decodedRawData to the last decodedRawData
    IrReceiver.decodedIRData.decodedRawData = last_decodedRawData;
  }
  else
  {
    Serial.print("IR code: 0x");
    Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);
  }

  switch (IrReceiver.decodedIRData.decodedRawData)
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
  if (IrReceiver.decode())
  {
    translateIR();
    IrReceiver.resume();
  }
}
