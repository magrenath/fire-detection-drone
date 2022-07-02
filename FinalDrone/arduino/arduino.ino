#include "Wire.h"                                           // This library allows you to communicate with I2C devices.
#include <Servo.h>


String GamePad_Commands;
const int MPU_ADDR=0x68;                                    // I2C address of the MPU-6050. If AD0 pin is set to HIGH, the I2C address will be 0x69.
int16_t accelerometer_x, accelerometer_y, accelerometer_z;  // variables for accelerometer raw data
int16_t gyro_x, gyro_y, gyro_z;                             // variables for gyro raw data

Servo L_F_prop;
Servo L_B_prop;
Servo R_F_prop;
Servo R_B_prop;


//define esc
#define lf 9 //left front motor
#define lb 10 //left back motor
#define rf 11 //right front motor 
#define rb 6 //right back motor
// define LEDs
#define LED_LB 7 // LED left back
#define LED_RB 2 // LED right back
#define LED_RF 3 // LED right front
#define LED_LF 4 // LED left front

// Command variables
//Variaveis de tempo
float elapsedTime, time, timePrev;

//Variaveis para o giroscopio
int gyro_error=0;                         //We use this variable to only calculate once the gyro data error
float Gyr_rawX, Gyr_rawY, Gyr_rawZ;       //Here we store the raw data read 
float Gyro_angle_x, Gyro_angle_y, Gyro_angle_z;         //Here we store the angle value obtained with Gyro data
float Gyro_raw_error_x, Gyro_raw_error_y, Gyro_raw_error_z; //Here we store the initial gyro data error

//Variaveis para o acelerometro
int acc_error=0;                            //We use this variable to only calculate once the Acc data error
float rad_to_deg = 180/3.141592654;         //This value is for pasing from radians to degrees values
float Acc_rawX, Acc_rawY, Acc_rawZ;         //Here we store the raw data read 
float Acc_angle_x, Acc_angle_y, Acc_angle_z;             //Here we store the angle value obtained with Acc data
float Acc_angle_error_x, Acc_angle_error_y, Acc_angle_error_z; //Here we store the initial Acc data error

float Total_angle_x, Total_angle_y, Total_angle_z;


//Variaveis para a velocidade dos motores
int MAX_SIGNAL = 2000; //Sinal máximo para o motor
int MIN_SIGNAL = 1000; //Sinal minimo para o motor
int MAX_Speed = 85; //Percentagem máxima da velocidade máxima do motor
int MIN_Speed = 10;
int lf_speed = 1000;
int rf_speed = 1000;
int lb_speed = 1000;
int rb_speed = 1000;
int Max_speed_val = 1500;
int Min_speed_val = 1500;
  // input
float input_THROTTLE = 0;
float input_YAW = 0;
float input_ROLL = 0;
float input_PITCH = 0;
  // output
float throttle = 1000;
float yaw = 0;
float pitch = 0;
float roll = 0;

//PID
//////////////////////////////PID FOR ROLL///////////////////////////
float ROLL, roll_error, roll_previous_error;
float roll_pid_p=0;
float roll_pid_i=0;
float roll_pid_d=0;
///////////////////////////////ROLL PID CONSTANTS////////////////////
double roll_kp=-10;//3.55
double roll_ki=0;//0.003
double roll_kd=0;//2.05
//////////////////////////////PID FOR PITCH//////////////////////////
float PITCH, pitch_error, pitch_previous_error;
float pitch_pid_p=0;
float pitch_pid_i=0;
float pitch_pid_d=0;
///////////////////////////////PITCH PID CONSTANTS///////////////////
double pitch_kp=-10;//3.55
double pitch_ki=0;//0.003
double pitch_kd=0;//2.05
float pitch_desired_angle = 0;     //This is the angle in which 

char tmp_str[7];                                            // temporary variable used in convert function
char* convert_int16_to_str(int16_t i) {                     // converts int16 to string. Moreover, resulting strings will have the same length in the debug monitor.
  sprintf(tmp_str, "%6d", i);
  return tmp_str;
}

