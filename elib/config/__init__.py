import os
from ..helpers import read_config

user_config = read_config()

library_path = os.path.abspath(os.path.expanduser(user_config['library_path']))