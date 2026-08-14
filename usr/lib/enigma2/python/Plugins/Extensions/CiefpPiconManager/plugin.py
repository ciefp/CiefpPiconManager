from __future__ import absolute_import
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.Button import Button
from Components.config import config, ConfigSubsection, ConfigText
from enigma import eServiceReference, eServiceCenter, eTimer, eDVBDB
from Tools.Directories import fileExists, resolveFilename, SCOPE_SKIN
from Tools.LoadPixmap import LoadPixmap
import os
import re

# Import PiconManager iz components foldera
from .components.picon_manager import PiconManager

# Plugin informacije
PLUGIN_VERSION = "1.0.1"
PLUGIN_NAME = "Ciefp Picon Manager"
PLUGIN_AUTHOR = "Ciefp"

# Debug
debug_file = "/tmp/ciefp_piconmanager_debug.log"

def log_debug(message):
    try:
        with open(debug_file, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")
    except:
        pass

class CiefpPiconManagerMain(Screen):
    """Glavni ekran za upravljanje piconima"""

class CiefpPiconManagerMain(Screen):
    """Glavni ekran za upravljanje piconima"""

    skin = """
    <screen position="center,center" size="1920,1080" backgroundColor="#011a2e">
        <!-- Titule -->
        <widget name="separator0" position="0,5" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />  
        <widget name="plugin_title" position="0,10" size="1920,40" font="Bold;30" halign="center" backgroundColor="#012e01" foregroundColor="#FFFFFF" text="..:: Ciefp Picon Manager ::.." />
        <widget name="bouquet_title" position="10,50" size="450,35" font="Bold;30" halign="center" backgroundColor="#012e01" foregroundColor="#FFFFFF" text="Bouquets" />
        <widget name="channel_title" position="460,50" size="900,35" font="Bold;30" halign="center" backgroundColor="#012e01" foregroundColor="#FFFFFF" text="Channels" />
        <widget name="picon_title" position="1360,50" size="530,35" font="Bold;30" halign="center" backgroundColor="#012e01" foregroundColor="#FFFFFF" text="Picons" />
        <widget name="separator1" position="0,87" size="1920,3" backgroundColor="#d5fa02" zPosition="1" /> 
        
        <!-- Liste sa scrollbar -->
        <widget name="bouquet_list" position="20,95" size="600,858" scrollbarMode="showOnDemand" itemHeight="33" font="Regular;26" backgroundColor="#011a2e" foregroundColor="#FFFFFF" />
        <widget name="channel_list" position="650,95" size="650,858" scrollbarMode="showOnDemand" itemHeight="33" font="Regular;26" backgroundColor="#011a2e" foregroundColor="#FFFFFF" />
        
        <!-- Picon i dugmad -->
        <widget name="picon_bg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpPiconManager/picon_bg.png" position="1350,100" size="540,250" backgroundColor="#0D1B36" />
        <widget name="picon" position="1530,420" size="220,132" alphatest="blend" />
        <widget name="channel_name" position="1370,570" size="540,50" font="Bold;28" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#011a2e" />
        <widget name="service_ref" position="1370,620" size="540,30" font="Regular;18" halign="center" valign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" />
        
        <!-- Dugmad -->
        <widget name="key_red" position="1350,700" size="540,40" backgroundColor="red" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="EXIT" />
        <widget name="key_green" position="1350,750" size="540,40" backgroundColor="green" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="ASSIGN PICON" />
        <widget name="key_yellow" position="1350,800" size="540,40" backgroundColor="yellow" font="Bold;24" foregroundColor="#000000" halign="center" valign="center" text="SETTINGS" />
        <widget name="key_blue" position="1350,850" size="540,40" backgroundColor="blue" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="DELETE PICON" />
        <widget name="key_menu" position="1350,900" size="540,40" backgroundColor="white" font="Bold;24" foregroundColor="#000000" halign="center" valign="center" text="MENU DOWNLOAD" />
        
        <!-- Status -->
        <widget name="status_label" position="1370,1000" size="540,30" font="Regular;18" halign="center" valign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" />
        <widget name="separator2" position="0,950" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
    </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        
        # Inicijalizacija podataka
        self.bouquet_list_data = []
        self.channel_list_data = []
        self.current_bouquet = None
        self.current_channel = None
        self.current_bouquet_file = None
        self.service_ref = ""
        self.channel_refs = {}
        self.channel_service_refs = {}
        self.focus_panel = 0
        self.lamedb_data = {}
        self.bouquet_index = 0
        self.channel_index = 0
        
        # Učitaj postavke
        self.load_settings()
        
        # Kreiraj PiconManager instancu
        self.picon_manager = PiconManager(self.picon_path)
        
        # Kreiraj widgete
        self["bouquet_list"] = MenuList([])
        self["channel_list"] = MenuList([])
        self["picon"] = Pixmap()
        self["picon_bg"] = Pixmap()
        self["channel_name"] = Label()
        self["service_ref"] = Label()
        self["status_label"] = Label()
        self["plugin_title"] = Label("..:: Ciefp Picon Manager ::..")
        self["bouquet_title"] = Label("Bouquets")
        self["channel_title"] = Label("Channels")
        self["picon_title"] = Label("Picons")
        self["separator0"] = Label()
        self["separator1"] = Label()
        self["separator2"] = Label()
        self["separator3"] = Label()
        
        # Dugmad kao Button widgeti
        self["key_red"] = Button("EXIT")
        self["key_green"] = Button("ASSIGN PICON")
        self["key_yellow"] = Button("SETTINGS")
        self["key_blue"] = Button("DELETE PICON")
        self["key_menu"] = Button("MENU")
        
        # Akcije
        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions", "ColorActions", "MenuActions"],
            {
                "cancel": self.exit,
                "ok": self.select_item,
                "left": self.focus_left,
                "right": self.focus_right,
                "up": self.move_up,
                "down": self.move_down,
                "red": self.exit,
                "green": self.assign_picon,
                "yellow": self.settings,
                "blue": self.delete_picon,
                "menu": self.show_menu
            },
            -1
        )
        
        # Inicijaliziraj podatke
        self.onLayoutFinish.append(self.init_data)
    
    def load_settings(self):
        """Učitaj postavke iz configa"""
        try:
            if not hasattr(config.plugins, "ciefp_picon_manager"):
                config.plugins.ciefp_picon_manager = ConfigSubsection()
                config.plugins.ciefp_picon_manager.picon_path = ConfigText(default="/media/usb/picon/")
            
            if hasattr(config.plugins.ciefp_picon_manager, "picon_path"):
                self.picon_path = config.plugins.ciefp_picon_manager.picon_path.value
                if not os.path.exists(self.picon_path):
                    self.picon_path = "/media/usb/picon/"
        except Exception as e:
            log_debug(f"Error loading settings: {e}")
    
    def init_data(self):
        """Inicijaliziraj podatke"""
        try:
            self["status_label"].setText("Loading data...")
            self.load_lamedb()
            self.load_bouquets()
            self.update_display()
        except Exception as e:
            log_debug(f"Init data error: {e}")
            self["status_label"].setText(f"Error loading data: {str(e)[:50]}")
    
    def safe_read_file(self, filepath):
        """Sigurno čitanje fajla sa UTF-8 encoding zaštitom"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            try:
                with open(filepath, 'r', encoding='latin-1', errors='ignore') as f:
                    return f.read()
            except:
                try:
                    with open(filepath, 'r', errors='ignore') as f:
                        return f.read()
                except:
                    return ""
    
    def safe_read_lines(self, filepath):
        """Sigurno čitanje linija fajla sa UTF-8 encoding zaštitom"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.readlines()
        except:
            try:
                with open(filepath, 'r', encoding='latin-1', errors='ignore') as f:
                    return f.readlines()
            except:
                try:
                    with open(filepath, 'r', errors='ignore') as f:
                        return f.readlines()
                except:
                    return []
    
    def load_lamedb(self):
        """Učitaj lamedb podatke za imena kanala"""
        self.lamedb_data = {}
        lamedb_path = "/etc/enigma2/lamedb"
        if not os.path.exists(lamedb_path):
            return
        
        try:
            content = self.safe_read_file(lamedb_path)
            if not content:
                return
            
            start = content.find("\nservices\n")
            end = content.find("\nend\n", start)
            if start == -1 or end == -1:
                return
            
            services_block = content[start + 10:end]
            lines = services_block.splitlines()
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if not line:
                    i += 1
                    continue
                
                if line.startswith("p:") or line.startswith("c:"):
                    i += 1
                    continue
                
                if ":" in line:
                    parts = line.split(":")
                    if len(parts) >= 4:
                        sid = parts[0].lower()
                        satfreq = parts[1].lower()
                        tsid = parts[2].lower()
                        onid = parts[3].lower()
                        
                        key1 = f"{sid}:{satfreq}:{tsid}:{onid}"
                        key2 = f"{sid}:{satfreq.zfill(8)}:{tsid}:{onid}"
                        
                        if i + 1 < len(lines):
                            name = lines[i + 1].strip()
                            if name and not name.startswith("p:") and not name.startswith("c:"):
                                self.lamedb_data[key1] = name
                                self.lamedb_data[key2] = name
                                
                                try:
                                    sid_hex = f"{int(sid, 16):04x}"
                                    tsid_hex = f"{int(tsid, 16):04x}"
                                    onid_hex = f"{int(onid, 16):04x}"
                                    key3 = f"{sid_hex}:{satfreq}:{tsid_hex}:{onid_hex}"
                                    self.lamedb_data[key3] = name
                                except:
                                    pass
                
                i += 1
                
        except Exception as e:
            log_debug(f"Error parsing lamedb: {e}")
    
    def load_bouquets(self):
        """Učitaj sve bukete"""
        try:
            bouquets_file = "/etc/enigma2/bouquets.tv"
            if not os.path.exists(bouquets_file):
                self["status_label"].setText("No bouquets found")
                return
            
            bouquet_files = []
            try:
                with open(bouquets_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if "FROM BOUQUET" in line:
                            start = line.find('"') + 1
                            end = line.find('"', start)
                            if start != -1 and end != -1:
                                bouquet_files.append(line[start:end])
            except:
                try:
                    with open(bouquets_file, 'r', encoding='latin-1', errors='ignore') as f:
                        for line in f:
                            if "FROM BOUQUET" in line:
                                start = line.find('"') + 1
                                end = line.find('"', start)
                                if start != -1 and end != -1:
                                    bouquet_files.append(line[start:end])
                except:
                    pass
            
            self.bouquet_list_data = []
            for bouquet_file in bouquet_files:
                file_path = os.path.join("/etc/enigma2", bouquet_file)
                if os.path.exists(file_path):
                    try:
                        lines = self.safe_read_lines(file_path)
                        if lines:
                            first_line = lines[0].strip() if lines else ""
                            if first_line.startswith("#NAME"):
                                display_name = first_line.replace("#NAME", "", 1).strip()
                                self.bouquet_list_data.append({
                                    'name': display_name,
                                    'file': bouquet_file
                                })
                    except Exception as e:
                        log_debug(f"Error reading bouquet {bouquet_file}: {e}")
            
            if self.bouquet_list_data:
                self.current_bouquet = self.bouquet_list_data[0]
                self.current_bouquet_file = self.bouquet_list_data[0]['file']
                self.load_channels_from_bouquet()
            
            self["status_label"].setText(f"Loaded {len(self.bouquet_list_data)} bouquets")
            
        except Exception as e:
            log_debug(f"Error loading bouquets: {e}")
            self["status_label"].setText(f"Error: {e}")
    
    def load_channels_from_bouquet(self):
        """Učitaj kanale iz selektovanog buketa"""
        if not self.current_bouquet or not self.current_bouquet_file:
            return
        
        try:
            file_path = os.path.join("/etc/enigma2", self.current_bouquet_file)
            if not os.path.exists(file_path):
                return
            
            self.channel_list_data = []
            self.channel_refs = {}
            self.channel_service_refs = {}
            
            lines = self.safe_read_lines(file_path)
            if not lines:
                return
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if not line:
                    i += 1
                    continue
                
                if line.startswith("#NAME"):
                    i += 1
                    continue
                
                elif line.startswith("#SERVICE"):
                    service_ref = line.replace("#SERVICE", "").strip()
                    
                    # Provjeri da li je marker (1:64)
                    if service_ref.startswith("1:64:"):
                        marker_name = None
                        if i + 1 < len(lines) and lines[i + 1].strip().startswith("#DESCRIPTION"):
                            desc_line = lines[i + 1].strip()
                            marker_name = desc_line.replace("#DESCRIPTION", "").strip()
                            i += 1
                        
                        if marker_name:
                            self.channel_list_data.append(marker_name)
                            self.channel_refs[marker_name] = service_ref
                            self.channel_service_refs[marker_name] = service_ref
                        i += 1
                        continue
                    
                    channel_name = self.get_channel_name(service_ref)
                    
                    if channel_name:
                        self.channel_list_data.append(channel_name)
                        self.channel_refs[channel_name] = service_ref
                        self.channel_service_refs[channel_name] = service_ref
                    
                    i += 1
                
                elif line.startswith("#DESCRIPTION"):
                    marker_name = line.replace("#DESCRIPTION", "").strip()
                    if marker_name:
                        self.channel_list_data.append(marker_name)
                        self.channel_refs[marker_name] = "#SERVICE 1:64:0:0:0:0:0:0:0:0:"
                        self.channel_service_refs[marker_name] = "#SERVICE 1:64:0:0:0:0:0:0:0:0:"
                    i += 1
                
                else:
                    i += 1
            
            if self.channel_list_data:
                self.current_channel = self.channel_list_data[0]
                self.channel_index = 0
                self.update_channel_info()
                self.refresh_picon()
            
            self.update_display()
            
        except Exception as e:
            log_debug(f"Error loading channels: {e}")
    
    def get_channel_name(self, service_ref):
        """Dohvati ime kanala iz service reference"""
        try:
            if "http" in service_ref.lower() or "4097:" in service_ref or "5001:" in service_ref or "5002:" in service_ref:
                parts = service_ref.split(":")
                if len(parts) >= 11 and parts[10]:
                    return f"{parts[10]} (IPTV)"
                return "IPTV Channel"
            
            parts = service_ref.split(":")
            if len(parts) >= 10:
                sid = parts[3].lower()
                tsid = parts[4].lower()
                onid = parts[5].lower()
                satfreq = parts[6].lower()
                
                keys = [
                    f"{sid}:{satfreq}:{tsid}:{onid}",
                    f"{sid}:{satfreq.zfill(8)}:{tsid}:{onid}"
                ]
                
                try:
                    sid_hex = f"{int(sid, 16):04x}"
                    tsid_hex = f"{int(tsid, 16):04x}"
                    onid_hex = f"{int(onid, 16):04x}"
                    keys.append(f"{sid_hex}:{satfreq}:{tsid_hex}:{onid_hex}")
                    keys.append(f"{sid_hex}:{satfreq.zfill(8)}:{tsid_hex}:{onid_hex}")
                except:
                    pass
                
                for key in keys:
                    if key in self.lamedb_data:
                        return self.lamedb_data[key]
                
                return f"Unknown ({sid}:{tsid}:{onid})"
            
            return "Unknown Channel"
            
        except Exception as e:
            log_debug(f"Error getting channel name: {e}")
            return "Unknown Channel"
    
    def update_display(self):
        """Ažuriraj prikaz listi - ponovnim setList-om"""
        bouquet_items = []
        if self.bouquet_list_data:
            for bouquet in self.bouquet_list_data:
                bouquet_items.append(bouquet['name'])
        
        self["bouquet_list"].setList(bouquet_items)
        
        if self.current_bouquet and self.current_bouquet['name'] in bouquet_items:
            index = bouquet_items.index(self.current_bouquet['name'])
            self.bouquet_index = index
            self["bouquet_list"].index = index
            # Označi selektirani item tako što se pomaknemo na njega
            self["bouquet_list"].moveToIndex(index)
        
        channel_items = []
        if self.channel_list_data:
            for channel in self.channel_list_data:
                channel_items.append(channel)
        
        self["channel_list"].setList(channel_items)
        
        if self.current_channel and self.current_channel in channel_items:
            index = channel_items.index(self.current_channel)
            self.channel_index = index
            self["channel_list"].index = index
            # Označi selektirani item tako što se pomaknemo na njega
            self["channel_list"].moveToIndex(index)
    
    def update_channel_info(self):
        """Ažuriraj info o kanalu"""
        if self.current_channel:
            self["channel_name"].setText(self.current_channel)
            service_ref = self.channel_refs.get(self.current_channel, "")
            display_ref = service_ref
            if len(display_ref) > 60:
                display_ref = display_ref[:57] + "..."
            self["service_ref"].setText(display_ref)
            self.service_ref = service_ref

    def refresh_picon(self):
        """Osvježi prikaz picona koristeći PiconManager"""
        if not self.current_channel:
            self["picon"].setPixmap(None)
            return

        service_ref = self.channel_refs.get(self.current_channel, "")
        if not service_ref:
            self["picon"].setPixmap(None)
            self["status_label"].setText("No service reference")
            return

        # Ignoriši markere (1:64)
        if service_ref.startswith("#SERVICE 1:64:") or "1:64:" in service_ref:
            self["picon"].setPixmap(None)
            self["status_label"].setText("")
            return

        # Proslijedi i ime kanala za fallback pretragu
        channel_name = self.current_channel
        picon = self.picon_manager.get_picon_pixmap(service_ref, channel_name)

        if picon:
            self["picon"].setPixmap(picon)
            self["status_label"].setText("Picon found")
            return

        # Pokaži placeholder
        placeholder = "/usr/lib/enigma2/python/Plugins/Extensions/CiefpPiconManager/placeholder.png"
        if fileExists(placeholder):
            picon = LoadPixmap(placeholder)
            if picon:
                self["picon"].setPixmap(picon)
                self["status_label"].setText("No picon assigned")
                return

        self["picon"].setPixmap(None)
        self["status_label"].setText("No picon assigned")

    def focus_left(self):
        self.focus_panel = 0
        self["status_label"].setText("Focus: Bouquets")
        self.update_display()
    
    def focus_right(self):
        self.focus_panel = 1
        self["status_label"].setText("Focus: Channels")
        self.update_display()
    
    def move_up(self):
        if self.focus_panel == 0:
            if self.bouquet_list_data:
                current_idx = self.bouquet_index
                if current_idx > 0:
                    new_idx = current_idx - 1
                else:
                    new_idx = 0
                self.bouquet_index = new_idx
                self["bouquet_list"].index = new_idx
                self["bouquet_list"].moveToIndex(new_idx)  # Pomjeri selekcionu traku
                self.current_bouquet = self.bouquet_list_data[new_idx]
                self.current_bouquet_file = self.current_bouquet['file']
                self.load_channels_from_bouquet()
                self.update_display()

        elif self.focus_panel == 1:
            if self.channel_list_data:
                current_idx = self.channel_index
                if current_idx > 0:
                    new_idx = current_idx - 1
                else:
                    new_idx = 0
                self.channel_index = new_idx
                self["channel_list"].index = new_idx
                self["channel_list"].moveToIndex(new_idx)  # Pomjeri selekcionu traku
                self.current_channel = self.channel_list_data[new_idx]
                self.update_channel_info()
                self.refresh_picon()

    def move_down(self):
        if self.focus_panel == 0:
            if self.bouquet_list_data:
                current_idx = self.bouquet_index
                max_idx = len(self.bouquet_list_data) - 1
                if current_idx < max_idx:
                    new_idx = current_idx + 1
                else:
                    new_idx = max_idx
                self.bouquet_index = new_idx
                self["bouquet_list"].index = new_idx
                self["bouquet_list"].moveToIndex(new_idx)  # Pomjeri selekcionu traku
                self.current_bouquet = self.bouquet_list_data[new_idx]
                self.current_bouquet_file = self.current_bouquet['file']
                self.load_channels_from_bouquet()
                self.update_display()

        elif self.focus_panel == 1:
            if self.channel_list_data:
                current_idx = self.channel_index
                max_idx = len(self.channel_list_data) - 1
                if current_idx < max_idx:
                    new_idx = current_idx + 1
                else:
                    new_idx = max_idx
                self.channel_index = new_idx
                self["channel_list"].index = new_idx
                self["channel_list"].moveToIndex(new_idx)  # Pomjeri selekcionu traku
                self.current_channel = self.channel_list_data[new_idx]
                self.update_channel_info()
                self.refresh_picon()

    def select_item(self):
        if self.focus_panel == 0:
            if self.current_bouquet:
                self.focus_panel = 1
                self.update_display()
                self["status_label"].setText(f"Bouquet: {self.current_bouquet['name']}")
                if self.channel_list_data:
                    self.current_channel = self.channel_list_data[0]
                    self.channel_index = 0
                    self["channel_list"].index = 0
                    self["channel_list"].moveToIndex(0)
                    self.update_channel_info()
                    self.refresh_picon()
        elif self.focus_panel == 1:
            if self.current_channel:
                self["status_label"].setText(f"Channel: {self.current_channel}")

    def assign_picon(self):
        if not self.current_channel:
            self["status_label"].setText("Please select a channel")
            return
        
        # Provjeri da li je marker
        service_ref = self.channel_refs.get(self.current_channel, "")
        if service_ref and (service_ref.startswith("#SERVICE 1:64:") or "1:64:" in service_ref):
            self["status_label"].setText("Cannot assign picon to marker")
            return
        
        if self.picon_manager.picon_path != self.picon_path:
            self.picon_manager.set_picon_path(self.picon_path)
        
        from .screens.assign_picon import AssignPiconScreen
        self.session.open(AssignPiconScreen, self.current_channel, self.channel_refs, self.picon_manager, self.assign_picon_callback)

    def assign_picon_callback(self, result):
        if result:
            self.refresh_picon()
            self["status_label"].setText("Picon assigned")
    
    def delete_picon(self):
        if not self.current_channel:
            self["status_label"].setText("Please select a channel")
            return
        
        service_ref = self.channel_refs.get(self.current_channel, "")
        if not service_ref:
            self["status_label"].setText("No service reference")
            return
        
        if self.picon_manager.delete_picon(service_ref):
            self.refresh_picon()
            self["status_label"].setText("Picon deleted")
        else:
            self["status_label"].setText("Picon does not exist")
    
    def settings(self):
        from .screens.settings import PiconSettingsScreen
        self.session.open(PiconSettingsScreen, self.picon_path, self.settings_callback)
    
    def settings_callback(self, path):
        if path:
            self.picon_path = path
            self.picon_manager.set_picon_path(path)
            self.refresh_picon()
            self["status_label"].setText(f"Path: {path}")
    
    def show_menu(self):
        from .screens.download_picons import DownloadPiconsScreen
        self.session.open(DownloadPiconsScreen)
    
    def exit(self):
        self.close()


# GLAVNA FUNKCIJA
def main(session, **kwargs):
    session.open(CiefpPiconManagerMain)


# PLUGIN DESCRIPTOR
def Plugins(**kwargs):
    return PluginDescriptor(
        name=f"{PLUGIN_NAME} v{PLUGIN_VERSION}",
        description="Advanced Picon Manager",
        icon="icon.png",
        where=PluginDescriptor.WHERE_PLUGINMENU,
        fnc=main
    )