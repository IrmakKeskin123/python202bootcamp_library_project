
import httpx
import json
from book import Kitap, e_kitap, sesli_kitap, fiziki_kitap





OPEN_LIBRARY_URL="https://openlibrary.org/search.json"

class Kütüphane:
    def __init__(self, dosya_adi="kutuphane.json"):
        self.dosya_adi= dosya_adi
        self._kitaplar= []
        self.load_books()

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
       

    def save_books(self): 
        print(f"Kitaplar '{self.dosya_adi}' dosyasına kaydediliyor...")
        try:
            with open(self.dosya_adi, "w", encoding="utf-8") as dosya:
                json.dump([self.kitap_to_dict(k) for k in self._kitaplar], dosya, indent=4, ensure_ascii=False)
            print("Kaydedildi!")
        except Exception as e:
            print(f"Hata: Dosya kaydı başarısız oldu - {e}")
                

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

    def add_book(self, isbn, kitap_turu, sayfa_sayisi=None, dosya_formati=None, ses_süresi=None): 
        parametre = {"isbn": isbn} 
        
        if not isbn.isdigit():
            raise ValueError("Hata: ISBN sadece rakamlardan oluşmalıdır!")

        for mevcut in self._kitaplar:
            if mevcut.isbn == isbn:
                if (kitap_turu == "e_kitap" and isinstance(mevcut, e_kitap)) or \
                   (kitap_turu == "sesli_kitap" and isinstance(mevcut, sesli_kitap)) or \
                   (kitap_turu == "fiziki_kitap" and isinstance(mevcut, fiziki_kitap)):
                    raise ValueError(f"Bu ISBN numarası ({isbn}) ile aynı türde kitap zaten var!")
        try:
            response = httpx.get(OPEN_LIBRARY_URL, params=parametre)
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise ValueError(f"API hatası: {response.status_code}")
        except httpx.RequestError:
            raise ValueError("İstek hatası: API'ye bağlanılamıyor")

            

        data = response.json() 
        print(f"Open Library API'den gelen veri: {data}")
        docs = data.get("docs", [])
        if not docs:      
            raise ValueError("Kitap bulunamadı.")

        kitap_adi = docs[0].get("title", "Ad Bilinmiyor")
        yazar = docs[0].get("author_name", ["Yazar Bilinmiyor"])[0]

        kitap= None
        if kitap_turu == "fiziki_kitap":
            kitap = fiziki_kitap(kitap_adi, yazar, isbn, sayfa_sayisi)
        elif kitap_turu == "e_kitap":
            kitap = e_kitap(kitap_adi, yazar, isbn, dosya_formati)
        elif kitap_turu == "sesli_kitap":
            kitap = sesli_kitap(kitap_adi, yazar, isbn, ses_süresi)
        else:
            raise ValueError("Geçersiz kitap türü.")

        self._kitaplar.append(kitap)
        self.save_books()
        return kitap

    def remove_book(self,isbn):
        self._kitaplar=[k for k in self._kitaplar if k.isbn!= isbn]
        self.save_books()

    def list_books(self):
        return self._kitaplar

    def find_book(self, isbn,kitap_turu=None):
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


    def odunc_al(self, isbn):
        kitap = self.find_book(isbn)
        if not kitap:
            raise ValueError ("Bu İSBN numarasına ait kitap bulunamadı")

        if not isinstance(kitap, fiziki_kitap):
            raise ValueError("Sadece fiziki kitaplar ödünç alınabilir")

        if kitap.odunc_alınmıs:
            raise ValueError("Bu kitap zaten ödünç alınmış")

        kitap.odunc_alınmıs= True
        self.save_books()

    def iade_et(self, isbn):
        kitap = self.find_book(isbn)
        if not kitap:
            raise ValueError ("Bu İSBN numarasına ait kitap bulunmadı")
        if not isinstance(kitap, fiziki_kitap):
            raise ValueError("Bu kitap zaten kütüphanede")

        kitap.odunc_alınmıs= False
        self.save_books()



