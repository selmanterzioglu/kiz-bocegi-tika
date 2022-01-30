class Ornek():
    def __init__(self, sayi):
        self.sayi = sayi
        
    def __enter__(self):
        print("İşleme başlanan sayi ", str(self.sayi.deger))
        return self.sayi
    
    def __exit__(self, type, value, traceback):
        print("Sayının son değeri ", str(self.sayi.deger))


class Sayi:
    def __init__(self, deger):
        self.deger = deger
    
    def arttir(self):
        self.deger += 10

sayi = Sayi(5)
with Ornek(sayi):
    sayi.arttir()


with Ornek(Sayi(3)) as sayi:
    sayi.arttir()