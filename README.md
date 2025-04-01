# CSV to Markdown Converter  

This script converts a CSV file into multiple Markdown files, organizing them into a structured format.  

## Features  
- Reads a CSV file and extracts question data  
- Saves the generated Markdown files both in the repository and in local storage (`~/Documents/my_markdown_files`)  
- Synchronizes changes between the local folder and the repository  

## Prerequisites  
Ensure you have the following installed on your system:  
- Python 3.10+  
- `pip` package manager  

## Installation  
1. Clone the repository:  

   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   
Install dependencies:
- pip install -r requirements.txt

## Usage
Run the script by specifying the CSV file path:
- python3 csv_to_markdown.py path/to/your/data.csv
Example (using a file inside the repo):
- python3 csv_to_markdown.py data.csv
For users running the script from their local storage:
- python3 csv_to_markdown.py ~/Documents/data.csv

## Synchronizing Changes
Any modifications made to the generated Markdown files in ~/Documents/my_markdown_files will reflect in the repository, and vice versa.

