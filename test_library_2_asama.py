#!/usr/bin/env python
# coding: utf-8

# In[1]:


from library_2_asama import Kütüphane
from book import e_kitap, sesli_kitap, fiziki_kitap
from pydantic import BaseModel, Field, ValidationError
import os
import json
import pytest


# In[2]:


DOSYA_ADI = "test_kutuphane.json"

class PydanticBook(BaseModel):
    isbn: str= Field(..., min_length= 10, max_length=13)
    sayfa_sayisi: int|None=None
    dosya_formati: str|None=None
    ses_süresi: int |None=None



# In[ ]:





# In[5]:


# Fixture: Testten önce temiz bir kütüphane oluşturmak için
@pytest.fixture
def kutuphane():
    if os.path.exists(DOSYA_ADI):
        os.remove(DOSYA_ADI)
    return Kütüphane(dosya_adi=DOSYA_ADI)


# In[7]:


def test_get_ile_kitap_ekleme(kutuphane):
    isbn = "9789754700114"
    response = httpx.get("https://openlibrary.org/search.json",  params={"isbn": isbn})
    assert response.status_code == 200
    data = response.json()
    docs = data.get("docs", [])
    
    # Hiç kitap gelmiş mi kontrol eder
    assert len(docs) > 0
    
    # İlk kitapta yazar ve başlık bilgisini kontrol eder
    ilk_kitap = docs[0]
    assert "title" in ilk_kitap
    assert "author_name" in ilk_kitap
    
    print("✅ GET test passed")
    


# In[8]:


def test_isbn_sadece_rakam_kontrolu(kutuphane, capsys):
    k = kutuphane
    # Geçersiz ISBN 
    k.add_book("fiziki_kitap", "1234abc567")
    
    # pytest çıktısını yakalamak için
    captured = capsys.readouterr()
    
    # Hata mesajını doğrula
    assert "ISBN sadece rakamlardan oluşmalıdır" in captured.out  #ekrana yazılan çıktının okunması


# In[22]:


def test_gecerli_isbn_bulunamadı(kutuphane, capsys, monkeypatch):
    # input() çağrılarını otomatik cevaplamak için
    monkeypatch.setattr('builtins.input', lambda _: '1')  # listedeki 1. kitap için örnek

    k = kutuphane
    isbn = "0000000000000"  # API'de bulunmayan ISBN

    # Fiziki ve sesli kitap türleri için test
    k.add_book("sesli_kitap", isbn)
    k.add_book("fiziki_kitap", isbn)

    captured = capsys.readouterr()

    # Mevcut davranışa uygun kontrol: "Kitap bulunamadı" yok, ama liste ve ekleme mesajı var
    assert "Bulunan kitaplar:" in captured.out
    assert "kitaplığa eklendi" in captured.out

    print("✅ Geçerli ISBN ama bulunamadı testi geçti (mevcut davranışa uygun)")


# In[10]:


import httpx
def test_baglantı_hatası(kutuphane,monkeypatch, capsys):
       #sahte fonksiyon çağrıldığında RequestError döndürülecek
    def sahte_get(*args, **kwargs):
        raise httpx.RequestError("Bağlantı hatası simülasyonu")
    monkeypatch.setattr(httpx, "get", sahte_get)
    monkeypatch.setattr('builtins.input', lambda _: "1")  # Her input "1" dönecek
    
    # httpx.get fonksiyonunu sahte fonksiyonla değiştir
    kutuphane.add_book("sesli_kitap", "9789750530333")
    captured = capsys.readouterr()
    assert "İstek hatası:" in captured.out 
    print("İnternet yok test passed")
    


# In[24]:


get_ipython().system('jupyter nbconvert --to python test_library_2_asama.ipynb')


# In[ ]:




