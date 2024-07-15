import os
import streamlit as st
import PyPDF2
import io

st.set_page_config(
    page_title='PDF Editor',
     # favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)
    layout='wide',
    initial_sidebar_state='auto'
)

def merge_pdfs(pdf1_bytes, pdf2_bytes):
    pdf1_file = io.BytesIO(pdf1_bytes)
    pdf2_file = io.BytesIO(pdf2_bytes)

    pdf1_reader = PyPDF2.PdfFileReader(pdf1_file)
    pdf2_reader = PyPDF2.PdfFileReader(pdf2_file)

    pdf_writer = PyPDF2.PdfFileWriter()

    for page_num in range(len(pdf1_reader.pages)):
        page = pdf1_reader.pages[page_num]
        pdf_writer.addPage(page)

    for page_num in range(len(pdf2_reader.pages)):
        page = pdf2_reader.pages[page_num]
        pdf_writer.addPage(page)

    output_file = io.BytesIO()
    pdf_writer.write(output_file)
    return output_file.getvalue()

def split_pdf_at_page(input_file, split_page):
    pdf_reader = PyPDF2.PdfFileReader(input_file)
    num_pages = len(pdf_reader.pages)

    if not 0 < split_page <= num_pages:
        st.error(f"Invalid split page number. Enter a number between 1 and {num_pages}.")
        return None, None

    filename = os.path.splitext(os.path.basename(input_file.name))[0]
    output_folder = "Files"
    os.makedirs(output_folder, exist_ok=True)

    output_path1 = os.path.join(output_folder, f"{filename}_split_part1.pdf")
    pdf_writer1 = PyPDF2.PdfFileWriter()

    for page_num in range(split_page - 1):
        page = pdf_reader.pages[page_num]
        pdf_writer1.addPage(page)

    output_file1 = open(output_path1, 'wb')
    pdf_writer1.write(output_file1)
    output_file1.close()

    output_path2 = os.path.join(output_folder, f"{filename}_split_part2.pdf")
    pdf_writer2 = PyPDF2.PdfFileWriter()

    for page_num in range(split_page - 1, num_pages):
        page = pdf_reader.pages[page_num]
        pdf_writer2.addPage(page)

    output_file2 = open(output_path2, 'wb')
    pdf_writer2.write(output_file2)
    output_file2.close()

    return output_path1, output_path2

def extract_pdf_pages(input_file, output_prefix, page_numbers):
    pdf_reader = PyPDF2.PdfFileReader(input_file)
    num_pages = len(pdf_reader.pages)
    page_numbers = [page_num for page_num in page_numbers if 0 < page_num <= num_pages]

    if not page_numbers:
        st.error(f"Invalid page numbers. Enter numbers between 1 and {num_pages}.")
        return None

    filename = os.path.splitext(os.path.basename(input_file.name))[0]
    output_folder = "Files"
    os.makedirs(output_folder, exist_ok=True)

    output_paths = []
    for page_num in page_numbers:
        output_path = os.path.join(output_folder, f"{output_prefix}_page_{page_num}.pdf")
        pdf_writer = PyPDF2.PdfFileWriter()

        page = pdf_reader.pages[page_num - 1]
        pdf_writer.addPage(page)

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        output_paths.append(output_path)

    return output_paths

def encrypt_pdf(input_file, output_file, password):
    pdf_reader = PyPDF2.PdfFileReader(input_file)
    pdf_writer = PyPDF2.PdfFileWriter()

    for page in pdf_reader.pages:
        pdf_writer.addPage(page)

    pdf_writer.encrypt(password)

    with open(output_file, 'wb') as output:
        pdf_writer.write(output)

def decrypt_pdf(input_file, output_file, password):
    pdf_reader = PyPDF2.PdfFileReader(input_file)

    if pdf_reader.decrypt(password):
        pdf_writer = PyPDF2.PdfFileWriter()

        for page in pdf_reader.pages:
            pdf_writer.addPage(page)

        with open(output_file, 'wb') as output:
            pdf_writer.write(output)
        return True
    else:
        return False

def compress_pdf(input_file, output_file, quality=75):
    pdf_reader = PyPDF2.PdfFileReader(input_file)
    pdf_writer = PyPDF2.PdfFileWriter()

    for page in pdf_reader.pages:
        pdf_writer.addPage(page)

    contains_images = any(has_images(page) for page in pdf_reader.pages)
    if contains_images:
        pdf_writer.compress_images(quality)

    with open(output_file, 'wb') as output:
        pdf_writer.write(output)

def rotate_pdf(input_file, output_file, rotation_angle):
    pdf_reader = PyPDF2.PdfFileReader(input_file)
    pdf_writer = PyPDF2.PdfFileWriter()

    for page in pdf_reader.pages:
        rotated_page = page.rotateClockwise(rotation_angle)
        pdf_writer.addPage(rotated_page)

    with open(output_file, 'wb') as output:
        pdf_writer.write(output)

def has_images(page):
    xObject = page['/Resources']['/XObject'].getObject()
    return '/Im0' in xObject


def merge_pdfs_page():
    st.header("PDF Merger")

    pdf1 = st.file_uploader("Upload the first PDF file", type="pdf")
    pdf2 = st.file_uploader("Upload the second PDF file", type="pdf")

    if st.button("Merge PDFs") and pdf1 and pdf2:
        merged_pdf_bytes = merge_pdfs(pdf1.read(), pdf2.read())
        filename1 = os.path.splitext(os.path.basename(pdf1.name))[0]
        filename2 = os.path.splitext(os.path.basename(pdf2.name))[0]
        output_folder = "Files"
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f"{filename1}_and_{filename2}_merged.pdf")
        with open(output_file, 'wb') as output:
            output.write(merged_pdf_bytes)
        st.success("PDF files merged successfully! You can download the merged PDF below.")
        st.download_button("Download Merged PDF", data=merged_pdf_bytes, file_name=os.path.basename(output_file), mime="application/pdf")

def split_pdf_page():
    st.header("PDF Splitter")

    input_file = st.file_uploader("Upload a PDF file", type="pdf")

    if input_file:
        split_page = st.number_input("Enter the page number where to split the PDF", min_value=1, max_value=100000, value=1)

        if st.button("Split"):
            part1, part2 = split_pdf_at_page(input_file, split_page)
            if part1 and part2:
                st.success("PDF split successfully!")
                st.download_button("Download Part 1", data=open(part1, 'rb').read(), file_name=os.path.basename(part1))
                st.download_button("Download Part 2", data=open(part2, 'rb').read(), file_name=os.path.basename(part2))

def extract_pdf_pages_page():
    st.header("PDF Page Extractor")

    input_file = st.file_uploader("Upload a PDF file", type="pdf")

    if input_file:
        page_numbers_input = st.text_input("Enter the page numbers to extract (e.g., 1, 3, 5)")
        page_numbers = [int(page_num.strip()) for page_num in page_numbers_input.split(",") if page_num.strip().isdigit()]

        if st.button("Extract"):
            output_prefix = st.text_input("Enter the output prefix", "extracted_pages")
            output_paths = extract_pdf_pages(input_file, output_prefix, page_numbers)

            if output_paths:
                st.success("PDF pages extracted successfully!")
                for i, output_path in enumerate(output_paths):
                    st.download_button(f"Download Page {page_numbers[i]}", data=open(output_path, 'rb').read(), file_name=os.path.basename(output_path))

def encrypt_decrypt_pdf_page():
    st.header("PDF Encryptor/Decryptor")

    input_file = st.file_uploader("Upload a PDF file", type="pdf")

    if input_file:
        operation = st.radio("Select operation:", ("Encrypt", "Decrypt"))
        password = st.text_input("Enter the password")

        if st.button(operation):
            filename = os.path.splitext(os.path.basename(input_file.name))[0]
            output_folder = "Files"
            os.makedirs(output_folder, exist_ok=True)

            if operation == "Encrypt":
                output_file = os.path.join(output_folder, f"{filename}_encrypted.pdf")
                encrypt_pdf(input_file, output_file, password)
                st.success("PDF encrypted successfully! You can download the encrypted PDF below.")
                st.download_button("Download", data=open(output_file, 'rb').read(), file_name=os.path.basename(output_file))
            else:
                output_file = os.path.join(output_folder, f"{filename}_decrypted.pdf")
                if decrypt_pdf(input_file, output_file, password):
                    st.success("PDF decrypted successfully! You can download the decrypted PDF below.")
                    st.download_button("Download", data=open(output_file, 'rb').read(), file_name=os.path.basename(output_file))
                else:
                    st.error("Incorrect password. Unable to decrypt the PDF.")

def compress_pdf_page():
    st.header("PDF Compressor")

    input_file = st.file_uploader("Upload a PDF file", type="pdf")

    if input_file:
        quality = st.slider("Select image quality (0 = low, 100 = high)", min_value=0, max_value=100, value=75)

        if st.button("Compress"):
            filename = os.path.splitext(os.path.basename(input_file.name))[0]
            output_folder = "Files"
            os.makedirs(output_folder, exist_ok=True)

            output_file = os.path.join(output_folder, f"{filename}_compressed.pdf")
            compress_pdf(input_file, output_file, quality)

            if os.path.exists(output_file):
                st.success("PDF compressed successfully! You can download the compressed PDF below.")
                st.download_button("Download Compressed PDF", data=open(output_file, 'rb').read(), file_name=os.path.basename(output_file))
            else:
                st.warning("The PDF file contains no images. Compression not applied.")

def rotate_pdf_page():
    st.header("PDF Page Rotator")

    input_file = st.file_uploader("Upload a PDF file", type="pdf")

    if input_file:
        rotation_angle = st.selectbox("Select rotation angle", [90, 180, 270])

        if st.button("Rotate"):
            filename = os.path.splitext(os.path.basename(input_file.name))[0]
            output_folder = "Files"
            os.makedirs(output_folder, exist_ok=True)

            output_file = os.path.join(output_folder, f"{filename}_rotated.pdf")
            rotate_pdf(input_file, output_file, rotation_angle)

            if os.path.exists(output_file):
                st.success("PDF pages rotated successfully! You can download the rotated PDF below.")
                st.download_button("Download Rotated PDF", data=open(output_file, 'rb').read(), file_name=os.path.basename(output_file))
def main():
    st.title("PDF Editor")
    st.markdown('[Github Link](https://github.com/srinidhim2/PDFEditor)')

    # Navigation options in the sidebar
    navigation = st.sidebar.radio("Select Operation:", 
                                      ["Merge PDFs", "Split PDF", "Extract Pages", "Encrypt/Decrypt", "Compress PDF", "Rotate PDF"])

    if navigation == "Merge PDFs":
        merge_pdfs_page()

    elif navigation == "Split PDF":
        split_pdf_page()

    elif navigation == "Extract Pages":
        extract_pdf_pages_page()

    elif navigation == "Encrypt/Decrypt":
        encrypt_decrypt_pdf_page()

    elif navigation == "Compress PDF":
        compress_pdf_page()

    elif navigation == "Rotate PDF":
        rotate_pdf_page()

if __name__ == "__main__":
    main()
