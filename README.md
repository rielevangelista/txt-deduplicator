# WhatsApp Chat Deduplicator

A Python script that removes duplicate content from WhatsApp chat exports while preserving important context like product-price relationships.

## Features

- ✅ **Smart Deduplication**: Removes duplicates in 3-line groups to preserve context
- ✅ **Preserves Product-Price Pairs**: Keeps important relationships intact
- ✅ **Emoji Normalization**: Handles emoji variations intelligently
- ✅ **Detailed Reporting**: Shows exactly what was removed
- ✅ **Massive File Reduction**: Typically reduces file size by 60-70%
- ✅ **Organized Structure**: Clean input/output folder organization

## Quick Start

1. **Place your chat file** in the `input/` folder
2. **Run the script**:
   ```bash
   python dedup-3line-with-report.py
   ```
3. **Get your results** from the `output/` folder

## Usage

### Default Usage
```bash
python dedup-3line-with-report.py
```
Processes `input/_chat.txt` by default.

### Custom File
```bash
python dedup-3line-with-report.py your_file.txt
```
Processes `input/your_file.txt`.

## File Structure

```
├── dedup-3line-with-report.py    # Main script
├── input/                        # Put your chat files here
│   └── _chat.txt                # Sample chat file
├── output/                       # Cleaned files appear here
│   ├── _chat_deduplicated.txt   # Clean output
│   └── _chat_duplicates_report.txt # Detailed report
└── README.md                     # This file
```

## Output Files

For input file `my_chat.txt`, you get:
- `output/my_chat_deduplicated.txt` - Clean chat file
- `output/my_chat_duplicates_report.txt` - Report of removed duplicates

## Example Results

```
Original lines: 355,977
Lines kept: 109,041
Lines removed: 246,936 (69% reduction!)
Duplicate 3-line groups removed: 82,312
```

## How It Works

1. **Groups lines** into sets of 3 for context preservation
2. **Normalizes content** by removing emojis and extra whitespace
3. **Identifies duplicates** using content hashing
4. **Preserves first occurrence** of each unique group
5. **Generates detailed report** of what was removed

## Requirements

- Python 3.6+
- No external dependencies (uses only built-in modules)

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use and modify as needed.
