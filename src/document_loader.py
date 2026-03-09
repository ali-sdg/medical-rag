#pymupdf library
import fitz 
import os


def load_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ''


    for page_num in range(len(doc)):

        page = doc[page_num]
        text = page.get_text()
        full_text += text
        print(f'page {page_num + 1 } readed' )
        doc.close()


        return full_text


def load_all_pdfs(folder_path):
    
    all_text = []

    # looking on folder
    for file_name in os.listdir(folder_path):

        # just get *.pdf files
        if file_name.endswith('.pdf'):

            file_path = os.path.join(folder_path, file_name)

            print(f'\n reading : {file_name}')

            text = load_pdf(file_path)

            # saving text with file name
            all_text.append({
                'source':file_name,
                'text' : text
            })

    return all_text

