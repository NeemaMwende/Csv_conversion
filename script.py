import csv
import os
import sys
import re

def sanitize_filename(name):
    """Convert a string to a valid filename by removing or replacing invalid characters."""
    return re.sub(r'[^\w\-\.]', '_', name)

def determine_difficulty(question_text):
    """Determine difficulty based on question content - simple heuristic for demo purposes."""

    if 'Hook' in question_text or 'React.Fragment' in question_text:
        return 3 
    elif 'JSX' in question_text or 'props' in question_text:
        return 2 
    else:
        return 1 

def convert_csv_to_markdown(csv_file):
    """
    Convert CSV file with quiz questions to individual markdown files.
    """
    output_dir = "markdown_questions"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  
        
        for i, row in enumerate(csv_reader):
        
            if not row or all(cell == '' for cell in row):
                continue
           
            question_type = row[0].strip('"')
            
            if not question_type or question_type == "":
                continue
                
            parent_category = row[1] if len(row) > 1 else ""
            category = row[2] if len(row) > 2 else ""
            points = row[7] if len(row) > 7 else "1"
            question_text = row[8] if len(row) > 8 else ""
            
            if not question_text:
                continue
                
            # Get correct answers
            correct_answers = row[9].split(",") if len(row) > 9 else []
            
            answers = []
            for j in range(10, min(20, len(row))):
                if row[j] and row[j] != '':
                    answers.append(row[j])
        
            difficulty = determine_difficulty(question_text)
            
            # Create tags from parent category and category
            tags = []
            if parent_category and parent_category != "":
                tags.append(parent_category)
            if category and category != "":
                tags.append(category)
            
            # Create a unique filename
            filename = f"{i+1:03d}_{sanitize_filename(question_text[:30])}.md"
            filepath = os.path.join(output_dir, filename)
            
            # Generate markdown content
            markdown_content = "---\n"
            markdown_content += f"difficulty: {difficulty}\n"
            markdown_content += f"tags: {', '.join(tags)}\n"
            markdown_content += "---\n\n"
            markdown_content += f"{question_text}\n\n"
            
            # Handle different question types
            if question_type == "multiplechoice":
                for j, answer in enumerate(answers):
                    marker = "#" if chr(65 + j) in correct_answers else ""
                    markdown_content += f"{marker}\n{answer}\n\n"
            elif question_type == "multipleresponse":
                for j, answer in enumerate(answers):
                    marker = "#" if chr(65 + j) in correct_answers else ""
                    markdown_content += f"{marker}\n{answer}\n\n"
            elif question_type == "matching":
               
                for j in range(len(answers) // 2):
                    clue = answers[j*2] if j*2 < len(answers) else ""
                    match = answers[j*2+1] if j*2+1 < len(answers) else ""
                    markdown_content += f"# {clue} -> {match}\n\n"
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)
            
            print(f"Created {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csv_to_markdown.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)
    
    convert_csv_to_markdown(csv_file)
    print("Conversion complete!")