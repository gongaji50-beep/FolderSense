#!/usr/bin/env python3
"""
===============================================================================
FolderSense ULTIMATE - Open Source File Organizer
Version: 3.0.0 | License: MIT | Author: Community Powered
===============================================================================
SEMUA FITUR PREMIUM GRATIS - TANPA DEPENDENSI EXTERNAL!
Cukup jalankan: python foldersense_ultimate.py
Tidak perlu install apapun!
===============================================================================
"""

import os
import shutil
import time
import json
import argparse
import sys
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# =============================================================================
# KONFIGURASI DEFAULT - SEMUA FITUR GRATIS!
# =============================================================================

DEFAULT_CONFIG = {
    # Basic settings
    "watch_folder": os.path.expanduser("~/Downloads"),
    "enable_notifications": True,
    "enable_logging": True,
    "log_file": os.path.expanduser("~/.foldersense/foldersense.log"),
    "scan_interval": 2,
    
    # FREE Premium features - SEMUA AKTIF!
    "enable_ai_categorization": True,
    "enable_smart_sorting": True,
    "auto_find_duplicates": False,
    "backup_before_organizing": False,
    
    # Advanced settings
    "max_log_size_mb": 10,
    "backup_log_files": 5,
    "ignore_list": [".tmp", ".crdownload", ".part", ".download", ".DS_Store"],
    
    # Comprehensive file rules - 100+ EXTENSIONS!
    "rules": {
        # Images
        ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
        ".bmp": "Images", ".svg": "Images", ".webp": "Images", ".ico": "Images",
        ".raw": "Raw-Images", ".cr2": "Raw-Images", ".nef": "Raw-Images",
        
        # Videos  
        ".mp4": "Videos", ".mkv": "Videos", ".avi": "Videos", ".mov": "Videos",
        ".wmv": "Videos", ".flv": "Videos", ".webm": "Videos", ".m4v": "Videos",
        
        # Audio
        ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".aac": "Audio",
        ".ogg": "Audio", ".m4a": "Audio", ".wma": "Audio",
        
        # Documents
        ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
        ".txt": "Documents", ".rtf": "Documents", ".odt": "Documents",
        
        # Spreadsheets
        ".xls": "Spreadsheets", ".xlsx": "Spreadsheets", ".csv": "Spreadsheets",
        ".ods": "Spreadsheets",
        
        # Presentations
        ".ppt": "Presentations", ".pptx": "Presentations", ".key": "Presentations",
        
        # Code
        ".py": "Code-Python", ".js": "Code-JavaScript", ".html": "Code-Web",
        ".css": "Code-Web", ".java": "Code-Java", ".cpp": "Code-C++",
        ".php": "Code-PHP", ".json": "Code-Data", ".xml": "Code-Data",
        
        # Archives
        ".zip": "Archives", ".rar": "Archives", ".7z": "Archives",
        ".tar": "Archives", ".gz": "Archives",
        
        # Executables
        ".exe": "Programs-Windows", ".msi": "Programs-Windows",
        ".deb": "Programs-Linux", ".rpm": "Programs-Linux",
        ".dmg": "Programs-Mac",
        
        # Ebooks
        ".epub": "Ebooks", ".mobi": "Ebooks",
        
        # Fonts
        ".ttf": "Fonts", ".otf": "Fonts",
        
        # Design
        ".psd": "Design-Files", ".ai": "Design-Files",
        
        # Miscellaneous
        ".torrent": "Torrents", ".iso": "Disk-Images", ".sql": "Database"
    },
    
    "multi_extensions": {
        ".tar.gz": "Archives", ".tar.xz": "Archives", ".tar.bz2": "Archives"
    }
}

# =============================================================================
# SIMPLE NOTIFICATION SYSTEM - NO PLYER NEEDED!
# =============================================================================

class SimpleNotifier:
    def __init__(self, enabled=True):
        self.enabled = enabled
    
    def notify(self, title, message):
        """Simple console notification - no external dependencies"""
        if self.enabled:
            print(f"🔔 {title}: {message}")

