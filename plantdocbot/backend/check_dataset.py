import os

def check_structure():
    base_path = r"C:\PD\New Plant Diseases Dataset(Augmented)"
    print(f"Checking contents of: {base_path}")
    
    try:
        items = os.listdir(base_path)
        print(f"Found {len(items)} items:")
        for item in items:
            path = os.path.join(base_path, item)
            is_dir = "DIR" if os.path.isdir(path) else "FILE"
            print(f" - [{is_dir}] {item}")
            
            # If it's a directory, peek inside
            if os.path.isdir(path):
                subitems = os.listdir(path)[:5]
                print(f"   -> {subitems}")
                
    except Exception as e:
        print(f"Error accessing path: {e}")

if __name__ == "__main__":
    check_structure()
