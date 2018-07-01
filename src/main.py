import os
import sys

from subprocess import call

directory = "repos"
if not os.path.exists(directory):
    os.makedirs(directory)

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

repoDir = "Iris"
call(["git", "clone", "https://github.com/jaccek/Iris.git", "repos/" + repoDir])
call(["git", "log", "--pretty=format:\"%h - %an, %ar : %s\""])
call(["rm", "-rf", "repos/" + repoDir])
