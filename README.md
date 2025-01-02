# PDF Processing API

This FastAPI application provides an API for handling PDF files with three main functionalities:

1. Merging multiple PDF files into one.
2. Compressing a PDF file.
3. Splitting a PDF file based on specified page ranges.
**Note**: For security reasons, the API currently uses ClamScan to scan for malware, which may result in longer processing times. Alternatively, you can use the VirusTotal API or its Python client. However, due to my commitment to open-source principles and privacy concerns, I have chosen not to use these alternatives.

## Table of Contents

- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Available Endpoints](#available-endpoints)
- [Using the API with `curl`](#using-the-api-with-curl)
- [License](#license)

## Requirements

To use this API, ensure you have the following installed:

- **Python** 3.8+
- **Ghostscript** for PDF compression
- **Clamscan** for the malware analysis
- **FastAPI** for creating the API
- **PyPDF2** for PDF manipulation
- **`curl`** to make HTTP requests from the command line

## Setup and Installation

1. **Clone the repository:**

  ```bash
  git clone https://github.com/Dax2405/PDFeditor-api.git
  cd PDFeditor-api
  ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv env
   source env/bin/activate # For Linux 
   ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI application:**

   ```bash
   uvicorn main:app --reload
   ```

5. **Install Ghostscript (if not already installed):**

   ```bash
   # On Debian/Ubuntu
   sudo apt install ghostscript

   # On Fedora
   sudo dnf install ghostscript
   
   # On Arch 
   sudo pacman -S ghostscript
   ```

## Available Endpoints

### 1. Merge PDFs

- **Endpoint**: `/unir_pdfs/`
- **Method**: `POST`
- **Description**: Merges multiple PDF files into a single PDF.
- **Parameters**: 
  - `files`: List of PDF files to be merged.

### 2. Compress PDF

- **Endpoint**: `/comprimir_pdf/`
- **Method**: `POST`
- **Description**: Compresses a single PDF file.
- **Parameters**:
  - `file`: PDF file to compress.

### 3. Split PDF

- **Endpoint**: `/dividir_pdf/`
- **Method**: `POST`
- **Description**: Splits a PDF file within a specified page range.
- **Parameters**:
  - `file`: PDF file to split.
  - `start`: Starting page number (1-indexed).
  - `end`: Ending page number (1-indexed).

## Using the API with `curl`

Below are `curl` commands for each endpoint. Replace `localhost:8000` with the appropriate IP address or domain if the API is deployed.

### 1. Merge PDFs

To merge multiple PDF files:

```bash
curl -X POST "http://localhost:8000/unir_pdfs/" -F "files=@file1.pdf" -F "files=@file2.pdf" -o merged_output.pdf
```

### 2. Compress PDF

To compress a single PDF file:

```bash
curl -X POST "http://localhost:8000/comprimir_pdf/" -F "file=@file_to_compress.pdf" -o compressed_output.pdf
```

### 3. Split PDF

To split a PDF from page `start` to `end`:

```bash
curl -X POST "http://localhost:8000/dividir_pdf/" -F "file=@file_to_split.pdf" -F "start=1" -F "end=3" -o split_output.pdf
```

## Using the API on Personal Hosting

You can also use the API on my personal hosting at `https://pdf-api.dax-ec.ru/`. Please note that it may take a longer time to process requests due to malware scanning. If you run the API locally, you can disable the malware scanner to speed up the process.

## License

This project is licensed under the MIT License.