
import httpx
import json
from book import Kitap, e_kitap, sesli_kitap, fiziki_kitap


# In[13]:


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
       

    def save_books(self): #kitapları json dosyasına kayıt eder
        with open(self.dosya_adi, "w", encoding="utf-8") as dosya:
            json.dump([self.kitap_to_dict(k) for k in self._kitaplar], dosya, indent=4, ensure_ascii=False)

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

    def add_book(self,kitap_turu, isbn): 
        parametre = {"isbn": isbn} #API'ye GET parametresi olarak İSBN gönderlmesini sağlar
        
        # ISBN'nin sadece rakamlardaan oluştuğundan emin olunur
        if not isbn.isdigit():
            print("Hata: ISBN sadece rakamlardan oluşmalıdır!")
            return

        # ISBN ve tür kontrolü yapar, aynı İSBN ve türde birden fazla kitap eklenmesini engeller
        for mevcut in self._kitaplar:
            if mevcut.isbn == isbn:
                if (kitap_turu == "e_kitap" and isinstance(mevcut, e_kitap)) or \
                   (kitap_turu == "sesli_kitap" and isinstance(mevcut, sesli_kitap)) or \
                   (kitap_turu == "fiziki_kitap" and isinstance(mevcut, fiziki_kitap)):
                    print(f"Hata: Bu ISBN numarası ({isbn}) ile aynı türde kitap zaten var!")
                    return
        try:
            response = httpx.get(OPEN_LIBRARY_URL, params=parametre)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"API hatası: {e.response.status_code}")
            return
        except httpx.RequestError as e:
            print(f"İstek hatası: {e}")
            return

        data = response.json() #API'den gelen bilgileri json sözlüğüne aktarıyor
        docs = data.get("docs", [])
        if not docs:      
            print("Kitap bulunamadı.")
            return

        # Yayın tarihine göre en yeniden eskiye sıralama yapıyor
        docs = [d for d in docs if "first_publish_year" in d]
        docs.sort(key=lambda x: x["first_publish_year"], reverse=True) 

         # Kullanıcıya seçenekleri göster 
        print("Bulunan kitaplar:")
        for i, kitap_info in enumerate(docs[:10], 1):  #sadece ilk 10 kitabı gösteriyor
            kitap_adi = kitap_info.get("title")
            yazar = kitap_info.get("author_name", ["Bilinmiyor"])[0]
            yil = kitap_info.get("first_publish_year", "Yıl yok")
            print(f"{i}. {kitap_adi} - {yazar} ({yil})")

        secim = input("Eklemek istediğiniz kitabın sıra numarasını girin: ")
        try:
            secim = int(secim) - 1
            if 0 <= secim < len(docs[:10]):
                secilen = docs[secim]
        except (ValueError, IndexError):
            print("Geçersiz seçim.")
            return

        kitap_adi = secilen.get("title")
        yazar = secilen.get("author_name", ["Bilinmiyor"])[0]
            
        kitap= None
        #Kitabın türüne göre sayfa sayısı, dosya formatı ve ses süresi bilgilerini otomatik alıyor 
        if kitap_turu == "fiziki_kitap":
            sayfa_sayisi = input("Sayfa sayısını girin: ")
            kitap = fiziki_kitap(kitap_adi, yazar, isbn, int(sayfa_sayisi))
        elif kitap_turu == "e_kitap":
            dosya_formati = input("Dosya formatını girin: ")
            kitap = e_kitap(kitap_adi, yazar, isbn, dosya_formati)
        elif kitap_turu == "sesli_kitap":
            ses_süresi = input("Ses süresini girin (dakika): ")
            kitap = sesli_kitap(kitap_adi, yazar, isbn, int(ses_süresi))
        else:
            print("Geçersiz kitap türü.")
            return

        #Küyüphaneye eklelme ve kayıt işlemleri yapılır
        self._kitaplar.append(kitap)
        self.save_books()
        print(f"{kitap.kitap_adi} kitaplığa eklendi.")
        
    def remove_book(self,isbn): #kitapları siler
        eslesen_kitaplar = [k for k in self._kitaplar if k.isbn == isbn]
        if not eslesen_kitaplar:
            print("Bu ISBN numarasına ait kitap bulunamadı.")
            return
      
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

    def list_books(self): #tüm kitapları listeler
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

    #İSBN numarası ile ödünç alınacak kitabı arar 
    def odunc_al(self, isbn):
        kitap = self.find_book(isbn)
        if not kitap:
            raise ValueError ("Bu İSBN numarasına ait kitap bulunamadı")

        if not isinstance(kitap, fiziki_kitap):
            raise ValueError("Sadece fiziki kitaplar ödünç alınabilir")

        #Kitabın ödünç alınma durumunun kontrolü
        if kitap.odunc_alınmıs:
            raise ValueError("Bu kitap zaten ödünç alınmış")

        kitap.odunc_alınmıs= True
        self.save_books()


     #İSBN numarassına göre iade işlemini yapar
    def iade_et(self, isbn):
        kitap = self.find_book(isbn)
        if not kitap:
            raise ValueError ("Bu İSBN numarasına ait kitap bulunmadı")
        if not isinstance(kitap, fiziki_kitap):
            raise ValueError("Bu kitap zaten kütüphanede")

        kitap.odunc_alınmıs= False
        self.save_books()



