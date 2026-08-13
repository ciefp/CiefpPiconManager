from __future__ import absolute_import
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Button import Button
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap
from enigma import eTimer
import os

class AssignPiconScreen(Screen):
    """Ekran za dodjelu picona kanalu - prikazuje pikone u gridu iz selektiranog foldera"""
    
    skin = """
    <screen position="center,center" size="1920,1080" backgroundColor="#011a2e">
        <!-- Titule -->
        <widget name="separator0" position="0,5" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
        <widget name="title" position="0,10" size="1920,40" font="Bold;30" halign="center" backgroundColor="#012e01" foregroundColor="#FFFFFF" text="..:: Assign a Picon ::.." />
        <widget name="channel_info" position="0,55" size="1920,30" font="Regular;20" halign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" />
        <widget name="separator1" position="0,87" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
        
        <!-- Info o folderu -->
        <widget name="folder_info" position="20,95" size="1350,30" font="Regular;20" halign="left" foregroundColor="#00FF00" backgroundColor="#011a2e" />
        
        <!-- Grid picona: 6 kolona x 4 reda -->
        <!-- Red 0 -->
        <widget name="pix_0" position="37,150" size="191,125" alphatest="blend" />
        <widget name="lab_0" position="35,277" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_1" position="257,150" size="191,125" alphatest="blend" />
        <widget name="lab_1" position="255,277" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_2" position="477,150" size="191,125" alphatest="blend" />
        <widget name="lab_2" position="475,277" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_3" position="697,150" size="191,125" alphatest="blend" />
        <widget name="lab_3" position="695,277" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_4" position="917,150" size="191,125" alphatest="blend" />
        <widget name="lab_4" position="915,277" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_5" position="1137,150" size="191,125" alphatest="blend" />
        <widget name="lab_5" position="1135,277" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        
        <!-- Red 1 -->
        <widget name="pix_6" position="37,360" size="191,125" alphatest="blend" />
        <widget name="lab_6" position="35,487" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_7" position="257,360" size="191,125" alphatest="blend" />
        <widget name="lab_7" position="255,487" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_8" position="477,360" size="191,125" alphatest="blend" />
        <widget name="lab_8" position="475,487" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_9" position="697,360" size="191,125" alphatest="blend" />
        <widget name="lab_9" position="695,487" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_10" position="917,360" size="191,125" alphatest="blend" />
        <widget name="lab_10" position="915,487" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_11" position="1137,360" size="191,125" alphatest="blend" />
        <widget name="lab_11" position="1135,487" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        
        <!-- Red 2 -->
        <widget name="pix_12" position="37,570" size="191,125" alphatest="blend" />
        <widget name="lab_12" position="35,697" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_13" position="257,570" size="191,125" alphatest="blend" />
        <widget name="lab_13" position="255,697" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_14" position="477,570" size="191,125" alphatest="blend" />
        <widget name="lab_14" position="475,697" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_15" position="697,570" size="191,125" alphatest="blend" />
        <widget name="lab_15" position="695,697" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_16" position="917,570" size="191,125" alphatest="blend" />
        <widget name="lab_16" position="915,697" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_17" position="1137,570" size="191,125" alphatest="blend" />
        <widget name="lab_17" position="1135,697" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        
        <!-- Red 3 -->
        <widget name="pix_18" position="37,780" size="191,125" alphatest="blend" />
        <widget name="lab_18" position="35,907" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_19" position="257,780" size="191,125" alphatest="blend" />
        <widget name="lab_19" position="255,907" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_20" position="477,780" size="191,125" alphatest="blend" />
        <widget name="lab_20" position="475,907" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_21" position="697,780" size="191,125" alphatest="blend" />
        <widget name="lab_21" position="695,907" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_22" position="917,780" size="191,125" alphatest="blend" />
        <widget name="lab_22" position="915,907" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_23" position="1137,780" size="191,125" alphatest="blend" />
        <widget name="lab_23" position="1135,907" size="195,42" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        
        <!-- Page info -->
        <widget name="page_label" position="20,965" size="1350,30" font="Regular;18" halign="center" valign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" />
        
        <!-- Preview -->
        <widget name="preview_bg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpPiconManager/picon_bg.png" position="1370,140" size="540,250" backgroundColor="#0D1B36" />
        <widget name="preview_picon" position="1530,450" size="220,132" alphatest="blend" />
        <widget name="preview_name" position="1370,650" size="540,40" font="Bold;24" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#011a2e" />
        
        <!-- Dugmad -->
        <widget name="key_red" position="1370,800" size="540,40" backgroundColor="red" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="EXIT" />
        <widget name="key_green" position="1370,850" size="540,40" backgroundColor="green" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="ASSIGN" />
        
        <!-- Status -->
        <widget name="status_label" position="1370,970" size="540,30" font="Regular;18" halign="center" valign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" />
        <widget name="separator2" position="0,950" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
        <widget name="separator3" position="0,1040" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
    </screen>
    """
    
    def __init__(self, session, channel_name, channel_refs, picon_manager, callback):
        Screen.__init__(self, session)
        
        self.channel_name = channel_name
        self.service_ref = channel_refs.get(channel_name, "")
        self.picon_manager = picon_manager
        self.callback = callback
        self.picon_files = []
        self.selected_index = 0
        
        # Podesavanja za grid
        self.grid_columns = 6
        self.grid_rows = 4
        self.grid_page_size = self.grid_columns * self.grid_rows
        self.grid_index = 0
        
        # Inicijaliziraj sve grid pixmap i label widgete
        self.grid_pixmaps = []
        self.grid_labels = []
        
        for i in range(self.grid_page_size):
            pix_key = f"pix_{i}"
            lab_key = f"lab_{i}"
            
            self[pix_key] = Pixmap()
            self[lab_key] = Label()
            
            self.grid_pixmaps.append(self[pix_key])
            self.grid_labels.append(self[lab_key])
        
        # Ostali widgeti
        self["page_label"] = Label()
        self["preview_picon"] = Pixmap()
        self["preview_bg"] = Pixmap()
        self["preview_name"] = Label()
        self["status_label"] = Label()
        self["folder_info"] = Label()
        self["separator0"] = Label()
        self["separator1"] = Label()
        self["separator2"] = Label()
        self["separator3"] = Label()
        
        # Dugmad
        self["key_red"] = Button("EXIT")
        self["key_green"] = Button("ASSIGN")
        
        # Naslovi
        self["title"] = Label("..:: Assign a Picon ::..")
        display_ref = self.service_ref
        if len(display_ref) > 60:
            display_ref = display_ref[:57] + "..."
        self["channel_info"] = Label(f"Channel: {channel_name}")
        
        # Pokaži koji folder se koristi
        self["folder_info"].setText(f"📁 Current folder: {picon_manager.picon_path}")
        
        # Akcije
        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions", "ColorActions"],
            {
                "cancel": self.exit,
                "ok": self.assign_picon,
                "up": self.move_up,
                "down": self.move_down,
                "left": self.move_left,
                "right": self.move_right,
                "red": self.exit,
                "green": self.assign_picon
            },
            -1
        )
        
        # Učitaj pikone nakon što je skin učitan
        self.onLayoutFinish.append(self.load_picons)
    
    def load_picons(self):
        """Učitaj pikone iz trenutno podešenog foldera i prikaži ih kao grid."""
        # Provjeri trenutnu putanju iz configa
        from Components.config import config
        if hasattr(config.plugins, "ciefp_picon_manager"):
            new_path = config.plugins.ciefp_picon_manager.picon_path.value
            if new_path and self.picon_manager.picon_path != new_path:
                print(f"[AssignPiconScreen] Updating path from {self.picon_manager.picon_path} to {new_path}")
                self.picon_manager.set_picon_path(new_path)
                self["folder_info"].setText(f"📁 Current folder: {new_path}")
        
        self.picon_files = self.picon_manager.get_picons_from_selected_folder()
        self.grid_index = 0

        if not self.picon_files:
            self.clear_grid()
            self["status_label"].setText("No picons found in selected folder")
            self["preview_picon"].setPixmap(None)
            self["preview_name"].setText("No picons available")
            self["page_label"].setText("0 / 0")
            return

        self["status_label"].setText(f"Found {len(self.picon_files)} picons in selected folder")
        self.render_grid()

    def clear_grid(self):
        """Očisti svih 24 polja grida."""
        for i in range(self.grid_page_size):
            if i < len(self.grid_pixmaps) and self.grid_pixmaps[i] is not None:
                try:
                    self.grid_pixmaps[i].setPixmap(None)
                except:
                    pass
            if i < len(self.grid_labels) and self.grid_labels[i] is not None:
                try:
                    self.grid_labels[i].setText("")
                except:
                    pass

    def render_grid(self):
        """Prikaži jednu stranicu sa 24 pikona."""
        self.clear_grid()

        if not self.picon_files:
            return

        page = self.grid_index // self.grid_page_size
        start = page * self.grid_page_size
        end = min(start + self.grid_page_size, len(self.picon_files))
        visible = self.picon_files[start:end]

        for slot, item in enumerate(visible):
            if slot >= self.grid_page_size:
                break

            name, path, filename = item
            try:
                pix = LoadPixmap(path)
                if pix and slot < len(self.grid_pixmaps) and self.grid_pixmaps[slot] is not None:
                    self.grid_pixmaps[slot].setPixmap(pix)
            except Exception as e:
                print(f"Error loading grid picon: {e}")

            short_name = name
            if len(short_name) > 24:
                short_name = short_name[:21] + "..."
                
            if slot < len(self.grid_labels) and self.grid_labels[slot] is not None:
                # Označi selektirani picon
                if (start + slot) == self.grid_index:
                    self.grid_labels[slot].setText(f"> {short_name}")
                else:
                    self.grid_labels[slot].setText(short_name)

        total_pages = (len(self.picon_files) + self.grid_page_size - 1) // self.grid_page_size
        current_page = page + 1
        self["page_label"].setText(
            f"Page {current_page} / {total_pages}    |    Picon {self.grid_index + 1} / {len(self.picon_files)}"
        )
        self.preview_picon()

    def move_up(self):
        """Pomeri izbor jedan red gore."""
        if not self.picon_files:
            return
        new_index = self.grid_index - self.grid_columns
        if new_index >= 0:
            self.grid_index = new_index
            self.render_grid()

    def move_down(self):
        """Pomeri izbor jedan red dole."""
        if not self.picon_files:
            return
        new_index = self.grid_index + self.grid_columns
        if new_index < len(self.picon_files):
            self.grid_index = new_index
            self.render_grid()

    def move_left(self):
        """Pomeri izbor ulevo."""
        if not self.picon_files:
            return
        if self.grid_index > 0:
            self.grid_index -= 1
            self.render_grid()

    def move_right(self):
        """Pomeri izbor udesno."""
        if not self.picon_files:
            return
        if self.grid_index < len(self.picon_files) - 1:
            self.grid_index += 1
            self.render_grid()

    def preview_picon(self):
        """Prikaži veliki preview trenutno selektovanog picona."""
        if not self.picon_files or self.grid_index >= len(self.picon_files):
            self["preview_picon"].setPixmap(None)
            self["preview_name"].setText("No selection")
            return

        name, path, filename = self.picon_files[self.grid_index]
        try:
            picon = LoadPixmap(path)
            if picon:
                self["preview_picon"].setPixmap(picon)
                self["preview_name"].setText(name[:30])
            else:
                self["preview_picon"].setPixmap(None)
                self["preview_name"].setText("Invalid picon")
        except Exception as e:
            print(f"Error loading picon preview: {e}")
            self["preview_picon"].setPixmap(None)
            self["preview_name"].setText("Error loading")

    def assign_picon(self):
        if not self.picon_files or self.grid_index >= len(self.picon_files):
            self["status_label"].setText("Please select a picon")
            return

        if not self.service_ref:
            self["status_label"].setText("No service reference")
            return

        source_path = self.picon_files[self.grid_index][1]

        print(f"[AssignPiconScreen] Assigning picon:")
        print(f"  - Service Ref: {self.service_ref}")
        print(f"  - Source: {source_path}")
        print(f"  - Target folder: {self.picon_manager.picon_path}")

        if self.picon_manager.assign_picon(self.service_ref, source_path):
            self["status_label"].setText("Picon assigned successfully")
            if self.callback:
                self.callback(True)
            self.timer = eTimer()
            self.timer.callback.append(self.exit)
            self.timer.start(1000, True)
        else:
            self["status_label"].setText("Error assigning picon")
            
    def exit(self):
        """Izlaz iz ekrana"""
        self.close()