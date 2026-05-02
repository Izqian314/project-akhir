import sqlite3

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# manual insert QNA

data = [
    ("Apa itu Yoke?", "Yoke pada pesawat Boeing adalah alat kendali utama berbentuk roda atau huruf "U" (disebut juga control wheel atau yoke column) yang digunakan pilot untuk mengemudikan pesawat. Alat ini berfungsi mengendalikan arah pesawat, yaitu untuk mengatur pitch (naik-turun) dengan mendorong/menarik dan roll (miring kanan-kiri) dengan memutar, serta menjadi ciri khas sistem kendali tradisional Boeing.", "cockpit.comp"),
    ("Apa itu Sidesticks?", "Sidestick adalah tuas kendali pesawat yang terletak di konsol samping pilot (biasanya di sisi kanan untuk kapten dan kiri untuk kopilot), berbentuk mirip joystick pada permainan video, dan umumnya ditemukan pada pesawat modern yang menggunakan sistem kontrol fly-by-wire, seperti pada pesawat Airbus.", "general"),
    ("Apa itu MCDU?", "MCDU (Multifunction/Multipurpose Control and Display Unit) Adalah layar dan keyboard fisik (antarmuka) yang digunakan pilot untuk berinteraksi, memasukkan data, dan melihat informasi dari FMC", "cockpit.comp"),
    ("Apa itu FMC?", "FMC (Flight Management Computer) adalah adalah software/hardware pemroses datanya di balik MCDU", "cockpit.comp"),
    ("Apa itu Vertical Speed atau VPI", " Vertical speed atau VPI adalah laju pendakian (climb) atau penurunan (descent) pesawat, yang diukur menggunakan instrumen bernama Vertical Speed Indicator (VSI) dalam satuan kaki per menit (feet per minute/fpm). Instrumen ini memberi tahu pilot seberapa cepat ketinggian pesawat berubah, dengan posisi nol saat terbang mendatar, angka positif saat naik, dan angka negatif saat turun.", "cocpit.comp"),
]

inserted = 0
skipped = 0

for question, answer, category in data:
    cursor.execute("SELECT id FROM qa WHERE question = ?", (question,))
    result = cursor.fetchone()

    if result:
        print(f"⏭️ Skip (sudah ada): {question}")
        skipped += 1
        
    else:
        cursor.execute("""
        INSERT INTO qa (question, answer, category)
        VALUES (?, ?, ?)
        """, (question, answer, category))
        inserted += 1

conn.commit()



# manual insert Quiz
data_q = [
    ("Apa kepanjangan NEO","New Engine Option","New Engine Operation","New Engine Option","Next Evolution Object"),
    ("Apa fungsi utama dari altimeter di kokpit","Mengukur ketinggian","Mengukur ketinggian","Mengukur kecepatan","Mengukur arah mata angin"),
    ("Apa fungsi dari rudder","Membelokkan pesawat ke kanan dan kiri","Mengubah arah pesawat dari atas kebawah","Mengontrol kecepatan","Membelokkan pesawat ke kanan dan kiri"),
]

inserted1 = 0
skipped1 = 0

print("=======Qa=======")
for question, correct_answer, option1, option2, option3 in data_q:
    cursor.execute("SELECT id FROM quiz WHERE question = ?", (question,))
    result = cursor.fetchone()

    if result:
        print(f"⏭️ Skip (sudah ada): {question}")
        skipped1 += 1
        
    else:
        cursor.execute("""
        INSERT INTO quiz (question, correct_answer, option1, option2, option3)
        VALUES (?, ?, ?, ?, ?)""", (question, correct_answer, option1, option2, option3))
        inserted1 += 1
conn.commit()
conn.close()
print("======Quiz======")

# manual insert aircraft
#data_a = [
#    ("A318", "Airbus 318", "Airbus", "Narrow, CFM56/PW600 engine"),
#    ("A319-100", "Airbus 319-100", "Airbus", "Narrow, CFM56-5B/IEO V2500-A5 engine"),
#    ("A319LR", "Airbus 319 LR", "Airbus", "Narrow, CFM56-5B or IAE V2500-A5 engine, tambahan 16.332 LBS tanki bahan bakar"),
#    ("A319N", "Airbus 319 New Engine Option(NEO)", "Airbus", "Narrow, CFM leap-1A/PW 1100G-JM, efisiensi bahan bakar 15-20%"),
#    ("A319CJ", "Airbus 319 Corporate Jet", "Airbus", "Narrow, Jet pribadi"),
#    ("A319", "Airbus 319 series", "Airbus", " Small Airbus plane series"),
#    ("", "", "", ""),
#    ("", "", "", ""),
#    ("", "", "", ""),
#    ("", "", "", ""),
#    ("", "", "", ""),
#    ("", "", "", ""),
#    ("", "", "", ""),
#    ("", "", "", ""),
#    ("", "", "", ""),
#    ("", "", "", "")
#]
#cursor.executemaney("""
#INSERT INTO quiz (code, type, manufacturer, description)
#VALUES (?, ?, ?)""", data_a)
#conn.commit(
#    conn.close
#)

print("Data berhasil ditambahkan!")