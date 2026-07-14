from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from android.storage import primary_external_storage_path
from os.path import join
import os
import base64
import requests
import random
import string
import hashlib

MASTER_PASSWORD_HASH = "01a40d28626c055d9d0e3991018aaec61fa55a62572eb44101b533c6680041ec"
KASALUKUYANG_BERSYON = "1.0"
UPDATE_JSON_URL = "https://raw.githubusercontent.com/fbvlink2026-lab/aking-mga-video/main/bersyon.json"
AUTHORITY_PROVIDER = "org.martodosko.martodoskoapp.fileprovider"
MGA_TAMANG_SUSI = []
PANGALAN_APP = "MartoDosko"

README_NILALAMAN = """
📹 Video Link Page Maker
Bersyon 1.1 | MartoDosko
"""

ABOUT_NILALAMAN = f"""✨ {PANGALAN_APP}
Video Link Page Maker
Bersyon: {KASALUKUYANG_BERSYON}
© 2026
"""

def gumawa_bagong_susi():
    b1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    b2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    b3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"VID-2026-{b1}-{b2}-{b3}"

def ay_susi_tama(susi):
    return susi.strip().upper() in MGA_TAMANG_SUSI

def ay_password_tama(pasahin):
    return hashlib.sha256(pasahin.strip().encode()).hexdigest() == MASTER_PASSWORD_HASH

PAHINA_TEMPLATE = """<!DOCTYPE html><html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="3; url={link_video}">
<title>{pamagat}</title>
<style>
body{{background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh}}
.card{{background:white;border-radius:12px;padding:30px 25px;max-width:380px;width:100%;text-align:center}}
.play{{width:100%;height:210px;border-radius:8px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;background-size:cover}}
.bilog{{width:75px;height:75px;background:rgba(255,0,0,.9);border-radius:50%;position:relative}}
.bilog::after{{content:"";position:absolute;top:50%;left:50%;transform:translate(-40%,-50%);border-top:16px solid transparent;border-bottom:16px solid transparent;border-left:26px solid #fff}}
h2{{font-size:17px;margin-bottom:10px}}
.btn{{display:block;padding:13px;background:#ff0000;color:#fff;font-size:16px;font-weight:bold;border-radius:6px;text-decoration:none}}
</style>
</head><body><div class="card"><a href="{link_video}" class="play" style="background-image:url({larawan})"><div class="bilog"></div></a><h2>{pamagat}</h2><a href="{link_video}" class="btn">🎬 Pumunta sa Video</a></div></body></html>"""

