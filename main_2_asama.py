#!/usr/bin/env python
# coding: utf-8

# In[1]:


kullanici_adi= input("Kullanıcı Adı:")
sifre= input("Şifre: ")
if kullanici_adi== "admin" and sifre== "1234":
    print("Giriş Başarılı")
else:
    print("Hatalı Giriş!")
    exit()     


# In[1]:


from library_2_asama import Kütüphane
from book import e_kitap, sesli_kitap, fiziki_kitap


# In[2]:


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
            tur_secimi= input("Seçiminiz: ")
            if tur_secimi== "1":
                kitap_turu= "e_kitap"

            elif tur_secimi=="2":
                kitap_turu= "sesli_kitap"

            elif tur_secimi== "3":
                kitap_turu= "fiziki_kitap"
                
            else:
                print("Hatalı Giriş Yaptınız!")
                continue

            isbn=input("Kitabın İSBN numarasını girin:")
            kütüphane.add_book(kitap_turu, isbn)
                
        
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


# In[ ]:


get_ipython().system('jupyter nbconvert --to python main_1_asama.ipynb')


# In[ ]:




