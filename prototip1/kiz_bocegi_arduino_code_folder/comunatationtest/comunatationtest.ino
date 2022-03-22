String okunan;

void setup() {
  Serial.begin(9600); 
}
 
void loop() {
  
  okunan = analogRead(A1); 
  Serial.print("A1 pininden okunan deger: ");
  Serial.println(okunan);
}