import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from pypdf import PdfWriter

def download_pdfs(url, directory = 'data_cvm'):
    """
    Downloads all the PDF files in a specific URL.

    :param url: The URL that contains the PDF links.
    :param directory: The name of the directory where the files will be saved.
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f'Directory {directory} succesfully created.')
    
    # Request the page HTML
    try:
        print(f'Accessing the URL: {url}')
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Error accessing URL: {e}')
        return

    # Analyze the HTML using BeautifulSoup
    soup = BeautifulSoup(response.content,'html.parser')
    report_pages_links = []
    
    # Find all the pages that lead to the PDF downloads
    content_div = soup.find(id = 'content-core')
    if content_div:
        for link in content_div.find_all('a', href = True):
            if 'view' in link['href']:
                abs_link = urljoin(url, link['href'])
                if abs_link not in report_pages_links:
                    report_pages_links.append(abs_link)
    if not report_pages_links:
        print('No report pages found.')
        return
    
    print(f'\n Found {len(report_pages_links)} report pages links. Checking them one by one...')
    
    # Visit every link found and search the pdf for download.
    for page_link in report_pages_links:
        try:
            print(f'\n-> Accessing report page: {page_link}')
            page_response = requests.get(page_link)
            page_response.raise_for_status()

            page_soup = BeautifulSoup(page_response.content, 'html.parser')

            pdf_link = None

            # Search for a link containing the '.pdf'
            pdf_tag = page_soup.find('a', href = lambda href: href and '@@download' in href.lower())
            
            
            if pdf_tag:
                pdf_link = urljoin(page_link, pdf_tag['href'])

                

            else:
                print(f'-> PDF link not found: {page_link}')
                continue
            
            # Downloads the PDF file:
            file_name = pdf_link.split('/')[-3]
            if not file_name.endswith('.pdf'):
                file_name += '.pdf'
            
            file_path = os.path.join(directory, file_name)

            print(f'-> Downloading "{file_name}"...')
            pdf_response = requests.get(pdf_link, stream=True)
            pdf_response.raise_for_status()

            with open(file_path, 'wb') as f:
                for chunk in pdf_response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f'-> Successfully saved in {directory}/')
        
        except requests.exceptions.RequestException as e:
            print(f"-> Failure at processing page {page_link}. Error: {e}")
    
    print('Download process finished.')

def merge_pdfs(folder_path = './', output_filename = 'merged_document.pdf'):
    """
    Merges all PDF files inside a folder into a single PDF document.

    :param folder_path: the path to folder containing the PDF files.
    :param output_filename: name of the file contaning the merged documents.
    """
    merger = PdfWriter()

    # Getting the list of all files inside the folder
    try:
        pdf_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')])
    except FileNotFoundError:
        print(f'The folder "{folder_path}" was not found.')

    if not pdf_files:
        print(f'No PDF files found in "{folder_path}".')
        return
    
    print(f'Found {len(pdf_files)} PDF files in {folder_path}.')

    # Appending all the PDF files found to the merger
    for filename in pdf_files:
        filepath = os.path.join(folder_path, filename)
        print(f'Adding: {filename}')
        try:
            merger.append(filepath)
        except Exception as e:
            print(f'An error occurred during the merging process: {e}')
    # Writing the merged PDF to the output file
    try:
        with open(os.path.join(folder_path,output_filename), 'wb') as output_file:
            merger.write(output_file)
        print(f'Succesfully merged the files into "{output_filename}".')
    except Exception as e:
        print(f'An error occurred during the writing process: {e}')
    finally:
        merger.close()


if __name__ == '__main__':
    url = 'https://www.gov.br/cvm/pt-br/centrais-de-conteudo/publicacoes/relatorios/relatorio-de-gestao-da-cvm'
    #download_pdfs(url)
    merge_pdfs(folder_path='./data_cvm')