import os
import sys
import json
import glob
from tqdm import tqdm

base_dir = "./syllabuses"
out_dir = "./results"

def main(argv):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    if len(argv) != 2:
        exit(1) 
    
    year = argv[1]
    file_paths = sorted(glob.glob(f"{base_dir}/{year}/*.json"))

    result = {}
    for path in tqdm(file_paths):
        basename = os.path.splitext(os.path.basename(path))[0]        
        with open(path, "r") as f:
            major_rec = {}
            rec_list = json.load(f)
            for rec in rec_list:
                major_rec[rec['code']] = rec
            result[basename] = major_rec
    with open(f"{out_dir}/{year}.json", "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main(sys.argv)            