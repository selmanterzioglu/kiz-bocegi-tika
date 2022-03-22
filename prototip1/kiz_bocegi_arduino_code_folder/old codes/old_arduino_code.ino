  #define dirPin 10
  #define stepPin 9

  int a1;
  int a2;
  
  int trigPinOn = 4;  //
  int echoPinOn = 5;  //  >  On sensor
  long sureOn;        //
  long uzaklikOn;     //


  int trigPinArka = 7;  //
  int echoPinArka = 6;  //  >  Arka sensor
  long sureArka;        //
  long uzaklikArka;     //

void setup() {

  int a1=0;
  int a2=0;
  
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(trigPinOn, OUTPUT);
  pinMode(trigPinArka, OUTPUT);
  pinMode(echoPinOn, INPUT);
  pinMode(echoPinArka, INPUT);
}

void ileri(){
  digitalWrite(dirPin, LOW);
  for (int i = 0;; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(3000);
  }
}
void geri(){
  digitalWrite(dirPin, HIGH);
  for (int i = 0;; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(3000);
  }
}

void loop() {

  digitalWrite(trigPinOn, LOW);         //İlk basta trig pinimizi low durumunda baslatiyoruz
  delayMicroseconds(0.01);                   //5 mikrosaniye bekletiyoruz
  digitalWrite(trigPinOn, HIGH);        //Daha sonra pinimizi, ses dalgasi göndermesi icin calistiriyoruz
  delayMicroseconds(0.02);                  //10 mikrosaniye bekletiyoruz
  digitalWrite(trigPinOn, LOW);         //Trig pinimizi pasif duruma getiriyoruz
  sureOn = pulseIn(echoPinOn, HIGH);  //Gonderilen dalganin geri donmesindeki sureyi olcuyor
  uzaklikOn = sureOn /29.1/2;         //Olctugu sureyi uzakliga ceviriyoruz
  if(uzaklikOn > 100)                   //200 cm ve üzeri tum uzakliklari 200 cm olarak sabitliyoruz
    uzaklikOn = 100;
  Serial.print("Uzaklik On "); 
  Serial.print(uzaklikOn);              //Olctugumuz uzakligi seri port ekranina yazdiriyoruz
  Serial.print(" cm *** "); 

  digitalWrite(trigPinArka, LOW);         //İlk basta trig pinimizi low durumunda baslatiyoruz
  delayMicroseconds(0.01);                   //5 mikrosaniye bekletiyoruz
  digitalWrite(trigPinArka, HIGH);        //Daha sonra pinimizi, ses dalgasi göndermesi icin calistiriyoruz
  delayMicroseconds(0.02);                  //10 mikrosaniye bekletiyoruz
  digitalWrite(trigPinArka, LOW);         //Trig pinimizi pasif duruma getiriyoruz
  sureArka = pulseIn(echoPinArka, HIGH);  //Gonderilen dalganin geri donmesindeki sureyi olcuyor
  uzaklikArka = sureArka /29.1/2;         //Olctugu sureyi uzakliga ceviriyoruz
  if(uzaklikArka > 100)                   //200 cm ve üzeri tum uzakliklari 200 cm olarak sabitliyoruz
    uzaklikArka = 100;
  Serial.print("Uzaklik Arka "); 
  Serial.print(uzaklikArka);              //Olctugumuz uzakligi seri port ekranina yazdiriyoruz
  Serial.print(" cm *** "); 

  if(((uzaklikOn > 0)&&(uzaklikOn <= 5))&&((uzaklikArka == 0)||(uzaklikArka > 5))){
    geri();
  }
  else if(((uzaklikArka > 0)&&(uzaklikArka <= 5))&&((uzaklikOn == 0)||(uzaklikOn > 5))){
    ileri();
  }
  else{
  }
  if(a1 > 0){
    geri();
  }
  else if(a2 > 0){
    ileri();
  }  

  
  
}
