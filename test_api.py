import pytest
from fastapi.testclient import TestClient
from fastapi import status
import json
import os
import httpx
from unittest.mock import patch

from api import app, API_KEY, kütüphane as api_kütüphane
from library_3_asama import Kütüphane
from book import fiziki_kitap, e_kitap, sesli_kitap

client = TestClient(app)

@pytest.fixture
def api_key_header():
    return {"X-API-KEY": API_KEY}

@pytest.fixture(autouse=True)
def clean_up_json_file():
    
    with open("test_kutuphane.json", "w", encoding="utf-8") as f:
        json.dump([], f)
    yield
    with open("test_kutuphane.json", "w", encoding="utf-8") as f:
        json.dump([], f)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "FastAPI Library Manegement System"}

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}

def test_add_book(api_key_header, monkeypatch):
 
    test_isbn = "9781408855652"
    test_data = {
        "isbn": test_isbn,
        "kitap_turu": "e_kitap",
        "dosya_formati": "PDF"
    }

    test_kutuphane = Kütüphane(dosya_adi="test_kutuphane.json")
    monkeypatch.setattr("api.kütüphane", test_kutuphane)

    response = client.post("/books", json=test_data, headers=api_key_header)
 
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["isbn"] == test_isbn
    assert response.json()["kitap_turu"] == "e_kitap"


def test_delete_book(api_key_header, monkeypatch):
    test_isbn = "9780321765723"
    

    test_kutuphane = Kütüphane(dosya_adi="test_kutuphane.json")
    test_kutuphane._kitaplar.append(e_kitap("Test Kitap Adı", "Test Yazar Adı", test_isbn, "PDF"))
    
    
    monkeypatch.setattr("api.kütüphane", test_kutuphane)

    response = client.delete(f"/books/{test_isbn}", headers=api_key_header)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/books")
    assert len(response.json()) == 0

def test_borrow_book(api_key_header, monkeypatch):
    test_isbn = "9780545010221"
    
    test_kutuphane = Kütüphane(dosya_adi="test_kutuphane.json")
    test_kutuphane._kitaplar.append(fiziki_kitap("Test Fiziksel Kitap", "Test Yazar", test_isbn, 350))
    monkeypatch.setattr("api.kütüphane", test_kutuphane)

    response = client.patch(f"/books/{test_isbn}/borrow", headers=api_key_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["odunc_alınmıs"] is True

def test_return_book(api_key_header, monkeypatch):
    test_isbn = "9780545010221"
    
    test_kutuphane = Kütüphane(dosya_adi="test_kutuphane.json")
    kitap = fiziki_kitap("Test Fiziksel Kitap", "Test Yazar", test_isbn, 350)
    kitap.odunc_alınmıs = True
    test_kutuphane._kitaplar.append(kitap)
    monkeypatch.setattr("api.kütüphane", test_kutuphane)

    response = client.patch(f"/books/{test_isbn}/return", headers=api_key_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["odunc_alınmıs"] is False

def test_yanlıs_api_key():
    wrong_header = {"X-API-KEY": "yanlis-api-key"}
    response = client.get("/secure/books", headers=wrong_header)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    response = client.delete("/books/12345", headers=wrong_header)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_aynı_isbn_aynı_turde_kitap(monkeypatch):
    test_isbn = "9781408855652"
    
    test_kutuphane = Kütüphane(dosya_adi="test_kutuphane.json")
    test_kutuphane._kitaplar.append(e_kitap("Test E-Kitap", "Test Yazar", test_isbn, "PDF"))
    monkeypatch.setattr("api.kütüphane", test_kutuphane)

    test_data = {
        "isbn": test_isbn,
        "kitap_turu": "e_kitap",
        "dosya_formati": "PDF"
    }
    response = client.post("/books", json=test_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert f"Bu ISBN ({test_isbn}) ve türdeki (e_kitap) kitap zaten kütüphanede mevcut" in response.json()["detail"]

def test_farkli_turde_kitap_ekleme(api_key_header, monkeypatch):
    test_isbn = "9780545010221"
    
    test_kutuphane = Kütüphane(dosya_adi="test_kutuphane.json")
    test_kutuphane._kitaplar.append(fiziki_kitap("Test Fiziksel Kitap", "Test Yazar", test_isbn, 350))
    monkeypatch.setattr("api.kütüphane", test_kutuphane)
    
    test_data = {
        "isbn": test_isbn,
        "kitap_turu": "e_kitap",
        "dosya_formati": "PDF"
    }
    
    response = client.post("/books", json=test_data, headers=api_key_header)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["isbn"] == test_isbn
    assert response.json()["kitap_turu"] == "e_kitap"
    assert response.json()["dosya_formati"] == "PDF"

    response_books = client.get("/books")
    assert len(response_books.json()) == 2

def test_add_book_api_bağlantısı_sorunu(api_key_header, monkeypatch):
    test_isbn = "9781408855652"
    test_data = {
        "isbn": test_isbn,
        "kitap_turu": "e_kitap",
        "dosya_formati": "PDF"
    }

    test_kutuphane = Kütüphane(dosya_adi="test_kutuphane.json")
    monkeypatch.setattr("api.kütüphane", test_kutuphane)
    
    
    def mock_get(*args, **kwargs):
        raise httpx.RequestError("Mocked connection error")
        
    monkeypatch.setattr(httpx, "get", mock_get)
    
    response = client.post("/books", json=test_data, headers=api_key_header)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "İstek hatası: API'ye bağlanılamıyor" in response.json()["detail"]



def test_tekrar_odunc_alma(api_key_header, monkeypatch):
    test_isbn = "9780545010221"
    
    test_kutuphane = Kütüphane(dosya_adi="test_kutuphane.json")
    kitap = fiziki_kitap("Test Kitap", "Test Yazar", test_isbn, 350)
    kitap.odunc_alınmıs = True
    test_kutuphane._kitaplar.append(kitap)
    monkeypatch.setattr("api.kütüphane", test_kutuphane)

    response = client.patch(f"/books/{test_isbn}/borrow", headers=api_key_header)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Bu kitap zaten ödünç alınmış" in response.json()["detail"]

def test_ödünc_alınmamıs_kitabi_iade(api_key_header, monkeypatch):
    test_isbn = "9780545010221"
    
    test_kutuphane = Kütüphane(dosya_adi="test_kutuphane.json")
    test_kutuphane._kitaplar.append(fiziki_kitap("Test Kitap", "Test Yazar", test_isbn, 350))
    monkeypatch.setattr("api.kütüphane", test_kutuphane)

    response = client.patch(f"/books/{test_isbn}/return", headers=api_key_header)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Bu kitap zaten kütüphanede" in response.json()["detail"]
