# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.8.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Modification Time of Linked File
#
# I found an issue with Jupytext when attempting to separate the .py file from the .ipynb file using a symbolic link, in that the modification time of the link rather than the file it pointed to was used.  
#
# What python code is needed to fix this up?

# +
import unittest
import subprocess
import os
import datetime
import time
import stat

class TestStuff(unittest.TestCase):
    TESTDIR = "/tmp/test"
    BASEFILE = "/tmp/test/Jupytext.base.py"
    BASEBOOK = "/tmp/test/Jupytext.ipynb"
    LINKFILE = "/tmp/test/Jupytext.link"
    
    @staticmethod
    def formatStatTime(t):
        dt = datetime.datetime.fromtimestamp(t)
        return(dt.strftime("%X %x"))
    
    @classmethod
    def setUpClass(cls):
        '''
        At time 0 we set up a .ipynb file and its associated base.py file
        A symlink is created, pointing at the base
        5 seconds pass
        We touch both the notebook and the link (simulating a Jupytext save)
        '''
        print("initializing environment")
        subprocess.run(["mkdir", TestStuff.TESTDIR])
        subprocess.run(["touch", TestStuff.BASEFILE])
        subprocess.run(["touch", TestStuff.BASEBOOK])
        subprocess.run(["ln", "-s", "-T", TestStuff.BASEFILE, TestStuff.LINKFILE])
        time.sleep(5)
        subprocess.run(["touch", TestStuff.LINKFILE])
        subprocess.run(["touch", TestStuff.BASEBOOK])
        
    @classmethod
    def tearDownClass(cls):
        print("do cleanup")
        subprocess.run(["rm", "-rf", "/tmp/test"])
        
    def test_00_theProblem(self):
        bookStat = os.lstat(TestStuff.BASEBOOK)
        fileStat = os.lstat(TestStuff.BASEFILE)
        linkStat = os.lstat(TestStuff.LINKFILE)
        print(TestStuff.BASEBOOK, TestStuff.formatStatTime(bookStat.st_mtime))
        print(TestStuff.BASEFILE, TestStuff.formatStatTime(fileStat.st_mtime))
        print(TestStuff.LINKFILE, TestStuff.formatStatTime(linkStat.st_mtime))
        
    def test_01_trySoln(self):
        linkStat = os.lstat(TestStuff.LINKFILE)
        print(linkStat)
        if stat.S_ISLNK(linkStat.st_mode):
            print(TestStuff.LINKFILE, "is a link to:")
            realPath = os.path.realpath(TestStuff.LINKFILE)
            realStat = os.lstat(realPath)
            print(realPath, TestStuff.formatStatTime(realStat.st_mtime))

suite = unittest.TestLoader().loadTestsFromTestCase(TestStuff)
unittest.TextTestRunner(verbosity=2).run(suite)

# -

# !ls -l /tmp/test