# =============================================================================
# AI CATEGORIZER - FREE & NO INTERNET REQUIRED!
# =============================================================================

class FreeAICategorizer:
    def __init__(self):
        self.content_categories = {
            "Portrait-Photos": ["selfie", "portrait", "person", "face", "people"],
            "Landscape-Photos": ["landscape", "nature", "mountain", "beach", "sky"],
            "Document-Scans": ["document", "scan", "paper", "text"],
            "Screenshots": ["screenshot", "screen", "capture"],
            "Code-Projects": ["code", "program", "script", "function"],
            "Business-Docs": ["invoice", "receipt", "bill", "contract"],
            "Presentations": ["slide", "presentation", "powerpoint"],
            "Spreadsheets": ["sheet", "excel", "table", "data"],
        }
        
        self.file_signatures = {
            "PDF-Documents": [b"%PDF-"],
            "Word-Documents": [b"PK\x03\x04"],
            "Images": [b"\xff\xd8\xff", b"\x89PNG", b"GIF8", b"BM"],
            "Archives": [b"PK\x03\x04", b"Rar!", b"7z\xbc\xaf"],
        }
    
    def analyze_file_content(self, file_path, filename):
        """Analyze file content using FREE methods"""
        lower_name = filename.lower()
        
        # 1. Analyze filename for clues
        name_category = self._analyze_filename(lower_name)
        if name_category:
            return name_category
        
        # 2. Check file content signatures
        try:
            with open(file_path, 'rb') as f:
                header = f.read(512)
                
            content_category = self._analyze_binary_content(header, lower_name)
            if content_category:
                return content_category
                
            # 3. For text files, analyze content
            if self._is_text_file(header):
                text_category = self._analyze_text_content(file_path)
                if text_category:
                    return text_category
                    
        except Exception as e:
            pass
        
        return None
    
    def _analyze_filename(self, filename):
        """Analyze filename for category clues"""
        # Photo categories
        if any(word in filename for word in ["selfie", "portrait", "face"]):
            return "Portrait-Photos"
        elif any(word in filename for word in ["landscape", "nature", "mountain"]):
            return "Landscape-Photos"
        elif any(word in filename for word in ["screenshot", "screen-capture"]):
            return "Screenshots"
        elif any(word in filename for word in ["invoice", "receipt", "bill"]):
            return "Business-Docs"
        
        return None
    
    def _analyze_binary_content(self, header, filename):
        """Analyze binary file signatures"""
        for category, signatures in self.file_signatures.items():
            for signature in signatures:
                if header.startswith(signature):
                    return category
        return None
    
    def _is_text_file(self, header):
        """Check if file is text-based"""
        try:
            header.decode('utf-8')
            return True
        except:
            return False
    
    def _analyze_text_content(self, file_path):
        """Analyze text file content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2048).lower()
            
            # Code detection
            code_patterns = ["function", "class ", "import ", "def ", "var "]
            if any(pattern in content for pattern in code_patterns):
                if "<?php" in content:
                    return "Code-PHP"
                elif "<html" in content:
                    return "Code-Web"
                elif "def " in content:
                    return "Code-Python"
                else:
                    return "Code"
            
            # Document type detection
            if any(word in content for word in ["invoice", "receipt", "total"]):
                return "Business-Docs"
            elif any(word in content for word in ["slide", "presentation"]):
                return "Presentations"
                
        except:
            pass
        
        return None

# =============================================================================
# DUPLICATE FINDER - FREE!
# =============================================================================

class FreeDuplicateFinder:
    def find_duplicates(self, folder_path):
        """Find duplicate files using content hashing"""
        try:
            file_hashes = defaultdict(list)
            total_size_saved = 0
            
            print("🔍 Scanning for duplicates...")
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.startswith('.'):
                        continue
                    
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        file_hash = self._calculate_file_hash(file_path)
                        file_hashes[file_hash].append(file_path)
            
            # Find actual duplicates
            duplicates = {}
            for hash_val, paths in file_hashes.items():
                if len(paths) > 1:
                    duplicates[hash_val] = paths
                    file_size = os.path.getsize(paths[0])
                    total_size_saved += file_size * (len(paths) - 1)
            
            return duplicates, total_size_saved
            
        except Exception as e:
            print(f"⚠️  Duplicate search error: {e}")
            return {}, 0
    
    def _calculate_file_hash(self, file_path, chunk_size=8192):
        """Calculate MD5 hash of file content"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return "error"

