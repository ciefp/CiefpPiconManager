from __future__ import absolute_import
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.Button import Button
from Components.config import config, ConfigSubsection, ConfigText
from enigma import eTimer
from Tools.Directories import fileExists
import os
import re
import threading
import subprocess
import time

class DownloadPiconsScreen(Screen):
    """Ekran za preuzimanje picona na FLASH (/picon/)"""
    
    skin = """
    <screen position="center,center" size="1920,1080" backgroundColor="#011a2e">
        <!-- Titule -->
        <widget name="separator0" position="0,5" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
        <widget name="title" position="0,10" size="1920,60" font="Bold;34" halign="center" backgroundColor="#012e01" foregroundColor="#FFFFFF" text="..:: Download Picons (FLASH) ::.." />
        <widget name="separator1" position="0,78" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
        
        <!-- Status -->
        <widget name="status_label" position="100,100" size="1720,30" font="Regular;22" halign="center" valign="center" foregroundColor="#00FF00" backgroundColor="#011a2e" />
        
        <!-- Progress indikator -->
        <widget name="progress_label" position="100,135" size="1720,30" font="Regular;18" halign="center" valign="center" foregroundColor="#FFFF00" backgroundColor="#011a2e" />
        
        <widget name="separator2" position="0,245" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
        
        <!-- Info -->
        <widget name="info_label" position="100,180" size="1720,30" font="Regular;20" halign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" text="Installation to: /picon/ (FLASH)" />
        
        <!-- Filter -->
        <widget name="filter_label" position="100,200" size="200,30" font="Bold;22" foregroundColor="#FFFFFF" backgroundColor="#011a2e" text="Filter:" />
        <widget name="filter_value" position="300,200" size="600,30" font="Regular;22" foregroundColor="#00FF00" backgroundColor="#011a2e" text="all" />
        
        <widget name="picon_dw" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpPiconManager/picon_dw.png" position="950,250" size="900,600" backgroundColor="#0D1B36" />
        
        <!-- Lista paketa -->
        <widget name="package_list" position="100,260" size="800,630" scrollbarMode="showOnDemand" itemHeight="35" font="Regular;20" backgroundColor="#011a2e" foregroundColor="#FFFFFF" />
        
        <!-- Dugmad -->
        <widget name="key_red" position="100,950" size="540,40" backgroundColor="red" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="EXIT" />
        <widget name="key_green" position="690,950" size="540,40" backgroundColor="green" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="INSTALL" />
        <widget name="key_yellow" position="1280,950" size="540,40" backgroundColor="yellow" font="Bold;24" foregroundColor="#000000" halign="center" valign="center" text="REFRESH" />
        
        <!-- Separator -->
        <widget name="separator3" position="0,1040" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
    </screen>
    """
    
    # Predefinisani picon paketi (OpenATV feed)
    PICON_PACKAGES = [
        # SRP (Srpski) paketi - 220x132
        {"name": "srp-full.220x132-190x102.dark.on.blue", "display": "SRP 220x132 Dark on Blue", "type": "srp", "size": "220x132"},
        {"name": "srp-full.220x132-190x102.dark.on.reflection", "display": "SRP 220x132 Dark on Reflection", "type": "srp", "size": "220x132"},
        {"name": "srp-full.220x132-190x102.dark.on.transparent", "display": "SRP 220x132 Dark on Transparent", "type": "srp", "size": "220x132"},
        {"name": "srp-full.220x132-190x102.dark.on.white", "display": "SRP 220x132 Dark on White", "type": "srp", "size": "220x132"},
        {"name": "srp-full.220x132-190x102.light.on.black", "display": "SRP 220x132 Light on Black", "type": "srp", "size": "220x132"},
        {"name": "srp-full.220x132-190x102.light.on.black-er", "display": "SRP 220x132 Light on Black ER", "type": "srp", "size": "220x132"},
        {"name": "srp-full.220x132-190x102.light.on.transparent", "display": "SRP 220x132 Light on Transparent", "type": "srp", "size": "220x132"},
        {"name": "srp-full.220x132-220x132.dark.on.transparent", "display": "SRP 220x132 Square Dark", "type": "srp", "size": "220x132"},
        {"name": "srp-full.220x132-220x132.light.on.transparent", "display": "SRP 220x132 Square Light", "type": "srp", "size": "220x132"},
        
        # SRP - 100x60
        {"name": "srp-full.100x60-86x46.dark.on.blue", "display": "SRP 100x60 Dark on Blue", "type": "srp", "size": "100x60"},
        {"name": "srp-full.100x60-86x46.dark.on.reflection", "display": "SRP 100x60 Dark on Reflection", "type": "srp", "size": "100x60"},
        {"name": "srp-full.100x60-86x46.dark.on.transparent", "display": "SRP 100x60 Dark on Transparent", "type": "srp", "size": "100x60"},
        {"name": "srp-full.100x60-86x46.dark.on.white", "display": "SRP 100x60 Dark on White", "type": "srp", "size": "100x60"},
        {"name": "srp-full.100x60-86x46.light.on.black", "display": "SRP 100x60 Light on Black", "type": "srp", "size": "100x60"},
        {"name": "srp-full.100x60-86x46.light.on.transparent", "display": "SRP 100x60 Light on Transparent", "type": "srp", "size": "100x60"},
        
        # SRP - 400x240
        {"name": "srp-full.400x240-370x210.dark.on.blue", "display": "SRP 400x240 Dark on Blue", "type": "srp", "size": "400x240"},
        {"name": "srp-full.400x240-370x210.light.on.transparent", "display": "SRP 400x240 Light on Transparent", "type": "srp", "size": "400x240"},
        {"name": "srp-full.400x240-400x240.light.on.transparent", "display": "SRP 400x240 Square Light", "type": "srp", "size": "400x240"},
        {"name": "srp-full.400x170-370x140.dark.on.transparent", "display": "SRP 400x170 Dark on Transparent", "type": "srp", "size": "400x170"},
        
        # UTF8SNP paketi - 220x132
        {"name": "utf8snp-full.220x132-190x102.dark.on.blue", "display": "UTF8SNP 220x132 Dark on Blue", "type": "utf8snp", "size": "220x132"},
        {"name": "utf8snp-full.220x132-190x102.dark.on.reflection", "display": "UTF8SNP 220x132 Dark on Reflection", "type": "utf8snp", "size": "220x132"},
        {"name": "utf8snp-full.220x132-190x102.dark.on.transparent", "display": "UTF8SNP 220x132 Dark on Transparent", "type": "utf8snp", "size": "220x132"},
        {"name": "utf8snp-full.220x132-190x102.dark.on.white", "display": "UTF8SNP 220x132 Dark on White", "type": "utf8snp", "size": "220x132"},
        {"name": "utf8snp-full.220x132-190x102.light.on.black", "display": "UTF8SNP 220x132 Light on Black", "type": "utf8snp", "size": "220x132"},
        {"name": "utf8snp-full.220x132-190x102.light.on.black-er", "display": "UTF8SNP 220x132 Light on Black ER", "type": "utf8snp", "size": "220x132"},
        {"name": "utf8snp-full.220x132-190x102.light.on.transparent", "display": "UTF8SNP 220x132 Light on Transparent", "type": "utf8snp", "size": "220x132"},
        {"name": "utf8snp-full.220x132-220x132.dark.on.transparent", "display": "UTF8SNP 220x132 Square Dark", "type": "utf8snp", "size": "220x132"},
        {"name": "utf8snp-full.220x132-220x132.light.on.transparent", "display": "UTF8SNP 220x132 Square Light", "type": "utf8snp", "size": "220x132"},
        
        # UTF8SNP - 100x60
        {"name": "utf8snp-full.100x60-86x46.dark.on.blue", "display": "UTF8SNP 100x60 Dark on Blue", "type": "utf8snp", "size": "100x60"},
        {"name": "utf8snp-full.100x60-86x46.dark.on.reflection", "display": "UTF8SNP 100x60 Dark on Reflection", "type": "utf8snp", "size": "100x60"},
        {"name": "utf8snp-full.100x60-86x46.dark.on.transparent", "display": "UTF8SNP 100x60 Dark on Transparent", "type": "utf8snp", "size": "100x60"},
        {"name": "utf8snp-full.100x60-86x46.dark.on.white", "display": "UTF8SNP 100x60 Dark on White", "type": "utf8snp", "size": "100x60"},
        {"name": "utf8snp-full.100x60-86x46.light.on.black", "display": "UTF8SNP 100x60 Light on Black", "type": "utf8snp", "size": "100x60"},
        {"name": "utf8snp-full.100x60-86x46.light.on.transparent", "display": "UTF8SNP 100x60 Light on Transparent", "type": "utf8snp", "size": "100x60"},
        
        # UTF8SNP - 400x240
        {"name": "utf8snp-full.400x240-370x210.light.on.transparent", "display": "UTF8SNP 400x240 Light on Transparent", "type": "utf8snp", "size": "400x240"},
        {"name": "utf8snp-full.400x170-370x140.dark.on.transparent", "display": "UTF8SNP 400x170 Dark on Transparent", "type": "utf8snp", "size": "400x170"},
        
        # Ostali paketi
        {"name": "tv-australia", "display": "Australia TV Picons", "type": "other", "size": "Various"},
        {"name": "zombi.lcd.13", "display": "Zombi LCD 13°E", "type": "zombi", "size": "LCD"},
        {"name": "zombi.lcd.19", "display": "Zombi LCD 19.2°E", "type": "zombi", "size": "LCD"},
        {"name": "zombi.lcd.dvb.t.berlin", "display": "Zombi LCD DVB-T Berlin", "type": "zombi", "size": "LCD"},
        {"name": "zombi.lcd.tele.columbus.berlin", "display": "Zombi LCD TeleColumbus Berlin", "type": "zombi", "size": "LCD"},
        {"name": "zombi.lcd.vodafone.kd", "display": "Zombi LCD Vodafone KD", "type": "zombi", "size": "LCD"},
    ]
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        
        # Inicijalizacija
        self.packages = []
        self.filtered_packages = []
        self.downloading = False
        self.current_filter = "all"
        self.progress_counter = 0
        self.progress_timer = None
        
        # Filter opcije
        self.filter_options = ["all", "srp", "utf8snp", "zombi", "other"]
        
        # Widgeti
        self["title"] = Label("..:: Download Picons (FLASH) ::..")
        self["status_label"] = Label("Select package and press INSTALL to install to FLASH")
        self["progress_label"] = Label("")
        self["info_label"] = Label("Installation to: /picon/ (FLASH)")
        self["filter_label"] = Label("Filter:")
        self["filter_value"] = Label("all")
        self["package_list"] = MenuList([])
        self["picon_dw"] = Pixmap()
        self["separator0"] = Label()
        self["separator1"] = Label()
        self["separator2"] = Label()
        self["separator3"] = Label()
        
        # Dugmad
        self["key_red"] = Button("EXIT")
        self["key_green"] = Button("INSTALL")
        self["key_yellow"] = Button("REFRESH")
        
        # Akcije
        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions", "ColorActions"],
            {
                "cancel": self.exit,
                "ok": self.install_selected,
                "up": self.move_up,
                "down": self.move_down,
                "left": self.filter_prev,
                "right": self.filter_next,
                "red": self.exit,
                "green": self.install_selected,
                "yellow": self.load_packages
            },
            -1
        )
        
        # Učitaj pakete
        self.load_packages()
    
    def load_packages(self):
        """Učitaj predefinisanu listu paketa"""
        self.packages = []
        installed_count = 0
        
        for pkg in self.PICON_PACKAGES:
            installed = self._is_installed(f"enigma2-plugin-picons-{pkg['name']}")
            if installed:
                installed_count += 1
            
            self.packages.append({
                'name': pkg['name'],
                'full_name': f"enigma2-plugin-picons-{pkg['name']}",
                'display': pkg['display'],
                'type': pkg['type'],
                'size': pkg['size'],
                'installed': installed
            })
        
        self._apply_filter()
        self["status_label"].setText(f"Loaded {len(self.packages)} packages ({installed_count} installed)")
        self["progress_label"].setText("")
    
    def _is_installed(self, package_name):
        """Provjeri da li je paket instaliran"""
        try:
            process = subprocess.Popen(
                f"opkg list-installed | grep '{package_name}'",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True
            )
            output, error = process.communicate(timeout=3)
            return bool(output.strip())
        except:
            return False
    
    def _apply_filter(self):
        """Primijeni trenutni filter"""
        if self.current_filter == "all":
            self.filtered_packages = self.packages[:]
        else:
            self.filtered_packages = [p for p in self.packages if p['type'] == self.current_filter]
        
        items = []
        for pkg in self.filtered_packages:
            installed = "[✓] " if pkg.get('installed') else "[ ] "
            items.append(f"{installed}{pkg['display']} ({pkg['size']})")
        
        if not items:
            items = ["No packages match filter"]
        
        self["package_list"].setList(items)
        self["filter_value"].setText(self.current_filter)
    
    def filter_prev(self):
        idx = self.filter_options.index(self.current_filter)
        idx = (idx - 1) % len(self.filter_options)
        self.current_filter = self.filter_options[idx]
        self._apply_filter()
        self["status_label"].setText(f"Filter: {self.current_filter}")
    
    def filter_next(self):
        idx = self.filter_options.index(self.current_filter)
        idx = (idx + 1) % len(self.filter_options)
        self.current_filter = self.filter_options[idx]
        self._apply_filter()
        self["status_label"].setText(f"Filter: {self.current_filter}")
    
    def move_up(self):
        self["package_list"].up()
    
    def move_down(self):
        self["package_list"].down()
    
    def install_selected(self):
        """Instaliraj selektirani paket na FLASH"""
        if self.downloading:
            self["status_label"].setText("Installation already in progress...")
            return
        
        current = self["package_list"].getCurrent()
        if not current or current == "No packages match filter":
            self["status_label"].setText("Please select a package")
            return
        
        selected_pkg = None
        for pkg in self.filtered_packages:
            installed = "[✓] " if pkg.get('installed') else "[ ] "
            item = f"{installed}{pkg['display']} ({pkg['size']})"
            if item == current:
                selected_pkg = pkg
                break
        
        if not selected_pkg:
            self["status_label"].setText("Package not found")
            return
        
        from Screens.MessageBox import MessageBox
        self.session.openWithCallback(
            self._confirm_install,
            MessageBox,
            f"Install {selected_pkg['display']} to /picon/ (FLASH)?",
            MessageBox.TYPE_YESNO
        )
        self._current_package = selected_pkg
    
    def _confirm_install(self, answer):
        if answer and self._current_package:
            self._start_progress_indicator()
            self._do_install(self._current_package['full_name'])
    
    def _start_progress_indicator(self):
        self.progress_counter = 0
        if self.progress_timer:
            self.progress_timer.stop()
        self.progress_timer = eTimer()
        self.progress_timer.callback.append(self._update_progress)
        self.progress_timer.start(500, True)
    
    def _update_progress(self):
        if not self.downloading:
            if self.progress_timer:
                self.progress_timer.stop()
            return
        
        self.progress_counter = (self.progress_counter + 1) % 4
        dots = ["", ".", "..", "..."]
        status = self["status_label"].getText()
        if "Installing" in status:
            self["progress_label"].setText(f"⏳ {status}{dots[self.progress_counter % len(dots)]}")
    
    def _do_install(self, package_name):
        self.downloading = True
        self["status_label"].setText(f"Installing: {package_name}")
        self["progress_label"].setText("⏳ Starting installation...")
        self._set_buttons_enabled(False)
        
        thread = threading.Thread(target=self._install_thread, args=(package_name,))
        thread.daemon = True
        thread.start()
    
    def _install_thread(self, package_name):
        try:
            # Osvježi opkg listu
            print("[DownloadPicons] Updating opkg...")
            update_cmd = "opkg update"
            process = subprocess.Popen(
                update_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True
            )
            update_output, update_error = process.communicate(timeout=30)
            
            if process.returncode != 0:
                eTimer(0, lambda: self._show_result(False, f"opkg update failed: {update_error[:80]}"), 0)
                return
            
            # Instaliraj
            cmd = f"opkg install --force-overwrite {package_name}"
            print(f"[DownloadPicons] Running: {cmd}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True
            )
            output, error = process.communicate(timeout=300)
            
            if process.returncode == 0:
                eTimer(0, lambda: self._show_result(True, f"✓ Successfully installed {package_name} to /picon/"), 0)
            else:
                error_msg = error[:80] if error else "Unknown error"
                eTimer(0, lambda: self._show_result(False, f"✗ Install failed: {error_msg}"), 0)
            
        except subprocess.TimeoutExpired:
            eTimer(0, lambda: self._show_result(False, "✗ Install timeout"), 0)
        except Exception as e:
            print(f"[DownloadPicons] Install error: {e}")
            eTimer(0, lambda: self._show_result(False, f"✗ Install error: {str(e)[:50]}"), 0)
    
    def _set_buttons_enabled(self, enabled):
        if enabled:
            self["key_red"].setText("EXIT")
            self["key_green"].setText("INSTALL")
            self["key_yellow"].setText("REFRESH")
        else:
            self["key_red"].setText("⏳ BUSY")
            self["key_green"].setText("⏳ BUSY")
            self["key_yellow"].setText("⏳ BUSY")
    
    def _show_result(self, success, message):
        self.downloading = False
        
        if self.progress_timer:
            self.progress_timer.stop()
            self.progress_timer = None
        
        self._set_buttons_enabled(True)
        self["status_label"].setText(message)
        self["progress_label"].setText("")
        
        if success:
            self["status_label"].setText(f"✅ {message}")
            self.load_packages()
            timer = eTimer()
            timer.callback.append(self.exit)
            timer.start(3000, True)
        else:
            self["status_label"].setText(f"❌ {message}")
    
    def exit(self):
        if self.progress_timer:
            self.progress_timer.stop()
            self.progress_timer = None
        self.close()