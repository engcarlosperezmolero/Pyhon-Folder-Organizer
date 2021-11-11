import tkinter as tk
from tkinter import Label, StringVar, Variable, filedialog, Text, Scrollbar, Checkbutton, IntVar, Button, Entry
from tkinter.constants import HORIZONTAL, LEFT
from tkinter.font import Font
from tkinter import ttk

import time
# from classes.folder_organizer_v2 import FolderOrganizer

# =================== FOLDER ORGANIZER CLASS ====================================================================
# ===============================================================================================================

"""
Ejemplo:

organizer = FolderOrganizer("C:\\Users\\cap32\\Desktop\\prueba_folder")
organizer.organize_folder()

"""


class FolderOrganizer:
    
    def __init__(self, folder_to_track, types_checkboxes_ints={}, new_spec_folder_name="", specnewfiletype = ""):
        self.folder_to_track = folder_to_track
        self.types_checkboxes_ints = types_checkboxes_ints
        self.new_spec_folder_name =  new_spec_folder_name
        self.specnewfiletype = specnewfiletype

        if self.new_spec_folder_name != "" and self.specnewfiletype != "":
            self.types_checkboxes_ints[self.new_spec_folder_name] = [1,self.new_spec_folder_name,[self.specnewfiletype],""]
        
    
    def _check_file_types(self, folder_name, condition_to_test, file, names_records_dictionary):
        """
           Se encarga de poblar un diccionario donde cada Key es el nombre del tipo de archivo y
           cada Value es una lista con los nombres de los archivos de ese tipo de archivo.
        """
        if condition_to_test:
            if folder_name in names_records_dictionary:
                if file not in names_records_dictionary[folder_name]:
                    names_records_dictionary[folder_name].append(file)
            else:
                names_records_dictionary[folder_name] = []
                names_records_dictionary[folder_name].append(file)


                
    def _create_lists_by_types(self):
        """
           Se encarga aqui se lleva a cabo la poblacion del diccionario con los nombres,
           solo son creados los Key-Value en caso de que exista ese tipo de archivo en 
           la carpeta que se este organizando
        """
        import os
        
        self.names_record_by_folder = dict()

        
        for file in  os.listdir(self.folder_to_track):
            # llenar de if segun los valores obtenidos en el checkbox list
            
            #{
            # "comprimidos": [IntVar(), "comprimidos", ["zip", "rar"], CheckBox()],
            # "codigos": [IntVar(), "codigos", {"python":["py","ipynb"], "htmlCss":["html", "css"]}, CheckBox()],
            # "imagenes": [IntVar(), "imagenes",, ["png", "jpg", "bmp", "tif", "gif"], CheckBox()],
            # }
            

            for folder, v in self.types_checkboxes_ints.items():

                try:
                    marked = v[0].get()
                except:
                    marked = v[0]

                if marked == 1:

                    if isinstance(v[2], list):
                        print("lista")                    
                        
                        for ext in v[2]: # arreglar formato folder_subfolder
                            self._check_file_types(folder+"_"+ext, file.lower().endswith("."+ext), file, self.names_record_by_folder)
                            print(f"{folder}_{ext} conditions: {file.lower().endswith('.'+ext)}")

                    elif isinstance(v[2], dict):
                        print("dict")
                        for subfolder,vi in v[2].items():

                            conditionsi = []
                            for vix in vi:
                                conditionsi.append(file.lower().endswith("."+vix))

                            self._check_file_types(folder+"_"+subfolder, any(conditionsi), file, self.names_record_by_folder)
                            print(f"{folder}_{subfolder} conditions: {any(conditionsi)}")
        
        
    
    
    def _create_folders_tree(self):
        """
           Crea las carpetas y subcarpetas basandose en los archivos unicos que existan en la
           carpeta que se esta ordenando, de esta manera no existiran categorias demas, solo
           las necesarias.
           
           Solo crea la carpeta en caso de que esta no exista.
           
           Para modificar el nombre de las carpetas se debe modificar el metodo _create_lists_by_types(),
           en donde cada Key del diccionario tiene la estructura 'NombreFolder_NombreSubFolder'
        """
        import os
        
        for folder_subfolder, names in self.names_record_by_folder.items():
            try:
                folder, subfolder = folder_subfolder.split("_")
                if not os.path.exists(f"{self.folder_to_track}\\{folder}"):
                    os.mkdir(f"{self.folder_to_track}\\{folder}")
                if not os.path.exists(f"{self.folder_to_track}\\{folder}\\{subfolder}"):
                    os.mkdir(f"{self.folder_to_track}\\{folder}\\{subfolder}")
            except:
                folder = folder_subfolder.split("_")[0]
                if not os.path.exists(f"{self.folder_to_track}\\{folder}"):
                    os.mkdir(f"{self.folder_to_track}\\{folder}")
            
            
    def _move_files_to_subfolders(self):
        """
           Mueve los archivos de la carpeta que se quiere ordenar a las
           distintas subcarpetas.
        """
        import os 
        
        for folder_subfolder, names in self.names_record_by_folder.items():
            for name in names:
                try:
                    folder, subfolder = folder_subfolder.split("_")
                    os.rename(f"{self.folder_to_track}\\{name}", f"{self.folder_to_track}\\{folder}\\{subfolder}\\{name}")
                except:
                    folder = folder_subfolder.split("_")[0]
                    os.rename(f"{self.folder_to_track}\\{name}", f"{self.folder_to_track}\\{folder}\\{name}")
                    
    
    def organize_folder(self):
        """
        es el metodo publico mediante el cual el usuario ordena las carpetas que necesite
        """
        self._create_lists_by_types()
        self._create_folders_tree()
        print(self.names_record_by_folder)
        print(20*"=")
        self._move_files_to_subfolders()


