import sqlite3
from collections import Counter



def veritabanina_baglan_ve_kaydet(text1, text2):
    baglan = sqlite3.connect('metinler.db')
    b = baglan.cursor()

    b.execute('CREATE TABLE IF NOT EXISTS Metinler (id INTEGER PRIMARY KEY, text TEXT)')

    b.execute('DELETE FROM Metinler')

    b.execute('INSERT INTO Metinler (text) VALUES (?)', (text1,))
    b.execute('INSERT INTO Metinler (text) VALUES (?)', (text2,))

    baglan.commit()
    baglan.close()



def metinleri_yukle_ve_karsilastir():
    baglan = sqlite3.connect('metinler.db')
    b = baglan.cursor()
    b.execute('SELECT text FROM Metinler')
    metinler = [text[0].lower() for text in b.fetchall()]  # Metinleri küçük harfe çevir
    baglan.close()


    metin1kelimeleri = Counter(metinler[0].split())
    metin2kelimeleri = Counter(metinler[1].split())


    butun_kelimeler = set(metin1kelimeleri).union(metin2kelimeleri)


    intersection = sum(min(metin1kelimeleri[word], metin2kelimeleri[word]) for word in butun_kelimeler)
    total_words = sum(metin1kelimeleri[word] + metin2kelimeleri[word] for word in butun_kelimeler)
    similarity_score = (2.0 * intersection) / total_words if total_words > 0 else 1.0

    return similarity_score



text1 = "Zorluklar başarıya giden yolda sadece adımlardır, vazgeçmek ise yolun sonu demektir"
text2 = "Başarıya giden yolda zorluklar sadece adım adımdır, yolun sonu vazgeçmektir"
veritabanina_baglan_ve_kaydet(text1, text2)


similarity_score = metinleri_yukle_ve_karsilastir()
print(f"Benzerlik Skoru: {similarity_score:.2f}")

with open('benzerlik_durumu.txt', 'w') as f:
    f.write(f"Metinler arasındaki benzerlik skoru: {similarity_score:.2f}")
