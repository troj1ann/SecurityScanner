"""
Kullanıcı Arayüzü Modülü
Terminal tabanlı arayüz ve menü sistemi
"""

import os
import sys
import time
from datetime import datetime

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Colorama yoksa boş class'lar oluştur
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""


class SecurityUI:
    """Terminal arayüzü yönetimi"""
    
    def __init__(self, scanner, logger):
        self.scanner = scanner
        self.logger = logger
        self.width = 70
        
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Program başlığını yazdır"""
        print(Fore.CYAN + "=" * self.width)
        title = "SİBER GÜVENLİK TARAMA ARACI v2.0"
        padding = (self.width - len(title)) // 2
        print(Fore.CYAN + " " * padding + Style.BRIGHT + title)
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
        print()
    
    def print_menu(self):
        """Ana menüyü yazdır"""
        print(Fore.GREEN + "1)" + Fore.WHITE + " Taramayı Başlat")
        print(Fore.GREEN + "2)" + Fore.WHITE + " Tarama Geçmişi")
        print(Fore.GREEN + "3)" + Fore.WHITE + " Rapor Oluştur")
        print(Fore.GREEN + "4)" + Fore.WHITE + " İstatistikler")
        print(Fore.GREEN + "5)" + Fore.WHITE + " Ayarlar")
        print(Fore.GREEN + "6)" + Fore.WHITE + " Hakkında")
        print(Fore.GREEN + "7)" + Fore.WHITE + " Çıkış")
        print()
    
    def loading_animation(self, duration=2, message="Tarama devam ediyor"):
        """Yükleme animasyonu"""
        chars = ['/', '-', '\\', '|']
        end_time = time.time() + duration
        idx = 0
        
        while time.time() < end_time:
            char = chars[idx % len(chars)]
            sys.stdout.write(f'\r{Fore.YELLOW}{char} {message}...')
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1
        
        sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')
        sys.stdout.flush()
    
    def progress_bar(self, current, total, prefix='', suffix=''):
        """İlerleme çubuğu göster"""
        bar_length = 40
        filled_length = int(bar_length * current / total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        percent = f"{100 * current / total:.1f}"
        
        sys.stdout.write(f'\r{prefix} |{Fore.GREEN}{bar}{Style.RESET_ALL}| {percent}% {suffix}')
        sys.stdout.flush()
        
        if current == total:
            print()
    
    def display_scan_progress(self, check_name, current, total):
        """Tarama ilerlemesini göster"""
        self.progress_bar(current, total, 
                         prefix=f'{Fore.CYAN}[{current}/{total}]{Style.RESET_ALL}',
                         suffix=f'{check_name}')
    
    def display_results(self, vulnerabilities, scan_info):
        """Tarama sonuçlarını göster"""
        self.clear_screen()
        self.print_header()
        
        print(Fore.YELLOW + Style.BRIGHT + "TARAMA TAMAMLANDI")
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
        
        # Tarama bilgileri
        print(f"{Fore.BLUE}Tarih:{Style.RESET_ALL} {scan_info.get('date', 'Bilinmiyor')}")
        print(f"{Fore.BLUE}Sistem:{Style.RESET_ALL} {scan_info.get('system', 'Bilinmiyor')}")
        print(f"{Fore.BLUE}Süre:{Style.RESET_ALL} {scan_info.get('duration', 0):.2f} saniye")
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
        print()
        
        # Sonuçlar
        if not vulnerabilities:
            print(Fore.GREEN + "✓ Herhangi bir güvenlik açığı tespit edilmedi.")
            print(Fore.GREEN + "  Sisteminiz temel güvenlik kontrollerini geçti." + Style.RESET_ALL)
        else:
            vuln_count = len(vulnerabilities)
            
            # Risk dağılımını hesapla
            risk_counts = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
            for vuln in vulnerabilities:
                risk = vuln.get('risk', 'medium').lower()
                risk_counts[risk] = risk_counts.get(risk, 0) + 1
            
            # Başlık
            print(Fore.RED + Style.BRIGHT + f"⚠ {vuln_count} adet güvenlik açığı tespit edildi!" + Style.RESET_ALL)
            print()
            
            # Risk dağılımı
            print(Fore.YELLOW + "Risk Dağılımı:")
            if risk_counts['critical'] > 0:
                print(f"{Fore.RED + Style.BRIGHT}  • KRİTİK: {risk_counts['critical']} ⚠️⚠️⚠️{Style.RESET_ALL}")
            if risk_counts['high'] > 0:
                print(f"{Fore.RED}  • Yüksek: {risk_counts['high']} ⚠️⚠️{Style.RESET_ALL}")
            if risk_counts['medium'] > 0:
                print(f"{Fore.MAGENTA}  • Orta: {risk_counts['medium']} ⚠️{Style.RESET_ALL}")
            if risk_counts['low'] > 0:
                print(f"{Fore.YELLOW}  • Düşük: {risk_counts['low']}{Style.RESET_ALL}")
            print()
            
            # Kritik uyarı
            if risk_counts['critical'] > 0:
                print(Fore.RED + Style.BRIGHT + "!" * self.width)
                print("KRİTİK SEVİYE GÜVENLİK AÇIKLARI TESPİT EDİLDİ!")
                print("Bu açıklar DERHAL düzeltilmelidir!")
                print("!" * self.width + Style.RESET_ALL)
                print()
            
            # Detaylı liste
            print(Fore.CYAN + "Detaylı Bulgular:" + Style.RESET_ALL)
            print()
            
            for idx, vuln in enumerate(vulnerabilities, 1):
                # Risk seviyesine göre renk
                risk_color = self.get_risk_color(vuln.get('risk', 'medium'))
                risk_text = vuln.get('risk', 'orta').upper()
                
                print(f"{Fore.WHITE}[{idx}] {risk_color}[{risk_text}]{Style.RESET_ALL} {vuln['message']}")
                
                if vuln.get('details'):
                    print(f"    {Fore.YELLOW}→ {vuln['details']}{Style.RESET_ALL}")
                
                if vuln.get('solution'):
                    print(f"    {Fore.GREEN}✓ Çözüm: {vuln['solution']}{Style.RESET_ALL}")
                
                print()
                time.sleep(0.3)
        
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
    
    def get_risk_color(self, risk_level):
        """Risk seviyesine göre renk döndür"""
        risk_colors = {
            'low': Fore.YELLOW,
            'medium': Fore.MAGENTA,
            'high': Fore.RED,
            'critical': Fore.RED + Style.BRIGHT
        }
        return risk_colors.get(risk_level.lower(), Fore.MAGENTA)
    
    def display_history(self, history):
        """Tarama geçmişini göster"""
        self.clear_screen()
        self.print_header()
        
        print(Fore.YELLOW + Style.BRIGHT + "TARAMA GEÇMİŞİ")
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
        print()
        
        if not history:
            print(Fore.YELLOW + "Henüz tarama geçmişi yok.")
        else:
            for idx, scan in enumerate(reversed(history[-10:]), 1):
                date = scan.get('date', 'Bilinmiyor')
                vuln_count = scan.get('vulnerability_count', 0)
                
                color = Fore.GREEN if vuln_count == 0 else Fore.RED
                print(f"{Fore.WHITE}[{idx}] {date}")
                print(f"    {color}→ {vuln_count} güvenlik açığı{Style.RESET_ALL}")
                print()
        
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
    
    def display_settings(self, config):
        """Ayarları göster"""
        self.clear_screen()
        self.print_header()
        
        print(Fore.YELLOW + Style.BRIGHT + "AYARLAR")
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
        print()
        
        print(f"{Fore.GREEN}1){Fore.WHITE} Otomatik rapor oluştur: {config.get('auto_report', False)}")
        print(f"{Fore.GREEN}2){Fore.WHITE} Rapor formatı: {config.get('report_format', 'txt')}")
        print(f"{Fore.GREEN}3){Fore.WHITE} Log seviyesi: {config.get('log_level', 'INFO')}")
        print(f"{Fore.GREEN}4){Fore.WHITE} Detaylı tarama: {config.get('detailed_scan', True)}")
        print(f"{Fore.GREEN}5){Fore.WHITE} Geri Dön")
        print()
        
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
    
    def display_about(self):
        """Hakkında bilgisi göster"""
        self.clear_screen()
        self.print_header()
        
        print(Fore.YELLOW + Style.BRIGHT + "HAKKINDA")
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
        print()
        
        print(Fore.WHITE + "Siber Güvenlik Tarama Aracı " + Fore.CYAN + "v2.0")
        print()
        print("Sisteminizin temel güvenlik açıklarını tespit eden")
        print("profesyonel bir masaüstü uygulaması.")
        print()
        print(Fore.RED + Style.BRIGHT + "⚠ UYARI:")
        print(Fore.YELLOW + "Bu araç sadece kendi sisteminizde kullanılmalıdır.")
        print("Başkasının sistemini izinsiz taramak yasa dışıdır.")
        print()
        print(Fore.GREEN + "Özellikler:")
        features = [
            "✓ 18 güvenlik kontrolü",
            "✓ Kritik risk tespiti (SMBv1, BitLocker, vs.)",
            "✓ Detaylı raporlama (TXT, JSON, HTML)",
            "✓ Tarama geçmişi",
            "✓ Çözüm önerileri",
            "✓ Log kayıt sistemi",
            "✓ Risk seviyesi analizi"
        ]
        for feature in features:
            print(f"  {feature}")
        
        print()
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
    
    def get_input(self, prompt="Seçiminiz: "):
        """Kullanıcıdan girdi al"""
        return input(Fore.GREEN + prompt + Style.RESET_ALL).strip()
    
    def pause(self, message="Devam etmek için Enter'a basın..."):
        """Duraklatma"""
        input(f"\n{Fore.YELLOW}{message}{Style.RESET_ALL}")
    
    def show_error(self, message):
        """Hata mesajı göster"""
        print(f"\n{Fore.RED}❌ Hata: {message}{Style.RESET_ALL}")
        time.sleep(2)
    
    def show_success(self, message):
        """Başarı mesajı göster"""
        print(f"\n{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
        time.sleep(1)
    
    def run(self):
        """Ana UI döngüsü"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = self.get_input()
            
            if choice == '1':
                self.handle_scan()
            elif choice == '2':
                self.handle_history()
            elif choice == '3':
                self.handle_report()
            elif choice == '4':
                self.handle_statistics()
            elif choice == '5':
                self.handle_settings()
            elif choice == '6':
                self.handle_about()
            elif choice == '7':
                self.handle_exit()
                break
            else:
                self.show_error("Geçersiz seçim! Lütfen 1-7 arası bir değer girin.")
    
    def handle_scan(self):
        """Tarama işlemini yönet"""
        self.clear_screen()
        self.print_header()
        print(Fore.YELLOW + "Güvenlik taraması başlatılıyor...\n" + Style.RESET_ALL)
        
        # Scanner'dan tarama yap
        result = self.scanner.perform_scan(progress_callback=self.display_scan_progress)
        
        # Sonuçları göster
        self.display_results(result['vulnerabilities'], result['scan_info'])
        self.pause()
    
    def handle_history(self):
        """Geçmiş işlemini yönet"""
        history = self.scanner.get_history()
        self.display_history(history)
        self.pause()
    
    def handle_report(self):
        """Rapor işlemini yönet"""
        self.clear_screen()
        self.print_header()
        print(Fore.YELLOW + "RAPOR OLUŞTUR")
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
        print()
        print(f"{Fore.GREEN}1){Fore.WHITE} TXT Raporu")
        print(f"{Fore.GREEN}2){Fore.WHITE} JSON Raporu")
        print(f"{Fore.GREEN}3){Fore.WHITE} HTML Raporu")
        print(f"{Fore.GREEN}4){Fore.WHITE} Geri Dön")
        print()
        
        choice = self.get_input()
        
        if choice in ['1', '2', '3']:
            format_map = {'1': 'txt', '2': 'json', '3': 'html'}
            report_format = format_map[choice]
            
            filename = self.scanner.generate_report(report_format)
            if filename:
                self.show_success(f"Rapor oluşturuldu: {filename}")
            else:
                self.show_error("Rapor oluşturulamadı. Önce bir tarama yapın.")
            self.pause()
    
    def handle_statistics(self):
        """İstatistik işlemini yönet"""
        self.clear_screen()
        self.print_header()
        
        print(Fore.YELLOW + Style.BRIGHT + "İSTATİSTİKLER")
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
        print()
        
        stats = self.scanner.get_statistics()
        
        if stats['total_scans'] == 0:
            print(Fore.YELLOW + "Henüz hiç tarama yapılmadı.")
        else:
            print(f"{Fore.GREEN}Toplam Tarama:{Style.RESET_ALL} {stats['total_scans']}")
            print(f"{Fore.GREEN}Toplam Güvenlik Açığı:{Style.RESET_ALL} {stats['total_vulnerabilities']}")
            print(f"{Fore.GREEN}Ortalama Açık/Tarama:{Style.RESET_ALL} {stats['average_vulnerabilities']}")
            print(f"{Fore.GREEN}Son Tarama:{Style.RESET_ALL} {stats['last_scan_date']}")
            
            if stats['most_vulnerable_scan']:
                most_vuln = stats['most_vulnerable_scan']
                print()
                print(Fore.RED + "En Çok Açık Bulunan Tarama:")
                print(f"  • Tarih: {most_vuln.get('date', 'Bilinmiyor')}")
                print(f"  • Açık Sayısı: {most_vuln.get('vulnerability_count', 0)}")
        
        print()
        print(Fore.CYAN + "=" * self.width + Style.RESET_ALL)
        self.pause()
    
    def handle_settings(self):
        """Ayarlar işlemini yönet"""
        config = self.scanner.get_config()
        self.display_settings(config)
        
        choice = self.get_input()
        
        if choice == '5':
            return
        
        # Ayar değişikliklerini yönet (gelecek özellik)
        self.show_success("Bu özellik yakında eklenecek...")
        self.pause()
    
    def handle_about(self):
        """Hakkında işlemini yönet"""
        self.display_about()
        self.pause()
    
    def handle_exit(self):
        """Çıkış işlemini yönet"""
        self.clear_screen()
        print(Fore.YELLOW + "Program sonlandırılıyor..." + Style.RESET_ALL)
        time.sleep(1)
        print(Fore.GREEN + "Güvenli kalın! 🛡️" + Style.RESET_ALL)
        time.sleep(0.5)