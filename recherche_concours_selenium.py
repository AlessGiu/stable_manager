from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER_PATH = r"C:\Users\apoll\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def get_concours_with_selenium():
    print("🚀 Lancement du navigateur...")

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Décommente si tu veux cacher la fenêtre
    options.add_argument("--window-size=1920,1080")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("🌍 Ouverture de la page FFE...")
        driver.get("https://ffecompet.ffe.com/concours")

        # (Optionnel) clic sur les cookies
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accepter')]"))
            )
            print("✅ Cookies : clic sur 'Accepter'")
            accept_button.click()
        except Exception:
            print("ℹ️ Pas de bouton cookies détecté.")

        # 🟢 Clic sur le bouton "Trouver un concours"
        try:
            print("🔘 Recherche des concours...")
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Trouver un concours')]"))
            )
            search_button.click()
            print("✅ Clic effectué sur 'Trouver un concours'")
        except Exception as e:
            print("❌ Impossible de cliquer sur 'Trouver un concours' :", e)
            return []

        # ⏳ Attente des résultats dans le tableau
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
            )
        except Exception:
            print("⏳ Timeout : aucune ligne trouvée après le clic.")
            print(driver.page_source[:1000])
            return []

        print("🔍 Extraction des lignes de concours...")
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"✅ {len(rows)} lignes trouvées.")

        concours = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 5:
                concours.append({
                    "date": cols[0].text.strip(),
                    "nom": cols[1].text.strip(),
                    "lieu": cols[2].text.strip(),
                    "disciplines": cols[3].text.strip(),
                    "niveau": cols[4].text.strip(),
                })

        return concours

    except Exception as e:
        print(f"❌ Erreur pendant le scraping : {e}")
        return []

    finally:
        print("🚪 Fermeture du navigateur.")
        driver.quit()


if __name__ == "__main__":
    concours = get_concours_with_selenium()
    for c in concours:
        print(f"📍 {c['date']} | {c['nom']} ({c['lieu']}) - {c['disciplines']} [{c['niveau']}]")
