# 🛡️ Siber Güvenlik Tarayıcı Aracı
Sisteminizdeki güvenlik açıklarını tespit etmek için profesyonel bir masaüstü uygulaması.

## 📋 Özellikler

### 🔍 Güvenlik Kontrolleri (18 Tür)
* ✅ Windows Defender durumu
* ✅ Güvenlik duvarı doğrulama
* ✅ Açık port taraması (12 riskli port)
* ✅ Yönetici hesabı kontrolü
* ✅ Parola politikası analizi
* ✅ Otomatik güncellemeler doğrulama
* ✅ Paylaşılan klasör güvenlik kontrolü
* ✅ UAC (Kullanıcı Hesabı Denetimi) doğrulama
* ✅ Uzak Masaüstü (RDP) kontrolü
* ✅ USB otomatik çalıştırma doğrulama
* ✅ BitLocker disk şifreleme kontrolü
* ✅ SMBv1 protokol kontrolü (KRİTİK!)
* ✅ PowerShell Script Block Logging
* ✅ Windows Script Host doğrulama
* ✅ Konuk hesabı kontrolü
* ✅ Boş parola politikası kontrolü
* ✅ Ekran koruyucu parola doğrulama
* ✅ Ağ keşfi kontrolü

### 📊 Raporlama Özellikleri
* ✅ Tarama geçmişi kayıt tutma
* ✅ Detaylı raporlar (TXT, JSON, HTML)
* ✅ Renkli terminal arayüzü
* ✅ Log kayıt sistemi
* ✅ Risk seviyesi analizi (Düşük/Orta/Yüksek/Kritik)

## 🚀 Kurulum

### Gereksinimler
* Python 3.7 veya üstü
* Windows işletim sistemi (bazı kontroller için)
* **⚠️ Yönetici yetkileri gereklidir** (yönetici olarak çalıştırılmalıdır)

### Adımlar
1. Projeyi klonlayın veya indirin
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

3. **Programı Yönetici olarak çalıştırın:**

**Yöntem 1 (Komut İstemi):**
```bash
# Komut İstemi'ne sağ tıklayın → Yönetici olarak çalıştır
cd yol\SecurityScanner
python main.py
```

**Yöntem 2 (PowerShell):**
```powershell
# PowerShell'e sağ tıklayın → Yönetici olarak çalıştır
cd yol\SecurityScanner
python main.py
```

**Yöntem 3 (Kısayol):**
- `main.py` dosyasına sağ tıklayın
- "Yönetici olarak çalıştır" seçeneğini seçin

## 📦 EXE Oluşturma
```bash
pip install pyinstaller
pyinstaller main.spec
```

**EXE dosyasını yönetici olarak çalıştırmak için:**
- `.exe` dosyasına sağ tıklayın
- "Yönetici olarak çalıştır" seçeneğini seçin

## 📁 Proje Yapısı
```
SecurityScanner/
├── main.py                 # Ana program
├── requirements.txt        # Gerekli kütüphaneler
├── README.md              # Dokümantasyon
├── modules/               # Çekirdek modüller
├── utils/                 # Yardımcı araçlar
├── data/                  # Veri dosyaları
└── logs/                  # Log dosyaları
```

## ⚠️ Önemli Uyarılar

**YASAL SORUMLULUK REDDİ:**
* ⚖️ Bu araç **YALNIZCA EĞİTİM AMAÇLIDIR**
* ⚖️ Sadece **SAHİP OLDUĞUNUZ** veya test etmek için **YAZILI İZNİ OLAN** sistemlerde kullanın
* ⚖️ Sistemlerin yetkisiz taranması **YASADIŞ**tır ve yasalarla cezalandırılır
* ⚖️ Çoğu güvenlik kontrolü için **yönetici yetkileri GEREKLİDİR**
* ⚖️ Geliştirici, bu aracın kötüye kullanımından **SORUMLU DEĞİLDİR**

**YÖNETİCİ YETKİLERİ:**
* 🔐 Birçok güvenlik kontrolü yükseltilmiş yetkiler gerektirir
* 🔐 Komut İstemi/PowerShell'i yönetici olarak çalıştırın
* 🔐 Bazı özellikler yönetici hakları olmadan çalışmayabilir

## 📝 Kullanım
1. **Programı yönetici olarak çalıştırın**
2. Ana menüden "Taramayı Başlat" seçeneğini seçin
3. Tarama tamamlandığında sonuçları inceleyin
4. Gerekirse rapor oluşturun

## 🔧 Geliştirme
* Python 3.x
* Modüler mimari
* Genişletilebilir yapı

## 📄 Lisans
MIT Lisansı - Bu proje eğitim amaçlıdır. Kullanım riski size aittir.

## 👤 Geliştirici
**Troj1ann**
* GitHub: [@troj1ann](https://github.com/troj1ann)

## 🛡️ Etik Kullanım Bildirimi
Bu araç, sistem yöneticilerinin ve güvenlik uzmanlarının kendi sistemlerindeki açıkları tespit etmelerine yardımcı olmak için tasarlanmıştır. Güvenlik değerlendirmeleri yapmadan önce her zaman uygun yetkilendirmeye sahip olduğunuzdan emin olun.

---

**Not:** Bu araç temel güvenlik kontrollerini gerçekleştirir. Profesyonel güvenlik denetimleri için siber güvenlik uzmanlarına danışın.