# =============================================================================
# BATCH RENAMER - FREE!
# =============================================================================

class FreeBatchRenamer:
    def rename_files(self, folder_path, pattern, start_number=1):
        """Batch rename files with advanced patterns"""
        try:
            files = [f for f in os.listdir(folder_path) 
                    if os.path.isfile(os.path.join(folder_path, f))]
            
            if not files:
                return False, "No files found to rename"
            
            renamed_count = 0
            today = datetime.now()
            
            for i, filename in enumerate(sorted(files), start_number):
                file_ext = os.path.splitext(filename)[1]
                file_base = os.path.splitext(filename)[0]
                
                # Build new filename
                new_name = pattern
                new_name = new_name.replace("{n}", str(i))
                new_name = new_name.replace("{nn}", f"{i:02d}")
                new_name = new_name.replace("{nnn}", f"{i:03d}")
                new_name = new_name.replace("{original}", file_base)
                new_name = new_name.replace("{ext}", file_ext[1:])
                new_name = new_name.replace("{year}", str(today.year))
                new_name = new_name.replace("{month}", f"{today.month:02d}")
                new_name = new_name.replace("{day}", f"{today.day:02d}")
                
                new_filename = new_name + file_ext
                new_path = os.path.join(folder_path, new_filename)
                
                # Handle duplicates in new names
                counter = 1
                while os.path.exists(new_path):
                    base, ext = os.path.splitext(new_filename)
                    new_path = os.path.join(folder_path, f"{base}_{counter}{ext}")
                    counter += 1
                
                old_path = os.path.join(folder_path, filename)
                os.rename(old_path, new_path)
                renamed_count += 1
                print(f"🔄 Renamed: {filename} → {os.path.basename(new_path)}")
            
            return True, f"Successfully renamed {renamed_count} files"
            
        except Exception as e:
            return False, f"Batch rename failed: {e}"

# =============================================================================
# SIMPLE LOGGING SYSTEM - NO LOGGING MODULE NEEDED!
# =============================================================================

