from django.utils import timezone
import os

def get_folder_name():
    '''
    the folder name will be create at the time the function is called
    it will be created in the blog/static/blog/<date created>
    '''
    dt = timezone.datetime.now()
    folder_name = "blog/static/blog/" + dt.strftime('%Y%m%d')
    if os.path.exists(folder_name) == False:
        os.mkdir(folder_name)

    return folder_name


def handle_uploaded_file(f, file_name):
    '''
    this function will save uploaded file to the folder
    file_name: the title of the blog

    return: 
        file_path: the path of the file (this will be saved in DB)
    '''
    folder_name = get_folder_name()
    file_path = f'{folder_name}/{file_name}.md'

    with open(file_path, 'wb+') as destination:
        body = f.read()
        destination.write(body)
        # body = md_converter.md_convert(body.decode('utf-8'))
        # print(body)

    print(f"[Info] File writen to {file_path}")

    return file_path

def save_md_to_file(md_text, file_name):
    '''
    this function will save the md text to the file
    file_name: the title of the blog

    return: 
        file_path: the path of the file (this will be saved in DB)
    '''
    folder_name = get_folder_name()
    file_path = f'{folder_name}/{file_name}.md'

    with open(file_path, 'wb+') as f:
        f.write(md_text)

    return file_path

def read_md_file(file_path):
    '''
    this will read the md file and return the md text
    '''
    with open(file_path, 'rb') as f:
        md_text = f.read()

    return md_text.decode('utf-8')

def update_md_file(file_path, md_text):
    '''
    this will update the md file
    '''
    with open(file_path, 'wb+') as f:
        f.write(md_text.encode('utf-8'))