# pylint: disable=c-extension-no-member,consider-using-with
import asyncio
import atexit
import json
import os
import pickle
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import List, Union

import plotly.graph_objects as go
import psutil
import requests
from websockets.client import connect

QT_PATH = Path(__file__).parent.resolve()
BACKEND_RUNNING = False
IS_TERMINAL = "terminal.py" in sys.argv[0]


class PlotsBackendError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self):
        self.message = "We've encountered an error while trying to start the Plots backend. Please try again."
        super().__init__(self.message)


def get_qt_backend_pid():
    """Returns the pid of the qt_backend process"""
    try:
        qt_backend_pid = pickle.load(open(QT_PATH / "assets/qt_backend_pid", "rb"))
    except FileNotFoundError:
        qt_backend_pid = None

    return qt_backend_pid


async def get_qt_backend_socket(error: bool = False):
    try:
        socket_port = pickle.load(open(QT_PATH / "assets/qt_socket", "rb"))
        if error:
            raise FileNotFoundError  # if there's an error, we need to run the qt_backend again
    except FileNotFoundError:
        # if the socket file is not found, the qt_backend is probably not running
        # or the socket file was deleted by the user
        # in both cases, we need to check if there's a qt_backend_pid file and try to kill the process
        # and then run the qt_backend again
        try:
            await asyncio.sleep(2)
            qt_backend_pid = get_qt_backend_pid()
            process = psutil.Process(qt_backend_pid)
            if process.is_running():
                process.kill()
            global BACKEND_RUNNING  # pylint: disable=global-statement
            BACKEND_RUNNING = False
            run_qt_backend()
            socket_port = pickle.load(open(QT_PATH / "assets/qt_socket", "rb"))
        except FileNotFoundError:
            socket_port = await get_qt_backend_socket()
        except psutil.NoSuchProcess as proc:
            raise PlotsBackendError from proc

    return socket_port


def run_qt_backend():
    """Runs the qt_backend.py script in a subprocess"""

    if BACKEND_RUNNING:
        return True

    qt_backend_pid = get_qt_backend_pid()

    def is_running(process_name):
        """Checks if the qt_backend is running and if the process is the same as qt_backend_pid"""
        try:
            process = psutil.Process(qt_backend_pid)
            print(
                f"Checking if running = {len(process.cmdline()) > 1 and process_name in process.cmdline()}"
            )
            if len(process.cmdline()) > 1 and process_name in process.cmdline():
                print("qt_backend is running")
                if process.is_running():
                    global BACKEND_RUNNING  # pylint: disable=global-statement
                    BACKEND_RUNNING = True
                    return True
        except psutil.NoSuchProcess:
            pass

        return False

    if not is_running(str(QT_PATH / "app.py")):
        # if the qt_backend is not running, we run it in a subprocess
        kwargs = {"stdin": subprocess.PIPE}

        # if the DEBUG env variable is set to True
        # we don't want to hide the output of the subprocess
        if os.environ.get("DEBUG", False):
            kwargs = {}

        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["preexec_fn"] = os.setsid  # pylint: disable=no-member

        subprocess.Popen([sys.executable, str(QT_PATH / "app.py")], **kwargs)
        return True

    return False


