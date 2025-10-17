"""
Güvenlik Kontrolleri Modülü
Her bir güvenlik kontrolünün detaylı implementasyonu
"""

import subprocess
import platform
import socket
import re


class SecurityChecks:
    """Güvenlik kontrol fonksiyonları"""
    
    def __init__(self, logger):
        self.logger = logger
        self.system = platform.system()
    
    def _run_command(self, command, timeout=5):
        """
        Güvenli komut çalıştırma
        
        Args:
            command: Çalıştırılacak komut (liste)
            timeout: Zaman aşımı süresi
            
        Returns:
            tuple: (stdout, stderr, returncode)
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',  # Encoding hatalarını görmezden gel
                timeout=timeout,
                creationflags=subprocess.CREATE_NO_WINDOW if self.system == "Windows" else 0
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Komut zaman aşımına uğradı: {' '.join(command)}")
            return "", "Timeout", -1
        except Exception as e:
            self.logger.error(f"Komut çalıştırma hatası: {e}")
            return "", str(e), -1
    
    def check_windows_defender(self):
        """Windows Defender durumunu kontrol et"""
        if self.system != "Windows":
            return None
        
        try:
            # PowerShell ile Windows Defender durumunu kontrol et
            stdout, stderr, returncode = self._run_command([
                'powershell',
                '-Command',
                'Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled'
            ])
            
            if returncode == 0 and stdout:
                # AntivirusEnabled ve RealTimeProtectionEnabled kontrol et
                if 'False' in stdout:
                    details = "Windows Defender veya gerçek zamanlı koruma devre dışı"
                    
                    return {
                        'message': 'Windows Defender tam olarak aktif değil',
                        'details': details,
                        'risk': 'high',
                        'solution': 'Windows Güvenliği > Virüs ve tehdit koruması bölümünden Windows Defender\'ı etkinleştirin'
                    }
            
            # Alternatif kontrol: Windows Defender servisi
            stdout2, _, returncode2 = self._run_command(['sc', 'query', 'WinDefend'])
            
            if returncode2 == 0 and ('STOPPED' in stdout2 or '1060' in stdout2):
                return {
                    'message': 'Windows Defender servisi çalışmıyor',
                    'details': 'WinDefend servisi durdurulmuş veya mevcut değil',
                    'risk': 'critical',
                    'solution': 'Windows Defender servisini başlatın: services.msc > Windows Defender'
                }
                
        except Exception as e:
            self.logger.error(f"Windows Defender kontrolünde hata: {e}")
        
        return None
    
    def check_firewall(self):
        """Güvenlik duvarı durumunu kontrol et"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'netsh', 'advfirewall', 'show', 'allprofiles', 'state'
            ])
            
            if returncode == 0 and stdout:
                # Kapalı profilleri bul
                off_profiles = []
                
                if 'Domain Profile' in stdout:
                    domain_section = stdout.split('Domain Profile')[1].split('\n')[0:3]
                    if any('OFF' in line for line in domain_section):
                        off_profiles.append('Domain')
                
                if 'Private Profile' in stdout:
                    private_section = stdout.split('Private Profile')[1].split('\n')[0:3]
                    if any('OFF' in line for line in private_section):
                        off_profiles.append('Private')
                
                if 'Public Profile' in stdout:
                    public_section = stdout.split('Public Profile')[1].split('\n')[0:3]
                    if any('OFF' in line for line in public_section):
                        off_profiles.append('Public')
                
                if off_profiles:
                    profiles_str = ', '.join(off_profiles)
                    return {
                        'message': f'Güvenlik duvarı bazı profillerde kapalı',
                        'details': f'Kapalı profiller: {profiles_str}',
                        'risk': 'high',
                        'solution': 'Windows Güvenliği > Güvenlik duvarı ve ağ koruması bölümünden güvenlik duvarını tüm profillerde etkinleştirin'
                    }
                    
        except Exception as e:
            self.logger.error(f"Güvenlik duvarı kontrolünde hata: {e}")
        
        return None
    
    def check_open_ports(self):
        """Açık portları kontrol et"""
        try:
            # Yaygın riskli portlar
            risky_ports = {
                21: 'FTP',
                22: 'SSH',
                23: 'Telnet',
                25: 'SMTP',
                135: 'RPC',
                139: 'NetBIOS',
                445: 'SMB',
                1433: 'SQL Server',
                3306: 'MySQL',
                3389: 'RDP',
                5900: 'VNC',
                8080: 'HTTP Proxy'
            }
            
            open_ports = []
            
            for port, service in risky_ports.items():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                result = sock.connect_ex(('127.0.0.1', port))
                
                if result == 0:
                    open_ports.append(f"{port} ({service})")
                
                sock.close()
            
            if open_ports:
                ports_str = ', '.join(open_ports)
                port_count = len(open_ports)
                
                # Risk seviyesi belirleme
                risk = 'low'
                if port_count >= 3:
                    risk = 'high'
                elif port_count >= 2:
                    risk = 'medium'
                
                return {
                    'message': f'{port_count} adet açık port tespit edildi',
                    'details': f'Açık portlar: {ports_str}',
                    'risk': risk,
                    'solution': 'Kullanılmayan servisleri kapatın ve güvenlik duvarı kurallarını gözden geçirin'
                }
                
        except Exception as e:
            self.logger.error(f"Port taramasında hata: {e}")
        
        return None
    
    def check_admin_account(self):
        """Administrator hesabı durumunu kontrol et"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'net', 'user', 'Administrator'
            ])
            
            if returncode == 0 and stdout:
                # Hesap aktif mi kontrol et
                if 'Account active' in stdout and 'Yes' in stdout:
                    return {
                        'message': 'Varsayılan Administrator hesabı aktif',
                        'details': 'Administrator hesabı güvenlik riski oluşturur',
                        'risk': 'medium',
                        'solution': 'Administrator hesabını devre dışı bırakın: net user Administrator /active:no'
                    }
                    
        except Exception as e:
            self.logger.error(f"Administrator hesabı kontrolünde hata: {e}")
        
        return None
    
    def check_password_policy(self):
        """Şifre politikasını kontrol et"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'net', 'accounts'
            ])
            
            if returncode == 0 and stdout:
                issues = []
                
                # Minimum şifre uzunluğu
                min_length_match = re.search(r'Minimum password length\s*:\s*(\d+)', stdout)
                if min_length_match:
                    min_length = int(min_length_match.group(1))
                    if min_length < 8:
                        issues.append(f'Minimum şifre uzunluğu çok düşük ({min_length} karakter)')
                
                # Maksimum şifre yaşı
                max_age_match = re.search(r'Maximum password age \(days\)\s*:\s*(\d+|Unlimited)', stdout)
                if max_age_match:
                    max_age = max_age_match.group(1)
                    if max_age == 'Unlimited' or (max_age.isdigit() and int(max_age) > 90):
                        issues.append('Şifre süresiz veya çok uzun (90+ gün)')
                
                # Şifre geçmişi
                history_match = re.search(r'Length of password history maintained\s*:\s*(\d+)', stdout)
                if history_match:
                    history = int(history_match.group(1))
                    if history < 5:
                        issues.append(f'Şifre geçmişi yetersiz ({history} önceki şifre)')
                
                if issues:
                    return {
                        'message': 'Zayıf şifre politikası tespit edildi',
                        'details': '; '.join(issues),
                        'risk': 'medium',
                        'solution': 'Güvenlik Politikası düzenleyicisinde şifre politikalarını güçlendirin (secpol.msc)'
                    }
                    
        except Exception as e:
            self.logger.error(f"Şifre politikası kontrolünde hata: {e}")
        
        return None
    
    def check_auto_updates(self):
        """Otomatik güncellemeleri kontrol et"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'powershell',
                '-Command',
                '(New-Object -ComObject Microsoft.Update.AutoUpdate).Settings.NotificationLevel'
            ])
            
            if returncode == 0 and stdout.strip():
                level = stdout.strip()
                
                # Notification Level:
                # 0 = Not configured
                # 1 = Disabled
                # 2 = Notify before download
                # 3 = Notify before installation
                # 4 = Scheduled installation (İdeal)
                
                if level in ['0', '1', '2']:
                    level_text = {
                        '0': 'Yapılandırılmamış',
                        '1': 'Devre dışı',
                        '2': 'İndirmeden önce bildirim'
                    }
                    
                    return {
                        'message': 'Otomatik güncellemeler tam olarak etkin değil',
                        'details': f'Güncelleme seviyesi: {level_text.get(level, level)}',
                        'risk': 'medium',
                        'solution': 'Windows Update ayarlarından otomatik güncellemeleri etkinleştirin'
                    }
            
            # Alternatif kontrol: Windows Update servisi
            stdout2, _, returncode2 = self._run_command(['sc', 'query', 'wuauserv'])
            
            if returncode2 == 0 and 'STOPPED' in stdout2:
                return {
                    'message': 'Windows Update servisi çalışmıyor',
                    'details': 'wuauserv servisi durdurulmuş',
                    'risk': 'high',
                    'solution': 'Windows Update servisini başlatın ve otomatik başlatmaya ayarlayın'
                }
                    
        except Exception as e:
            self.logger.error(f"Otomatik güncelleme kontrolünde hata: {e}")
        
        return None
    
    def check_shared_folders(self):
        """Paylaşılan klasörleri kontrol et"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'net', 'share'
            ])
            
            if returncode == 0 and stdout:
                # Satırları ayır ve paylaşımları filtrele
                lines = stdout.split('\n')
                shares = []
                
                for line in lines:
                    line = line.strip()
                    # Başlık ve boş satırları atla
                    if not line or 'Share name' in line or line.startswith('-') or 'The command' in line:
                        continue
                    
                    # Varsayılan sistem paylaşımlarını atla
                    if any(default in line for default in ['IPC$', 'ADMIN$', 'C$', 'D$', 'print$']):
                        continue
                    
                    # Paylaşım adını al
                    share_name = line.split()[0] if line.split() else None
                    if share_name:
                        shares.append(share_name)
                
                if shares:
                    shares_str = ', '.join(shares)
                    share_count = len(shares)
                    
                    # Risk seviyesi
                    risk = 'low'
                    if share_count >= 3:
                        risk = 'medium'
                    
                    return {
                        'message': f'{share_count} adet dosya paylaşımı tespit edildi',
                        'details': f'Paylaşımlar: {shares_str}',
                        'risk': risk,
                        'solution': 'Gereksiz dosya paylaşımlarını kaldırın ve paylaşım izinlerini gözden geçirin'
                    }
                    
        except Exception as e:
            self.logger.error(f"Paylaşılan klasör kontrolünde hata: {e}")
        
        return None
    
    def check_uac_settings(self):
        """UAC (User Account Control) ayarlarını kontrol et"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'reg', 'query',
                'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System',
                '/v', 'EnableLUA'
            ])
            
            if returncode == 0 and stdout:
                if 'EnableLUA' in stdout and '0x0' in stdout:
                    return {
                        'message': 'UAC (Kullanıcı Hesabı Denetimi) devre dışı',
                        'details': 'Sistem yönetici izinleri konusunda uyarmıyor',
                        'risk': 'high',
                        'solution': 'Denetim Masası > Kullanıcı Hesapları > UAC ayarlarını değiştir'
                    }
                    
        except Exception as e:
            self.logger.error(f"UAC kontrolünde hata: {e}")
        
        return None
    
    def check_remote_desktop(self):
        """Uzak Masaüstü (RDP) durumunu kontrol et"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'reg', 'query',
                'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server',
                '/v', 'fDenyTSConnections'
            ])
            
            if returncode == 0 and stdout:
                # 0 = RDP Etkin, 1 = RDP Devre Dışı
                if 'fDenyTSConnections' in stdout and '0x0' in stdout:
                    return {
                        'message': 'Uzak Masaüstü (RDP) etkin',
                        'details': 'RDP güvenlik riski oluşturabilir',
                        'risk': 'medium',
                        'solution': 'Kullanılmıyorsa RDP\'yi devre dışı bırakın veya güçlü kimlik doğrulama kullanın'
                    }
                    
        except Exception as e:
            self.logger.error(f"RDP kontrolünde hata: {e}")
        
        return None
    
    def check_usb_autorun(self):
        """USB otomatik çalıştırma kontrolü"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'reg', 'query',
                'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer',
                '/v', 'NoDriveTypeAutoRun'
            ])
            
            if returncode == 0 and stdout:
                # 255 (0xFF) = Tüm sürücülerde autorun kapalı (GÜVENLİ)
                # Düşük değer = Autorun açık (RİSKLİ)
                if 'NoDriveTypeAutoRun' in stdout:
                    if '0xff' not in stdout.lower() and '0x0' not in stdout:
                        return None  # Güvenli
                    
            # Kayıt yoksa veya 0x0 ise tehlikeli
            return {
                'message': 'USB otomatik çalıştırma etkin',
                'details': 'USB bellekler zararlı yazılım yayabilir',
                'risk': 'medium',
                'solution': 'USB autorun\'ı devre dışı bırakın: gpedit.msc > Bilgisayar Yapılandırması > Yönetim Şablonları'
            }
                    
        except Exception as e:
            self.logger.error(f"USB autorun kontrolünde hata: {e}")
        
        return None
    
    def check_bitlocker(self):
        """BitLocker disk şifreleme kontrolü"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'powershell',
                '-Command',
                'Get-BitLockerVolume | Select-Object MountPoint, ProtectionStatus'
            ])
            
            if returncode == 0 and stdout:
                # ProtectionStatus: Off = Şifresiz, On = Şifreli
                if 'Off' in stdout or 'ProtectionStatus' not in stdout:
                    return {
                        'message': 'Disk şifreleme (BitLocker) kapalı',
                        'details': 'Verileriniz fiziksel erişimde korumasız',
                        'risk': 'medium',
                        'solution': 'BitLocker\'ı etkinleştirin: Denetim Masası > BitLocker Sürücü Şifrelemesi'
                    }
                    
        except Exception as e:
            self.logger.error(f"BitLocker kontrolünde hata: {e}")
        
        return None
    
    def check_smb_v1(self):
        """SMB v1 protokol kontrolü (Eski ve tehlikeli)"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'powershell',
                '-Command',
                'Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol'
            ])
            
            if returncode == 0 and stdout:
                if 'State' in stdout and 'Enabled' in stdout:
                    return {
                        'message': 'SMBv1 protokolü etkin (TEHLİKELİ!)',
                        'details': 'WannaCry ve NotPetya bu protokolü kullandı',
                        'risk': 'critical',
                        'solution': 'SMBv1\'i devre dışı bırakın: Denetim Masası > Windows Özellikleri > SMB 1.0/CIFS'
                    }
                    
        except Exception as e:
            self.logger.error(f"SMB v1 kontrolünde hata: {e}")
        
        return None
    
    def check_powershell_logging(self):
        """PowerShell Script Block Logging kontrolü"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'reg', 'query',
                'HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\ScriptBlockLogging',
                '/v', 'EnableScriptBlockLogging'
            ])
            
            if returncode != 0 or 'EnableScriptBlockLogging' not in stdout or '0x1' not in stdout:
                return {
                    'message': 'PowerShell Script Block Logging kapalı',
                    'details': 'PowerShell saldırıları tespit edilemiyor',
                    'risk': 'medium',
                    'solution': 'PowerShell logging\'i etkinleştirin: gpedit.msc > Yönetim Şablonları > Windows PowerShell'
                }
                    
        except Exception as e:
            self.logger.error(f"PowerShell logging kontrolünde hata: {e}")
        
        return None
    
    def check_wsh(self):
        """Windows Script Host (WSH) kontrolü"""
        if self.system != "Windows":
            return None
        
        try:
            # WSH'nin devre dışı olup olmadığını kontrol et
            stdout, stderr, returncode = self._run_command([
                'reg', 'query',
                'HKLM\\SOFTWARE\\Microsoft\\Windows Script Host\\Settings',
                '/v', 'Enabled'
            ])
            
            # Kayıt yoksa veya 1 ise WSH aktif (Risk)
            if returncode != 0 or 'Enabled' not in stdout or '0x1' in stdout or '0x0' not in stdout:
                return {
                    'message': 'Windows Script Host (WSH) etkin',
                    'details': 'VBS/JS zararlı script\'leri çalışabilir',
                    'risk': 'low',
                    'solution': 'Gerekmedikçe WSH\'yi devre dışı bırakın: reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Script Host\\Settings" /v Enabled /t REG_DWORD /d 0 /f'
                }
                    
        except Exception as e:
            self.logger.error(f"WSH kontrolünde hata: {e}")
        
        return None
    
    def check_guest_account(self):
        """Misafir hesabı kontrolü"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'net', 'user', 'Guest'
            ])
            
            if returncode == 0 and stdout:
                if 'Account active' in stdout and 'Yes' in stdout:
                    return {
                        'message': 'Misafir (Guest) hesabı aktif',
                        'details': 'Yetkisiz erişime kapı açar',
                        'risk': 'medium',
                        'solution': 'Guest hesabını devre dışı bırakın: net user Guest /active:no'
                    }
                    
        except Exception as e:
            self.logger.error(f"Guest hesabı kontrolünde hata: {e}")
        
        return None
    
    def check_blank_passwords(self):
        """Boş şifreli hesaplar kontrolü"""
        if self.system != "Windows":
            return None
        
        try:
            # Boş şifre politikası kontrolü
            stdout, stderr, returncode = self._run_command([
                'net', 'accounts'
            ])
            
            if returncode == 0 and stdout:
                # Minimum şifre uzunluğu 0 ise boş şifreye izin veriliyor
                if 'Minimum password length' in stdout and ': 0' in stdout:
                    return {
                        'message': 'Boş şifrelere izin veriliyor',
                        'details': 'Kullanıcılar şifresiz hesap oluşturabilir',
                        'risk': 'high',
                        'solution': 'Minimum şifre uzunluğunu artırın: net accounts /minpwlen:8'
                    }
                    
        except Exception as e:
            self.logger.error(f"Boş şifre kontrolünde hata: {e}")
        
        return None
    
    def check_screen_saver_password(self):
        """Ekran koruyucu şifre kontrolü"""
        if self.system != "Windows":
            return None
        
        try:
            stdout, stderr, returncode = self._run_command([
                'reg', 'query',
                'HKCU\\Control Panel\\Desktop',
                '/v', 'ScreenSaverIsSecure'
            ])
            
            # 0x0 veya kayıt yoksa şifre koruması yok
            if returncode != 0 or 'ScreenSaverIsSecure' not in stdout or '0x0' in stdout:
                return {
                    'message': 'Ekran koruyucu şifre koruması yok',
                    'details': 'Bilgisayar başında olmadığınızda başkaları erişebilir',
                    'risk': 'low',
                    'solution': 'Ekran koruyucu şifresini etkinleştirin: Ayarlar > Kişiselleştirme > Kilit ekranı'
                }
                    
        except Exception as e:
            self.logger.error(f"Ekran koruyucu kontrolünde hata: {e}")
        
        return None
    
    def check_network_discovery(self):
        """Ağ keşfi (Network Discovery) kontrolü"""
        if self.system != "Windows":
            return None
        
        try:
            # FDResPub servisi Network Discovery için gerekli
            stdout, stderr, returncode = self._run_command([
                'sc', 'query', 'FDResPub'
            ])
            
            if returncode == 0 and stdout:
                if 'RUNNING' in stdout:
                    return {
                        'message': 'Ağ keşfi (Network Discovery) etkin',
                        'details': 'Bilgisayarınız ağda görünür durumda',
                        'risk': 'low',
                        'solution': 'Genel ağlarda Network Discovery\'yi kapatın: Denetim Masası > Ağ ve Paylaşım Merkezi'
                    }
                    
        except Exception as e:
            self.logger.error(f"Network Discovery kontrolünde hata: {e}")
        
        return None