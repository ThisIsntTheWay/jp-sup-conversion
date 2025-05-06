import os
import os.path
import sys
from tqdm import tqdm
from pysubs2 import SSAFile, SSAEvent, make_time
from manga_ocr import MangaOcr
import json
from termcolor import colored
import shutil

"""
Convert .sup to .png
"""
def convert_file(file_path):
    print(colored(f"[i] Processing file: {file_path}", "cyan"))
    
    # Convert shit to idx and sub
    # CLI args: https://github.com/mjuhasz/BDSup2Sub/wiki/Command-line-Interface
    output_file_base = os.path.splitext(os.path.basename(file_path))[0]    
    print(colored(f"[i] Splitting sup...", "cyan"))
    if os.system(f"java -jar BDSup2Sub.jar \"{file_path}\" -o \"{output_file_base + '.sub'}\"") == 0:
        print(colored(f"[✓] Split to idx and sub", "green"))
    else:
        raise Exception(f"Error processing file: {file_path}")
    
    # Convert to png
    if os.path.exists("subimg") and os.path.isdir("subimg"):
        shutil.rmtree("subimg")
    
    print(colored(f"[i] Converting to png...", "cyan"))
    if os.system(f"vobsub2png -o subimg \"{output_file_base + '.idx'}\"") == 0:
        print(colored(f"[✓] Converted to png", "green"))
    else:
        raise Exception(f"Error converting idx to png!")

"""
OCR pngs into SRT
"""
def process_sub(subtitle_name, output_folder=".", mocr=MangaOcr()):
    print(colored(f"[i] Converting to ass...", "cyan"))
    subtitle_name = os.path.splitext(os.path.basename(subtitle_name))[0]
    with open('subimg/index.json') as user_file:
        subs_meta = json.load(user_file)

    subs = SSAFile()
    for m in tqdm(subs_meta['subtitles']):
        subs.append(SSAEvent(
            start=make_time(s=m["start"]),
            end=make_time(s=m["end"]),
            text=mocr("subimg/"+m["path"]))
        )

    file_name = f"{output_folder}/{subtitle_name}.ass"
    if (os.path.isfile(file_name)):
        os.remove(file_name)
        
    subs.save(file_name, 'utf-8', 'ass')
    print(colored("[✓] Generated ass:", "green"), file_name)

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(colored(f"[!] Error: {folder_path} is not a valid directory.", "red"))
        sys.exit(1)
        
    mocr = MangaOcr()
    for root, _, files in os.walk(folder_path):
        valid_files = 0
        for file in files:
            if file.endswith(".sup"):
                valid_files += 1
                file_path = os.path.join(root, file)
                
                convert_file(file_path)
                process_sub(file_path, folder_path, mocr)
                
                # Cleanup
                print(colored(f"[!] Cleaning .idx and .sub files...", "yellow"))
                for file in files:
                    if file.endswith(".idx") or file.endswith(".sub"):
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                
        if valid_files == 0:
            print(colored(f"[!] No .sup files found in {root}", "yellow"))
            
if __name__ == "__main__":
    main()