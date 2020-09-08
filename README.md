# WebArchiver

Will download HTML of URL provided at runtime, will also parse html extract embeded links and download associated html.

  - requests library used to GET HTML and parse embeded links
  - Will normalise a url by removing and non alphanumeric chars and replace with _ also remove http:// eg. https://python.org/ => python_org_
  - Save main url and embeded urls as .html and produce lookup.json to reconstruct urls from normalised filenames.
  
![](images/screen1 (1).png?raw=true)
![](images/screen2 (1).png?raw=true)
![](images/screen4.png?raw=true)
