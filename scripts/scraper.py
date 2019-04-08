from urllib.request import urlopen
# from bs4 import BeautifulSoup


def main():
    base_url = "http://www.parttarget.com/4730-01-077-4893_4730010774893_NAS516-1A.html/"
    with urlopen(base_url) as f:
        print(f.read())


if __name__ == "__main__":
    main()