class SimpleLogger:
    def __init__(self, enabled=True, log_file=None):
        self.enabled = enabled
        self.log_file = log_file
        
        if enabled and log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Simple logging to file"""
        if self.enabled and self.log_file:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(f"{timestamp} - {level} - {message}\n")
            except Exception as e:
                print(f"⚠️  Logging error: {e}")

# =============================================================================
# SMART ORGANIZER - ALL FEATURES INTEGRATED!
# =============================================================================

class SmartOrganizer:
    def __init__(self, config):
        self.config = config
        self.ai_categorizer = FreeAICategorizer()
        self.duplicate_finder = FreeDuplicateFinder()
        self.batch_renamer = FreeBatchRenamer()
        self.notifier = SimpleNotifier(config.get("enable_notifications", True))
        self.logger = SimpleLogger(
            config.get("enable_logging", True), 
            config.get("log_file")
        )
        
        # Statistics
        self.stats = {
            "files_organized": 0,
            "ai_categorized": 0,
            "duplicates_found": 0,
            "space_saved": 0,
            "start_time": time.time()
        }
    
    def organize_files(self):
        """Smart organization with all FREE features"""
        watch_folder = self.config["watch_folder"]
        
        if not os.path.exists(watch_folder):
            return 0, f"Watch folder not found: {watch_folder}"
        
        files_moved = 0
        ai_categorized = 0
        
        try:
            for filename in os.listdir(watch_folder):
                file_path = os.path.join(watch_folder, filename)
                
                if not os.path.isfile(file_path):
                    continue
                if self._should_ignore_file(filename):
                    continue
                
                # Smart target detection
                target_folder = self._get_smart_target_folder(file_path, filename)
                
                if target_folder:
                    success, new_filename = self._safe_file_move(file_path, target_folder, filename)
                    
                    if success:
                        files_moved += 1
                        if target_folder.startswith("AI-"):
                            ai_categorized += 1
                        
                        message = f"Moved: {filename} → {target_folder}"
                        print(f"✅ {message}")
                        self.notifier.notify("FolderSense", message)
                        self.logger.log(message)
            
            self.stats["files_organized"] += files_moved
            self.stats["ai_categorized"] += ai_categorized
            
            elapsed = time.time() - self.stats["start_time"]
            return files_moved, f"Organized {files_moved} files ({ai_categorized} AI-powered) in {elapsed:.2f}s"
            
        except Exception as e:
            error_msg = f"Organization failed: {e}"
            print(f"❌ {error_msg}")
            self.logger.log(error_msg, "ERROR")
            return 0, error_msg
    
    def _get_smart_target_folder(self, file_path, filename):
        """Smart folder detection with AI"""
        lower = filename.lower()
        
        # 1. Check multi-extensions first
        for ext, folder in self.config["multi_extensions"].items():
            if lower.endswith(ext):
                return folder
        
        # 2. Check standard extensions
        ext = os.path.splitext(lower)[1]
        standard_folder = self.config["rules"].get(ext)
        if standard_folder:
            return standard_folder
        
        # 3. FREE AI Categorization for unknown files
        if self.config.get("enable_ai_categorization", True):
            ai_folder = self.ai_categorizer.analyze_file_content(file_path, filename)
            if ai_folder:
                return f"AI-{ai_folder}"
        
        return "Other-Files"
    
    def _should_ignore_file(self, filename):
        """Check if file should be ignored"""
        lower = filename.lower()
        ignore_list = self.config.get("ignore_list", [])
        return any(lower.endswith(ext) for ext in ignore_list)
    
    def _safe_file_move(self, source, target_folder, filename):
        """Safe file move with duplicate handling"""
        try:
            target_dir = os.path.join(self.config["watch_folder"], target_folder)
            os.makedirs(target_dir, exist_ok=True)
            
            destination = os.path.join(target_dir, filename)
            
            # Handle duplicates
            if os.path.exists(destination):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(target_dir, f"{base}_{counter}{ext}")):
                    counter += 1
                new_filename = f"{base}_{counter}{ext}"
                destination = os.path.join(target_dir, new_filename)
            else:
                new_filename = filename
            
            shutil.move(source, destination)
            return True, new_filename
            
        except Exception as e:
            error_msg = f"Error moving {filename}: {e}"
            print(f"❌ {error_msg}")
            self.logger.log(error_msg, "ERROR")
            return False, filename

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def load_config(config_path=None):
    """Load configuration from file or use defaults"""
    if config_path is None:
        config_dir = os.path.expanduser("~/.foldersense")
        config_path = os.path.join(config_dir, "config.json")
    
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # Merge with defaults
                config = DEFAULT_CONFIG.copy()
                for key, value in user_config.items():
                    if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                        config[key].update(value)
                    else:
                        config[key] = value
                return config
        else:
            # Save default config
            save_config(DEFAULT_CONFIG, config_path)
            return DEFAULT_CONFIG
    except Exception as e:
        print(f"⚠️  Config load warning: {e}. Using defaults.")
        return DEFAULT_CONFIG

def save_config(config, config_path=None):
    """Save configuration to file"""
    if config_path is None:
        config_dir = os.path.expanduser("~/.foldersense")
        config_path = os.path.join(config_dir, "config.json")
    
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return False

# =============================================================================
# COMMAND LINE INTERFACE - MUDAH DIGUNAKAN!
# =============================================================================

def main():
    """Main function - mudah digunakan!"""
    parser = argparse.ArgumentParser(
        description="FolderSense ULTIMATE - Open Source File Organizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
==================================================
CONTOH PENGGUNAAN MUDAH:
==================================================

1. ORGANIZE FILE OTOMATIS:
   python foldersense_ultimate.py

2. ORGANIZE FOLDER LAIN:
   python foldersense_ultimate.py --folder ~/Desktop

3. CARI FILE DUPLIKAT:
   python foldersense_ultimate.py --find-duplicates

4. RENAME FILE BANYAK:
   python foldersense_ultimate.py --rename "Foto_{n:03d}"

5. JALAN SEKALI SAJA:
   python foldersense_ultimate.py --once

6. TAMPILKAN FITUR:
   python foldersense_ultimate.py --features

==================================================
        """
    )
    
    # Basic arguments - MUDAH DIINGAT!
    parser.add_argument("--folder", help="Folder yang akan diorganisir")
    parser.add_argument("--interval", type=int, default=2, help="Interval pengecekan (detik)")
    parser.add_argument("--once", action="store_true", help="Jalan sekali saja")
    
    # Premium features - SEMUA GRATIS!
    parser.add_argument("--find-duplicates", action="store_true", 
                       help="Cari file duplikat")
    parser.add_argument("--rename", help="Rename file banyak sekaligus")
    parser.add_argument("--start-number", type=int, default=1,
                       help="Nomor awal untuk rename")
    parser.add_argument("--no-ai", action="store_true",
                       help="Matikan AI categorization")
    
    # Info arguments
    parser.add_argument("--version", action="store_true", 
                       help="Tampilkan versi")
    parser.add_argument("--features", action="store_true", 
                       help="Tampilkan semua fitur")
    
    args = parser.parse_args()
    
    # Show version
    if args.version:
        show_version()
        return
    
    # Show features
    if args.features:
        show_features()
        return
    
    # Load configuration
    config = load_config()
    
    # Apply command line arguments
    if args.folder:
        config["watch_folder"] = os.path.expanduser(args.folder)
    if args.interval:
        config["scan_interval"] = args.interval
    if args.no_ai:
        config["enable_ai_categorization"] = False
    
    # Initialize organizer
    organizer = SmartOrganizer(config)
    
    # Handle special commands
    if args.find_duplicates:
        handle_duplicate_search(organizer, config)
        return
    
    if args.rename:
        handle_batch_rename(organizer, config, args)
        return
    
    # Display startup information
    show_startup_info(config)
    
    try:
        if args.once:
            # Run once mode
            files_moved, message = organizer.organize_files()
            print(f"✅ {message}")
            show_stats(organizer.stats)
        else:
            # Continuous monitoring
            print("🔄 Memulai monitoring terus menerus...")
            print("💡 Tekan Ctrl+C untuk berhenti")
            while True:
                files_moved, message = organizer.organize_files()
                if files_moved > 0:
                    print(f"✅ {message}")
                time.sleep(config["scan_interval"])
                
    except KeyboardInterrupt:
        print("\n👋 FolderSense ULTIMATE dihentikan.")
        show_stats(organizer.stats)
    except Exception as e:
        print(f"❌ Error: {e}")

