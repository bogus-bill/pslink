import logging as log
import pslink.symap as symap
import pslink

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    symap.add_stopword("class")
    pslink.link("../data")
