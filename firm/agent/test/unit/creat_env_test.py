import os

from agent.creat_env import creat_env

print(creat_env())
print(os.environ["API_KEY"])
print(os.environ["MODEL"])
print(os.environ["api_url"])