# =================== FINAL DE FOLDER ORGANIZER CLASS ===========================================================
# ===============================================================================================================


# Funciones importantes
def all_checkboxes(checkboxes_dict_ints): # { [IntVar(), Checkbutton()], ... }

    if checkboxes_dict_ints["ninguno"][0].get() == 1:
        for k, v in checkboxes_dict_ints.items():
            checkboxes_dict_ints[k][3].deselect()

    if checkboxes_dict_ints["todos"][0].get() == 1:
        for k, v in checkboxes_dict_ints.items():
            if k not in ["todos", "ninguno"]:
                checkboxes_dict_ints[k][3].select()

def search_folder_to_track(root):
    foldername = filedialog.askdirectory(initialdir="C:\\Users\\cap32\\Desktop",
                                         title="Select Folder to Organize")
    #folders_to_organize.append(foldername)
    globals()["foldername"] = foldername

    label = tk.Label(root, text=f"Folder to organize: {foldername.split('/')[-1]} in {foldername.split('/')[-2]}",
                     bg=BG_COLOR, fg="white", justify="left", font=Font(size=9))
    label.grid(row=2,column=1, columnspan=2, sticky="w")

    excuteOrganizer["state"] = "normal"


def execute_organizer(foldername, types_check_dict, new_folder="", new_extension=""): 

    def progressBarWindown():
        progressWindow = tk.Toplevel(root)
        progressWindow.title("Organizing folder...")
        progressWindow.resizable(0, 0)
        progressWindow.geometry("+200+45")


        #row 0
        insert_columns_in_row_detail(0, progressWindow, 10, 2)

        #row 1
        organizer = FolderOrganizer(foldername,types_check_dict, new_folder,new_extension)
        organizer.organize_folder()

        percentLabel1 = Label(progressWindow, text="Folder has been organized!")
        percentLabel1.grid(row=1,column=1, columnspan=1)


        # row 2
        Button(progressWindow, text="Close", padx=3, pady=5, font=Font(size=9),
          fg="white", bg=BG_COLOR, width=9, command=lambda: progressWindow.destroy(), cursor="hand2").grid(row=2,column=2, columnspan=2)
        

        #row 3
        insert_columns_in_row_detail(3, progressWindow, 10, 2)


    progressBarWindown()


    
    



    #label_temp_1 = tk.Label(root, text=f"Folder {folder.split('/')[-1]} is being organized...",
    #                bg="gray", fg="white", justify="left", font=Font(size=10))
    #label_temp_1.pack()
    print(foldername)
    
    #label_temp = tk.Label(frame, text=f"Folder {folder.split('/')[-1]} has been organized",
    #               bg="gray", fg="white", justify="left", font=Font(size=10))
    #label_temp.pack()


    



