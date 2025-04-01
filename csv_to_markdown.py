import csv
import os
import sys
import re
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define directories
APP_DIR = "markdown_questions"
HOME_DIR = os.path.expanduser("~/Documents/my_markdown_files")

def sanitize_filename(name):
    return re.sub(r'[^\w\-\.]', '_', name)

def determine_difficulty(parent_category):
    if 'Advanced' in parent_category:
        return 3
    elif 'Intermediate' in parent_category:
        return 2
    elif "Basics" in parent_category:
        return 1
    else:
        return 1

class SyncHandler(FileSystemEventHandler):
    def __init__(self, source_dir, target_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.syncing = False
        
    def on_modified(self, event):
        if event.is_directory or self.syncing or event.src_path.endswith('.tmp') or '.goutputstream-' in event.src_path:
            return
        
        filename = os.path.basename(event.src_path)
        if filename.startswith('.') or not filename.endswith('.md'):
            return
            
        target_path = os.path.join(self.target_dir, filename)
        
        try:
            self.syncing = True
            if os.path.exists(event.src_path):
                shutil.copy2(event.src_path, target_path)
                print(f"Synced: {filename}")
        except Exception as e:
            print(f"Error syncing {filename}: {e}")
        finally:
            time.sleep(0.1)
            self.syncing = False
            
    def on_created(self, event):
        self.on_modified(event)

def setup_sync():
    os.makedirs(APP_DIR, exist_ok=True)
    os.makedirs(HOME_DIR, exist_ok=True)
    
    # Initial sync of existing files
    for filename in os.listdir(APP_DIR):
        if filename.endswith('.md'):
            shutil.copy2(os.path.join(APP_DIR, filename), os.path.join(HOME_DIR, filename))
    
    observer = Observer()
    
    # Watch for changes in both directories
    app_handler = SyncHandler(APP_DIR, HOME_DIR)
    home_handler = SyncHandler(HOME_DIR, APP_DIR)
    
    observer.schedule(app_handler, APP_DIR, recursive=False)
    observer.schedule(home_handler, HOME_DIR, recursive=False)
    
    observer.start()
    print(f"Synchronizing files between {APP_DIR} and {HOME_DIR}")
    return observer

def convert_csv_to_markdown(csv_file):
    os.makedirs(APP_DIR, exist_ok=True)
    os.makedirs(HOME_DIR, exist_ok=True)
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        
        question_counter = 1
        
        for row in csv_reader:
            if not row or all(cell == '' for cell in row):
                continue
                
            question_type = row[0].strip('"')
            
            if not question_type:
                continue
                
            parent_category = row[1] if len(row) > 1 else ""
            category = row[2] if len(row) > 2 else ""
            question_text = row[8] if len(row) > 8 else ""
            
            if not question_text:
                continue
                
            correct_answers = row[9].split(",") if len(row) > 9 and row[9] else []
            
            answers = []
            for j in range(10, min(20, len(row))):
                if row[j] and row[j] != '':
                    answers.append(row[j])
            
            difficulty = determine_difficulty(question_text)
            
            tags = []
            if question_type:
                tags.append(question_type)
            if parent_category and parent_category != "":
                tags.append(parent_category)
            if category and category != "":
                tags.append(category)
            
            filename = f"{question_counter:03d}.md"
            app_filepath = os.path.join(APP_DIR, filename)
            home_filepath = os.path.join(HOME_DIR, filename)
            
            markdown_content = "---\n"
            markdown_content += f"difficulty: {difficulty}\n"
            markdown_content += f"tags: {', '.join(tags)}\n"
            markdown_content += "---\n\n"
            markdown_content += f"{question_text}\n\n"
            
            for j, answer in enumerate(answers):
                if chr(65 + j) in correct_answers:
                    markdown_content += f"# Correct\n\n{answer}\n\n"
                else:
                    markdown_content += f"#\n\n{answer}\n\n"
            
            # Write to both locations
            with open(app_filepath, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)
            
            with open(home_filepath, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)
            
            print(f"Created {filename}")
            question_counter += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)
    
    convert_csv_to_markdown(csv_file)
    print("Conversion complete!")
    
    observer = setup_sync()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("Sync stopped")