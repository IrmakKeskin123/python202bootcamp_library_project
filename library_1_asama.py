


import json
from book import Kitap, e_kitap, sesli_kitap, fiziki_kitap





class Kütüphane:
    def __init__(self, dosya_adi="kutuphane.json"):
        self.dosya_adi= dosya_adi
        self._kitaplar= []
        self.load_books()
        
   #JSON dosyasındaki kitapları yükleyecek fonksiyon oluşturulur
    def load_books(self):
        try: 
            with open(self.dosya_adi, "r" ,encoding="utf-8")as dosya:
                veri=json.load(dosya)
                self._kitaplar= []
                for k in veri:
                    tur= k.get("tur")
                    if tur=="e_kitap":
                        kitap= e_kitap(k["kitap_adi"], k["yazar"], k["isbn"], k["dosya_formati"])
                    elif tur=="sesli_kitap":
                        kitap= sesli_kitap(k["kitap_adi"], k["yazar"], k["isbn"], k["ses_süresi"])
                    elif tur=="fiziki_kitap":
                        kitap= fiziki_kitap(k["kitap_adi"], k["yazar"], k["isbn"], k["sayfa_sayisi"])
                        kitap.odunc_alınmıs= k.get("odunc_alınmıs", False)
                    else:
                        kitap= Kitap(k["kitap_adi"], k["yazar"], k["isbn"])
                    self._kitaplar.append(kitap)
        except (FileNotFoundError, json.JSONDecodeError):
            self._kitaplar= []
       
       #Kitapları JSON dosyasına kayıt eden fonksiyon oluşturulur
    def save_books(self): 
        with open(self.dosya_adi, "w", encoding="utf-8") as dosya:
            json.dump([self.kitap_to_dict(k) for k in self._kitaplar], dosya, indent=4, ensure_ascii=False)

     #Kütüphane sınıfındaki kitap nesnelerini JSON formatında saklanabilen bir şekile dönüştürür 
    def kitap_to_dict(self, kitap):
        veri= {
            "kitap_adi": kitap.kitap_adi,
            "yazar": kitap.yazar,
            "isbn": kitap.isbn

        }
        if isinstance(kitap,e_kitap):
            veri["tur"]= "e_kitap"
            veri["dosya_formati"]= kitap.dosya_formati
        elif isinstance(kitap,sesli_kitap):
            veri["tur"] = "sesli_kitap"
            veri["ses_süresi"]= kitap.ses_süresi
        elif isinstance(kitap,fiziki_kitap):
            veri["tur"]= "fiziki_kitap"
            veri["sayfa_sayisi"]= kitap.sayfa_sayisi
            veri["odunc_alınmıs"]= kitap.odunc_alınmıs
        else:
            veri["tur"]="kitap"
        return veri
        
      #JSON dosyasına kitap ekleme fonsiyonu oluşturulur
    def add_book(self, kitap): 
         # ISBN ve tür kontrolü yapar, aynı İSBN ve türde birden fazla kitap eklenmesini engeller
        for mevcut in self._kitaplar:
            if mevcut.isbn == kitap.isbn and type(mevcut) == type(kitap):
                print(f"Hata: Bu ISBN numarası ({kitap.isbn}) ile aynı türde kitap zaten var!")
                return

            # ISBN'nin sadece rakamlardaan oluştuğundan emin olunur
        if not kitap.isbn.isdigit():
            print("Hata: ISBN sadece rakamlardan oluşmalıdır!")
            return
            
        self._kitaplar.append(kitap)
        self.save_books()
        print("Kitap başarıyla eklendi.")
        
    #Kitapları JSON dosyasından İSBN numarası ile siler
    def remove_book(self,isbn): 
        eslesen_kitaplar = [k for k in self._kitaplar if k.isbn == isbn]
        if not eslesen_kitaplar:
            print("Bu ISBN numarasına ait kitap bulunamadı.")
            return
      #Aynı İSBN ile farklı türlerde eklenmiş kitap olup olmadığını kontrol eder
     #Aynı İSBN ile birden fazla türde kitap varsa hangi türdeki kitabı silmek istediğimizi sorar
        if len(eslesen_kitaplar) == 1:
            self._kitaplar.remove(eslesen_kitaplar[0])
            print("Kitap silindi.")
        else:
            print("Bu ISBN numarasıyla birden fazla türde kitap var. Silmek istediğiniz türü seçin:")
            for i, kitap in enumerate(eslesen_kitaplar, start=1):
                tur_adi = type(kitap).__name__
                print(f"{i}. {tur_adi} - {kitap.kitap_adi}")
            secim = input("Seçim: ")
            try:
                secim_index = int(secim) - 1
                secilen_kitap = eslesen_kitaplar[secim_index]
                self._kitaplar.remove(secilen_kitap)
                print(f"{type(secilen_kitap).__name__} türündeki kitap silindi.")
            except (ValueError, IndexError): #Sayı yerine harf girilirse veya listede olmayan bir İSBN girilirse hata mesajı verir
                print("Geçersiz seçim, silme işlemi iptal edildi.")
                return
        self.save_books()

    #Tüm kitapları listeler
    def list_books(self): 
        return self._kitaplar

     #İSBN numarası ile kitap arar
    def find_book(self, isbn, kitap_turu=None): 
        for kitap in self._kitaplar:
            if kitap.isbn==isbn:
                if kitap_turu and kitap.__class__.__name__ == kitap_turu:
                    return kitap
                if not kitap_turu and isinstance(kitap, fiziki_kitap):
                    return kitap

        for kitap in self._kitaplar:
            if kitap.isbn == isbn:
                return kitap
        return None


    #İSBN numarası ile ödünç alınacak kitabı arar 
    def odunc_al(self, isbn):
        kitap = self.find_book(isbn)
        if not kitap:
            raise ValueError("Bu ISBN numarasına ait kitap kütüphanede mevcut değil.")
        if not isinstance(kitap, fiziki_kitap):
            raise ValueError("Bu kitap fiziki bir kitap değil, ödünç alınamaz.")
        if getattr(kitap, "odunc_alınmıs", False):  # Kitap zaten ödünç alınmış mı kontrolü yap
            raise ValueError("Bu kitap zaten ödünç alınmış.")

        kitap.odunc_alınmıs = True  # ödünç alındı olarak işaretle
        self.save_books()
    
     #İSBN numarassına göre iade işlemini yapar
    def iade_et(self, isbn):
        kitap = self.find_book(isbn)
        if not kitap or not isinstance(kitap, fiziki_kitap):
            raise ValueError("Bu ISBN numarasına ait fiziki kitap bulunamadı.")
        try:
            kitap.iade()
            self.save_books()
        except ValueError as e:
            raise e

                                    

