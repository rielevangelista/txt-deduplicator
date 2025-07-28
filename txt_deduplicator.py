import re
import hashlib
from collections import defaultdict

def normalize_line(line):
    """Normalize a line for comparison by removing emojis and extra whitespace."""
    # Remove common emojis
    normalized = re.sub(r'[✅🔹🔸☘️💙✨🇭🇰🌈🔥💅❤️🏷️🆕]', '', line)
    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', normalized.strip())
    return normalized

def remove_duplicate_3line_groups(filepath, output_path, duplicates_report_path):
    print("📖 Reading file...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"📊 Processing {total_lines:,} lines in groups of 3...")
    
    seen_groups = {}  # hash -> first occurrence (lines)
    duplicate_groups = defaultdict(list)  # hash -> list of duplicate occurrences
    kept_lines = []
    removed_groups = 0
    
    i = 0
    while i < len(lines):
        # Get current group of 3 lines (or remaining lines if less than 3)
        group_size = min(3, len(lines) - i)
        current_group = lines[i:i + group_size]
        
        # Skip empty lines
        non_empty_lines = [line for line in current_group if line.strip()]
        if not non_empty_lines:
            kept_lines.extend(current_group)
            i += group_size
            continue
        
        # Normalize the group for comparison (ignore timestamps)
        normalized_group = []
        for line in non_empty_lines:
            line_text = line.strip()
            # Skip timestamp lines in comparison
            if not re.match(r'^\[\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2}:\d{2}[^\]]*\]', line_text):
                normalized_group.append(normalize_line(line_text))
        
        # Create hash for this normalized group
        if normalized_group:
            group_text = '\n'.join(normalized_group)
            group_hash = hashlib.sha256(group_text.encode()).hexdigest()
            
            # Check if we've seen this group before
            if group_hash not in seen_groups:
                seen_groups[group_hash] = current_group.copy()
                kept_lines.extend(current_group)
            else:
                duplicate_groups[group_hash].append(current_group.copy())
                removed_groups += 1
                # Skip this duplicate group
                pass
        else:
            # No content to compare, keep the group
            kept_lines.extend(current_group)
        
        if i % 3000 == 0:  # Progress indicator
            print(f"   Processed {i:,} lines...")
        
        i += group_size
    
    print("💾 Writing deduplicated file...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(kept_lines)
    
    print("📝 Writing duplicates report...")
    with open(duplicates_report_path, 'w', encoding='utf-8') as f:
        f.write("=== DUPLICATE 3-LINE GROUPS REPORT ===\n\n")
        f.write(f"Total unique groups that had duplicates: {len(duplicate_groups)}\n")
        f.write(f"Total duplicate groups removed: {removed_groups}\n\n")
        
        # Sort by number of duplicates (most duplicated first)
        sorted_duplicates = sorted(duplicate_groups.items(), key=lambda x: len(x[1]), reverse=True)
        
        for i, (group_hash, duplicates) in enumerate(sorted_duplicates, 1):
            original = seen_groups[group_hash]
            f.write(f"--- DUPLICATE GROUP #{i} (appeared {len(duplicates) + 1} times) ---\n")
            f.write("ORIGINAL (kept):\n")
            for line in original:
                f.write(f"  {line.rstrip()}\n")
            
            f.write(f"\nDUPLICATES (removed {len(duplicates)} copies):\n")
            for j, duplicate in enumerate(duplicates, 1):
                f.write(f"\nDuplicate #{j}:\n")
                for line in duplicate:
                    f.write(f"  {line.rstrip()}\n")
            
            f.write("\n" + "="*60 + "\n\n")
    
    print(f"✅ Done!")
    print(f"   Original lines: {total_lines:,}")
    print(f"   Lines kept: {len(kept_lines):,}")
    print(f"   Lines removed: {total_lines - len(kept_lines):,}")
    print(f"   Duplicate 3-line groups removed: {removed_groups:,}")
    print(f"   Duplicates report saved to: {duplicates_report_path}")

# Example usage
import os
import sys

# Define folder paths
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

# Ensure folders exist
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Get input file from command line argument or use default
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = '_chat.txt'

# Construct full paths
input_file = os.path.join(INPUT_FOLDER, filename)

print(f"🎯 Processing file: {filename}")
print(f"📁 Looking in: {INPUT_FOLDER}/")

# Check if input file exists
if not os.path.exists(input_file):
    print(f"❌ Error: File '{filename}' not found in '{INPUT_FOLDER}' folder!")
    print("Usage: python dedup-3line-with-report.py [filename]")
    print("Example: python dedup-3line-with-report.py my_chat.txt")
    print(f"Make sure your file is in the '{INPUT_FOLDER}' folder!")
    sys.exit(1)

# Generate output filenames based on input filename
base_name = os.path.splitext(filename)[0]  # Remove extension
extension = os.path.splitext(filename)[1]  # Get extension

output_file = os.path.join(OUTPUT_FOLDER, f'{base_name}_deduplicated{extension}')
duplicates_report = os.path.join(OUTPUT_FOLDER, f'{base_name}_duplicates_report.txt')

print(f"📄 Output file: {OUTPUT_FOLDER}/{base_name}_deduplicated{extension}")
print(f"📋 Report file: {OUTPUT_FOLDER}/{base_name}_duplicates_report.txt")
print()

remove_duplicate_3line_groups(input_file, output_file, duplicates_report)