class QtBackend:
    def __new__(cls):
        # We only want to create one instance of the class
        # so we use the __new__ method to check if the instance already exists
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, max_retries: int = 5):
        self.socket_port: Union[int, None] = None
        self.figures: List[go.Figure] = []
        self.dashboard: List[str] = []
        self.thread = None
        self.init_engine = ["init"]
        self.max_retries = max_retries

    async def connect(self):
        """Connects to qt_backend and maintains the connection until the terminal is closed"""
        try:
            run_qt_backend()
            global BACKEND_RUNNING  # pylint: disable=global-statement
            BACKEND_RUNNING = True
            self.socket_port = await get_qt_backend_socket()

            async with connect(
                f"ws://localhost:{self.socket_port}",
                open_timeout=6,
                timeout=1,
                ssl=None,
            ) as websocket:
                if self.init_engine:
                    # sends init message to qt_backend to initialize the engine
                    # this is only done once, and makes sure the first plot doesn't
                    # have to wait for the engine to be initialized
                    for msg in self.init_engine:
                        await websocket.send(msg)
                    self.init_engine = []

                while True:
                    if self.figures:
                        data = self.figures.pop(0)
                        # Just in case the user still had windows open from a previous
                        # terminal session and closed them after starting a new session
                        # [ at terminal close we set backend to quit after last window is closed ]
                        # we append the fig json to the init_engine so that if the send fails, the engine will
                        # still have the fig data to display at the next connection
                        self.init_engine.append(data.to_json())

                        await websocket.send(data.to_json())
                        self.init_engine = ["init"]

                    if self.dashboard:
                        data = self.dashboard.pop(0)
                        await websocket.send(json.dumps({"dashboard": data}))

                    await asyncio.sleep(0.1)

        except Exception as exc:
            if self.max_retries == 0:
                raise PlotsBackendError from exc

            self.max_retries -= 1
            print("Connection to qt_backend failed. Trying again...")
            await get_qt_backend_socket()
            BACKEND_RUNNING = False
            await self.connect()

    def start(self):
        """Connect to qt_backend in a separate thread."""
        if self.max_retries == 0:
            raise PlotsBackendError

        thread = threading.Thread(
            target=asyncio.run, args=(self.connect(),), daemon=True
        )
        self.thread = thread
        thread.start()

        # We check to see if initialize was called from the OpenBB terminal
        # or from a script. If it was called from a script, we need to wait
        # in case the user is using the sdk in a script called from the command line
        # e.g. `python custom_script.py`
        if not IS_TERMINAL:
            asyncio.run(asyncio.sleep(8))

    def send_fig(self, fig: go.Figure):
        """Send figure to qt_backend."""
        self.check_backend()
        self.figures.append(fig)

    def send_dashboard(self, dashboard: Union[Path, str]):
        """Send dashboard to qt_backend."""
        self.check_backend()
        self.dashboard.append(str(dashboard))

    def check_backend(self):
        """Check if the backend is running."""
        if not BACKEND_RUNNING or not self.thread.is_alive():
            self.start()

    def close(self):
        """Close the connection."""
        self.thread.join()


# To avoid having plotly.js in the repo, we download it if it's not present
if not (Path(__file__).parent.resolve() / "assets/plotly.js").exists():
    download = requests.get("https://cdn.plot.ly/plotly-2.16.1.min.js", stream=True)
    with open(Path(__file__).parent.resolve() / "assets/plotly.js", "wb") as f:
        for chunk in download.iter_content(chunk_size=1024):
            f.write(chunk)


def closeonlastwindowclosed(is_terminal: bool):
    socket_port = pickle.load(open(QT_PATH / "assets/qt_socket", "rb"))
    message = "isterminal" if is_terminal else "isatty"

    async def close():
        async with connect(f"ws://localhost:{socket_port}") as websocket:
            await websocket.send(message)
            sys.exit(1)

    asyncio.run(close())


def setCloseonLastWindowClosed():
    """Sends a message to qt_backend when the terminal is closed"""
    if BACKEND_RUNNING:
        try:
            if not IS_TERMINAL:
                # We make sure the qt_backend has time to start up
                # if the user is using the sdk in a script called from the command line
                time.sleep(2)

            # We run the closeonlastwindowclosed function in a subprocess
            # since we can't create a new future after interpreter shutdown
            subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    "import asyncio;from backend import closeonlastwindowclosed; "
                    f"closeonlastwindowclosed({IS_TERMINAL})",
                ],
                shell=True,
                cwd=QT_PATH,
            )
        except FileNotFoundError:
            pass


QT_BACKEND = QtBackend()

atexit.register(setCloseonLastWindowClosed)