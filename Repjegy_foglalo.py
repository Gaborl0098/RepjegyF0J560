from abc import ABC, abstractmethod
from datetime import datetime

class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar, indulasi_ido):
        self.jaratszam = jaratszam.upper()
        self.celallomas = celallomas
        self.jegyar = jegyar
        self.indulasi_ido = indulasi_ido

    @abstractmethod
    def info(self):
        pass

class BelfoldiJarat(Jarat):
    def info(self):
        return f"Belföldi Járat {self.jaratszam} - {self.celallomas}, Ár: {self.jegyar} Ft, Indulás: {self.indulasi_ido.strftime('%Y-%m-%d %H:%M')}"

class NemzetkoziJarat(Jarat):
    def info(self):
        return f"Nemzetközi Járat {self.jaratszam} - {self.celallomas}, Ár: {self.jegyar} Ft, Indulás: {self.indulasi_ido.strftime('%Y-%m-%d %H:%M')}"

class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def jarat_hozzaadas(self, jarat):
        self.jaratok.append(jarat)

    def jarat_kereses(self, jaratszam):
        jaratszam = jaratszam.upper().strip()
        for jarat in self.jaratok:
            if jarat.jaratszam == jaratszam:
                return jarat
        return None

class JegyFoglalas:
    def __init__(self):
        self.foglalasok = {}

    def foglalas(self, jarat, utas_nev):
        if jarat.jaratszam not in self.foglalasok:
            self.foglalasok[jarat.jaratszam] = []
        self.foglalasok[jarat.jaratszam].append(utas_nev)
        return jarat.jegyar

    def lemondas(self, jaratszam, utas_nev):
        jaratszam = jaratszam.upper().strip()
        if jaratszam in self.foglalasok and utas_nev in self.foglalasok[jaratszam]:
            self.foglalasok[jaratszam].remove(utas_nev)
            return True
        return False

    def listaz(self):
        if not self.foglalasok:
            print("Nincs még foglalás.")
            return
        for jarat, utasok in self.foglalasok.items():
            for utas in utasok:
                print(f"Járatszám: {jarat}, Utas: {utas}")

def adatok_betoltese(fajlnev):
    utasok = []
    try:
        with open(fajlnev, "r", encoding="utf-8") as f:
            for sor in f:
                nev, szak, neptun = map(str.strip, sor.strip().split(","))
                utasok.append({"nev": nev, "szak": szak, "neptun": neptun})
    except FileNotFoundError:
        print("Hiba: 'adatok.txt' fájl nem található!")
    return utasok

def main():
    utasok = adatok_betoltese("adatok.txt")
    lt = LegiTarsasag("LovasAIR")
    foglalasok = JegyFoglalas()

    lt.jarat_hozzaadas(BelfoldiJarat("B001", "Budapest", 18000, datetime(2025, 6, 1, 10, 0)))
    lt.jarat_hozzaadas(BelfoldiJarat("B002", "Debrecen", 13000, datetime(2025, 6, 1, 15, 0)))
    lt.jarat_hozzaadas(NemzetkoziJarat("N001", "London", 39000, datetime(2025, 6, 2, 9, 0)))
    lt.jarat_hozzaadas(NemzetkoziJarat("N002", "Moszkva", 43000, datetime(2025, 6, 3, 20, 30)))
    lt.jarat_hozzaadas(NemzetkoziJarat("N003", "Teherán", 51000, datetime(2020, 1, 1, 0, 0)))

    if len(utasok) >= 6:
        foglalasok.foglalas(lt.jarat_kereses("B001"), utasok[0]["nev"])
        foglalasok.foglalas(lt.jarat_kereses("B002"), utasok[1]["nev"])
        foglalasok.foglalas(lt.jarat_kereses("B002"), utasok[2]["nev"])
        foglalasok.foglalas(lt.jarat_kereses("B001"), utasok[3]["nev"])
        foglalasok.foglalas(lt.jarat_kereses("N001"), utasok[4]["nev"])
        foglalasok.foglalas(lt.jarat_kereses("N002"), utasok[5]["nev"])

    while True:
        print("\n| Repülőjegy Foglalási Rendszer |")
        print("1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        print("\n - - - - - - - - - - - - -")
        valasztas = input("Választás: ")

        if valasztas == "1":
            print("\nElérhető járatok:")
            for jarat in lt.jaratok:
                print(jarat.info())

            jaratszam = input("Adja meg a foglalni kívánt járatszámot: ").strip().upper()
            jarat = lt.jarat_kereses(jaratszam)

            if not jarat:
                print("Hibás járatszámot adott meg!")
                continue

            if datetime.now() > jarat.indulasi_ido:
                print("Ez a járat már elindult, nem lehet rá foglalni.")
                continue

            print("Elérhető utasok:")
            for i, utas in enumerate(utasok):
                print(f"{i+1}. {utas['nev']} ({utas['neptun']})")

            try:
                sorszam = int(input("Válasszon utast (szám): "))
                if sorszam < 1 or sorszam > len(utasok):
                    raise ValueError
                utas = utasok[sorszam - 1]
            except ValueError:
                print("Érvénytelen utasszám! Csak a listában szereplő számot adhat meg.")
                continue

            ar = foglalasok.foglalas(jarat, utas["nev"])
            print(f"Sikeres foglalás! Jegy ára: {ar} Ft")

        elif valasztas == "2":
            jaratszam = input("Adja meg a járatszámot: ").strip().upper()
            jarat = lt.jarat_kereses(jaratszam)

            if not jarat:
                print("Nem létező járat.")
                continue

            utasnev = input("Adja meg az utas nevét: ").strip()
            if foglalasok.lemondas(jaratszam, utasnev):
                print("Foglalás sikeresen lemondva.")
            else:
                print("Foglalás nem található.")

        elif valasztas == "3":
            print("\nAktuális foglalások:")
            foglalasok.listaz()

        elif valasztas == "4":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás.")

if __name__ == "__main__":
    main()