import argparse
import time

from parser import PinterestParser

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Pinterest parser')
    argparser.add_argument('login', type=str, help='Pinterest account login')
    argparser.add_argument('password', type=str, help='Pinterest account password')
    argparser.add_argument('query', type=str, help='Query', default="Khokhloma")
    argparser.add_argument('output', type=str, help='Name of output file', default="dataset")
    args = argparser.parse_args()

    # sleepers to avoid not found errors
    parser = PinterestParser(args.query)
    time.sleep(5)
    parser.authorize(login=args.login, password=args.password)
    time.sleep(10)

    data = parser.get_data()
    parser.save_data(args.output, data)

    # for i in range(1, 4):
    #     parser.scroll()
    #     time.sleep(5)
    #     data = parser.get_data()
    #     parser.save_data(args.output, data)