def createNewWindow():
    newWindow = tk.Toplevel(root)
    newWindow.title("New Extension")
    newWindow.resizable(0, 0)
    newWindow.geometry("+350+45")

    def search_specific_file_format(frame):
        specfilename = filedialog.askopenfilename(initialdir="C:\\Users\\cap32\\Desktop",
                                            title="Select Folder to Organize")

        globals()["specnewfiletype"] = specfilename.split(".")[-1]
        newWindow.focus()
        #print(specnewfiletype)
    # row 0
    insert_columns_in_row_detail(0, newWindow, 10, 2)

    # row 1

    new_folder_name = tk.StringVar()



    input_1 = Entry(newWindow, width=60, textvariable=new_folder_name)

    def click(*args):
        input_1.delete(0, 'end')

    def leave(*args):
        #input_1.delete(0, 'end')
        #input_1.insert(0, 'Enter Text:- ')
        print(new_folder_name.get())
        globals()["new_spec_folder_name"] = new_folder_name.get()
        newWindow.focus()

    input_1.insert(0, 'Insert name for new sub-folder...')
    input_1.grid(row=1,column=1)
    input_1.bind("<Button-1>", click)
    input_1.bind("<Leave>", leave)

    # row 2
    insert_columns_in_row_detail(2, newWindow, 10, 2)

    # row 3
    Button(newWindow, text="Pick Specific File", padx=3, pady=5, font=Font(size=9),
          fg="white", bg=BG_COLOR, width=20, command=lambda: search_specific_file_format(newWindow), cursor="hand2").grid(row=3,column=0, columnspan=4)

    # row 4
    insert_columns_in_row_detail(4, newWindow, 10, 2)

    # row 5 (button que diga continuar...)
    Button(newWindow, text="Continue", padx=3, pady=5, font=Font(size=9),
          fg="white", bg=BG_COLOR, width=9, command=lambda: newWindow.destroy(), cursor="hand2").grid(row=5,column=3, columnspan=2)

    # row 6 insert columns
    insert_columns_in_row_detail(6, newWindow, 10, 2)

    


    
def insert_columns_in_row_detail(row_num, frame, wbig=20, wlit = 2):
    for column_num in range(4):
        if column_num % 2 == 0: # es par o cero
            Label(frame, text="", width=wbig).grid(row=row_num,column=column_num)
        else: # es impar
            Label(frame, text="", width=wlit).grid(row=row_num,column=column_num)

    
    



def insert_columns_in_row(row_num, frame):
    for column_num in range(4):
        if column_num % 2 == 0: # es par o cero
            Label(frame, text="", width=40).grid(row=row_num,column=column_num)
        else: # es impar
            Label(frame, text="", width=4).grid(row=row_num,column=column_num)

# ==================================================================================
# ==================================================================================


root = tk.Tk()
root.title("Folder Organizer App by Charly")
root.resizable(0, 0)
#root.iconbitmap('./folder_organizer_icon.ico')
root.geometry("+100+45")

BG_COLOR = "#263D42"
FONT_COLOR_BUTTON = "white"



# row 0 and row 1
insert_columns_in_row(0, root)
insert_columns_in_row(1, root)

# row 2
Button(root, text="Pick Folder", padx=7, pady=5, font=Font(size=9),
          fg="white", bg=BG_COLOR, width=20, command=lambda: search_folder_to_track(root), cursor="hand2").grid(row=2,column=0)

Label(text="  /path/to/folder/to/organize/",anchor="w", bg=BG_COLOR, fg=FONT_COLOR_BUTTON, width=44, height=2).grid(row=2,column=1, columnspan=2, sticky="w")

# row 3
insert_columns_in_row(3, root)

# row 4
Button(root, text="New Extensions", padx=7, pady=5, font=Font(size=9),
          fg="white", bg=BG_COLOR, width=20, command=createNewWindow, cursor="hand2").grid(row=4,column=0)

descripcion_1 = "Descripción de la funcionalidad, y se muestra\nen caso de existir alguna nueva carpeta."
Label(text=descripcion_1,anchor="nw", bg=BG_COLOR, fg=FONT_COLOR_BUTTON, width=44, height=2, justify=LEFT).grid(row=4,column=1, columnspan=2, sticky="w")

# row 5
insert_columns_in_row(5, root)

# row 6