void setup() {
  Max_speed_val = 1850;
  Min_speed_val = MIN_SIGNAL + MIN_SIGNAL * MIN_Speed / 100;

  //Inicio de comunicação serial
  Serial.begin(9600);
  pinMode(LED_LB, OUTPUT);
  pinMode(LED_RB, OUTPUT);
  pinMode(LED_RF, OUTPUT);
  pinMode(LED_LF, OUTPUT);
  digitalWrite(LED_LB, LOW);
  digitalWrite(LED_RB, LOW);
  digitalWrite(LED_RF, LOW);
  digitalWrite(LED_LF, LOW);

  // Associar pinos aos ESC e evitar que estes entrem no modo de alteração de definições
  L_F_prop.attach(lf);
  L_F_prop.writeMicroseconds(MIN_SIGNAL);
  delay(10);
  L_B_prop.attach(lb);
  L_B_prop.writeMicroseconds(MIN_SIGNAL);
  delay(10);
  R_F_prop.attach(rf);
  R_F_prop.writeMicroseconds(MIN_SIGNAL);
  delay(10);
  R_B_prop.attach(rb);
  R_B_prop.writeMicroseconds(MIN_SIGNAL);
  delay(10);
  delay(7500); //Dar tempo para os ESC se configurarem
  
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR);                         // Begins a transmission to the I2C slave (GY-521 board)
  Wire.write(0x6B);                                         // PWR_MGMT_1 register
  Wire.write(0);                                            // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
}

void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);                                         // starting with register 0x3B (ACCEL_XOUT_H) [MPU-6000 and MPU-6050 Register Map and Descriptions Revision 4.2, p.40]
  Wire.endTransmission(false);                              // the parameter indicates that the Arduino will send a restart. As a result, the connection is kept active.
  Wire.requestFrom(MPU_ADDR, 7*2, true);                    // request a total of 7*2=14 registers
  
  // "Wire.read()<<8 | Wire.read();" means two registers are read and stored in the same variable
  accelerometer_x = Wire.read()<<8 | Wire.read();     // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
  accelerometer_y = Wire.read()<<8 | Wire.read();     // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
  accelerometer_z = Wire.read()<<8 | Wire.read();     // reading registers: 0x3F (ACCEL_ZOUT_H) and 0x40 (ACCEL_ZOUT_L)
  gyro_x = Wire.read()<<8 | Wire.read();              // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)
  gyro_y = Wire.read()<<8 | Wire.read();              // reading registers: 0x45 (GYRO_YOUT_H) and 0x46 (GYRO_YOUT_L)
  gyro_z = Wire.read()<<8 | Wire.read();              // reading registers: 0x47 (GYRO_ZOUT_H) and 0x48 (GYRO_ZOUT_L)
  
  // Serial communication to send data to Rasberry Pi
  Serial.print("aX = "); Serial.print(convert_int16_to_str(accelerometer_x));
  Serial.print(" | aY ="); Serial.print(convert_int16_to_str(accelerometer_y));
  Serial.print(" | aZ ="); Serial.print(convert_int16_to_str(accelerometer_z));
  Serial.print(" | gX ="); Serial.print(convert_int16_to_str(gyro_x));
  Serial.print(" | gY ="); Serial.print(convert_int16_to_str(gyro_y));
  Serial.print(" | gZ ="); Serial.print(convert_int16_to_str(gyro_z));
  Serial.print(" |Th="); Serial.print(input_THROTTLE);
  Serial.print(" |Ya="); Serial.print(input_YAW);
  Serial.print(" |Pt="); Serial.print(input_PITCH);
  Serial.print(" |RL="); Serial.print(input_ROLL);
  Serial.println();

  
  // Serial communication to receive commands
  if (Serial.available()){
    GamePad_Commands = Serial.readStringUntil('\n');
    String strArr[4];
    int stringStart = 0;
    int arrayIndex = 0;
    for (int i=0; i < GamePad_Commands.length(); i++){
      if(GamePad_Commands.charAt(i) == ','){
        strArr[arrayIndex] = "";
        strArr[arrayIndex] = GamePad_Commands.substring(stringStart, i);
        stringStart = (i+1);
        arrayIndex++;
      }
    }
    //Put values from the array into the variables.
    String v1 = strArr[0];
    String v2 = strArr[1];
    String v3 = strArr[2];
    String v4 = strArr[3];
    //Convert string to int if you need it.
    int aux_THROTTLE = v1.toInt();
    int aux_YAW = v2.toInt();
    int aux_PITCH = v3.toInt();
    int aux_ROLL = v4.toInt();
    input_THROTTLE = map(aux_THROTTLE,0,100,1000,2000);
    input_YAW = map(aux_YAW,-100,100,-50,50);
    input_PITCH = map(aux_PITCH,-100,100,-30,30);
    input_ROLL = map(aux_ROLL,-100,100,-30,30);
    
  }
    
  // LED conditions
  if (accelerometer_x < 1000 && accelerometer_y < -5000) {
    digitalWrite(LED_LB, HIGH);
    digitalWrite(LED_RB, HIGH);
    digitalWrite(LED_RF, LOW);
    digitalWrite(LED_LF, LOW);
  } else if (accelerometer_x < 1000 && accelerometer_y > 5000) {
    digitalWrite(LED_LB, LOW);
    digitalWrite(LED_RB, LOW);
    digitalWrite(LED_RF, HIGH);
    digitalWrite(LED_LF, HIGH);
  } else if (accelerometer_x > 5000 && accelerometer_y < 1000) {
    digitalWrite(LED_LB, LOW);
    digitalWrite(LED_RB, HIGH);
    digitalWrite(LED_RF, HIGH);
    digitalWrite(LED_LF, LOW);
  } else if (accelerometer_x < -5000 && accelerometer_y < 1000) {
    digitalWrite(LED_LB, HIGH);
    digitalWrite(LED_RB, LOW);
    digitalWrite(LED_RF, LOW);
    digitalWrite(LED_LF, HIGH);
  } else {
    digitalWrite(LED_LB, LOW);
    digitalWrite(LED_RB, LOW);
    digitalWrite(LED_RF, LOW);
    digitalWrite(LED_LF, LOW);
  }
  
  // delay
  delay(100);
  //Comandos de yaw, pitch e roll podem ir de -1000 a 1000
  //Limitar comandos para evitar movimentos bruscos
  if(throttle < 1000){throttle = 1000;}
  if(throttle > 2000){throttle = 2000;}
  if(yaw < -400){yaw = -400;}
  if(yaw > 400){yaw = 400;}
  if(pitch < -400){pitch = -400;}
  if(pitch > 400){pitch = 400;}
  if(roll < -400){roll = -400;}
  if(roll > 400){roll = 400;}
  if(-3 < roll_error <3)
  {
    roll_pid_i = roll_pid_i+(roll_ki*roll_error);  
  }
  if(-3 < pitch_error <3)
  {
    pitch_pid_i = pitch_pid_i+(pitch_ki*pitch_error);  
  }
