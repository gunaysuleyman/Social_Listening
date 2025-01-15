from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import os
from selenium.webdriver.chrome.options import Options

def download_trends_csv(auto_close=False, headless=False):
    current_directory = os.getcwd()
    chrome_options = Options()

    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    prefs = {
        "download.default_directory": current_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    actions = ActionChains(driver)

    try:
        print("Sayfa yükleniyor...")
        driver.get("https://trends.google.com/trending?geo=TR&hours=168&status=active&sort=search-volume")

        time.sleep(5)

        print("Dışa aktar düğmesi aranıyor...")
        export_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Dışa aktar')]"))
        )

        print("Dışa aktar düğmesine tıklanıyor...")
        # Farklı tıklama yöntemlerini dene
        try:
            export_button.click()
        except:
            try:
                actions.move_to_element(export_button).click().perform()
            except:
                driver.execute_script("arguments[0].click();", export_button)

        time.sleep(1)

        print("CSV düğmesi aranıyor...")
        csv_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//li[@data-action='csv']"))
        )

        print("CSV düğmesinin tıklanabilir olması bekleniyor...")
        time.sleep(1)


        try:
            print("Yöntem 1: JavaScript ile tıklama deneniyor...")
            driver.execute_script("arguments[0].click();", csv_button)
            #print("Yöntem 1: Normal tıklama deneniyor...")
            #csv_button.click()
        except:
            try:
                print("Yöntem 2: ActionChains ile tıklama deneniyor...")
                actions.move_to_element(csv_button).click().perform()
            except:
                try:
                    print("Yöntem 3: Normal tıklama deneniyor...")
                    csv_button.click()
                    #print("Yöntem 3: JavaScript ile tıklama deneniyor...")
                    #driver.execute_script("arguments[0].click();", csv_button)
                except:
                    try:
                        print("Yöntem 4: Alternatif seçici ile deneniyor...")
                        alt_csv_button = driver.find_element(By.CSS_SELECTOR, "li[data-action='csv']")
                        driver.execute_script("arguments[0].click();", alt_csv_button)
                    except:
                        raise Exception("CSV düğmesine tıklanamadı")

        print("CSV dosyasının inmesi bekleniyor...")
        time.sleep(2)

        
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

    except TimeoutException as e:
        print(f"Zaman aşımı hatası: {str(e)}")
    except NoSuchElementException as e:
        print(f"Element bulunamadı hatası: {str(e)}")
    except Exception as e:
        print(f"Beklenmeyen hata: {str(e)}")
    finally:
        if auto_close or headless:
            driver.quit()
            print("Tarayıcı kapatıldı.")
        else:
            input("Tarayıcıyı kapatmak için Enter tuşuna basın...")
            driver.quit()
            print("Tarayıcı kapatıldı.")

if __name__ == "__main__":
    download_trends_csv(auto_close=True, headless=True)