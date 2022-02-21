from dotenv import Dotenv
import os


def load_dotenv():
    dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))  # Of course, replace by your correct path
    os.environ.update(dotenv)
