from exiftool import ExifToolHelper
from customtkinter import *
from PIL import Image
import os


class ErrorWindow(CTkToplevel):
    def __init__(self, parent, message): 
        super().__init__()
        set_appearance_mode("dark")
        self.geometry("300x100")
        self.title("ERROR")
        self.resizable(False, False)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "ICON.ico")
        self.iconbitmap(icon_path)

        self.transient(parent)
        self.grab_set()

        self.label = CTkLabel(master=self, text=message, wraplength=225)
        self.label.pack(pady=3, padx=20)

        self.close_button = CTkButton(master=self, text="Close", corner_radius=32, fg_color="#ffb114", hover_color="#bb7d00", command=self.destroy)
        self.close_button.pack(padx=20, pady=10)


class MetaEdit(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
        self.geometry("750x500")
        self.title("MetaClean")
        self.resizable(False, False)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "ICON.ico")
        bg_path = os.path.join(current_dir, "BG.png")
        self.font_path = os.path.join(current_dir, "Montserrat-VariableFont_wght.ttf")
        self.exiftool_path = os.path.join(current_dir, "exiftool.exe")
        self.iconbitmap(icon_path)

        bg_image = CTkImage(light_image=Image.open(bg_path), size=(750, 500))
        image_label = CTkLabel(self, image=bg_image, text="")
        image_label.place(x=0, y=0)

        button = CTkButton(master=self, text="Choose File", command=self.selectFile, font=(self.font_path, 24), height=35, width=150, 
                           bg_color="#0f0f0f", fg_color="#ffb114", hover_color="#bb7d00", text_color="#ffffff")
        button.place(x=300, y=410)
    

    def selectFile(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path != "":
            self.calculateMetaData()
        

    def calculateMetaData(self):
        self.tabview = CTkTabview(self, width=600, height=300, border_width=2.5, border_color="#ffffff", fg_color="#0f0f0f",  text_color="#ffffff", 
                                  segmented_button_fg_color="#ffffff", segmented_button_selected_color="#ffb114", segmented_button_selected_hover_color="#bb7d00", 
                                  bg_color="#0f0f0f", segmented_button_unselected_color="#0f0f0f")

        self.catagories = []
        self.textboxes = {}
        self.excluded = ['SourceFile', 'ExifTool']

        with ExifToolHelper(executable=self.exiftool_path) as ET:
            metadata = ET.get_metadata(self.file_path)
            for i in metadata:
                for j, k in i.items():
                    catagory = j.split(":")[0]

                    if catagory not in self.catagories and catagory not in self.excluded:
                        self.catagories.append(catagory)
                        self.tabview.add(catagory)

                        textbox = CTkTextbox(master=self.tabview.tab(catagory), width=600, height=260, fg_color="#0f0f0f")
                        self.textboxes[catagory] = textbox
                        textbox.place(x=0, y=0)
                        
                    if catagory in self.textboxes:
                        self.textboxes[catagory].insert("end", f"{j}: {k}\n")
            
            for i in self.catagories:
                self.textboxes[i].configure(state="disabled")

            self.deleteButton = CTkButton(self, text="Delete MetaData", width=125, height=25, command=self.stripMetaData
                                          , fg_color="#D22B2B", hover_color="#A52A2A", bg_color="#0f0f0f")

            self.deleteButton.place(x=375-(self.deleteButton.cget("width")/2), y=455)
            self.tabview.place(x=375-(self.tabview.cget("width")/2), y=100)


    def stripMetaData(self):
        try:
            with ExifToolHelper(executable=self.exiftool_path) as ET:
                ET.execute("-all=", "-overwrite_original", self.file_path)
        except Exception:
            ErrorWindow(self, "File Type not Supported or File not Selected")
        
        if self.file_path != "":
            self.calculateMetaData()


if __name__ == "__main__":
    app = MetaEdit()
    app.mainloop()


'''
COLORS
#ffffff - White
#ffb114 - Orange
#bb7d00 - Dark Orange
#0f0f0f - Dark Color
#000000 - Black
'''
