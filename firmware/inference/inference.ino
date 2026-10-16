// Edryn Clyde Fernandez — ESP32 live on-device inference.
// Uses GUVA-S12SD UV ADC pin 34 and TSL2591 IR-only channel (I2C 21/22).
// Generate model.h with scripts/train_model.py then generate_model_header.py.
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2591.h>
#include "model.h"
Adafruit_TSL2591 tsl(2591);
float uv=0, ir=0;
bool ready=false;
unsigned long prev=0;
const float ALPHA=.2f;
int cell(float raw,float lo,float hi) {
  if (hi <= lo) return 0;
  int i=(int)floorf(((log1pf(fmaxf(raw,0))-lo)/(hi-lo))*GRID_N);
  return constrain(i,0,GRID_N-1);
}
void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  Wire.begin(21,22);
  if (!tsl.begin()) {Serial.println("# TSL2591 missing");while(true)delay(1000);}
  tsl.setGain(TSL2591_GAIN_MED);
  tsl.setTiming(TSL2591_INTEGRATIONTIME_100MS);
  Serial.println("# time_ms,uv_sensor,IR_sensor,prediction,lookup_us");
}
void loop() {
  if(millis()-prev<100)return;
  prev=millis();
  int rawUV=analogRead(34);
  uint32_t lum=tsl.getFullLuminosity();
  uint16_t rawIR=lum>>16;
  if(rawIR==0xffff || (uint16_t)lum==0xffff) return;
  if(!ready){uv=rawUV;ir=rawIR;ready=true;}
  else {uv=ALPHA*rawUV+(1-ALPHA)*uv;ir=ALPHA*rawIR+(1-ALPHA)*ir;}
  unsigned long t=micros();
  int col=cell(uv,SCALE_BOUNDS[0],SCALE_BOUNDS[1]);
  int row=cell(ir,SCALE_BOUNDS[2],SCALE_BOUNDS[3]);
  int best=-1;uint8_t high=0;
  for(int c=0;c<NUM_CLASSES;c++) {
    uint8_t val=pgm_read_byte(&CLASS_TABLE[c][row][col]);
    if(best<0||val>high){best=c;high=val;}
  }
  const char* name=high/255.0f<REJECT_TAU?"UNKNOWN":CLASS_NAMES[best];
  unsigned long elapsed=micros()-t;
  Serial.printf("%lu,%.3f,%.3f,%s,%lu\n",millis(),uv,ir,name,elapsed);
}
