# PDF Splitter Script

This Python script splits a PDF file into multiple PDFs based on its table of contents (TOC). It's particularly useful for large PDFs with a complex structure, where you want to separate different sections into individual files.

## Features

- Splits PDF based on top-level sections in the table of contents
- Handles PDFs with complex TOC structures, including sections without specific page numbers
- Creates separate PDF files for each main section
- Provides detailed logging for troubleshooting

## Requirements

- Python 3.6 or higher
- PyMuPDF (fitz) library

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.

2. Install the required PyMuPDF library using pip:

   ```
   pip install PyMuPDF
   ```

3. Download the `pdf_splitter.py` script to your local machine.

## Usage

Run the script from the command line with the following syntax:

```
python pdf_splitter.py <input_pdf> <output_prefix>
```

- `<input_pdf>`: Path to the input PDF file you want to split
- `<output_prefix>`: Prefix for the output PDF files

Example:

```
python pdf_splitter.py rest-api-fabric.pdf output_prefix
```

This command will split the `rest-api-fabric.pdf` file and create multiple PDFs with names starting with `output_prefix`.

## Output

The script will create separate PDF files for each top-level section in the table of contents. The output files will be named in the format:

```
<output_prefix>_XX_SectionName.pdf
```

Where:
- `XX` is a two-digit number indicating the section order
- `SectionName` is the name of the section from the table of contents (with special characters replaced by underscores)

## Troubleshooting

If you encounter any issues:

1. Check the console output for error messages and warnings.
2. Ensure your input PDF is not corrupted and has a valid table of contents.
3. If no files are created, try running the script with a different PDF to see if the issue is specific to your input file.
4. Make sure you have write permissions in the directory where you're running the script.

## Limitations

- The script primarily focuses on top-level sections (level 1 headers in the TOC).
- PDFs without a table of contents or with non-standard TOC structures may not split correctly.
- Very large PDFs may require significant processing time and memory.

## Contributing

Feel free to fork this project and submit pull requests with any enhancements. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).