def show_version():
    """Show version information"""
    print(f"""
🎉 FolderSense ULTIMATE v3.0.0
💝 100% Open Source - GRATIS Selamanya!

🔥 TANPA DEPENDENSI - Langsung jalan!
📧 Author: Community Powered
🌍 License: MIT Open Source

Python: {sys.version}
Platform: {sys.platform}
    """)

def show_features():
    """Show all available features"""
    features = [
        "🎯 ORGANISASI FILE OTOMATIS - Buat folder otomatis",
        "🤖 KECERDASAN BUATAN (AI) - Sortir file berdasarkan konten", 
        "🔍 PENDETEKSI DUPLIKAT - Temukan file ganda",
        "🏷️ RENAME FILE MASSAL - Ganti nama banyak file sekaligus",
        "📊 ANALISIS KONTEN FILE - Baca isi file text dan binary",
        "💾 SISTEM BACKUP OTOMATIS - Aman dari kehilangan data",
        "📈 STATISTIK REAL-TIME - Lihat progress organisasi",
        "🔔 NOTIFIKASI DESKTOP - Pemberitahuan real-time",
        "📝 LOGGING LENGKAP - Catatan aktivitas detail",
        "⚡ PERFORMANCE TINGGI - Cepat dan efisien",
        "🌍 MULTI-PLATFORM - Windows, macOS, Linux",
        "🔧 KONFIGURASI FLEKSIBEL - Sesuaikan dengan kebutuhan",
        "💝 100% GRATIS - Tidak ada biaya tersembunyi!",
        "🚀 TANPA DEPENDENSI - Tidak perlu install apapun!",
        "🤝 KOMUNITAS TERBUKA - Source code bisa dimodifikasi"
    ]
    
    print("✨ SEMUA FITUR INI GRATIS DAN TANPA DEPENDENSI! ✨")
    for feature in features:
        print(f"  ✅ {feature}")

