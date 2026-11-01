from __future__ import absolute_import
from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Button import Button
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap
from enigma import eTimer, ePoint
import os
import re
import xml.etree.ElementTree as ET

class AssignPiconScreen(Screen):
    """Ekran za dodjelu picona kanalu - prikazuje pikone u gridu iz selektiranog foldera"""
    skin = """
    <screen position="center,center" size="1920,1080" backgroundColor="#011a2e">
        <widget name="separator0" position="0,5" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />
        <widget name="title" position="0,10" size="1920,40" font="Bold;30" halign="center" backgroundColor="#012e01" foregroundColor="#FFFFFF" text="..:: Assign a Picon ::.." />
        <widget name="channel_info" position="0,55" size="1920,30" font="Bold;24" halign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" />
        <widget name="separator1" position="0,87" size="1920,3" backgroundColor="#d5fa02" zPosition="1" />

        <widget name="folder_info" position="20,95" size="1350,30" font="Regular;20" halign="left" foregroundColor="#00FF00" backgroundColor="#011a2e" />
        <widget name="filter_info" position="20,125" size="1350,25" font="Regular;20" halign="left" foregroundColor="#FFAA00" backgroundColor="#011a2e" />

        <widget name="pix_0" position="20,155" size="220,132" alphatest="blend" />
        <widget name="lab_0" position="20,290" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_1" position="245,155" size="220,132" alphatest="blend" />
        <widget name="lab_1" position="245,290" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_2" position="470,155" size="220,132" alphatest="blend" />
        <widget name="lab_2" position="470,290" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_3" position="695,155" size="220,132" alphatest="blend" />
        <widget name="lab_3" position="695,290" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_4" position="920,155" size="220,132" alphatest="blend" />
        <widget name="lab_4" position="920,290" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_5" position="1145,155" size="220,132" alphatest="blend" />
        <widget name="lab_5" position="1145,290" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />

        <widget name="pix_6" position="20,345" size="220,132" alphatest="blend" />
        <widget name="lab_6" position="20,480" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_7" position="245,345" size="220,132" alphatest="blend" />
        <widget name="lab_7" position="245,480" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_8" position="470,345" size="220,132" alphatest="blend" />
        <widget name="lab_8" position="470,480" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_9" position="695,345" size="220,132" alphatest="blend" />
        <widget name="lab_9" position="695,480" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_10" position="920,345" size="220,132" alphatest="blend" />
        <widget name="lab_10" position="920,480" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_11" position="1145,345" size="220,132" alphatest="blend" />
        <widget name="lab_11" position="1145,480" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />

        <widget name="pix_12" position="20,535" size="220,132" alphatest="blend" />
        <widget name="lab_12" position="20,670" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_13" position="245,535" size="220,132" alphatest="blend" />
        <widget name="lab_13" position="245,670" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_14" position="470,535" size="220,132" alphatest="blend" />
        <widget name="lab_14" position="470,670" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_15" position="695,535" size="220,132" alphatest="blend" />
        <widget name="lab_15" position="695,670" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_16" position="920,535" size="220,132" alphatest="blend" />
        <widget name="lab_16" position="920,670" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_17" position="1145,535" size="220,132" alphatest="blend" />
        <widget name="lab_17" position="1145,670" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />

        <widget name="pix_18" position="20,725" size="220,132" alphatest="blend" />
        <widget name="lab_18" position="20,860" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_19" position="245,725" size="220,132" alphatest="blend" />
        <widget name="lab_19" position="245,860" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_20" position="470,725" size="220,132" alphatest="blend" />
        <widget name="lab_20" position="470,860" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_21" position="695,725" size="220,132" alphatest="blend" />
        <widget name="lab_21" position="695,860" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_22" position="920,725" size="220,132" alphatest="blend" />
        <widget name="lab_22" position="920,860" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />
        <widget name="pix_23" position="1145,725" size="220,132" alphatest="blend" />
        <widget name="lab_23" position="1145,860" size="220,34" font="Regular;17" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#0D1B36" />

        <!-- Pokretni okvir (frame) koji prati selekciju -->
        <widget name="selection_frame" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpPiconManager/frame.png" position="-999,-999" size="225,137" zPosition="10" alphatest="blend" />

        <widget name="page_label" position="20,965" size="1350,30" font="Bold;24" halign="center" valign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" />

        <widget name="preview_bg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpPiconManager/picon_bg.png" position="1370,140" size="540,250" backgroundColor="#0D1B36" />
        <widget name="preview_picon" position="1530,450" size="220,132" alphatest="blend" />
        <widget name="preview_name" position="1370,650" size="540,40" font="Bold;24" halign="center" valign="center" foregroundColor="#FFFFFF" backgroundColor="#011a2e" />

        <widget name="key_red" position="1370,760" size="540,40" backgroundColor="red" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="EXIT" />
        <widget name="key_green" position="1370,805" size="540,40" backgroundColor="green" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="ASSIGN" />
        <widget name="key_yellow" position="1370,850" size="265,40" backgroundColor="#FFD700" font="Bold;24" foregroundColor="#000000" halign="center" valign="center" text="PREV" />
        <widget name="key_blue" position="1645,850" size="265,40" backgroundColor="#0000CC" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="NEXT" />
        <widget name="key_menu" position="1370,895" size="540,40" backgroundColor="#444444" font="Bold;24" foregroundColor="#FFFFFF" halign="center" valign="center" text="MENU - Filter" />

        <widget name="status_label" position="1370,965" size="540,30" font="Bold;24" halign="center" valign="center" foregroundColor="#BBBBBB" backgroundColor="#011a2e" />
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

        self.original_picon_files = []   
        self.picon_files = []            
        self.selected_index = 0
        self.active_filter = None        

        self.grid_columns = 6
        self.grid_rows = 4
        self.grid_page_size = self.grid_columns * self.grid_rows
        self.grid_index = 0

        self.grid_pixmaps = []
        self.grid_labels = []

        for i in range(self.grid_page_size):
            pix_key = f"pix_{i}"
            lab_key = f"lab_{i}"
            self[pix_key] = Pixmap()
            self[lab_key] = Label()
            self.grid_pixmaps.append(self[pix_key])
            self.grid_labels.append(self[lab_key])

        self["selection_frame"] = Pixmap()
        self["page_label"] = Label()
        self["preview_picon"] = Pixmap()
        self["preview_bg"] = Pixmap()
        self["preview_name"] = Label()
        self["status_label"] = Label()
        self["folder_info"] = Label()
        self["filter_info"] = Label()
        self["separator0"] = Label()
        self["separator1"] = Label()
        self["separator2"] = Label()
        self["separator3"] = Label()

        self["key_red"] = Button("EXIT")
        self["key_green"] = Button("ASSIGN")
        self["key_yellow"] = Button("PREV")
        self["key_blue"] = Button("NEXT")
        self["key_menu"] = Button("MENU - Filter")

        self["title"] = Label("..:: Assign a Picon ::..")
        self["channel_info"] = Label(f"Channel: {channel_name}")
        self["folder_info"].setText(f"Current folder: {picon_manager.picon_path}")

        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions", "ColorActions", "MenuActions"],
            {
                "cancel": self.exit,
                "ok": self.assign_picon,
                "up": self.move_up,
                "down": self.move_down,
                "left": self.move_left,
                "right": self.move_right,
                "red": self.exit,
                "green": self.assign_picon,
                "yellow": self.prev_page,
                "blue": self.next_page,
                "menu": self.open_filter_menu,
            },
            -1
        )

        self.onLayoutFinish.append(self.load_picons)

    def load_picons(self):
        from Components.config import config
        if hasattr(config.plugins, "ciefp_picon_manager"):
            new_path = config.plugins.ciefp_picon_manager.picon_path.value
            if new_path and self.picon_manager.picon_path != new_path:
                self.picon_manager.set_picon_path(new_path)
                self["folder_info"].setText(f"Current folder: {new_path}")

        self.original_picon_files = self.picon_manager.get_picons_from_selected_folder()
        self.picon_files = list(self.original_picon_files)
        self.grid_index = 0
        self.active_filter = None
        self.update_filter_label()

        if not self.picon_files:
            self.clear_grid()
            self["status_label"].setText("No picons found in selected folder")
            self["preview_picon"].setPixmap(None)
            self["preview_name"].setText("No picons available")
            self["page_label"].setText("0 / 0")
            self["selection_frame"].instance.hide()
            return

        self["status_label"].setText(f"Found {len(self.picon_files)} picons in selected folder")
        self.render_grid()

    def clear_grid(self):
        for i in range(self.grid_page_size):
            if i < len(self.grid_pixmaps):
                try:
                    self.grid_pixmaps[i].setPixmap(None)
                except:
                    pass
            if i < len(self.grid_labels):
                try:
                    self.grid_labels[i].setText("")
                except:
                    pass
        try:
            self["selection_frame"].instance.hide()
        except:
            pass

    def render_grid(self):
        self.clear_grid()
        if not self.picon_files:
            self["page_label"].setText("0 / 0")
            self["preview_picon"].setPixmap(None)
            self["preview_name"].setText("No selection")
            return

        if self.grid_index >= len(self.picon_files):
            self.grid_index = max(0, len(self.picon_files) - 1)

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
                if pix and slot < len(self.grid_pixmaps):
                    self.grid_pixmaps[slot].setPixmap(pix)
            except Exception as e:
                print(f"Error loading grid picon: {e}")

            short_name = name if len(name) <= 24 else name[:21] + "..."
            # Uklonjen stari "> " prefiks, sada koristimo okvir
            self.grid_labels[slot].setText(short_name)

        # Pozicioniranje okvira na trenutno selektovani slot na stranici
        slot_on_page = self.grid_index % self.grid_page_size
        if slot_on_page < len(visible):
            row = slot_on_page // self.grid_columns
            col = slot_on_page % self.grid_columns

            # X start = 20, korak = 225
            # Y start = 155, korak = 190
            x = 20 + (col * 225) - 2
            y = 155 + (row * 190) - 2

            try:
                self["selection_frame"].instance.move(ePoint(x, y))
                self["selection_frame"].instance.show()
            except Exception as e:
                print(f"[AssignPicon] Error moving selection frame: {e}")
        else:
            try:
                self["selection_frame"].instance.hide()
            except:
                pass

        total_pages = max(1, (len(self.picon_files) + self.grid_page_size - 1) // self.grid_page_size)
        self["page_label"].setText(
            f"Page {page + 1} / {total_pages}    |    Picon {self.grid_index + 1} / {len(self.picon_files)}"
        )
        self.preview_picon()

    def preview_picon(self):
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

    def get_picon_filename_from_ref(self, ref):
        if not ref:
            return None
        parts = ref.split(':')
        if len(parts) < 6:
            return None
        sid = parts[0].upper()
        ns = parts[1].upper()
        tsid = parts[2].upper()
        onid = parts[3].upper()
        srv_type = parts[4].upper()
        return f"1_0_{srv_type}_{sid}_{tsid}_{onid}_{ns}_0_0_0.png"

    def move_up(self):
        if not self.picon_files:
            return
        n = self.grid_index - self.grid_columns
        if n >= 0:
            self.grid_index = n
            self.render_grid()

    def move_down(self):
        if not self.picon_files:
            return
        n = self.grid_index + self.grid_columns
        if n < len(self.picon_files):
            self.grid_index = n
            self.render_grid()

    def move_left(self):
        if not self.picon_files:
            return
        if self.grid_index > 0:
            self.grid_index -= 1
            self.render_grid()

    def move_right(self):
        if not self.picon_files:
            return
        if self.grid_index < len(self.picon_files) - 1:
            self.grid_index += 1
            self.render_grid()

    def prev_page(self):
        if not self.picon_files:
            return
        if self.grid_index >= self.grid_page_size:
            self.grid_index -= self.grid_page_size
            self.render_grid()
        else:
            self["status_label"].setText("Already on first page")

    def next_page(self):
        if not self.picon_files:
            return
        n = self.grid_index + self.grid_page_size
        if n < len(self.picon_files):
            self.grid_index = n
            self.render_grid()
        else:
            self["status_label"].setText("Already on last page")

    def open_filter_menu(self):
        options = [
            ("1. Search by name (VirtualKeyboard)", "search"),
            ("2. Filter by satellite", "sat"),
            ("3. Filter by provider", "provider"),
            ("X. Clear all filters", "clear"),
        ]
        self.session.openWithCallback(self.filter_menu_callback, ChoiceBox, title="Filter picons", list=options)

    def filter_menu_callback(self, choice):
        if not choice:
            return
        key = choice[1]
        if key == "search":
            self.session.openWithCallback(self.apply_search_filter, VirtualKeyBoard, title="Search picon by name:", text="")
        elif key == "sat":
            self.open_satellite_chooser()
        elif key == "provider":
            self.open_provider_chooser()
        elif key == "clear":
            self.clear_filters()

    def apply_search_filter(self, text):
        if not text:
            return
        text_l = text.lower()
        found_refs = []
        try:
            with open("/etc/enigma2/lamedb", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            in_services = False
            current_service = None
            current_channel_name = ""
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped == "services":
                    in_services = True
                    continue
                if in_services and stripped == "end":
                    break
                if in_services:
                    if ":" in stripped and not stripped.startswith("p:") and not stripped.startswith("c:") and not stripped.startswith("f:"):
                        parts = stripped.split(":")
                        if len(parts) >= 5:
                            current_service = (parts[0].upper(), parts[1].upper())
                            if i + 1 < len(lines):
                                current_channel_name = lines[i + 1].strip()
                                if text_l in current_channel_name.lower():
                                    found_refs.append(current_service)
                            if "p:" in stripped:
                                p_part = stripped.split("p:")[1].split(",")[0].strip()
                                if text_l in p_part.lower():
                                    if current_service not in found_refs:
                                        found_refs.append(current_service)
                    elif stripped.startswith("p:") and current_service:
                        p_name = stripped[2:].split(",")[0].strip()
                        if text_l in p_name.lower():
                            if current_service not in found_refs:
                                found_refs.append(current_service)
                        current_service = None
                        current_channel_name = ""
        except Exception as e:
            print(f"Error searching lamedb: {e}")

        if found_refs:
            filtered_picons = []
            for item in self.original_picon_files:
                filename = item[2].upper().replace(".PNG", "")
                parts = filename.split("_")
                if len(parts) >= 7:
                    picon_sid = parts[3].lstrip('0') or '0'
                    picon_ns = parts[6].lstrip('0') or '0'
                    for sid, ns in found_refs:
                        lamedb_sid = sid.lstrip('0') or '0'
                        lamedb_ns = ns.lstrip('0') or '0'
                        if picon_sid == lamedb_sid and picon_ns == lamedb_ns:
                            filtered_picons.append(item)
                            break
            self.picon_files = filtered_picons
            self.active_filter = ("search", text)
            self.grid_index = 0
            self.update_filter_label()
            self.render_grid()
            self["status_label"].setText(f"Search '{text}': {len(self.picon_files)} picons found in lamedb")
        else:
            self.picon_files = [
                item for item in self.original_picon_files
                if text_l in item[0].lower() or text_l in item[2].lower()
            ]
            self.active_filter = ("search", text)
            self.grid_index = 0
            self.update_filter_label()
            self.render_grid()
            self["status_label"].setText(f"Search '{text}': {len(self.picon_files)} picons found (filename)")

    def open_satellite_chooser(self):
        satellites = self.load_satellite_names()
        if not satellites:
            self["status_label"].setText("No satellites found in satellites.xml")
            return
        choices = [("Show All Satellites", "ALL")]
        for display_name, pos_str in satellites:
            choices.append((display_name, pos_str))
        self.session.openWithCallback(self.satellite_selected_callback, ChoiceBox, title="Filter by Satellite", list=choices)

    def satellite_selected_callback(self, choice):
        if not choice:
            return
        pos_str = choice[1]
        if pos_str == "ALL":
            self.picon_files = list(self.original_picon_files)
            self.active_filter = None
            self.grid_index = 0
            self.update_filter_label()
            self.render_grid()
            self["status_label"].setText(f"Filter cleared. Total: {len(self.picon_files)} picons")
            return

        ns_hex = None
        try:
            clean_pos = pos_str.replace("°", "").replace(" ", "")
            if clean_pos.endswith("E"):
                deg = float(clean_pos[:-1])
                ns_val = int(deg * 10)
                ns_hex = f"{ns_val:04x}"
            elif clean_pos.endswith("W"):
                deg = float(clean_pos[:-1])
                ns_val = 3600 - int(deg * 10)
                ns_hex = f"{ns_val:04x}"
        except Exception as e:
            print(f"[AssignPicon] Error calculating HEX for {pos_str}: {e}")

        variants = []
        if ns_hex:
            variants.append(ns_hex.lower())
            if ns_hex.startswith("00"):
                variants.append(ns_hex[2:].lower())
            variants.append(ns_hex.upper())

        pos_clean = pos_str.replace(".", "").replace("°", "")
        pos_no_dot = pos_str.replace(".0", "").replace("°", "")
        variants.extend([
            pos_str.lower(),
            pos_clean.lower(),
            pos_no_dot.lower(),
            pos_str.replace(".", "_").replace("°", "").lower()
        ])
        variants = list(set(variants))

        def matches(filename, name):
            fname_lower = filename.lower()
            name_lower = name.lower()
            for variant in variants:
                if variant in fname_lower or variant in name_lower:
                    return True
            return False

        self.picon_files = [
            item for item in self.original_picon_files
            if matches(item[2], item[0])
        ]
        self.active_filter = ("sat", pos_str)
        self.grid_index = 0
        self.update_filter_label()
        self.render_grid()
        self["status_label"].setText(f"Filter '{pos_str}' [{ns_hex}]: {len(self.picon_files)} picons found")

    def open_provider_chooser(self):
        providers = self.get_all_providers_from_lamedb()
        if not providers:
            self["status_label"].setText("No providers found in lamedb")
            return
        choices = [("Show All Providers", "ALL")]
        for prov in sorted(providers):
            choices.append((prov, prov))
        self.session.openWithCallback(self.provider_selected_callback, ChoiceBox, title="Filter by Provider", list=choices)

    def provider_selected_callback(self, choice):
        if not choice:
            return
        provider = choice[1]
        if provider == "ALL":
            self.picon_files = list(self.original_picon_files)
            self.active_filter = None
            self.grid_index = 0
            self.update_filter_label()
            self.render_grid()
            self["status_label"].setText(f"Filter cleared. Total: {len(self.picon_files)} picons")
            return

        found_refs = []
        prov_lower = provider.lower()
        try:
            with open("/etc/enigma2/lamedb", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            in_services = False
            current_service = None
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped == "services":
                    in_services = True
                    continue
                if in_services and stripped == "end":
                    break
                if in_services:
                    if ":" in stripped and not stripped.startswith("p:") and not stripped.startswith("c:") and not stripped.startswith("f:"):
                        parts = stripped.split(":")
                        if len(parts) >= 5:
                            current_service = (parts[0].upper(), parts[1].upper())
                            if "p:" in stripped:
                                p_part = stripped.split("p:")[1].split(",")[0].strip()
                                if p_part.lower() == prov_lower:
                                    found_refs.append(current_service)
                    elif stripped.startswith("p:") and current_service:
                        p_name = stripped[2:].split(",")[0].strip()
                        if p_name.lower() == prov_lower:
                            found_refs.append(current_service)
                        current_service = None
        except Exception as e:
            print(f"Error searching provider in lamedb: {e}")

        if found_refs:
            filtered_picons = []
            for item in self.original_picon_files:
                filename = item[2].upper().replace(".PNG", "")
                parts = filename.split("_")
                if len(parts) >= 7:
                    picon_sid = parts[3].lstrip('0') or '0'
                    picon_ns = parts[6].lstrip('0') or '0'
                    for sid, ns in found_refs:
                        lamedb_sid = sid.lstrip('0') or '0'
                        lamedb_ns = ns.lstrip('0') or '0'
                        if picon_sid == lamedb_sid and picon_ns == lamedb_ns:
                            filtered_picons.append(item)
                            break
            self.picon_files = filtered_picons
            self.active_filter = ("provider", provider)
            self.grid_index = 0
            self.update_filter_label()
            self.render_grid()
            self["status_label"].setText(f"Provider '{provider}': {len(self.picon_files)} picons found in lamedb")
        else:
            self["status_label"].setText(f"Provider '{provider}' not found in lamedb or no matching picons")

    def load_satellite_names(self):
        """Učitaj listu satelita iz satellites.xml. Vraća listu (display_name, pos_str)."""
        sat_list = []
        paths = ["/etc/tuxbox/satellites.xml", "/etc/enigma2/satellites.xml"]
        xml_path = None
        for path in paths:
            if os.path.exists(path):
                xml_path = path
                break

        if not xml_path:
            return sat_list

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            for sat in root.findall('sat'):
                name = sat.get('name', '')
                position_raw = sat.get('position', '')
                if name and position_raw:
                    pos_val = int(position_raw)
                    if pos_val < 0:
                        deg = abs(pos_val) / 10.0
                        pos_str = f"{deg:.1f}°W".replace(".0°W", "°W")
                    else:
                        if pos_val > 1800:
                            deg = (3600 - pos_val) / 10.0
                            pos_str = f"{deg:.1f}°W".replace(".0°W", "°W")
                        else:
                            deg = pos_val / 10.0
                            pos_str = f"{deg:.1f}°E".replace(".0°E", "°E")

                    clean_name = re.sub(r'\(\d+\)\s*', '', name)
                    display_name = f"{clean_name} ({pos_str})"
                    sat_list.append((display_name, pos_str))
        except Exception as e:
            print(f"Error parsing satellites.xml: {e}")

        # Ukloni duplikate
        seen = set()
        unique = []
        for item in sat_list:
            if item[1] not in seen:
                seen.add(item[1])
                unique.append(item)

        return unique

    def get_all_providers_from_lamedb(self):
        """Vrati set svih provajdera iz lamedb."""
        providers = set()
        try:
            with open("/etc/enigma2/lamedb", "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            start_idx = content.find("\nservices\n")
            end_idx = content.find("\nend\n", start_idx)
            if start_idx == -1 or end_idx == -1:
                print("[AssignPicon] Could not find services section in lamedb")
                return providers

            # Uzmi samo blok između "services" i "end"
            services_block = content[start_idx + 10:end_idx]
            lines = services_block.splitlines()

            # Nema potrebe za in_services flag-om - već smo u services bloku
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("p:"):
                    # Format može biti:
                    #   p:M7 Group,c:0007d1,c:0307d1,...
                    #   p:Mediaset
                    #   p:           (prazno - preskoči)
                    prov = stripped[2:].split(",")[0].strip()
                    if prov and prov != "Unknown":
                        providers.add(prov)

            print(f"[AssignPicon] Found {len(providers)} providers in lamedb")
        except Exception as e:
            print(f"Error reading providers from lamedb: {e}")

        return providers
        
    def clear_filters(self, *args):
        self.picon_files = list(self.original_picon_files)
        self.active_filter = None
        self.grid_index = 0
        self.update_filter_label()
        self.render_grid()
        self["status_label"].setText(f"All filters cleared. {len(self.picon_files)} picons.")

    def update_filter_label(self):
        if not self.active_filter:
            self["filter_info"].setText("Filter: none")
            return
        kind, val = self.active_filter
        if kind == "search":
            self["filter_info"].setText(f"Filter: search '{val}'")
        elif kind == "sat":
            self["filter_info"].setText(f"Filter: satellite {val}")
        elif kind == "provider":
            self["filter_info"].setText(f"Filter: provider '{val}'")
        else:
            self["filter_info"].setText(f"Filter: {kind} = {val}")

    def assign_picon(self):
        if not self.picon_files or self.grid_index >= len(self.picon_files):
            self["status_label"].setText("Please select a picon")
            return
        if not self.service_ref:
            self["status_label"].setText("No service reference")
            return

        source_path = self.picon_files[self.grid_index][1]
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
        self.close()