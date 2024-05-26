import argparse
import multiprocessing

import subprocess

from ._task_interop import *
from .index_calculus import index_calculus
from datetime import datetime

def solver(args):
    algo = index_calculus
    p = (args.a, args.b, args.p)
    then = datetime.now()
    print(then)

    print("Solving a = {}; b = {}; p = {}".format(*p))
    x = algo(*p, parallel=args.parallel)
    print(f"x = {x}")
    assert pow(p[0], x, p[2]) == p[1], "WRONG"

    now = datetime.now()
    print((then-now).microseconds)



def benchmark(args):
    rc = 0
    try:
        rc = subprocess.run("docker --version", shell=True, capture_output=True).returncode
    except FileNotFoundError:
        rc = -1
    finally:
        if rc:
            logging.error("Can not run benchmark: docker not available")
            exit(3)

    algo = index_calculus

    for l in range(args.l, args.L):
        print(f"Solving tasks of length {l}")
        t = start_task()
        set_length(l, t)
        wq, rq = Queue(), Queue()
        w = Writer(wq, t)
        r = Reader(rq, t)
        w.daemon = True
        r.daemon = True
        w.start()
        r.start()

        for tp in range(1, 3):

            # set up a watchdog
            wdq = wd(GET_TASK_DELAY)

            # get the task
            p = rq.get()

            print("Task type {}:\n a = {}; b = {}; p = {}.".format(tp, *p))
            wdq.put(None)  # wd ok

            # solve it
            wdq = wd(GET_SOLUTION_DELAY)

            # we'll measure execution time
            t = time.perf_counter_ns()
            x = algo(*p, parallel=args.parallel)
            t = time.perf_counter_ns() - t

            assert pow(p[0], x, p[2]) == p[1], "WRONG"
            wdq.put(None)  # wd ok
            print(" Solution: x = {}\n".format(x))

            # append stats
            if args.o:
                with open(args.o, "at") as f:
                    f.write("{},{},{},{},{},{},{}\n".format(tp, l, p[0], p[1], p[2], x, t))

            # send the solution
            wq.put(x)

            # exit watchdog
            wdq.put(None)

        # exit writer
        wq.put(None)
        w.join()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "-v", help="verbose (debug) output", action="store_true", dest="verbose"
    )

    argparser.add_argument(
        "--parallel", help="Generate equations in parallel", action="store_true"
    )

    subps = argparser.add_subparsers(dest="command")

    solver_parser = subps.add_parser(
        "solver", help="Run selected algorithm to solve one task"
    )
    solver_parser.add_argument_group("Task parameters")
    solver_parser.add_argument("a", type=int)
    solver_parser.add_argument("b", type=int)
    solver_parser.add_argument("p", type=int)

    benchmark_parser = subps.add_parser(
        "benchmark",
        help='Test the implementation with generated tasks (runs "docker run --rm -i salo1d/nta_cp2_helper:2.0" multiple times under the hood, so requires docker to be available in the execution environment)',
    )
    benchmark_parser.add_argument(
        "-l", help="minimum length", type=int, metavar="l", default=3
    )
    benchmark_parser.add_argument(
        "-L", help="maximum length", type=int, metavar="L", default=30
    )

    benchmark_parser.add_argument("-o", type=str, help="Path to CSV file for stats (will be appended)")

    args = argparser.parse_args()
    # print(args)
    # print(args.o)
    # exit(0)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        match args.command:
            case "solver":
                solver(args)
            case "benchmark":
                benchmark(args)

    except KeyboardInterrupt:
        print("Exiting...")
        map(lambda c: c.kill(), multiprocessing.active_children())
        exit(1)
