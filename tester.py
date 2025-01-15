import requests
import os
import pandas as pd

def download_trends_csv():
    
    current_directory = os.getcwd()

   
    csv_download_url = "https://www.google-analytics.com/collect"

    
    params = {
        "v": "1",
        "_v": "j101",
        "a": "1352005713",
        "t": "event",
        "_s": "9",
        "dl": "https://trends.google.com/trending?geo=TR&status=active&hours=168&sort=search-volume",
        "ul": "tr-tr",
        "de": "UTF-8",
        "dt": "Şu Anda Trend Olanlar - Google Trendler",
        "sd": "24-bit",
        "sr": "1536x864",
        "vp": "463x731",
        "je": "0",
        "ec": "trending_toolbar",
        "ea": "click",
        "el": "csv",
        "_u": "SACAAUABAAAAACAAI~",
        "jid": "",
        "gjid": "",
        "cid": "1897692294.1735052792",
        "tid": "UA-4401283",
        "_gid": "2029189585.1736936520",
        "gtm": "457e51e0za200zb899589902",
        "gcd": "13l3l3l3l1l1",
        "dma": "0",
        "tag_exp": "101925629~102067555~102067808~102081485~102198178",
        "jsscut": "1",
        "z": "246885235"
    }

    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://trends.google.com/",
        "Origin": "https://trends.google.com",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "Cookie": "ar_debug=1"
    }

    
    print("CSV dosyasını indirme isteği gönderiliyor...")
    response = requests.get(csv_download_url, params=params, headers=headers)

    
    if response.status_code == 200:
        print("CSV dosyası başarıyla indirildi.")
        
        csv_filename = os.path.join(current_directory, "trends_data.csv")
        with open(csv_filename, "wb") as file:
            file.write(response.content)
        print(f"CSV dosyası kaydedildi: {csv_filename}")

        
        try:
            csv_files = [f for f in os.listdir(current_directory) if f.endswith('.csv')]
            if csv_files:
                latest_csv = max([os.path.join(current_directory, f) for f in csv_files], key=os.path.getctime)

                print(f"CSV dosyası bulundu: {latest_csv}")
                
                df = pd.read_csv(latest_csv, encoding='utf-8-sig')
                excel_filename = 'trends_data.xlsx'
                df.to_excel(excel_filename, index=False)
                print(f"Excel dosyası oluşturuldu: {excel_filename}")
            else:
                print("CSV dosyası bulunamadı!")

            print("İşlem tamamlandı.")
        except Exception as e:
            print(f"CSV'den Excel'e dönüştürme hatası: {e}")
    else:
        print(f"CSV dosyası indirilemedi. HTTP Durum Kodu: {response.status_code}")
        print(f"Yanıt: {response.text}")

if __name__ == "__main__":
    download_trends_csv()