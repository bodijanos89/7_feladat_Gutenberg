import requests
import csv


def magyar_konyvek_lekérése():
    # Kezdő adatok
    next_url = "https://gutendex.com/books/?languages=hu"
    osszes_talalat = []
    oldal_szamlalo = 1
    max_oldal = 4

    print("Adatok lekérése folyamatban...")

    # Ciklus a maximum 4 oldal bejárásához
    while next_url and oldal_szamlalo <= max_oldal:
        print(f"{oldal_szamlalo}. oldal letöltése: {next_url}")

        try:
            valasz = requests.get(next_url)
            valasz.raise_for_status()  # Hibakezelés, ha nem 200 a válasz
            adatok = valasz.json()

            konyvek = adatok.get("results", [])

            for konyv in konyvek:
                # 1. Title kinyerése
                cim = konyv.get("title", "Nincs cím")

                # 2. Authors összefűzése vesszővel
                szerzok_lista = [a.get("name", "") for a in konyv.get("authors", [])]
                szerzok_string = ", ".join(szerzok_lista)

                # 3. Summaries összefűzése sortöréssel
                summaries_lista = konyv.get("summaries", [])
                summaries_string = "\n".join(summaries_lista)

                # Rekord összeállítása
                osszes_talalat.append({
                    "title": cim,
                    "authors": szerzok_string,
                    "summaries": summaries_string,
                    "page": oldal_szamlalo
                })

            # Következő oldal URL-jének lekérése
            next_url = adatok.get("next")
            oldal_szamlalo += 1

        except Exception as e:
            print(f"Hiba történt a lekérés során: {e}")
            break

    # Adatok mentése CSV fájlba
    mezok = ["title", "authors", "summaries", "page"]

    try:
        with open("talalatok.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=mezok)
            writer.writeheader()
            writer.writerows(osszes_talalat)

        print(f"\nSiker! Összesen {len(osszes_talalat)} könyv elmentve a 'talalatok.csv' fájlba.")
    except Exception as e:
        print(f"Hiba a fájlba íráskor: {e}")


if __name__ == "__main__":
    magyar_konyvek_lekérése()