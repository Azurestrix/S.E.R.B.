from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp




# Define screens

class MainMenu(Screen):
    pass


class ReceiveMenu(Screen):
    generalList = [
        "FERŐTLENÍTŐ----------", "Brado Clean 1L", "Brado Clean 5L",
        "Brado Plus 1000ML", "Brado Plus 250ML", "Bradogél 500ML",
        "Bradogél 1000ML", "Bradosept 1L", "Bradosept 5L", "Mikorzid AF 100ML",
        "Mikrozid szórófej", "Mikrozid dobozos törlőkendő 150x",
        "Mikrozid dobozos törlőkendő utántöltő 150x", "Sekusept Aktív",
        "Skinman Soft Protect", "Skinman Soft Plus", "Skinsan Scrub",
        "Imi Orange", "Melsept 1000ML", "", "KESZTYŰ----------", "XL Kesztyű",
        "L Kesztyű", "M Kesztyű", "S Kesztyű", "", "CÍMKÉK----------",
        "500-as címke", "80x80 donor címke hűtőházas", "Donorkártya címke 80x50",
        "1000-es címke (Mintacső)", "150x80 dobozos címkehűtőházas", "",
        "TAKARÍTÓ----------", "Lucart Jumbo WC papír 12x (donor?)",
        "Lucart kéztörlő 155 ID", "Lucart kéztörlő henger 140A",
        "Lucart WC papír 10x (személyzeti)", "Lucart Z kéztörlő 15x",
        "Tork Illatosító", "Tork folyékony szappan", "", "EGYÉB----------",
        "Szájmaszk", "Szájmaszk FFP2", "Fénymásoló papír 500x", "Vizes Ballon",
        "Műanyag pohár"
    ]

    receptionList = [
        "AJÁNDÉK----------", "Biotech USA műzli", "Belvita", "Sportszelet",
        "Swiss ital", "", "EGYÉB----------", "Függőmappa", "Függőmappa lefűző",
        "Lábzsák", "Archiváló doboz"
    ]

    donorList = [
        "CSÖVEK----------", "BD Vacutainer", "Biztonsági tű 21G", "NAT 4ML",
        "NAT 6ML", "S-Monovette Fehér", "S-Monovette Zöld", "S-Monovette Lila",
        "S-Monovette Piros", "Vérvételi harang", "", "EGYÉB----------",
        "Hányós zacskó", "Papírlepedő", "Omnisilk", "Pur-Zellin", "Peha-Haft"
    ]

    productionList = [
        "FŐ SEGÉDANYAG----------", "Szerelék ZBK", "Szerelék 4117",
        "Egyszer használatos kanül", "NaCl - Fresenius 250ML",
        "NaCl - Fresenius 500ML", "NaCl - B. Braun", "Citrát - Fresenius",
        "Citrát - Medites Pharma", "Citrát - Macopharma", "Citrát - Haemonetics",
        "", "SYSMEX----------", "Cellclean 50ML", "Cellpack 20L",
        "Stromatolyser", "Kontrollvér Low", "Kontrollvér Normal", "",
        "VESZÉLYES HULLADÉK----------"
        "Veszélyes hulladék kanna", "Veszélyes hulladék kuka 2L",
        "Veszélyes hulladék 5L", "Veszélyes hulladék 10L",
        "Veszélyes hulladék 20L", "Veszélyes hulladék 60L",
        "Veszélyes hulladék zsák", "", "EGYÉB----------",
        "Egyszerhasználatos köpeny", "Hőpapír", "Élvédő"
                                                "Gyorskötegelő", "NAT hungarocell", "NAT hungarocell nylon",
        "Raklapfólia", "Plazmatároló M5 rekesz fagyasztókamrához", "Élvédő"
    ]






    def spinner_clicked(self, value):
        if value == "Általános":
            self.ids.item_spinner.values = self.generalList
            self.ids.item_spinner.text = "Általános"
        elif value == "Termelés":
            self.ids.item_spinner.values = self.productionList
            self.ids.item_spinner.text = "Termelés"
        elif value == "Donorterem":
            self.ids.item_spinner.values = self.donorList
            self.ids.item_spinner.text = "Donorterem"
        else:
            self.ids.item_spinner.values = self.receptionList
            self.ids.item_spinner.text = "Recepció"


















class ExpendMenu(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file(
    'MyApp.kv')  # returnnél visszaadom mivel ez vonatkozik a kv fájlra ami tartalmazni fogja a windowokat

class MyApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyApp().run()