class PahinaNgPagpasok(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ly = BoxLayout(orientation="vertical", padding=20, spacing=12)
        ly.add_widget(Label(text=PANGALAN_APP, font_size=28, bold=True, color=(0.1,0.47,0.95,1)))
        ly.add_widget(Label(text=f"v{KASALUKUYANG_BERSYON}", font_size=14))
        tabs = TabbedPanel(size_hint_y=None, height=180)
        tabs.do_default_tab = False
        t1 = TabbedPanelItem(text="Gabay")
        sc = ScrollView(); sc.add_widget(Label(text=README_NILALAMAN, size_hint_y=None))
        t1.add_widget(sc)
        t2 = TabbedPanelItem(text="Tungkol")
        sc2 = ScrollView(); sc2.add_widget(Label(text=ABOUT_NILALAMAN, size_hint_y=None))
        t2.add_widget(sc2)
        tabs.add_widget(t1); tabs.add_widget(t2)
        ly.add_widget(tabs)
        ly.add_widget(Label(text="🔑 Ilagay ang Susi"))
        self.susi = TextInput(hint_text="VID-2026-XXXX-XXXX")
        ly.add_widget(self.susi)
        self.btn = Button(text="Patunayan", background_color=(0,0.6,0.2,1), size_hint_y=None, height=45)
        self.btn.bind(on_press=self.suriin)
        ly.add_widget(self.btn)
        self.mensahe = Label(text="")
        ly.add_widget(self.mensahe)
        self.btn_adm = Button(text="Admin", background_color=(0.3,0.3,0.3,1), size_hint_y=None, height=35)
        self.btn_adm.bind(on_press=self.bukas_admin)
        ly.add_widget(self.btn_adm)
        self.add_widget(ly)

    def suriin(self, i):
        if ay_susi_tama(self.susi.text):
            self.manager.current = "pangunahin"
        else: self.mensahe.text = "❌ Hindi wasto"

    def bukas_admin(self, i):
        l = BoxLayout(orientation="vertical", padding=15)
        l.add_widget(Label(text="Password ng Admin"))
        self.pas = TextInput(password=True)
        l.add_widget(self.pas)
        b_ok = Button(text="Pasok", background_color=(0,0.6,0.2,1))
        b_ok.bind(on_press=self.tignan)
        l.add_widget(b_ok)
        self.pop = Popup(title="Admin", content=l, size_hint=(0.8,0.3))
        self.pop.open()

    def tignan(self, i):
        if ay_password_tama(self.pas.text):
            self.pop.dismiss(); self.manager.current = "admin"
        else: self.pas.text=""

class AdminPanel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ly = BoxLayout(orientation="vertical", padding=15, spacing=10)
        ly.add_widget(Label(text="⚙️ ADMIN PANEL", font_size=16, bold=True, color=(0.9,0.5,0,1)))
        ly.add_widget(Label(text="Pangalan ng App:"))
        self.pang = TextInput(text=PANGALAN_APP)
        ly.add_widget(self.pang)
        ly.add_widget(Button(text="I-save", on_press=lambda x:self.isave_pangalan(), size_hint_y=None, height=40))
        ly.add_widget(Label(text="Gumawa ng Susi:"))
        ly.add_widget(Button(text="Bumuo Susi", on_press=lambda x:self.buo_susi(), size_hint_y=None, height=40))
        self.lbl_susi = Label(text="")
        ly.add_widget(self.lbl_susi)
        ly.add_widget(Button(text="Bumalik", on_press=lambda x:setattr(self.manager,'current','pasok'), size_hint_y=None, height=40))
        self.add_widget(ly)

    def isave_pangalan(self):
        global PANGALAN_APP; PANGALAN_APP=self.pang.text.strip()
        Popup(title="Tapos", content=Label(text="Magkakabisa pag-restart"), size_hint=(0.8,0.3)).open()

    def buo_susi(self):
        bago = gumawa_bagong_susi()
        MGA_TAMANG_SUSI.append(bago)
        self.lbl_susi.text = "Bago: " + bago + "
Lahat:
" + "
".join(MGA_TAMANG_SUSI)

class PahinaNgPaggawa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ly = BoxLayout(orientation="vertical", padding=12, spacing=8)
        ly.add_widget(Label(text=f"📹 {PANGALAN_APP}", font_size=17, bold=True))
        ly.add_widget(Label(text="GitHub Username:")); self.u=TextInput(); ly.add_widget(self.u)
        ly.add_widget(Label(text="Repository:")); self.r=TextInput(); ly.add_widget(self.r)
        ly.add_widget(Label(text="Token:")); self.t=TextInput(password=True); ly.add_widget(self.t)
        ly.add_widget(Label(text="Link ng Video:")); self.lv=TextInput(); ly.add_widget(self.lv)
        ly.add_widget(Label(text="Pangalan ng Pahina:")); self.pn=TextInput(); ly.add_widget(self.pn)
        ly.add_widget(Label(text="Pamagat ng Video:")); self.tt=TextInput(); ly.add_widget(self.tt)
        ly.add_widget(Label(text="Pangalan ng Larawan (hal: vid.jpg):"))
        self.img_n = TextInput(hint_text="hal: thumbnail.jpg"); ly.add_widget(self.img_n)
        ly.add_widget(Button(text="✅ Bumuo at I-upload", background_color=(0,0.6,0.2,1), size_hint_y=None, height=45))
        self.res = Label(text=""); ly.add_widget(ScrollView(size_hint_y=None, height=120, children=[self.res]))
        self.add_widget(ly)

class Aplikasyon(App):
    def build(self):
        m = ScreenManager()
        m.add_widget(PahinaNgPagpasok(name="pasok"))
        m.add_widget(AdminPanel(name="admin"))
        m.add_widget(PahinaNgPaggawa(name="pangunahin"))
        return m

if __name__ == "__main__": Aplikasyon().run()
