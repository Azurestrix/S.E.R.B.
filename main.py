#Time despite it stops the main thread I want it to actually stop it so the user won't mess up stuff.
import time
#Datetime important to call it techically twiche because there is also and inner datetime module
from datetime import datetime
# Kivy
from kivy.uix.screenmanager import ScreenManager, Screen
# KivyMD for Datepicker
from kivymd.app import MDApp
# KivyMD DatePicker module
from kivymd.uix.pickers import MDDatePicker
# Kivy Factory
from kivy.factory import Factory

# Google Sheet communication
import gspread
# Authenticate with Google Sheets
from oauth2client.service_account import ServiceAccountCredentials

# Defining screens
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
        "Imi Orange", "Melsept 1000ML", "", "KESZTYŰ----------", "XXL Kesztyű", "XL Kesztyű",
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


    sync_List = []
    input_values_dictionary = {'Anyag': 'N/A', 'Részleg': 'N/A', 'Beérkezés': 'N/A', 'Gyártás': 'N/A', 'Lejárat': 'N/A', 'Gyártási szám': 'N/A', 'Mennyiség': 'N/A'}

    # ReceiveMenu Dropdown spinner logic
    def spinner_clicked(self, value):
        """
        Logic for changing the values in item_spinner by interacting with category_spinner.
        When clicked it is going to change the naming of both itself and the other spinner but also change the contents of the secondary spinner which will contain all the chooseable items.
        On click event the button is going to give itself back the chosen value thus it know what to display in both dropdown menus.
        """
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
        self.input_values_dictionary.update({"Részleg": value})

    def on_spinner_select(self, text):
        self.input_values_dictionary.update({"Anyag": text})

    # Datepicker----------------------------------------------------------------------------------
    def show_date_picker(self, title, button_id):
        """
        Makes DatePicker Widget, binds on_save/on_cancel function to it, and opens it.
        """

        date_dialog = MDDatePicker(title=title, title_input='')  #Do it wrong and it throws up possible keywords
        date_dialog.bind(
            on_save=lambda instance, value, date_range: self.on_save(instance, value, date_range, button_id),
            on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range, button_id):
        """
        Save function for DatePicker.
        def on_save(self, instance, value, date_range, ids):
        instance ->
        value -> The date data itself. (2777-07-07)
        date_range -> date_dialog= MDDatePicker(mode= "range") return a python list of the dates. Techically you can select a range of dates from 01 to 27.

        !!!!!!!!!!!!!!! Solve it so it dispalys the date next to the text on the button!!!!!!!!
        """
        # Access the button ID (button_id) here
        if button_id == "date_receive":
            converted_time = value.strftime('%Y-%m-%d')
            self.input_values_dictionary.update({"Beérkezés": converted_time})
            # self.ids.date_receive.text = f'Beérkezés: {converted_time}'
        elif button_id == "date_production":
            converted_time = value.strftime('%Y-%m-%d')
            self.input_values_dictionary.update({"Gyártás": converted_time})
            # self.ids.date_production.text = f'Gyártás: {converted_time}'
        else:
            converted_time = value.strftime('%Y-%m-%d')
            self.input_values_dictionary.update({"Lejárat": converted_time})
            # self.ids.date_expiry.text = f'Lejárat: {converted_time}'


    def on_cancel(self, instance, value):
        return

    # Local update and Sync Update Buttons-----------------------------------------------------
    local_update_display_list = []



    def local_update(self):

        if self.input_values_dictionary["Részleg"] == 'N/A' or self.input_values_dictionary["Anyag"] in ['Általános', 'Termelés', 'Donorterem', 'Recepció']:
            pass


        else:

            # Not the most elegant solution and quite overcomplicated Kivy does open up the Popup as a different instance thus I can not techically interact with ids and thus elements inside here I instantinated it so I can reference it from outisde sad after effect is that the Popup needs to be opened to make everything work nicely.
            # Also, I changed quite a bit so maybe this part is not relevant because from now on I am going to open the popup from the .py file due to if I open it in .kv it will have NO connection to that data in the main file and it is really confusing to make it work.
            # Create an instance of the Popup
            popup_instance = Factory.local_popup()

            """
            Needed because the text field does not have an onclick event to put their values into the dictionary.
            Also with SyncList and input_values_dictionary data can be stored offline in case there is no internet or to synchronise multiple data.
            """
            #self.input_values_dictionary.update({"Gyártási szám": self.ids.product_number.text})
            # Here self.ids.product_number.text == True WILL NOT work due to that comparsion the other value must be True or False thus it is always false thats why use it like this.
            # condition_if_true if condition else condition_if_else
            self.input_values_dictionary.update({"Gyártási szám": self.ids.product_number.text if self.ids.product_number.text else "N/A"})
            #self.input_values_dictionary.update({"Mennyiség": self.ids.quantity.text})
            self.input_values_dictionary.update({"Mennyiség": self.ids.quantity.text if self.ids.quantity.text else 'N/A'})
            self.local_update_display_list.append(
                f'{int(len(self.local_update_display_list) + 1)}.\n Kategória: {self.input_values_dictionary.get("Anyag", "N/A")} \n Anyag: {self.input_values_dictionary.get("Részleg", "N/A")} \n Bevételezési Dátum: {self.input_values_dictionary.get("Beérkezés", "N/A")} \n Gyártási idő: {self.input_values_dictionary.get("Gyártás", "N/A")} \n Lejárat: {self.input_values_dictionary.get("Lejárat", "N/A")} \n Gyártási szám: {self.input_values_dictionary.get("Gyártási szám", "N/A")} \n Mennyiség: {self.input_values_dictionary.get("Mennyiség", "N/A")} \n-------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

            #Important because without copy() it is just a reference to the previous one thus the latest value will overwrite the previous one.
            self.sync_List.append(self.input_values_dictionary.copy())
            popup_instance.ids.local_popup_content.text = '\n'.join(self.local_update_display_list)
            print(self.local_update_display_list)



            # Open it for actual instantiation of the class.
            popup_instance.open()


    def sync_data(self, syncList=sync_List):

        if syncList == []:
            pass

        else:
            sync_popup_instance = Factory.sync_popup()
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'rich-sprite.json', scope)
            client = gspread.authorize(credentials)

            def convertUniqueIDToColumn(uniqueID):
                """
                Formula for converting the unique ID-s to columns in Google Sheets on the X axis.
                Max number is 16384 XFD apparently, but it never got tested.
                """

                dividend = uniqueID
                column_name = ''

                while dividend > 0:
                    modulo = (dividend - 1) % 26
                    column_name = chr(65 + modulo) + column_name
                    dividend = (dividend - modulo) // 26

                return column_name

            for item in syncList:
                if item["Részleg"] == 'Általános':
                        # Open an existing Google Sheets spreadsheet
                        sheet = client.open("Inventory Management App").worksheet(
                            "Általános")
                        sheet.add_cols(1)
                        uniqueID = int(sheet.cell(2, 1).value[1:])  # Number
                        columnLetter = convertUniqueIDToColumn(uniqueID)  # One word
                        # Python 's default string representation of a tuple gets used (G, C) if you do it with , and not +
                        g_product_identifier = 'G' + columnLetter
                        # Here what happens

                        sheet.update_cell(1, uniqueID, 11)
                        sheet.update_cell(2, uniqueID, "G" + columnLetter)  # Which column
                        sheet.update_cell(3, uniqueID, item["Anyag"])
                        sheet.update_cell(4, uniqueID, item["Beérkezés"])
                        sheet.update_cell(5, uniqueID, item["Gyártás"])
                        sheet.update_cell(6, uniqueID, item["Gyártási szám"])
                        sheet.update_cell(7, uniqueID, item["Lejárat"])
                        sheet.update_cell(8, uniqueID, item["Mennyiség"])
                        # Img

                        # Here goes the current data
                        uniqueID = uniqueID + 1
                        sheet.update_cell(2, 1, "G" + str(uniqueID))
                        sync_popup_instance.ids.sync_popup_content.text += f'{g_product_identifier}\n      {item["Anyag"]} \n\n'

                        time.sleep(3)

                        # Depositing into Event Viewer
                        sheet = client.open("Inventory Management App").worksheet(
                            "Event Viewer")
                        sheet.add_cols(1)

                        uniqueID = int(sheet.cell(1, 1).value[1:])

                        sheet.update_cell(1, uniqueID, "G" + columnLetter)
                        sheet.update_cell(2, uniqueID, item["Anyag"])
                        sheet.update_cell(3, uniqueID, item["Beérkezés"])
                        sheet.update_cell(4, uniqueID, item["Gyártás"])
                        sheet.update_cell(5, uniqueID, item["Gyártási szám"])
                        sheet.update_cell(6, uniqueID, item["Lejárat"])
                        sheet.update_cell(7, uniqueID, item["Mennyiség"])
                        sheet.update_cell(8, uniqueID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                        # Here goes the current data
                        uniqueID = uniqueID + 1
                        sheet.update_cell(1, 1, "E" + str(uniqueID))

                        time.sleep(3)


                elif item["Részleg"] == 'Termelés':
                        # Open an existing Google Sheets spreadsheet
                        sheet = client.open("Inventory Management App").worksheet("Termelés")
                        sheet.add_cols(1)
                        uniqueID = int(sheet.cell(2, 1).value[1:])
                        columnLetter = convertUniqueIDToColumn(uniqueID)
                        p_product_identifier = 'P' + columnLetter

                        # Here what should happen

                        sheet.update_cell(1, uniqueID, 11)
                        sheet.update_cell(2, uniqueID, "P" + columnLetter)  # Which column
                        sheet.update_cell(3, uniqueID, item["Anyag"])
                        sheet.update_cell(4, uniqueID, item["Beérkezés"])
                        sheet.update_cell(5, uniqueID, item["Gyártás"])
                        sheet.update_cell(6, uniqueID, item["Gyártási szám"])
                        sheet.update_cell(7, uniqueID, item["Lejárat"])
                        sheet.update_cell(8, uniqueID, item["Mennyiség"])
                        # Img

                        # Here goes the current data
                        uniqueID = uniqueID + 1
                        sheet.update_cell(2, 1, "P" + str(uniqueID))
                        sync_popup_instance.ids.sync_popup_content.text += f'{p_product_identifier}\n      {item["Anyag"]} \n\n'

                        time.sleep(3)

                        # Depositing into Event Viewer
                        sheet = client.open("Inventory Management App").worksheet(
                            "Event Viewer")
                        sheet.add_cols(1)

                        uniqueID = int(sheet.cell(1, 1).value[1:])

                        sheet.update_cell(1, uniqueID, "P" + columnLetter)
                        sheet.update_cell(2, uniqueID, item["Anyag"])
                        sheet.update_cell(3, uniqueID, item["Beérkezés"])
                        sheet.update_cell(4, uniqueID, item["Gyártás"])
                        sheet.update_cell(5, uniqueID, item["Gyártási szám"])
                        sheet.update_cell(6, uniqueID, item["Lejárat"])
                        sheet.update_cell(7, uniqueID, item["Mennyiség"])
                        sheet.update_cell(8, uniqueID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


                        # Here goes the current data
                        uniqueID = uniqueID + 1
                        sheet.update_cell(1, 1, "E" + str(uniqueID))

                        time.sleep(3)

                elif item["Részleg"] == 'Donorterem':
                        # Open an existing Google Sheets spreadsheet
                        sheet = client.open("Inventory Management App").worksheet(
                            "Donorterem")
                        sheet.add_cols(1)
                        uniqueID = int(sheet.cell(2, 1).value[1:])
                        columnLetter = convertUniqueIDToColumn(uniqueID)
                        d_product_identifier = 'D' + columnLetter
                        # ide hogy mitötrténjen vele

                        sheet.update_cell(1, uniqueID, 11)
                        sheet.update_cell(2, uniqueID, "D" + columnLetter)  # Which column
                        sheet.update_cell(3, uniqueID, item["Anyag"])
                        sheet.update_cell(4, uniqueID, item["Beérkezés"])
                        sheet.update_cell(5, uniqueID, item["Gyártás"])
                        sheet.update_cell(6, uniqueID, item["Gyártási szám"])
                        sheet.update_cell(7, uniqueID, item["Lejárat"])
                        sheet.update_cell(8, uniqueID, item["Mennyiség"])
                        # Img

                        # Here goes the current data
                        uniqueID = uniqueID + 1
                        sheet.update_cell(2, 1, "D" + str(uniqueID))
                        sync_popup_instance.ids.sync_popup_content.text += f'{d_product_identifier}\n      {item["Anyag"]} \n\n'

                        time.sleep(3)

                        # Depositing into Event Viewer
                        sheet = client.open("Inventory Management App").worksheet(
                            "Event Viewer")
                        sheet.add_cols(1)

                        uniqueID = int(sheet.cell(1, 1).value[1:])

                        sheet.update_cell(1, uniqueID, "D" + columnLetter)
                        sheet.update_cell(2, uniqueID, item["Anyag"])
                        sheet.update_cell(3, uniqueID, item["Beérkezés"])
                        sheet.update_cell(4, uniqueID, item["Gyártás"])
                        sheet.update_cell(5, uniqueID, item["Gyártási szám"])
                        sheet.update_cell(6, uniqueID, item["Lejárat"])
                        sheet.update_cell(7, uniqueID, item["Mennyiség"])
                        sheet.update_cell(8, uniqueID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


                        # Here goes the current data
                        uniqueID = uniqueID + 1
                        sheet.update_cell(1, 1, "E" + str(uniqueID))

                        time.sleep(3)

                elif item["Részleg"] == 'Recepció':
                        # Open an existing Google Sheets spreadsheet
                        sheet = client.open("Inventory Management App").worksheet("Recepció")
                        sheet.add_cols(1)
                        uniqueID = int(sheet.cell(2, 1).value[1:])
                        columnLetter = convertUniqueIDToColumn(uniqueID)
                        r_product_identifier = 'R' + columnLetter
                        # ide hogy mitötrténjen vele

                        sheet.update_cell(1, uniqueID, 11)
                        sheet.update_cell(2, uniqueID, "R" + columnLetter)  # Which column
                        sheet.update_cell(3, uniqueID, item["Anyag"])
                        sheet.update_cell(4, uniqueID, item["Beérkezés"])
                        sheet.update_cell(5, uniqueID, item["Gyártás"])
                        sheet.update_cell(6, uniqueID, item["Gyártási szám"])
                        sheet.update_cell(7, uniqueID, item["Lejárat"])
                        sheet.update_cell(8, uniqueID, item["Mennyiség"])
                        # Img

                        # ebbe megy a jelenlegi adat
                        uniqueID = uniqueID + 1
                        sheet.update_cell(2, 1, "R" + str(uniqueID))
                        sync_popup_instance.ids.sync_popup_content.text += f'{r_product_identifier}\n      {item["Anyag"]} \n\n'

                        time.sleep(3)

                        # Depositing into Event Viewer
                        sheet = client.open("Inventory Management App").worksheet(
                            "Event Viewer")
                        sheet.add_cols(1)

                        uniqueID = int(sheet.cell(1, 1).value[1:])

                        sheet.update_cell(1, uniqueID, "R" + columnLetter)
                        sheet.update_cell(2, uniqueID, item["Anyag"])
                        sheet.update_cell(3, uniqueID, item["Beérkezés"])
                        sheet.update_cell(4, uniqueID, item["Gyártás"])
                        sheet.update_cell(5, uniqueID, item["Gyártási szám"])
                        sheet.update_cell(6, uniqueID, item["Lejárat"])
                        sheet.update_cell(7, uniqueID, item["Mennyiség"])
                        sheet.update_cell(8, uniqueID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


                        # Here goes the current data
                        uniqueID = uniqueID + 1
                        sheet.update_cell(1, 1, "E" + str(uniqueID))

                        time.sleep(3)
            self.local_update_display_list.clear()
            syncList.clear()

            sync_popup_instance.open()


class ExpendMenu(Screen):
    expendList = []
    expend_local_update_display_list = []
    expend_sync_update_display_list = []

    def allow_alpha(self, input, from_undo):
        """
        When used in a input_filter, a function should take two parameters: the input string
         and a boolean indicating if the change is resulting from an undo operation technically that a base template how to do it so it goes with kivy infrastructure tho not entirely clear.
        """
        if input.isalpha():
            return input
        else:
            return None


    """ Grand example of why you are not using chatgpt braindeadly only as a beefed up google because it overcomplicates stuff and then you cry in blogs that it made you a worse programmer and makes code harder to debug: overcomplicating NEEDLESSLY easy stuff, meanwhile being entirely confident in its own capabilities.
    def allow_alpha(self, input, from_undo):

    # Only retain alphabetic characters
    filtered_input = ''.join(char for char in input if char.isalpha())

    # Return the filtered input (could be an empty string if no valid characters)
    return filtered_input
    """




    def materialExpend(self):
        #If expend_local_update_display_list is a local variable to the materialExpend method. Each time I call materialExpend, I initialize this list to an empty list, which means any previous entries from past calls to the method are discarded. Thus NEED to keep the list as an instance variabble.


        if self.ids.expend_id.text and self.ids.expend_quantity.text:

            expend_popup_instance = Factory.expend_local_popup()
            expendMaterialDictionary = {'ID': 'N/A', 'Quantity': 'N/A'}
            expendMaterialDictionary.update({"ID": self.ids.expend_id.text})
            expendMaterialDictionary.update({"Quantity": self.ids.expend_quantity.text})

            self.expend_local_update_display_list.append((
                f'{int(len(self.expend_local_update_display_list) + 1)}.\n ID: {expendMaterialDictionary.get("ID", "N/A")} \n Mennyiség: {expendMaterialDictionary.get("Quantity", "N/A")} \n-------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'))

            self.expendList.append(expendMaterialDictionary.copy())

            expend_popup_instance.ids.expend_local_popup_content.text = '\n'.join(self.expend_local_update_display_list)
            expend_popup_instance.open()

        else:
            return






    def eSychronizeData(self, syncList=expendList):
        print(syncList)  # List with dictionaries inside good question where do I amke that dictioanry? xd
        self.expend_local_update_display_list.clear()
        expend_sync_popup_instance = Factory.expend_sync_popup()



        if syncList == []:
            return

        else:
            def convertColumnToUniqueID(column_name):
                num = 0
                for c in column_name:
                    if c.isalpha():
                        num = num * 26 + (ord(c.upper()) - ord('A')) + 1
                return num

            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'rich-sprite.json', scope)
            client = gspread.authorize(credentials)



            # Rename id after because it's a keyword
            for item in syncList:
                worksheet = item["ID"][0]
                id = item["ID"][1:]
                quantity = int(item["Quantity"])


    #expend_sync_popup_content.ids.sync_popup_content.text += f'{g_product_identifier}\n      {item["Anyag"]} \n\n'

                if worksheet == "G":
                    # Open an existing Google Sheets spreadsheet
                    sheet = client.open("Inventory Management App").worksheet(
                        "Általános")
                    columnInt = convertColumnToUniqueID(id)
                    rowValue = sheet.cell(8, columnInt).value
                    sheet.update_cell(8, columnInt, int(rowValue) - quantity)

                    product_name = sheet.cell(3, columnInt).value
                    # Number in the top of GS to know which row the new outtake need to go into: 10
                    row_id = sheet.cell(1, columnInt).value

                    # Writes the taken product under its intake column.
                    sheet.add_rows(3)
                    sheet.update_cell(row_id, columnInt, '-' + item['Quantity'])
                    sheet.update_cell(int(row_id) + 1, columnInt, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    sheet.update_cell(1, columnInt, int(row_id) + 3)




                    self.expend_sync_update_display_list.append((
                        f'{int(len(self.expend_sync_update_display_list) + 1)}.\n {item.get("ID", "N/A")}       {product_name} \n {item.get("Quantity", "N/A")} \n-------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'))

                    expend_sync_popup_instance.ids.expend_sync_popup_content.text = '\n'.join(
                        self.expend_sync_update_display_list)

                    # Depositing into Event Viewer
                    sheet = client.open("Inventory Management App").worksheet(
                        "Event Viewer")
                    sheet.add_cols(1)

                    uniqueID = int(sheet.cell(1, 1).value[1:])

                    sheet.update_cell(10, uniqueID, str(worksheet) + str(id))
                    sheet.update_cell(11, uniqueID, '-' + str(quantity))
                    sheet.update_cell(12, uniqueID, int(rowValue) - quantity)
                    sheet.update_cell(13, uniqueID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                    # Here goes the current data
                    uniqueID = uniqueID + 1
                    sheet.update_cell(1, 1, "E" + str(uniqueID))


                elif worksheet == "P":
                    # Open an existing Google Sheets spreadsheet
                    sheet = client.open("Inventory Management App").worksheet("Termelés")
                    columnInt = convertColumnToUniqueID(id)
                    rowValue = sheet.cell(8, columnInt).value
                    sheet.update_cell(8, columnInt, int(rowValue) - quantity)

                    product_name = sheet.cell(3, columnInt).value
                    row_id = sheet.cell(1, columnInt).value

                    sheet.add_rows(3)
                    sheet.update_cell(row_id, columnInt, '-' + item['Quantity'])
                    sheet.update_cell(int(row_id) + 1, columnInt, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    sheet.update_cell(1, columnInt, int(row_id) + 3)

                    self.expend_sync_update_display_list.append((
                        f'{int(len(self.expend_sync_update_display_list) + 1)}.\n {item.get("ID", "N/A")}       {product_name} \n {item.get("Quantity", "N/A")} \n-------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'))

                    expend_sync_popup_instance.ids.expend_sync_popup_content.text = '\n'.join(
                        self.expend_sync_update_display_list)

                    # Depositing into Event Viewer
                    sheet = client.open("Inventory Management App").worksheet(
                        "Event Viewer")
                    sheet.add_cols(1)

                    uniqueID = int(sheet.cell(1, 1).value[1:])

                    sheet.update_cell(10, uniqueID, str(worksheet) + str(id))
                    sheet.update_cell(11, uniqueID, '-' + str(quantity))
                    sheet.update_cell(12, uniqueID, int(rowValue) - quantity)
                    sheet.update_cell(13, uniqueID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                    # Here goes the current data
                    uniqueID = uniqueID + 1
                    sheet.update_cell(1, 1, "E" + str(uniqueID))





                elif worksheet == "D":
                    # Open an existing Google Sheets spreadsheet
                    sheet = client.open("Inventory Management App").worksheet(
                        "Donorterem")
                    columnInt = convertColumnToUniqueID(id)
                    rowValue = sheet.cell(8, columnInt).value
                    sheet.update_cell(8, columnInt, int(rowValue) - quantity)

                    product_name = sheet.cell(3, columnInt).value
                    row_id = sheet.cell(1, columnInt).value

                    sheet.add_rows(3)
                    sheet.update_cell(row_id, columnInt, '-' + item['Quantity'])
                    sheet.update_cell(int(row_id) + 1, columnInt, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    sheet.update_cell(1, columnInt, int(row_id) + 3)

                    self.expend_sync_update_display_list.append((
                        f'{int(len(self.expend_sync_update_display_list) + 1)}.\n {item.get("ID", "N/A")}       {product_name} \n {item.get("Quantity", "N/A")} \n-------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'))

                    expend_sync_popup_instance.ids.expend_sync_popup_content.text = '\n'.join(
                        self.expend_sync_update_display_list)

                    # Depositing into Event Viewer
                    sheet = client.open("Inventory Management App").worksheet(
                        "Event Viewer")
                    sheet.add_cols(1)

                    uniqueID = int(sheet.cell(1, 1).value[1:])

                    sheet.update_cell(10, uniqueID, str(worksheet) + str(id))
                    sheet.update_cell(11, uniqueID, '-' + str(quantity))
                    sheet.update_cell(12, uniqueID, int(rowValue) - quantity)
                    sheet.update_cell(13, uniqueID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                    # Here goes the current data
                    uniqueID = uniqueID + 1
                    sheet.update_cell(1, 1, "E" + str(uniqueID))




                else:
                    # Open an existing Google Sheets spreadsheet
                    sheet = client.open("Inventory Management App").worksheet("Recepció")
                    columnInt = convertColumnToUniqueID(id)
                    rowValue = sheet.cell(8, columnInt).value
                    sheet.update_cell(8, columnInt, int(rowValue) - quantity)

                    product_name = sheet.cell(3, columnInt).value
                    row_id = sheet.cell(1, columnInt).value

                    sheet.add_rows(3)
                    sheet.update_cell(row_id, columnInt, '-' + item['Quantity'])
                    sheet.update_cell(int(row_id) + 1, columnInt, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    sheet.update_cell(1, columnInt, int(row_id) + 3)

                    self.expend_sync_update_display_list.append((
                        f'{int(len(self.expend_sync_update_display_list) + 1)}.\n {item.get("ID", "N/A")}       {product_name} \n {item.get("Quantity", "N/A")} \n-------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'))

                    expend_sync_popup_instance.ids.expend_sync_popup_content.text = '\n'.join(
                        self.expend_sync_update_display_list)

                    # Depositing into Event Viewer
                    sheet = client.open("Inventory Management App").worksheet(
                        "Event Viewer")
                    sheet.add_cols(1)

                    uniqueID = int(sheet.cell(1, 1).value[1:])

                    sheet.update_cell(10, uniqueID, str(worksheet) + str(id))
                    sheet.update_cell(11, uniqueID, '-' + str(quantity))
                    sheet.update_cell(12, uniqueID, int(rowValue) - quantity)
                    sheet.update_cell(13, uniqueID, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                    # Here goes the current data
                    uniqueID = uniqueID + 1
                    sheet.update_cell(1, 1, "E" + str(uniqueID))



                time.sleep(3)

            expend_sync_popup_instance.open()
            self.expend_sync_update_display_list.clear()
            self.expendList.clear()




class WindowManager(ScreenManager):
    # Due to the popup windows being an entirely different entity and I failed with multiple methods to synchronisde the data dynamically I keep the list here so I can simply reference it from here.
    # local_update_display_list_parent = ListProperty([])
    pass


# Works without it if you run it will conflict with the popup because
# kivy automatically runs it however you explicitly say that run it again, so it
# is going to be run 2X(the .kv file that is.) and it will conflict with the Popup.
class MyApp(MDApp):
    title = 'Inventory Management App'
    icon = 'serb.ico'
    '''
    def build(self):
        kv = Builder.load_file(
            'MyApp.kv')  # returnnél visszaadom mivel ez vonatkozik a kv fájlra ami tartalmazni fogja a windowokat
        return kv
    '''



if __name__ == '__main__':
    MyApp().run()

# Important to actually get the parent of my current widget.

'''
                ██        ██                                                        
              ██▒▒██    ██▒▒██                                                      
            ██▒▒▒▒▒▒████▒▒▒▒▒▒██                                                    
        ▓▓████▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▓▓██                                                  
      ▓▓▒▒▒▒██▒▒▒▒██████▒▒▒▒▒▒▒▒▓▓                                                  
      ██▒▒▒▒▒▒▒▒██▒▒▒▒▒▒██▒▒▒▒▒▒██                                                  
    ▓▓████▒▒▒▒██▒▒░░▒▒░░▒▒████▒▒██                                                  
    ██▒▒▒▒▒▒██▒▒░░░░░░░░░░░░░░████                                                  
    ██████████▒▒██░░▒▒░░░░░░░░░░██                                                  
  ██░░░░░░██▒▒░░░░░░░░░░░░░░░░░░░░██                                                
██░░░░░░░░██▒▒░░▒▒░░▒▒░░░░░░░░░░░░██                                                
  ██░░░░░░██▒▒▒▒░░░░░░░░░░░░░░░░░░░░██                                              
    ████░░██▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░██                                            
        ████▒▒▒▒░░▒▒░░░░░░░░░░░░░░░░░░██                                            
          ██▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░██                                            
            ██▒▒▒▒░░▒▒░░░░░░░░░░░░░░░░░░██                                          
            ██▒▒░░░░░░░░░░░░░░░░░░▒▒░░░░██                                          
            ██▒▒░░▒▒░░░░░░▒▒░░░░░░░░▒▒░░▒▒▒▒                                  ▓▓    
            ██▒▒▒▒░░▒▒░░░░░░▒▒░░░░░░░░▒▒░░░░▓▓██                            ▓▓░░██  
            ██▒▒▒▒░░░░▒▒░░░░▒▒▒▒░░░░▒▒██▒▒▒▒░░░░██                        ██░░░░██  
              ██▒▒░░░░░░▒▒░░▒▒██▒▒░░▒▒██████▒▒▒▒▒▒██                    ██░░░░░░██  
              ██▒▒▒▒░░░░▒▒░░▒▒██▒▒░░▒▒██░░░░██████░░██████          ████░░░░░░██    
            ▓▓▒▒▒▒▓▓▒▒▒▒▓▓▒▒▒▒██▓▓▒▒▒▒██░░░░▒▒░░▓▓░░▓▓▓▓▒▒░░▓▓▓▓░░▓▓▓▓▒▒░░░░▓▓██▓▓  
            ██▒▒▓▓██▒▒▓▓██▒▒▒▒██▒▒▓▓▒▒██░░▓▓▓▓▓▓████▓▓██▓▓░░░░░░▒▒░░░░░░░░░░░░░░▒▒▓▓
            ██▓▓▒▒██▒▒██▒▒▓▓▒▒██░░▒▒▓▓░░▓▓▓▓▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░▓▓░░
          ▓▓▒▒▒▒░░▒▒▓▓▒▒░░▒▒██▒▒░░░░▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▓▓░░░░░░░░░░░░░░░░██  
          ██░░░░░░░░▒▒░░░░░░▒▒░░░░░░░░██▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██░░░░░░░░░░░░▓▓▓▓    
          ██░░░░░░░░░░░░░░░░░░░░░░░░░░██▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██░░░░░░░░░░░░░░▓▓  
          ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░██▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██░░░░░░░░░░░░░░██    
            ██░░░░░░░░░░░░░░░░░░░░░░░░░░██▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓██░░░░░░░░░░██      
            ██░░░░░░░░░░░░░░░░░░░░░░░░░░██▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▓▓████░░░░░░░░░░██        
            ██░░░░░░░░░░░░░░░░░░░░░░░░░░██▓▓▓▓▓▓████▓▓▓▓▒▒▓▓▓▓██░░░░░░░░██          
            ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░██▓▓▓▓██░░██▓▓▓▓████░░░░░░▒▒░░██          
            ▒▒▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░████░░░░░░████░░░░░░░░░░░░░░██          
              ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██            
                ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██            
                ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██              
                  ████░░░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░░░░░░░░░░░██                
                    ██░░░░░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░░░░░░░██                  
                      ████░░░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░░░██                    
                        ██░░░░░░░░░░░░░░░░░░░░░░██░░░░░░██████                      
                          ██████████░░░░░░░░░░░░░░██░░██                            
                            ██░░██  ████████████████████                            
                        ██████░░██                ██░░██                            
                      ██░░░░░░░░░░██          ██████░░██                            
                        ████░░░░██░░▓▓      ██░░░░░░░░░░██                          
                        ██▒▒██░░██▓▓          ████░░░░██░░▓▓                        
                        ██████░░██            ██░░██░░████                          
                              ██              ██████░░██                            
                                                    ██                              
'''

'''
UNIQUE ID
MATERIAL
INTAKE
PRODUCTION
LOT
EXPIRY
QUANTITY
'''
