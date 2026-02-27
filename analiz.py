# ============================================
# DUNYA NUFUS ANALIZI
# Kaggle - World Population Dataset
# ============================================

import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# 1. VERİYİ OKU
# ============================================

df = pd.read_csv("world_population.csv")

# Kolay kullanım icin sutun isimlerini kisalt
df = df.rename(columns={
    "Country/Territory": "Ulke",
    "Continent": "Kita",
    "2022 Population": "Nufus_2022",
    "2000 Population": "Nufus_2000",
    "1970 Population": "Nufus_1970",
    "Area (km²)": "Alan_km2",
    "Density (per km²)": "Yogunluk",
    "Growth Rate": "Buyume_Orani",
    "World Population Percentage": "Dunya_Yuzdesi"
})

print("=" * 50)
print("DUNYA NUFUS ANALIZI")
print("=" * 50)
print(f"Toplam ulke sayisi: {len(df)}")
print(f"Sutunlar: {df.columns.tolist()}")

# ============================================
# 2. TEMEL ANALİZ
# ============================================

print("\n--- GENEL ISTATISTIKLER ---")
print(f"En kalabalk ulke   : {df.loc[df['Nufus_2022'].idxmax(), 'Ulke']} ({df['Nufus_2022'].max():,})")
print(f"En az nufuslu ulke : {df.loc[df['Nufus_2022'].idxmin(), 'Ulke']} ({df['Nufus_2022'].min():,})")
print(f"En yogun ulke      : {df.loc[df['Yogunluk'].idxmax(), 'Ulke']} ({df['Yogunluk'].max():.0f} kisi/km2)")
print(f"En hizli buyuyen   : {df.loc[df['Buyume_Orani'].idxmax(), 'Ulke']} (%{df['Buyume_Orani'].max():.2f})")

print("\n--- KITAYA GORE TOPLAM NUFUS (2022) ---")
kita_nufus = df.groupby("Kita")["Nufus_2022"].sum().sort_values(ascending=False)
for kita, nufus in kita_nufus.items():
    print(f"  {kita}: {nufus:,}")

# ============================================
# 3. KULLANICI INPUTU — ULKE ARA
# ============================================

print("\n" + "=" * 50)
print("ULKE ARAMA")
print("=" * 50)

while True:
    aranan = input("\nUlke adi girin (cikmak icin 'q'): ").strip()

    if aranan.lower() == "q":
        print("Program sonlandiriliyor...")
        break

    sonuc = df[df["Ulke"].str.lower() == aranan.lower()]

    if sonuc.empty:
        # Benzer isimleri oner
        benzer = df[df["Ulke"].str.lower().str.contains(aranan.lower())]
        if not benzer.empty:
            print(f"'{aranan}' bulunamadi. Bunu mu demek istediniz?")
            print(", ".join(benzer["Ulke"].tolist()))
        else:
            print(f"'{aranan}' bulunamadi.")
    else:
        r = sonuc.iloc[0]
        print(f"\n--- {r['Ulke']} ---")
        print(f"  Kita            : {r['Kita']}")
        print(f"  Nufus (2022)    : {r['Nufus_2022']:,}")
        print(f"  Nufus (2000)    : {r['Nufus_2000']:,}")
        print(f"  Nufus (1970)    : {r['Nufus_1970']:,}")
        print(f"  Alan            : {r['Alan_km2']:,} km2")
        print(f"  Yogunluk        : {r['Yogunluk']:.1f} kisi/km2")
        print(f"  Buyume orani    : %{r['Buyume_Orani']:.2f}")
        print(f"  Dunya nufusunun : %{r['Dunya_Yuzdesi']:.2f}")

# ============================================
# 4. GRAFIKLER
# ============================================

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("Dunya Nufus Analizi (Kaggle Dataset)", fontsize=16, fontweight="bold")

# Grafik 1: En kalabalik 10 ulke (2022)
top10 = df.nlargest(10, "Nufus_2022").sort_values("Nufus_2022")
axes[0, 0].barh(top10["Ulke"], top10["Nufus_2022"] / 1_000_000, color="steelblue")
axes[0, 0].set_title("En Kalabalk 10 Ulke (2022)")
axes[0, 0].set_xlabel("Nufus (Milyon)")

# Grafik 2: Kitaya gore nufus dagilimi
kita_nufus.plot(kind="pie", ax=axes[0, 1], autopct="%1.1f%%", startangle=90)
axes[0, 1].set_title("Kitalara Gore Nufus Dagilimi")
axes[0, 1].set_ylabel("")

# Grafik 3: Nufus degisimi - 1970 vs 2022 (ilk 10)
top10_ulke = df.nlargest(10, "Nufus_2022")
x = range(len(top10_ulke))
width = 0.35
axes[1, 0].bar([i - width/2 for i in x], top10_ulke["Nufus_1970"] / 1_000_000, width, label="1970", color="lightblue")
axes[1, 0].bar([i + width/2 for i in x], top10_ulke["Nufus_2022"] / 1_000_000, width, label="2022", color="steelblue")
axes[1, 0].set_title("Nufus Degisimi: 1970 vs 2022")
axes[1, 0].set_ylabel("Nufus (Milyon)")
axes[1, 0].set_xticks(list(x))
axes[1, 0].set_xticklabels(top10_ulke["Ulke"], rotation=45, ha="right")
axes[1, 0].legend()

# Grafik 4: En yuksek nufus yogunlugu (ilk 10)
top10_yogun = df.nlargest(10, "Yogunluk").sort_values("Yogunluk")
axes[1, 1].barh(top10_yogun["Ulke"], top10_yogun["Yogunluk"], color="coral")
axes[1, 1].set_title("En Yuksek Nufus Yogunlugu (kisi/km2)")
axes[1, 1].set_xlabel("Yogunluk (kisi/km2)")

plt.tight_layout()
plt.savefig("nufus_analizi.png", dpi=150, bbox_inches="tight")
plt.show()

print("\nGrafik 'nufus_analizi.png' olarak kaydedildi!")
