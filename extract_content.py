import os
from bs4 import BeautifulSoup

# Path to your local mirror
BASE_PATH = "./openfrontpro.com"  # Relative path from current directory
# Alternative: BASE_PATH = os.path.join(os.getcwd(), "openfrontpro.com")  # Absolute path

# File extensions to parse
HTML_EXTENSIONS = ('.html', '.htm')

# Store extracted content
documents = []

for root, _, files in os.walk(BASE_PATH):
    for file in files:
        if file.endswith(HTML_EXTENSIONS):
            full_path = os.path.join(root, file)
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f, 'lxml')

                # Optional: remove nav, footer, scripts
                for tag in soup(['nav', 'footer', 'script', 'style']):
                    tag.decompose()

                text = soup.get_text(separator='\n', strip=True)
                if text:
                    documents.append({
                        "path": full_path,
                        "text": text
                    })

# Print summary
print(f"Extracted {len(documents)} HTML files.")

# Save to text file
output_file = "extracted_content.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"OpenFront Pro Website Content Extraction\n")
    f.write(f"Total files processed: {len(documents)}\n")
    f.write(f"Generated on: {os.popen('date').read().strip()}\n")
    f.write("=" * 80 + "\n\n")
    
    for i, doc in enumerate(documents):
        f.write(f"📄 FILE: {doc['path']}\n")
        f.write("-" * 60 + "\n")
        f.write(doc['text'])
        f.write("\n\n" + "=" * 80 + "\n\n")

print(f"Content saved to: {output_file}")

# Print example output to console
print("\n--- Example Output ---")
for i, doc in enumerate(documents[:3]):
    print(f"\n📄 {doc['path']}")
    print(doc['text'][:500] + '...\n') 