descripcion_2 = "Seleccione los tipos de archivo a ordenar: "
Label(text=descripcion_2,anchor="center", bg=BG_COLOR, fg=FONT_COLOR_BUTTON, width=88, height=2, justify=LEFT).grid(row=6,column=0, columnspan=4)

# aqui va el list box .grid(row=6, column=2)
"""
listbox = tk.Listbox(selectmode="multiple")
types_listbox_items = ["comprimidos", "pdf", "word", "txt", "csv", "excel", "json",
                       "power point", "videos", "imagenes", "audios", "codigos", "instaladores",
                       "Spotfire dxp"]

for i in range(len(types_listbox_items)):
    listbox.insert(i + 1, types_listbox_items[i])

listbox.grid(row=6, column=2)
"""
# row 7 
insert_columns_in_row(7, root)



# row 8 ... row 23
types_checkboxes = ["todos","ninguno","comprimidos",
                    "textos",
                    "datos",
                    "power point",
                    "videos",
                    "imagenes", "audios",
                    "codigos",
                    "instaladores", "spotfire"]

extension_checkboxes = [["todos"], ["ninguno"], ["zip", "7z", "rar"],
                        {"pdf": ["pdf"], "word": ["docx", "doc"], "txt": ["txt"]},
                        {"csv": ["csv"], "excel": ["xlsx", "xlsm", "xlsb", "xls"], "json": ["json"]}, 
                        ["pptx", "ppt"],
                        ["mp4", "avi", "mkv", "mov", "flv", "wmv"],
                        ["png", "jpg", "bmp", "tif", "gif"], ["mp3", "aiff", "au","flac", "wma", "opus"],
                        {"python":["py", "ipynb"], "R":["r", "rscript"], "htmlCss": ["html", "css", "svg"], "javascript":["js"], "xml":["xml"]},
                        ["msi", "exe"], ["dxp"]]

# inicializando las varibles que guardan el estado de cada checkbox
types_checkboxes_ints = dict() # { "comprimidos": [IntVar(), "comprimidos",Checkbutton()], ... }


for i in range(len(types_checkboxes)):
    types_checkboxes_ints[types_checkboxes[i]] = []
    types_checkboxes_ints[types_checkboxes[i]].append(IntVar())
    types_checkboxes_ints[types_checkboxes[i]].append(types_checkboxes[i])
    types_checkboxes_ints[types_checkboxes[i]].append(extension_checkboxes[i])


# poblando la interfaz
for i in range(len(types_checkboxes)):
    if i % 2 == 0:
        types_checkboxes_ints[types_checkboxes[i]].append(Checkbutton(root, text=types_checkboxes[i].capitalize(), variable=types_checkboxes_ints[types_checkboxes[i]][0], command=lambda: all_checkboxes(types_checkboxes_ints)))
        types_checkboxes_ints[types_checkboxes[i]][3].grid(row=i+8,column=0, sticky="w")
    else:
        types_checkboxes_ints[types_checkboxes[i]].append(Checkbutton(root, text=types_checkboxes[i].capitalize(), variable=types_checkboxes_ints[types_checkboxes[i]][0], command=lambda: all_checkboxes(types_checkboxes_ints)))
        types_checkboxes_ints[types_checkboxes[i]][3].grid(row=i+7,column=2, sticky="w")
#Checkbutton(root, text="Ninguno").grid(row=8,column=2, sticky="w")

print(types_checkboxes_ints)

# row 24
insert_columns_in_row(24, root)
insert_columns_in_row(25, root)

# row 26
if ("specnewfiletype" not in globals()) and ("new_spec_folder_name" not in globals()):
    globals()["specnewfiletype"] = ""
    globals()["new_spec_folder_name"] = ""


excuteOrganizer = Button(text="Organize my Folder",anchor="center", bg=BG_COLOR, fg=FONT_COLOR_BUTTON, width=44, height=2, justify=LEFT, font=Font(size=10), cursor="hand2", command=lambda: execute_organizer(globals()["foldername"], types_checkboxes_ints, globals()["new_spec_folder_name"], globals()["specnewfiletype"]))

excuteOrganizer["state"] = "disabled"
excuteOrganizer.grid(row=26,column=0, columnspan=4)

# row 27
insert_columns_in_row(27, root)

#

all_checkboxes(types_checkboxes_ints)

root.mainloop()
