from server import run_server
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    run_server()


if __name__ == '__main__':
    main()
