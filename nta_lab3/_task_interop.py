import logging
import re
import subprocess
import threading
import time
import os
import signal
import queue

from time import sleep
from queue import Queue, Empty

TASK = re.compile(r".*^a = (\d+);\nb = (\d+);\np = (\d+)\.", re.MULTILINE | re.DOTALL)
TASK_START_CMD = "docker run --rm -i salo1d/nta_cp2_helper:2.0"

log = logging.getLogger(__name__)  # thread-safe or whatever

def set_length(l, popen: subprocess.Popen):
    popen.stdin.write(str(l).encode() + b"\n")


def read_task(popen: subprocess.Popen):
    buf = ""

    while not (params := parse_task(buf)):
        if popen.poll():
            return None

        buf += popen.stdout.read(1).decode()

    return params


def parse_task(s) -> tuple:
    om = re.match(TASK, s)
    if om is not None:
        return tuple(map(lambda x: int(x), om.groups()))


def start_task():
    popen = subprocess.Popen(
        TASK_START_CMD,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0,
    )

    if popen.poll():
        raise RuntimeError("Could not start task generator: {}".format({popen.returncode}))
    return popen


class Writer(threading.Thread):
    def __init__(
            self, write_queue: Queue, subp: subprocess.Popen, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.subp = subp
        self.wq = write_queue

    def run(self):
        log.debug("Writer started")
        while (w := self.wq.get()) is not None:
            self.subp.stdin.write(str(w).encode() + b"\n")

        log.debug("Writer exited")



class Reader(threading.Thread):
    def __init__(
        self, read_queue: Queue, subp: subprocess.Popen, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.subp = subp
        self.rq = read_queue

    def run(self):
        log.debug("Reader started")
        while p := read_task(self.subp):
            self.rq.put(p)

        log.debug("Reader exited")



GET_TASK_DELAY = 10 * 60
GET_SOLUTION_DELAY = 5 * 60


def watchdog(initial_delay, update_queue: Queue):
    log = logging.getLogger("WATCHDOG")
    log.debug("Watchdog %d starting", threading.get_ident())
    sleep(initial_delay)
    while True:
        try:
            d = update_queue.get_nowait()
            if d:
                log.debug("Resetting watchdog, delay: %d", d)
                sleep(d)
            else:
                log.debug("Watchdog %d exiting", threading.get_ident())
                break
        except Empty:
            log.error("Timed out")
            os.kill(os.getpid(), signal.SIGTERM)  # rude!


# simple one-shot watchdog interface
def wd(delay):
    wdq = Queue()
    wd = threading.Thread(target=watchdog, args=(delay, wdq))
    wd.daemon = True
    wd.start()
    return wdq

