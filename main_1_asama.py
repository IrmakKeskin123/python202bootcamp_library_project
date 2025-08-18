


kullanici_adi= input("Kullanıcı Adı:")
sifre= input("Şifre: ")
if kullanici_adi== "admin" and sifre== "1234":
    print("Giriş Başarılı")
else:
    print("Hatalı Giriş!")
    exit() 





from library_1_asama import Kütüphane
from book import e_kitap, sesli_kitap, fiziki_kitap





def menu():
    kütüphane = Kütüphane()
    
    while True:
        print("  Kütüphane Menüsü  ")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Fiziki Kitap Ödünç Al")
        print("6. Fiziki Kitap İade Et")
        print("7. çıkış")
        secim= input("Seçim yapınız")

        if secim=="1":
            print("Kitabı eklemek istediğiniz türü seçiniz")
            print("1. E-Kitap")
            print("2. Sesli Kitap")
            print("3. Fiziksel Kitap")
            kitap_türü= input("Seçiminiz: ")
            if kitap_türü== "1":
                kitap_adi= input("Kitap Adı:")
                yazar= input("Yazar Adı:")
                isbn= input("İSBN Numarası: ")
                dosya_formati= input("Dosya Formatı: ")
                kitap= e_kitap(kitap_adi, yazar, isbn, dosya_formati)
                kütüphane.add_book(kitap)
                
            elif kitap_türü== "2":
                kitap_adi= input("Kitap Adı:")
                yazar= input("Yazar Adı:")
                isbn= input("İSBN Numarası: ")
                ses_süresi= input("Oynatma Süresi (Dakika): ")
                kitap= sesli_kitap(kitap_adi, yazar, isbn, ses_süresi)
                kütüphane.add_book(kitap)
                
            elif kitap_türü== "3":
                kitap_adi= input("Kitap Adı:")
                yazar= input("Yazar Adı:")
                isbn= input("İSBN Numarası: ")
                sayfa_sayisi= input("Sayfa Sayısı: ")
                kitap= fiziki_kitap(kitap_adi, yazar,isbn,  sayfa_sayisi)
                kütüphane.add_book(kitap)
                
            else:
                print("Hatalı Giriş Yaptınız!")
        
        elif secim=="2":
            isbn = input("Silmek istediğiniz kitabın ISBN numarasını girin: ")
            kütüphane.remove_book(isbn)
            

        elif secim=="3":
            kitaplar = kütüphane.list_books()
            if not kitaplar:
                print("Kütüphane Boş.")
            else:
                print("\n--- E-Kitaplar ---")
                for kitap in kitaplar:
                    if isinstance(kitap, e_kitap):
                        print(f"{kitap.kitap_adi} - {kitap.yazar} - ISBN: {kitap.isbn} - Dosya Formatı: {kitap.dosya_formati}")

                print("\n--- Sesli Kitaplar ---")
                for kitap in kitaplar:
                    if isinstance(kitap, sesli_kitap):
                        print(f"{kitap.kitap_adi} - {kitap.yazar} - ISBN: {kitap.isbn} - Oynatma Süresi: {kitap.ses_süresi} dakika")

                print("\n--- Fiziksel Kitaplar ---")
                for kitap in kitaplar:
                    if isinstance(kitap, fiziki_kitap):
                        print(f"{kitap.kitap_adi} - {kitap.yazar} - ISBN: {kitap.isbn} - Sayfa Sayısı: {kitap.sayfa_sayisi}")

        elif secim=="4":
            isbn = input("Aramak istediğiniz kitabın ISBN numarasını girin: ")
            kitap = kütüphane.find_book(isbn)
            if kitap:
                if isinstance(kitap, e_kitap):
                    print(f"Bulundu: {kitap.kitap_adi} - {kitap.yazar} - {kitap.isbn} - Dosya Formatı: {kitap.dosya_formati}")
                elif isinstance(kitap, sesli_kitap):
                    print(f"Bulundu: {kitap.kitap_adi} - {kitap.yazar} - {kitap.isbn} - Oynatma Süresi: {kitap.ses_süresi}")
                elif isinstance(kitap, fiziki_kitap):
                    print(f"Bulundu: {kitap.kitap_adi} - {kitap.yazar} - {kitap.isbn} - Sayfa Sayısı: {kitap.sayfa_sayisi}")
            else:
                print("Bu ISBN numarasına ait kitap bulunamadı.")

        elif secim=="5":
            isbn = input("Ödünç almak istediğiniz fiziki kitabın ISBN numarasını girin: ")
            try:
                kütüphane.odunc_al(isbn)
                kitap = kütüphane.find_book(isbn)
                print(f"'{kitap.kitap_adi}' ödünç alındı.")
            except ValueError as e:
                print("Hata:", e)

        elif secim=="6":
            isbn = input("İade etmek istediğiniz fiziki kitabın ISBN numarasını girin: ")
            try:
                kütüphane.iade_et(isbn)
                kitap = kütüphane.find_book(isbn)
                print(f"'{kitap.kitap_adi}' iade edildi.")
            except ValueError as e:
                print("Hata:", e)
                
        elif secim=="7":
            print("Çıkış Yapılıyor")
            break
        else:
            print("Karşılıksız Seçim")
            
            

menu()






