# 🛡️ Siber Güvenlik Tarama Aracı
Sisteminizdeki güvenlik açıklarını tespit etmek için profesyonel bir masaüstü uygulaması.

## 📋 Özellikler

### 🔍 Güvenlik Kontrolleri (18 Tür)
* ✅ Windows Defender durumu
* ✅ Güvenlik Duvarı doğrulama
* ✅ Açık bağlantı noktası taraması (12 riskli bağlantı noktası)
* ✅ Yönetici hesabı kontrolü
* ✅ Parola politikası analizi
* ✅ Otomatik güncellemelerin doğrulanması
* ✅ Paylaşılan klasör güvenlik kontrolü
* ✅ UAC (Kullanıcı Hesabı Denetimi) doğrulama
* ✅ Uzak Masaüstü (RDP) kontrolü
* ✅ USB otomatik çalıştırma (autorun) doğrulama
* ✅ BitLocker disk şifreleme kontrolü
* ✅ SMBv1 protokol kontrolü (KRİTİK!)
* ✅ PowerShell Betik Bloğu Günlüğü (Script Block Logging)
* ✅ Windows Betik Ana Bilgisayarı (Windows Script Host) doğrulama
* ✅ Misafir hesabı (Guest account) kontrolü
* ✅ Boş parola politikası kontrolü
* ✅ Ekran koruyucu parola doğrulama
* ✅ Ağ keşfi (Network discovery) kontrolü

### 📊 Raporlama Özellikleri
* ✅ Tarama geçmişi kaydı
* ✅ Detaylı raporlar (TXT, JSON, HTML)
* ✅ Renkli terminal arayüzü
* ✅ Günlük kayıt sistemi
* ✅ Risk seviyesi analizi (Düşük/Orta/Yüksek/Kritik)

## 🚀 Kurulum

### Gereksinimler
* Python 3.7 veya üzeri
* Windows işletim sistemi (bazı kontroller için)
* **⚠️ Yönetici ayrıcalıkları gereklidir** (yönetici olarak çalıştırılmalıdır)

### Adımlar
1. Projeyi klonlayın veya indirin
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
Programı Yönetici olarak çalıştırın:

Yöntem 1 (Komut İstemi - Command Prompt):

Bash

# Komut İstemine sağ tıklayın → Yönetici olarak çalıştırın
cd path\to\SecurityScanner
python main.py
Yöntem 2 (PowerShell):

PowerShell

# PowerShell'e sağ tıklayın → Yönetici olarak çalıştırın
cd path\to\SecurityScanner
python main.py
Yöntem 3 (Kısayol):

main.py dosyasına sağ tıklayın

"Yönetici olarak çalıştır"ı seçin

📦 EXE Oluşturma
Bash

pip install pyinstaller
pyinstaller main.spec
EXE dosyasını yönetici olarak çalıştırmak için:

.exe dosyasına sağ tıklayın

"Yönetici olarak çalıştır"ı seçin

📁 Proje Yapısı
SecurityScanner/
├── main.py                 # Ana program
├── requirements.txt        # Gerekli kütüphaneler
├── README.md              # Dokümantasyon
├── modules/               # Çekirdek modüller
├── utils/                 # Yardımcı araçlar
├── data/                  # Veri dosyaları
└── logs/                  # Log dosyaları
⚠️ Önemli Uyarılar
YASAL UYARI:

⚖️ Bu araç SADECE EĞİTİM AMAÇLIDIR

⚖️ Yalnızca SAHİBİ OLDUĞUNUZ veya test etmek için YAZILI İZİN aldığınız sistemlerde kullanın

⚖️ Sistemlerin izinsiz taranması YASALARA AYKIRIDIR ve kanunla cezalandırılabilir

⚖️ Çoğu güvenlik kontrolü için YÖNETİCİ AYRICALIKLARI GEREKLİDİR

⚖️ Geliştirici, bu aracın kötüye kullanılmasından dolayı HİÇBİR SORUMLULUK KABUL ETMEZ

YÖNETİCİ AYRICALIKLARI:

🔐 Birçok güvenlik kontrolü yükseltilmiş ayrıcalıklar gerektirir

🔐 Komut İstemi/PowerShell'i yönetici olarak çalıştırın

🔐 Bazı özellikler yönetici hakları olmadan çalışmayabilir

📝 Kullanım
Programı yönetici olarak çalıştırın

Ana menüden "Taramayı Başlat"ı seçin

Tarama tamamlandığında sonuçları gözden geçirin

Gerekirse rapor oluşturun

🔧 Geliştirme
Python 3.x

Modüler mimari

Genişletilebilir yapı

📄 Lisans
MIT Lisansı - Bu proje eğitim amaçlıdır. Kullanım riski size aittir.

👤 Geliştirici
Troj1ann

GitHub: @troj1ann

🛡️ Etik Kullanım Beyanı
Bu araç, sistem yöneticilerinin ve güvenlik uzmanlarının kendi sistemlerindeki güvenlik açıklarını belirlemelerine yardımcı olmak için tasarlanmıştır. Güvenlik değerlendirmeleri yapmadan önce daima uygun yetkiye sahip olduğunuzdan emin olun.

Not: Bu araç temel güvenlik kontrolleri gerçekleştirir. Profesyonel güvenlik denetimleri için siber güvenlik uzmanlarına danışın.
