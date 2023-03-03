

from tools import environmental_setter
import os

es = environmental_setter

returned_dict = es.env_var(["testOne", "testTwo"])
print(f"returned_dict is: {returned_dict}")
print(f"testOne is: {os.environ['testOne']}")
