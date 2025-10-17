# 🛡️ Siber Güvenlik Tarama Aracı

Sisteminizin güvenlik açıklarını tespit eden profesyonel bir masaüstü uygulaması.

## 📋 Özellikler

### 🔍 Güvenlik Kontrolleri (18 Adet)
- ✅ Windows Defender kontrolü
- ✅ Güvenlik duvarı kontrolü
- ✅ Açık port taraması (12 riskli port)
- ✅ Administrator hesabı kontrolü
- ✅ Şifre politikası analizi
- ✅ Otomatik güncelleme kontrolü
- ✅ Paylaşılan klasör güvenlik kontrolü
- ✅ UAC (Kullanıcı Hesabı Denetimi) kontrolü
- ✅ Uzak Masaüstü (RDP) kontrolü
- ✅ USB otomatik çalıştırma kontrolü
- ✅ BitLocker disk şifreleme kontrolü
- ✅ SMBv1 protokol kontrolü (KRİTİK!)
- ✅ PowerShell Script Block Logging
- ✅ Windows Script Host kontrolü
- ✅ Misafir hesabı kontrolü
- ✅ Boş şifre politikası kontrolü
- ✅ Ekran koruyucu şifre kontrolü
- ✅ Ağ keşfi kontrolü

### 📊 Raporlama Özellikleri
- ✅ Tarama geçmişi kaydetme
- ✅ Detaylı raporlama (TXT, JSON, HTML)
- ✅ Renkli terminal arayüzü
- ✅ Log kayıt sistemi
- ✅ Risk seviyesi analizi (Düşük/Orta/Yüksek/Kritik)

## 🚀 Kurulum

### Gereksinimler
- Python 3.7 veya üzeri
- Windows işletim sistemi (bazı kontroller için)
- Yönetici yetkileri (bazı taramalar için)

### Adımlar

1. Projeyi klonlayın veya indirin
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Programı çalıştırın:
```bash
python main.py
```

## 📦 EXE Oluşturma

```bash
pip install pyinstaller
pyinstaller --onefile --name "GuvenlikTarayici" --icon=icon.ico main.py
```

## 📁 Proje Yapısı

```
SecurityScanner/
├── main.py                 # Ana program
├── requirements.txt        # Gerekli kütüphaneler
├── README.md              # Dokümantasyon
├── modules/               # Ana modüller
├── utils/                 # Yardımcı araçlar
├── data/                  # Veri dosyaları
└── logs/                  # Log dosyaları
```

## ⚠️ Önemli Uyarılar

- Bu araç sadece **kendi sisteminizde** kullanılmalıdır
- Başkasının sistemini izinsiz taramak **yasa dışıdır**
- Bazı taramalar için **yönetici yetkisi** gerekebilir
- Yalnızca eğitim ve yasal güvenlik testi amaçlıdır

## 📝 Kullanım

1. Programı çalıştırın
2. Ana menüden "Taramayı Başlat" seçeneğini seçin
3. Tarama tamamlandığında sonuçları inceleyin
4. İsterseniz rapor oluşturun

## 🔧 Geliştirme

- Python 3.x
- Modüler mimari
- Genişletilebilir yapı

## 📄 Lisans

Bu proje eğitim amaçlıdır. Kendi sorumluluğunuzda kullanın.

## 👤 Geliştirici

Siber Güvenlik Tarama Aracı v1.0

---

**Not:** Bu araç temel güvenlik kontrollerini yapar. Profesyonel güvenlik denetimi için uzman desteği alın.