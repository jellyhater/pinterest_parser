import argparse
import time

from parser import PinterestParser

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Pinterest parser')
    argparser.add_argument('login', type=str, help='Pinterest account login')
    argparser.add_argument('password', type=str, help='Pinterest account password')
    argparser.add_argument('query', type=str, help='Query', default="Khokhloma")
    args = argparser.parse_args()

    # sleepers to avoid not found errors
    parser = PinterestParser(args.query)
    time.sleep(5)
    parser.authorize(login=args.login, password=args.password)
    time.sleep(5)

    for i in range(3):
        parser.scroll()
        time.sleep(5)
        data = parser.get_data()
        parser.save_data(f"dataset_{i}", data)