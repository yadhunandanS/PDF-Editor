# [PDFEditor](https://pdfeditor.streamlit.app/)
Small python app for modifying PDFs


## PDF Manipulation Tools

This GitHub repository contains a collection of Python scripts and a Streamlit web application to perform various operations on PDF files. The scripts utilize the PyPDF2 library for PDF manipulation and Streamlit for creating a user-friendly interface.

### Supported Operations

1. **PDF Merger:** Merge two PDF files into a single PDF.

2. **PDF Splitter:** Split a PDF into two parts at a specified page number.

3. **PDF Encryptor/Decryptor:** Encrypt or decrypt a PDF using a password.

4. **PDF Compressor:** Compress images in a PDF to reduce file size.

5. **PDF Page Rotator:** Rotate all pages in a PDF by 90, 180, or 270 degrees.

6. **PDF Page Extractor:** Extract specific pages from a PDF into separate PDFs.

## Web Application

The Streamlit web application provides a user-friendly interface for performing these operations. Users can upload their PDF files, set parameters as needed, and perform the desired operation with a single click. The application handles various scenarios, such as wrong passwords during encryption/decryption and non-image PDFs during compression.

The merged, split, encrypted, compressed, rotated, or extracted PDFs are stored in the "Files" folder within the repository for easy access and can be downloaded directly from the interface. The web application is designed to be intuitive and user-friendly, allowing users to manipulate their PDF files efficiently.

## Instructions

1. Clone the repository and navigate to the project directory.

2. Install the required dependencies using `pip install -r requirements.txt` and `pip install PyPDF2`. 

3. Run the Streamlit application using `streamlit run app.py`.

4. Access the web application via the provided local URL or visit [**this site**](https://pdfeditor.streamlit.app/).

5. Choose the desired PDF operation from the navigation bar and follow the instructions on the page.

6. Upload the necessary PDF files, set the required parameters, and perform the operation.

7. The result PDFs will be stored in the "Files" folder and can be downloaded directly from the interface.

This repository provides a convenient and user-friendly way to perform essential PDF operations without the need for complex software. Whether you need to merge, split, encrypt, compress, rotate, or extract pages from PDFs, this collection of tools simplifies the process and enhances your PDF manipulation capabilities.
