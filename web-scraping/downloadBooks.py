from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from os.path import join
from os import makedirs
import re


def url_download_for_each_book(url):

    html_data, url_download = [], []
    with urlopen(url) as f:
        html_data.append(f.read().decode('utf-8'))

    for line in html_data[0].split():
        if line.startswith('href="https://knigogo.net/knigi/') and line.endswith('/#lib_book_download"'):
            line = line.replace('href="', '').replace('"', '')
            url_download.append(line)
    return url_download


def get_book_name_or_year(url, key):
    response = requests.get(url)
        
    soup = BeautifulSoup(response.text, "html.parser")
    li_elem = soup.find("li", string=lambda text: text and key in text)
    
    # Depend on key return book name or year 
    return li_elem.text.split(":")[1].strip()



def  get_author_or_genre(url, key):
    response = requests.get(url)
    html_text = response.text
  
    author_or_genre = re.findall(r''+str(key)+'\s*(.*?)</li>', html_text)
 
    if author_or_genre:
        author_or_genre = [genre.strip() for genre in author_or_genre[0].split(',')]
    else:
        print(url)
        print("No result found.")

    filtered_data = []
    for item in author_or_genre:
        soup = BeautifulSoup(item, 'html.parser')
        if soup.find('a'):
            text = soup.a.text
            filtered_data.append(text)
    
    return filtered_data



def url_text_download_for_each_book(url_download):
    file_text, url_text, allYears = [], [], []
    dicAllData={}
    allValues=[]
    for url in url_download:
#=====================================================================
        # get book name
        allValues.append(get_book_name_or_year(url, "Название:"))
    
        # get author
        allValues.append(get_author_or_genre(url, "Писатель:"))
        
        # get year
        allValues.append(get_book_name_or_year(url, "Год:"))      
            
        # get genre
        allValues.append(get_author_or_genre(url, "Жанры:"))  
      
        #allValue.append(filtered_data)
        #print(allValue)
        #print(filtered_data)
        dicAllData[url]= allValues
       
    
#=====================================================================


        with urlopen(url) as f:
            file_text.append(f.read().decode('utf-8'))
        #print(file_text)
    for i in range(len(file_text)):
        for line in file_text[i].split():
            if line.startswith('href="https://knigogo.net/wp-content/uploads/') and line.endswith('.txt"'):
                line = line.replace('href="', '').replace('"', '')
                url_text.append(line)

#=====================================================================
    #print(dicAllYears)
#=====================================================================
  
    return url_text,dicAllData

# download html and return parsed doc or None on error
def download_url(urlpath):
    try:
        # open a connection to the server
        with urlopen(urlpath, timeout=3) as connection:
            # read the contents of the html doc
            return connection.read()
    except:
        # bad url, socket timeout, http forbidden, etc.
        return None

# download one book from project gutenberg
def download_book(url, book_id, save_path):
    # download the content
    data = download_url(url)
    if data is None:
        return f'Failed to download {url}'
    # create local path
    save_file = join(save_path, f'{book_id}.txt')
    # save book to file
    with open(save_file, 'wb') as file:
        file.write(data)
    return f'Saved {save_file}'

def download_all_books(url_text):
    for url in url_text:
        book_id = url.split('/')[-1].split('.')[0]
        download_book(url, book_id, save_path)

        

if __name__ == '__main__':
    url = 'https://knigogo.net/besplatnye-knigi/page/2/'
    save_path = 'test'
    # create the save directory if needed
    makedirs(save_path, exist_ok=True)
    # get a url of books that you can download
    url_download = url_download_for_each_book(url)
    # get a url of text files you can download
    oneBook=[]
    oneBook.append(url_download[3])
    url_text,x = url_text_download_for_each_book(oneBook)
    print(x)
    download_all_books(url_text)