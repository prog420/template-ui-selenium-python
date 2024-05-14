from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class EnvVariables:
    """
    Container for sensitive information loaded from .env config files
    """
    pass
