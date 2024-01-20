import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sys
import os
from urllib.parse import unquote



def get_links(url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad requests
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

def save_links_to_file(links, filename='links.txt'):
    with open(filename, 'w') as file:
        for link in links:
            file.write(url + link + '\n')

def download_file_from_url(url, directory='music'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Convert URL-encoded characters to human-readable and replace spaces with hyphens
        filename_to_save = os.path.join(directory, os.path.basename(unquote(url)).replace(' ', '-'))

        if not os.path.exists(filename_to_save):
            with open(filename_to_save, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename_to_save}")
        else:
            print(f"File already exists: {filename_to_save}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

def download_links_from_file(filename, directory='music'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(filename, 'r') as file:
            links = file.readlines()
            ua = UserAgent()
            headers = {'User-Agent': ua.random}

            for link in links:
                link = link.strip()
                try:
                    response = requests.get(link, headers=headers)
                    response.raise_for_status()

                    # Convert URL-encoded characters to human-readable and replace spaces with hyphens
                    filename_to_save = os.path.join(directory, os.path.basename(unquote(link)).replace(' ', '-'))

                    if not os.path.exists(filename_to_save):
                        with open(filename_to_save, 'wb') as file:
                            file.write(response.content)
                        print(f"Downloaded: {filename_to_save}")
                    else:
                        print(f"File already exists: {filename_to_save}")

                except requests.exceptions.RequestException as e:
                    print(f"Error downloading {link}: {e}")

        print(f"Files downloaded from {filename} and saved to the '{directory}' directory.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python " + sys.argv[0] + " <url>")
        sys.exit(1)

    url = sys.argv[1]
    links = get_links(url)

    if links:
        save_links_to_file(links)
        print(f"Links extracted from {url} and saved to links.txt.")
    else:
        print(f"No links found on {url}.")

    download_links_from_file("links.txt")

