
 #Kitap adlı sınıf oluşturulur
class Kitap:
    def __init__  (self, kitap_adi:str, yazar:str, isbn:str):
        self.kitap_adi= kitap_adi
        self.yazar= yazar
        self.isbn= isbn
    def __str__(self):
        return f"Kitap Adı: {self.kitap_adi}\nYazar: {self.yazar}\nİSBN Numarası:{self.isbn}"
#Kitap sınıfından miras alan e_kitap, sesli_kitap ve fiziki_kitap sınıfları oluşturulur
class e_kitap(Kitap):
    def __init__ (self,kitap_adi:str, yazar:str, isbn:str, dosya_formati:str):
        super().__init__(kitap_adi, yazar, isbn)
        self.dosya_formati= dosya_formati
    def __str__(self):
        return f"Kitap Adı: {self.kitap_adi}\nYazar: {self.yazar}\nİSBN Numarası:{self.isbn}\nDosya Formatı: {self.dosya_formati}"

class sesli_kitap(Kitap):
    def __init__(self,kitap_adi:str, yazar:str, isbn:str, ses_süresi:int):
        super().__init__(kitap_adi, yazar, isbn)
        self.ses_süresi= ses_süresi
    def __str__(self):
        return f"Kitap Adı: {self.kitap_adi}\nYazar: {self.yazar}\nİSBN Numarası:{self.isbn}\nDosya Süresi: {self.ses_süresi} Dakika"

class fiziki_kitap(Kitap):
    def __init__(self,kitap_adi:str, yazar:str, isbn:str, sayfa_sayisi:int):
        super().__init__(kitap_adi, yazar, isbn)
        self.sayfa_sayisi= sayfa_sayisi
        self.odunc_alınmıs= False
     #Fiziksel kitaplara özgü ödünç alma ve iade fonksiyonları oluşturulur
    def odunc_alma(self):
        if self.odunc_alınmıs:
            print(f"{self.kitap_adi} adlı, yazarı {self.yazar} olan kitap şuan mevcut değil.")
        else:
            self.odunc_alınmıs= True

    def iade(self):
        if not self.odunc_alınmıs:
            print(f"{self.kitap_adi} adlı, yazarı {self.yazar} olan kitap şuan mevcut.")
        else:
            self.odunc_alınmıs= False

    def durum(self):
        return "Mevcut" if not self.odunc_alınmıs else "Mevcut Değil"

    
    def __str__(self):
       return (
            f"Kitap Adı: {self.kitap_adi}\n"
            f"Yazar: {self.yazar}\n"
            f"İSBN Numarası: {self.isbn}\n"
            f"Sayfa Sayısı: {self.sayfa_sayisi}\n"
            f"Durum: {self.durum()}"
        )
        