/*The last part is the derivate. The derivate acts upon the speed of the error.
As we know the speed is the amount of error that produced in a certain amount of
time divided by that time. For taht we will use a variable called previous_error.
We substract that value from the actual error and divide all by the elapsed time. 
Finnaly we multiply the result by the derivate constant*/
  roll_pid_d = roll_kd*((roll_error - roll_previous_error)/elapsedTime);
  pitch_pid_d = pitch_kd*((pitch_error - pitch_previous_error)/elapsedTime);
//The final PID values is the sum of each of this 3 parts/
  roll = roll_pid_p + roll_pid_i + roll_pid_d;
  pitch = pitch_pid_p + pitch_pid_i + pitch_pid_d;
  yaw = input_YAW;
  throttle = input_THROTTLE;
 
  //Obter velocidade de cada motor
  lf_speed = throttle + yaw + pitch + roll;
  rf_speed = throttle - yaw + pitch - roll;
  lb_speed = throttle - yaw - pitch + roll;
  rb_speed = throttle + yaw - pitch - roll;

  //Limitar velocidade dos motores
  if (lf_speed > Max_speed_val) {lf_speed = Max_speed_val;}
  if (lf_speed < Min_speed_val) {lf_speed = Min_speed_val;}
  if (rf_speed > Max_speed_val) {rf_speed = Max_speed_val;}
  if (rf_speed < Min_speed_val) {rf_speed = Min_speed_val;}
  if (lb_speed > Max_speed_val) {lb_speed = Max_speed_val;}
  if (lb_speed < Min_speed_val) {lb_speed = Min_speed_val;}
  if (rb_speed > Max_speed_val) {rb_speed = Max_speed_val;}
  if (rb_speed < Min_speed_val) {rb_speed = Min_speed_val;}
}