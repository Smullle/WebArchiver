from requests_html import HTMLSession
from tqdm import tqdm
import re
import json
import os


def get_filename(link):
    """
    @param link: url link to normalise
    Will normalise a url by removing and non alphanumeric chars and replace with _
    also remove http:// eg. https://python.org/ => python_org_
    """
    link = re.search("\/\/(.*)$", link)
    link = link.group(1)
    return re.sub('[^0-9a-zA-Z]+', '_', link)

def get_files(url):
    """
    @param url: url of page to archive
    Save main url and embeded urls as .html and produce lookup.json to reconstruct
    urls from filenames.
    """
    session = HTMLSession()
    r = session.get(url)
    embeded_URLs = r.html.absolute_links # type: set
    
    print("Number of files to download: ", len(embeded_URLs) + 1)
    ans = input("Continue Y or N: ")
    
    if ans.lower() == "n":
        return "exit"

    # save main page
    root = get_filename(url)
    os.mkdir(root)
    main_page = open(root + "/" + root + ".html", "w", encoding="utf-8")
    main_page.write(r.text)
    main_page.close()

    # generate url lookup table to to un-sanatise file names
    lookup = {'root': {root + ".html": url}}
    embeded_urls = {}

    os.mkdir(root + "/embeded_urls")

    # save embeded links
    for link in tqdm(embeded_URLs):
        r = session.get(link)
        file_name = get_filename(link)
        file = open(root + "/embeded_urls/" + file_name + ".html", "w", encoding="utf-8")
        file.write(r.text)
        file.close()

        embeded_urls.update({file_name + ".html": link})

    # append embeded urls to main lookup
    lookup.update({'embeded_urls': embeded_urls})

    # save url dict to json
    with open(root + '/lookup.json', 'w') as fp:
        json.dump(lookup, fp, indent=4)

    return "saved " + str(len(embeded_URLs)) + " to ~/" + root


if __name__ == "__main__":
    # url = 'https://python.org/'
    url = input("Enter Web Server eg. https://python.org/: ")
    print(get_files(url))
