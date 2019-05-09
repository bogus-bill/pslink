import logging as log
import pslink

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    pslink.link("../data")