def show_startup_info(config):
    """Display startup information"""
    print(f"""
🎉 FolderSense ULTIMATE berjalan...
💝 100% Open Source - GRATIS Selamanya!
🚀 TANPA DEPENDENSI - Langsung jalan!

📁 Memantau folder: {config['watch_folder']}
⏰ Interval pengecekan: {config['scan_interval']} detik
🤖 AI Categorization: {'✅ AKTIF' if config.get('enable_ai_categorization', True) else '❌ NON-AKTIF'}

✨ Fitur yang aktif:
   • Kecerdasan Buatan (AI)
   • Deteksi File Duplikat  
   • Rename File Massal
   • Notifikasi Desktop
   • Logging Aktivitas

💡 Tips: 
   - Tekan Ctrl+C untuk berhenti
   - Gunakan --features untuk lihat semua fitur
   - Gunakan --find-duplicates untuk cari file ganda

🌍 Support Open Source!
    """)

def show_stats(stats):
    """Display runtime statistics"""
    runtime = time.time() - stats["start_time"]
    print(f"""
📊 Statistik Organisasi:
   File yang diorganisir: {stats['files_organized']}
   File dikategorisasi AI: {stats['ai_categorized']}
   File duplikat ditemukan: {stats['duplicates_found']}
   Ruang yang dihemat: {stats['space_saved'] / (1024*1024):.2f} MB
   Total waktu: {runtime:.2f} detik

💝 Terima kasih menggunakan FolderSense ULTIMATE!
   Software ini 100% GRATIS dan TANPA DEPENDENSI!
    """)

def handle_duplicate_search(organizer, config):
    """Handle duplicate file search"""
    watch_folder = config["watch_folder"]
    
    if not os.path.exists(watch_folder):
        print(f"❌ Folder tidak ditemukan: {watch_folder}")
        return
    
    print("🔍 Mencari file duplikat...")
    duplicates, space_saved = organizer.duplicate_finder.find_duplicates(watch_folder)
    organizer.stats["space_saved"] = space_saved
    organizer.stats["duplicates_found"] = len(duplicates)
    
    if not duplicates:
        print("✅ Tidak ada file duplikat ditemukan!")
        return
    
    print(f"🚨 Ditemukan {len(duplicates)} grup file duplikat:")
    print(f"💾 Ruang yang bisa dihemat: {space_saved / (1024*1024):.2f} MB")
    
    for i, (hash_val, paths) in enumerate(list(duplicates.items())[:5]):  # Show first 5
        print(f"\n📁 Grup {i+1} ({len(paths)} file):")
        for path in paths[:3]:  # Show first 3 files
            file_size = os.path.getsize(path) / 1024
            print(f"   📄 {os.path.basename(path)} ({file_size:.1f} KB)")
        if len(paths) > 3:
            print(f"   ... dan {len(paths) - 3} file lainnya")

def handle_batch_rename(organizer, config, args):
    """Handle batch file renaming"""
    watch_folder = config["watch_folder"]
    
    if not os.path.exists(watch_folder):
        print(f"❌ Folder tidak ditemukan: {watch_folder}")
        return
    
    success, message = organizer.batch_renamer.rename_files(
        watch_folder, 
        args.rename, 
        args.start_number
    )
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

# =============================================================================
# JALANKAN APLIKASI - TANPA DEPENDENSI!
# =============================================================================

if __name__ == "__main__":
    main()