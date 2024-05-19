import argparse


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument("a", help="generator of G", type=int)
    argparser.add_argument("b", help="element of G", type=int)
    argparser.add_argument("n", help="order of G", type=int)

    argparser.add_argument(
        "--parallel", help="Generate equations in parallel", action="store_true"
    )
