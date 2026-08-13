from __future__ import absolute_import
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Button import Button
from Components.config import config, ConfigSubsection, ConfigText
from Tools.Directories import fileExists
from enigma import eTimer
import os

class PiconSettingsScreen(Screen):
    """Ekran za postavke picona sa file browserom"""
    
    skin = """
    <screen position="center,center" size="1920,1080" backgroundColor="#011a2e">
        <widget name="separator0" position="0,5" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
        <widget name="plugin_title" position="0,10" size="1920,60" font="Bold;34" halign="center" backgroundColor="#012e01" foregroundColor="#FFFFFF" text="..:: Picon Settings - Set path ::.." />
        <widget name="separator1" position="0,70" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
        
        <widget name="path_label" position="100,120" size="300,30" font="Bold;24" foregroundColor="#FFFFFF" backgroundColor="#011a2e" text="Current Path:" />
        <widget name="path_value" position="400,120" size="1420,30" font="Regular;24" foregroundColor="#00FF00" backgroundColor="#011a2e" />
        
        <widget name="info_label" position="100,160" size="1720,30" font="Regular;20" foregroundColor="#BBBBBB" backgroundColor="#011a2e" text="Select a directory or press OK to choose current folder" />
        
        <widget name="path_list" position="100,200" size="1720,760" scrollbarMode="showOnDemand" itemHeight="33" font="Regular;24" backgroundColor="#011a2e" foregroundColor="#FFFFFF" />
        
        <!-- Dugmad -->
        <widget name="key_red" position="100,970" size="360,40" backgroundColor="red" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="EXIT" />
        <widget name="key_green" position="500,970" size="360,40" backgroundColor="green" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="SELECT" />
        <widget name="key_yellow" position="900,970" size="360,40" backgroundColor="yellow" font="Bold;24" foregroundColor="#000000" halign="center" valign="center" text="DEFAULT" />
        <widget name="key_blue" position="1300,970" size="360,40" backgroundColor="blue" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="PARENT" />
        
        <widget name="status_label" position="100,1020" size="1720,30" font="Regular;22" halign="center" valign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" />
        <widget name="separator2" position="0,1050" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
    </screen>
    """
    
    def __init__(self, session, current_path, callback):
        Screen.__init__(self, session)
        self.session = session
        
        self.current_path = current_path
        self.callback = callback
        self.entries = []
        self.selected_entry = None
        
        # Osiguraj da path završava sa /
        if not self.current_path.endswith('/'):
            self.current_path += '/'
        
        # Widgeti
        self["plugin_title"] = Label("..::  Picon Settings - Set path  ::..")
        self["path_label"] = Label("Current Path:")
        self["path_value"] = Label(self.current_path)
        self["info_label"] = Label("Select a directory or press OK to choose current folder")
        self["path_list"] = MenuList([])
        self["status_label"] = Label()
        self["separator0"] = Label()
        self["separator1"] = Label()
        self["separator2"] = Label()
        
        # Dugmad
        self["key_red"] = Button("EXIT")
        self["key_green"] = Button("SELECT")
        self["key_yellow"] = Button("DEFAULT")
        self["key_blue"] = Button("PARENT")
        
        # Akcije
        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions", "ColorActions"],
            {
                "cancel": self.exit,
                "ok": self.select_current,
                "up": self.move_up,
                "down": self.move_down,
                "red": self.exit,
                "green": self.select_current,
                "yellow": self.set_default,
                "blue": self.go_parent
            },
            -1
        )
        
        # Učitaj direktorijum
        self.load_directory(self.current_path)
    
    def load_directory(self, path):
        """Učitaj sadržaj direktorijuma"""
        self.current_path = path
        if not self.current_path.endswith('/'):
            self.current_path += '/'
        
        self["path_value"].setText(self.current_path)
        self.entries = []
        
        try:
            # Provjeri postoji li direktorijum
            if not os.path.exists(self.current_path):
                self["status_label"].setText(f"Directory does not exist: {self.current_path}")
                self["path_list"].setList(["Directory does not exist"])
                return
            
            # Učitaj sve stavke u direktorijumu
            items = os.listdir(self.current_path)
            
            # Prvo dodaj parent (ako nismo u root-u)
            if self.current_path != "/" and self.current_path != "/media/" and self.current_path != "/media/usb/":
                self.entries.append((".. (Parent Directory)", "parent", True))
            
            # Sortiraj stavke - folderi prvo, pa fajlovi
            dirs = []
            files = []
            
            for item in items:
                full_path = os.path.join(self.current_path, item)
                if os.path.isdir(full_path):
                    # Provjeri ima li PNG fajlova u folderu
                    has_picons = self.has_picon_files(full_path)
                    dirs.append((item, full_path, True, has_picons))
                elif item.lower().endswith('.png'):
                    files.append((item, full_path, False, True))
            
            # Sortiraj po nazivu
            dirs.sort(key=lambda x: x[0].lower())
            files.sort(key=lambda x: x[0].lower())
            
            # Dodaj foldere sa ikonicom
            for name, full_path, is_dir, has_picons in dirs:
                if has_picons:
                    display_name = f"📁 {name} (has picons)"
                else:
                    display_name = f"📁 {name}"
                self.entries.append((display_name, full_path, is_dir))
            
            # Dodaj picon fajlove
            for name, full_path, is_dir, has_picons in files:
                display_name = f"🖼️ {name}"
                self.entries.append((display_name, full_path, is_dir))
            
            # Ažuriraj listu
            if self.entries:
                display_list = [entry[0] for entry in self.entries]
                self["path_list"].setList(display_list)
                self["status_label"].setText(f"Found {len(self.entries)} items in {self.current_path}")
            else:
                self["path_list"].setList(["Empty directory"])
                self["status_label"].setText(f"Directory is empty: {self.current_path}")
                
        except Exception as e:
            self["status_label"].setText(f"Error: {str(e)}")
            self["path_list"].setList([f"Error: {str(e)}"])
    
    def has_picon_files(self, directory):
        """Provjeri ima li PNG fajlova u direktorijumu"""
        try:
            for item in os.listdir(directory):
                if item.lower().endswith('.png'):
                    return True
                # Provjeri i podfoldere (samo jedan nivo dubine)
                full_path = os.path.join(directory, item)
                if os.path.isdir(full_path):
                    for subitem in os.listdir(full_path):
                        if subitem.lower().endswith('.png'):
                            return True
            return False
        except:
            return False
    
    def move_up(self):
        """Kretanje gore kroz listu"""
        self["path_list"].up()
        self.update_selection()
    
    def move_down(self):
        """Kretanje dolje kroz listu"""
        self["path_list"].down()
        self.update_selection()
    
    def update_selection(self):
        """Ažuriraj selektirani item"""
        current = self["path_list"].getCurrent()
        if current:
            for entry in self.entries:
                if entry[0] == current:
                    self.selected_entry = entry
                    break
        else:
            self.selected_entry = None
    
    def select_current(self):
        """Selektiraj trenutni direktorijum ili uđi u folder"""
        current = self["path_list"].getCurrent()
        if not current:
            self.select_current_path()
            return
        
        # Pronađi selektirani entry
        selected = None
        for entry in self.entries:
            if entry[0] == current:
                selected = entry
                break
        
        if not selected:
            self.select_current_path()
            return
        
        name, full_path, is_dir = selected
        
        if is_dir:
            # Ako je parent, idi gore
            if name.startswith(".. (Parent Directory)"):
                parent = os.path.dirname(self.current_path.rstrip('/'))
                if parent:
                    self.load_directory(parent + '/')
            else:
                # Uđi u folder
                self.load_directory(full_path + '/')
        else:
            # Ako je fajl, selektiraj putanju (za slučaj da neko hoće da selektira fajl)
            self.select_path(os.path.dirname(full_path) + '/')
    
    def select_current_path(self):
        """Selektiraj trenutnu putanju"""
        self.select_path(self.current_path)
    
    def select_path(self, path):
        """Selektiraj putanju i spremi"""
        if not path.endswith('/'):
            path += '/'
        
        self.current_path = path
        self["path_value"].setText(self.current_path)
        
        # Spremi u config
        try:
            if not hasattr(config.plugins, "ciefp_picon_manager"):
                config.plugins.ciefp_picon_manager = ConfigSubsection()
            config.plugins.ciefp_picon_manager.picon_path = ConfigText(default=self.current_path)
            config.plugins.ciefp_picon_manager.picon_path.value = self.current_path
            config.save()
        except Exception as e:
            pass
        
        if self.callback:
            self.callback(self.current_path)
        
        self["status_label"].setText(f"Path saved: {self.current_path}")
        
        # Zatvori nakon kratke pauze
        timer = eTimer()
        timer.callback.append(self.exit)
        timer.start(1000, True)
    
    def go_parent(self):
        """Idi u parent direktorijum"""
        parent = os.path.dirname(self.current_path.rstrip('/'))
        if parent:
            self.load_directory(parent + '/')
        else:
            self["status_label"].setText("Already at root directory")
    
    def set_default(self):
        """Postavi default putanju - prvo traži /media/usb/picons/"""
        default_path = "/media/usb/picons/"
        if os.path.exists(default_path):
            self.load_directory(default_path)
            self["status_label"].setText(f"Loaded default: {default_path}")
            self.auto_select_picon_folder()
        else:
            # Pokušaj druge default putanje
            default_paths = [
                "/media/usb/picon/",
                "/media/hdd/picon/",
                "/media/hdd/picons/",
                "/usr/share/enigma2/picon/",
                "/picon/"
            ]
            found = False
            for path in default_paths:
                if os.path.exists(path):
                    self.load_directory(path)
                    self["status_label"].setText(f"Loaded default: {path}")
                    found = True
                    break
            
            if not found:
                self["status_label"].setText("No default directory found")
    
    def auto_select_picon_folder(self):
        """Automatski selektiraj folder koji sadrži pikone"""
        # Prvo provjeri trenutni direktorijum
        if self.has_picon_files(self.current_path):
            self.select_current_path()
            return
        
        # Provjeri podfoldere
        try:
            for entry in self.entries:
                if entry[2] and "has picons" in entry[0]:
                    # Pronađen folder sa piconima
                    self["status_label"].setText(f"Found picon folder: {entry[1]}")
                    self.load_directory(entry[1])
                    self.select_current_path()
                    return
        except:
            pass
        
        self["status_label"].setText("No picon folder found automatically")
    
    def exit(self):
        """Izlaz iz ekrana"""
        self.close()