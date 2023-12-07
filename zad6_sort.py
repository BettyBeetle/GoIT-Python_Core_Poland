import sys
import os
import shutil
import glob
import re
import zipfile
import tarfile
import gzip

def get_path():
    if len(sys.argv) > 2:
        print(f"Error: wrong path, give a right path of folder to sort")
        sys.exit()
    else:
        folder_path = sys.argv[1]
        if os.path.exists(os.path.dirname(folder_path)) and os.path.isdir(folder_path):
            return folder_path
        print("Sorting out..")
  
### Uznawane rozszerzenia plików
img_ext = ["*.jpg", "*.png", "*.jpeg", "*.svg", "*.tiff"]
txt_ext = ["*.pdf", "*.txt", "*.doc", "*.docx", "*.txt", "*.xlsx", "*.pptx", "*.odp", "*.odg","*.ods", "*.odt" ]
audio_ext  = ["*.mp3", "*.ogg", "*.wav", "*.amr"]
video_ext = ["*.avi", "*.mp4", "*.mov", "*.mkv"]
arch_ext = ["*.zip", "*.gz", "*.tar"]
py_ext = ["*.py"]

### Tablica do transliteracji
polish = ("ą", "Ą", "ć", "Ć", "ę", "Ę", "ł", "Ł", "ń", "Ń", "ó", "Ó", "ś", "Ś", "ż", "Ż", "ź", "Ź")
translation = ("a", "A", "c", "C", "e", "E", "l", "L", "n", "N", "o", "O", "s", "S", "z", "Z", "z", "Z")
TRANS = {}

for p, t in zip(polish, translation):
    TRANS[ord(p)] = t
    TRANS[ord(p.upper())] = t.upper()



### Normalizacja nazw plików
def normalize(destination):
    files = list(os.listdir(destination))   
    for file in files:
        if file != ".":
            name, file_ext = os.path.splitext(file)  # Rozdziel nazwę pliku i rozszerzenie
            normalized_name = name.translate(TRANS)
            normalized_name = re.sub(r"[^\w.]+", "_", normalized_name)    
            if normalized_name != name:
                i = 1
                while os.path.exists(os.path.join(destination, f"{normalized_name}_{i}{file_ext}")):
                    i += 1
                new_name = f"{normalized_name}_{i}{file_ext}"
                os.rename(os.path.join(destination, file), os.path.join(destination, new_name))
            print(f"Normalized name of {file} in {destination} folder")


    folder_path = sys.argv[1]
    ignored = ["_audio", "_images", "_documents", "_video", "_archives"]
    for subdir, dirs, files in os.walk(folder_path):
        for dir in dirs:
            folder_path = os.path.join(subdir, dir)
            if dir in ignored:
                continue
            if not os.listdir(folder_path):     
                print(f"Usunięto puste foldery: {folder_path}")
                os.rmdir(folder_path) 



### Sprawdzanie rozszerzenia archiwów
def unzip():
    prev_dir = os.getcwd() 
    print(prev_dir)
    os.chdir("_archives")
    #print(os.getcwd())
    archives = list(os.listdir())


    for archive in archives:
        extension = os.path.splitext(archive)[1]
        
        if extension == ".zip":
            extracted_file_path = os.path.splitext(archive)[0]
            with zipfile.ZipFile(archive, "r") as zip:
                zip.extractall(extracted_file_path)
            os.remove(archive)
            print(f"Usunięto archiwum: {archive}.")

        elif extension == ".tar":
            extracted_file_path = os.path.splitext(archive)[0]
            with tarfile.open(archive, 'r') as tar:
                    tar.extractall(extracted_file_path)
            os.remove(archive)
            print(f"Usunięto archiwum: {archive}.")

        elif extension == ".gz":
            extracted_file_path = os.path.splitext(archive)[0]
            with gzip.open(archive, 'rb') as f_in:
                with open(extracted_file_path, 'wb') as f_out:
                    f_out.write(f_in.read())
            os.remove(archive)
            print(f"Usunięto archiwum: {archive}.")
    os.chdir("..") 

### Tworzenie nowych folderów z pominięciem ich jeśli już isnieją
def create_folders():
    folder_names = ["_images", "_documents", "_audio", "_video", "_archives"]
    for folder_name in folder_names:
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print(f"Creating a {folder_name}")

### Przenoszenie plików do folderów
def move_files(extensions, destination):
    for ext in extensions:      
        for file in glob.glob("**/" + ext, recursive = True):            
            shutil.move(file, destination + "/" + os.path.basename(file))
            print(f"Moving: {file} to folder: {destination}")
        

        
def main():
    create_folders()
    move_files(img_ext, "_images")  
    move_files(txt_ext, "_documents") 
    move_files(audio_ext, "_audio") 
    move_files(video_ext, "_video") 
    move_files(arch_ext, "_archives") 
    unzip()
    normalize("_images")  
    normalize("_documents") 
    normalize("_audio")
    normalize("_video") 
    normalize("_archives") 


if __name__ == "__main__":
    folder_path = get_path()
    os.chdir(folder_path)
    main()



