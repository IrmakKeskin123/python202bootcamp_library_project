##KÜTÜPHANE YÖNETİMİ SİSTEMİ
Bu proje, Python'da Nesne Yönelimli Programlama (OOP), harici bir API entegrasyonu ve FastAPI kullanarak geliştirilmiş üç aşamalı bir kütüphane yönetim sistemidir. Uygulama, hem komut satırı hem de web API'si üzerinden kitapları yönetmenizi sağlar.
#Proje aşamaları:
  1.Türüne göre(e-kitap, sesli kitap, fiziksel kitap) ekleme, silme(İSBN numarası ile), listeleme, arama(İSBN), ödünç alma ve iade (fiziksel kitaplara özgü) işlemlerini 
   komut satısı üzerinden yapma imkanı verir.
  2.Kitap ekleme kısmı harici bir API (OPEN LİBRARY API) ile zenginleştirerek kitap ekleme kısmında kullanıcıdan sadece kitapın İSBN numarasını manuel olarak alır, kitap 
   adı, yazar ve basım tarihi bilgisini API üzerinden çekerek basım tarihlerine göre en yeniden eskiye doğru en fazla 10 kitap olacak şekilde listeler ve kullanıcıdan 
   sıralanan kitaplardan birini seçmesi istenir.
  3. Proje FAST API ile zenginleştirilerek önceki aşamalarda komut satırı üzerinden yapılan işlemler web arayüzünde yapılır hale getirilmiştir.

#FAST API kurulumu
  Repoyu link ile klonlayabilirsiniz:
  Proje gereksinimleri için 'pip install -r requirements.txt'
  1 ve 2. aşama main_1_asama ve main_2_asama adlı dosyaların komut satırları ile çalıştırılabilir.
  FAST API için terminalde 'uvicorn api:app --reload' ile başlattıktan sonra tarayıcıdan **http://127.0.0.1:8000/docs** adresine giriş yapılmalıdır.

#API dökümantasyonu
  Authorize kısmına **SECRET_API_KEY_12345** anahtarı ile giriş yapılır.
  <img width="920" height="479" alt="Ekran görüntüsü 2025-08-18 220808" src="https://github.com/user-attachments/assets/1135917b-4fc1-4fa7-951a-ff03e06e079e" />

#Endpointler

<img width="912" height="463" alt="Ekran görüntüsü 2025-08-18 220847" src="https://github.com/user-attachments/assets/3a4dde0c-639b-4410-855b-f53fa94827f4" />

  GET /
     API'nin durumunu kontrol eder.
                  {
                      "message": "FastAPI Library Manegement System"
                   }

   GET /books 
        Kütüphanedeki tüm kitapların listesini döndürür.
                [
                    {
                      "kitap_adi": "Harry Potter and the Philosopher's Stone",
                      "yazar": "J. K. Rowling",
                      "isbn": "9781408855652",
                      "kitap_turu": "e_kitap",
                      "sayfa_sayisi": null,
                      "dosya_formati": "PDF",
                      "ses_süresi": null,
                      "odunc_alınmıs": null
                    }
                  ]

     <img width="877" height="380" alt="Ekran görüntüsü 2025-08-18 220917" src="https://github.com/user-attachments/assets/f00e6be8-b02c-42b7-bd49-c8852ac62247" />


       
   POST /books
       Verilen ISBN numarasıyla Open Library API'den kitap bilgilerini çeker ve kütüphaneye ekler.
                   {
                    "isbn": "9780451524935",
                    "kitap_turu": "fiziki_kitap",
                    "sayfa_sayisi": 326
                  }

  DELETE /books/{isbn}
        Belirtilen ISBN numarasına sahip kitabı kütüphaneden siler.
        Başarılı olursa 204 No Content döndürür.

  PATCH /books/{isbn}/borrow
        İSBN numarası verilmiş fiziki kitabı ödünç alınmış olarak işaretler.
                   {
                      "kitap_adi": "Nineteen Eighty-Four",
                      "yazar": "George Orwell",
                      "isbn": "9780451524935",
                      "sayfa_sayisi": 326,
                      "odunc_alinmis": true
                  }
   
  PATCH /books/{isbn}/return
       Ödünç alınan bir fiziki kitabı İSBN numarası ile iade edilmiş olarak işaretler.
                 {
                      "kitap_adi": "Nineteen Eighty-Four",
                      "yazar": "George Orwell",
                      "isbn": "9780451524935",
                      "sayfa_sayisi": 326,
                      "odunc_alinmis": false
                  }






        



    

 
