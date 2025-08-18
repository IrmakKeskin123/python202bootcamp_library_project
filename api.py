

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
from enum import IntEnum
from library_3_asama import Kütüphane 
from book import fiziki_kitap, e_kitap, sesli_kitap




#AYARLAR VE VERİ TABANI
logging.basicConfig(level=logging.INFO)           
logger = logging.getLogger(__name__)




class HTTPStatusCodes(IntEnum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    UNPROCESSABLE_ENTITY = 422




API_KEY= "SECRET_API_KEY_12345"
API_KEY_NAME= "X-API-KEY"
api_key_header= APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kimlik Bilgileri Doğrulanamadı"
        )





app= FastAPI(
    title= "Library Management API",
    description= "Kütüphane uygulaması için FastAPI örneği",
    version= "1.0.0"
)

kütüphane= Kütüphane()




class BookResponse(BaseModel):
    kitap_adi: str
    yazar: str
    isbn: str
    kitap_turu: str
    sayfa_sayisi: Optional[int] = None
    dosya_formati: Optional[str] = None
    ses_süresi: Optional[int] = None
    odunc_alınmıs: Optional[bool] = None

#Kullanıcıdan hangi  verinin alınacağı bilgis
class BookCreateRequest(BaseModel): 
    isbn: str
    kitap_turu: str
    sayfa_sayisi:  Optional[int] = None
    dosya_formati:  Optional[str] = None
    ses_süresi:  Optional[int] = None
    




#Get (Veriyi Okur)
@app.get("/",status_code=HTTPStatusCodes.OK)
def root():
    return {"message":"FastAPI Library Manegement System"}

@app.get("/health", status_code=HTTPStatusCodes.OK)
def health():
    return{"status":"healthy"}





@app.get("/books", response_model=list[BookResponse], status_code= HTTPStatusCodes.OK)
def list_books():
    books= []
    for kitap in kütüphane.list_books():
        books.append(
            BookResponse(
                isbn=kitap.isbn,
                kitap_adi=kitap.kitap_adi,
                yazar=kitap.yazar,
                kitap_turu=kitap.__class__.__name__,
                sayfa_sayisi=getattr(kitap, "sayfa_sayisi", None),
                dosya_formati=getattr(kitap, "dosya_formati",None),
                ses_süresi=getattr(kitap,"ses_süresi", None),
                odunc_alınmıs=getattr(kitap, "odunc_alınmıs", None)
            )
        )
    return books
                                  





#Post (Yeni veri oluşturur)
@app.post("/books", response_model=BookResponse, status_code= HTTPStatusCodes.CREATED)
def add_book_endpoint(bookreq: BookCreateRequest):
    for kitap in kütüphane.list_books():
        if kitap.isbn == bookreq.isbn and kitap.__class__.__name__ == bookreq.kitap_turu:
            raise HTTPException(
                status_code=HTTPStatusCodes.BAD_REQUEST,
                detail=f"Bu ISBN ({bookreq.isbn}) ve türdeki ({bookreq.kitap_turu}) kitap zaten kütüphanede mevcut"
            )
    
    try:
        kitap = kütüphane.add_book(
            isbn=bookreq.isbn,
            kitap_turu=bookreq.kitap_turu,
            sayfa_sayisi=bookreq.sayfa_sayisi,
            dosya_formati=bookreq.dosya_formati,
            ses_süresi=bookreq.ses_süresi
        )
        
        return BookResponse(
            isbn=kitap.isbn,
            kitap_adi=kitap.kitap_adi,
            yazar=kitap.yazar,
            kitap_turu=kitap.__class__.__name__,
            sayfa_sayisi=getattr(kitap, "sayfa_sayisi", None),
            dosya_formati=getattr(kitap, "dosya_formati", None),
            ses_süresi=getattr(kitap, "ses_süresi", None),
            odunc_alınmıs=getattr(kitap, "odunc_alınmıs", None)
        )

    except ValueError as e:
        raise HTTPException(status_code=HTTPStatusCodes.BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTPStatusCodes.UNPROCESSABLE_ENTITY, detail=str(e))




#Delete{isbn} (İSBN ile veriyi siler
@app.delete("/books/{isbn}", status_code=HTTPStatusCodes.NO_CONTENT)
def delete_book(isbn:str, api_key: str = Depends(get_api_key)):
    kitap=kütüphane.find_book(isbn)
    if not kitap:
        raise HTTPException(
            status_code=HTTPStatusCodes.NOT_FOUND,
            detail=f"{isbn} numaralı kitap bulunamadı"
        )
    kütüphane.remove_book(isbn)
    kütüphane.save_books() 
    return
    





@app.get("/secure/books", response_model=List[BookResponse])
def secure_list_books(api_key:str= Depends(get_api_key)):
    books= []
    for kitap in kütüphane.list_books():
        books.append(
            BookResponse(
                isbn= kitap.isbn,
                kitap_adi= kitap.kitap_adi,
                yazar= kitap.yazar,
                kitap_turu= kitap.__class__.__name__,
                sayfa_sayisi=getattr(kitap, "sayfa_sayisi", None),
                dosya_formati=getattr(kitap, "dosya_formati", None),
                ses_süresi=getattr(kitap, "ses_süresi", None),
                odunc_alınmıs=getattr(kitap, "odunc_alınmıs", None)
            )
        )
    return books
            





#Patch{isbn} fiziksel kitaplarda ödünç alınma durumunu günceller
@app.patch("/books/{isbn}/borrow", response_model=BookResponse)
def borrow_book(isbn:str, api_key:str= Depends(get_api_key)):
    try:
        kütüphane.odunc_al(isbn)
        kitap= kütüphane.find_book(isbn)

        return BookResponse(
            isbn= kitap.isbn,
            kitap_adi= kitap.kitap_adi,
            yazar= kitap.yazar,
            kitap_turu= kitap.__class__.__name__,
            sayfa_sayisi=getattr(kitap, "sayfa_sayisi", None),
            dosya_formati=getattr(kitap, "dosya_formati", None),
            ses_süresi=getattr(kitap, "ses_süresi", None),
            odunc_alınmıs=kitap.odunc_alınmıs
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        




#Patch{isbn} fiziksel kitaplarda iade durumunu günceller
@app.patch("/books/{isbn}/return", response_model=BookResponse)
def return_book(isbn:str, api_key:str= Depends(get_api_key)):
    kitap = kütüphane.find_book(isbn)
    if not kitap:
        raise HTTPException(
            status_code=HTTPStatusCodes.NOT_FOUND,
            detail=f"{isbn} numaralı kitap bulunamadı"
        )
    if not getattr(kitap, 'odunc_alınmıs', False):
        raise HTTPException(
            status_code=HTTPStatusCodes.BAD_REQUEST,
            detail="Bu kitap zaten kütüphanede"
        )
    
    
    try:
        kütüphane.iade_et(isbn)
        kitap= kütüphane.find_book(isbn)

        return BookResponse(
            isbn= kitap.isbn,
            kitap_adi= kitap.kitap_adi,
            yazar= kitap.yazar,
            kitap_turu= kitap.__class__.__name__,
            sayfa_sayisi=getattr(kitap, "sayfa_sayisi", None),
            dosya_formati=getattr(kitap, "dosya_formati", None),
            ses_süresi=getattr(kitap, "ses_süresi", None),
            odunc_alınmıs=kitap.odunc_alınmıs
        )
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatusCodes.BAD_REQUEST, detail=str(e))
        
            





if __name__ == "__main__":
    import uvicorn

    
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )



