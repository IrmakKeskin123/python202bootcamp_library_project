


from library_1_asama import Kütüphane
from book import e_kitap, sesli_kitap, fiziki_kitap
from pydantic import BaseModel, Field, ValidationError
import os
import json
import pytest





DOSYA_ADI = "test_kutuphane.json"




class PydanticBook(BaseModel):
    kitap_adi: str
    yazar: str
    isbn: str= Field(..., min_length= 10, max_length=13)
    sayfa_sayisi: int|None=None
    dosya_formati: str|None=None
    ses_süresi: int |None=None



# Fixture: Testten önce temiz bir kütüphane oluşturmak için
@pytest.fixture
def kutuphane():
    if os.path.exists(DOSYA_ADI):
        os.remove(DOSYA_ADI)
    return Kütüphane(dosya_adi=DOSYA_ADI)

#Kitap ekleme kısmını test eder
def test_kitap_ekleme():
    k = Kütüphane(dosya_adi=DOSYA_ADI)
    kitap = sesli_kitap("Sesli 1", "Yazar 2", "67890456731", 60)
    k.add_book(kitap)
    assert any(b.isbn == "67890456731" for b in k.list_books())
    
#Kitap silme kısmını test eder
def test_kitap_silme(dosya_adi= DOSYA_ADI):
    k = Kütüphane(dosya_adi="test.json")
    kitap = sesli_kitap("Sesli 3", "Yazar 5", "12345678910", 80)
    k.add_book(kitap)
    k.remove_book("12345678910")
    assert all(b.isbn != "12345678910" for b in k.list_books())
#Geçerli İSBN numarası girilme durumunu test eder
def test_pydantic_gecerli():
    valid = PydanticBook(kitap_adi="Test Kitap", yazar="Yazar", isbn="1234567890", sayfa_sayisi=200)
    assert valid.isbn == "1234567890"
#Geçersiz İSBN numarası girilme durumunu test eder
def test_pydantic_gecersiz():
    with pytest.raises(ValidationError):
        PydanticBook(kitap_adi="Hatalı", yazar="Yazar", isbn="125678", sayfa_sayisi=200)
#Kitap ödünç alma durumları ve hataları test edilir
def test_odunc_alma(kutuphane):
    kitap = fiziki_kitap("Fiziki Kitap", "Yazar 3", "5432102861", 250)
    kutuphane.add_book(kitap)
    kutuphane.odunc_al("5432102861")
    assert any(b.isbn == "5432102861" and b.odunc_alınmıs for b in kutuphane.list_books())

def test_odunc_alma_tekrar_hata(kutuphane):
    kitap = fiziki_kitap("Fiziki Kitap", "Yazar 4", "11111111111", 300)
    kutuphane.add_book(kitap)
    kutuphane.odunc_al("11111111111")
    with pytest.raises(ValueError):
        kutuphane.odunc_al("11111111111")  # Aynı kitap ikinci kez ödünç alınamaz
#Kitap iade etmeyi tercih eder
def test_iade_etme(kutuphane):
    kitap = fiziki_kitap("Fiziki Kitap", "Yazar 5", "2222222222", 150)
    kutuphane.add_book(kitap)
    kutuphane.odunc_al("2222222222")
    kutuphane.iade_et("2222222222")
    assert any(b.isbn == "2222222222" and not b.odunc_alınmıs for b in kutuphane.list_books())









