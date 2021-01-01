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
    LINKLINK = "/tmp/test/Jupytext.link.link"

    @staticmethod
    def formatStatTime(t):
        dt = datetime.datetime.fromtimestamp(t)
        return dt.strftime("%X %x")

    @classmethod
    def setUpClass(cls):
        """
        At time 0 we set up a .ipynb file and its associated base.py file
        A symlink is created, pointing at the base
        5 seconds pass
        We touch both the notebook and the link (simulating a Jupytext save)
        """
        print("initializing environment")
        subprocess.run(["mkdir", TestStuff.TESTDIR])
        subprocess.run(["touch", TestStuff.BASEFILE])
        subprocess.run(["touch", TestStuff.BASEBOOK])
        subprocess.run(["ln", "-s", "-T", TestStuff.BASEFILE, TestStuff.LINKFILE])
        subprocess.run(["ln", "-s", "-T", TestStuff.LINKFILE, TestStuff.LINKLINK])
        time.sleep(5)
        subprocess.run(["touch", TestStuff.LINKFILE])
        subprocess.run(["touch", TestStuff.BASEBOOK])
        cp = subprocess.run(
            ["ls", "-l", "--time-style=full-iso", TestStuff.TESTDIR],
            capture_output=True,
            text=True,
        )
        print(cp.stdout)

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

        # we check that mtimes are within 3 seconds
        self.assertAlmostEqual(bookStat.st_mtime, fileStat.st_mtime, delta=3)
        self.assertAlmostEqual(bookStat.st_mtime, linkStat.st_mtime, delta=3)

    def test_01_trySoln(self):
        bookStat = os.lstat(TestStuff.BASEBOOK)
        linkStat = os.lstat(TestStuff.LINKFILE)
        print(linkStat)
        if stat.S_ISLNK(linkStat.st_mode):
            print(TestStuff.LINKFILE, "is a link to:")
            realPath = os.path.realpath(TestStuff.LINKFILE)
            realStat = os.lstat(realPath)
            print(realPath, TestStuff.formatStatTime(realStat.st_mtime))
        self.assertAlmostEqual(bookStat.st_mtime, realStat.st_mtime, delta=3)

    @staticmethod
    def getStat(fn):
        """
        Read the stats of the named file, but, if it happens to be a link
        resolve the link, and return those stats intead
        """
        fileStat = os.lstat(fn)
        iterGuard = 0
        while stat.S_ISLNK(fileStat.st_mode) and iterGuard < 5:
            realPath = os.path.realpath(fn)
            print(f"{iterGuard} - resolving: {realPath}")
            fileStat = os.lstat(realPath)
            iterGuard += 1
            if iterGuard == 4:
                raise LoopException()
        return fileStat

    def test_02_encapSoln(self):
        bookStat = os.lstat(TestStuff.BASEBOOK)
        testStat = TestStuff.getStat(TestStuff.BASEBOOK)
        # the retrieved mtime for the notebook should be identical
        self.assertEqual(bookStat.st_mtime, testStat.st_mtime)

        # the retrieved mtime for the notebook and scriptfile should be close
        testStat = TestStuff.getStat(TestStuff.BASEFILE)
        self.assertAlmostEqual(bookStat.st_mtime, testStat.st_mtime, delta=3)

        # the mtimes for notebook, and scriptfile link should be close
        testStat = TestStuff.getStat(TestStuff.LINKFILE)
        self.assertAlmostEqual(bookStat.st_mtime, testStat.st_mtime, delta=3)

        # and we even expect to work with links to links
        testStat = TestStuff.getStat(TestStuff.LINKLINK)
        self.assertAlmostEqual(bookStat.st_mtime, testStat.st_mtime, delta=3)


suite = unittest.TestLoader().loadTestsFromTestCase(TestStuff)
unittest.TextTestRunner(verbosity=2).run(suite)

# -

# !ls -l /tmp/test
