# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
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

# # Getting Started
#
# So the promise here is that Jupytext allows Jupyter Notebooks to be version controlled.  This is done by saving the input cell contents into some kind of flat file, and merging the output cells from the `.ipynb` file when the notebook is reloaded.
#
# I'm going to pair this notebook with a `light script`.

print("hello Pete")

# When I used the 'pair' command, another file appeared in the directory with a `.py` extension instead.  I can see the input cell information in that file, with the markdown cells hidden behind '#'s.  The python fragments are exposed, so the `.py` file can be conveniently run.

# !python Jupytext\ First.py

# Luckily, shell commands (`!cmd`) are commented out too, otherwise executing it would have resulted in a loop :-) 

# ## Version Control
#
# To achieve this, I'm going to copy the `.py` shadow into my github environment, and then shadow it back by creating a link.
# ```bash
# # mkdir ~/github/versionWithJupytext
# # cp Jupytext\ First.py ~/github/versionWithJupytext
# # rm ./Jupytext\ First.py
# ln -s ~/github/versionWithJupytext/Jupytext\ First.py
# ```
#
# After getting the commands sorted out, I did get a 'resync' prompt at the next autosave, as JupyterLab detected the underlying file had changed since the previous save.

# ### The Git Bits
#
# Off to my atom editor in the `~/github` tree to create the new repository and checkin the file.
#
# Now I'll go edit that "Hello World" fragment above and go see what the diff looks like 

# ## Nice Too
#
# While reading up on this, I came across a couple of packages, 'Black' and 'isort' which force formatting of python code in a specific style and sorting the import statements. Both are aimed at reducing diff sizes.
#

# ## Uh Oh, Found a Problem
#
# When I came to reload the next day, it appears that jupytext read the .py file's modification time from the symbolic link and not what that pointed to.  It was therefore a few hours older (and static) compared with the modification time of the .ipynb file.
#
# I looked at where it gets this info from, but the jupytext code has subclassed a jupyter notebook file object.  Which pushes any code change into jupyter rather than jupytext.
#
# So, I've changed the layout to make the notebook project folder a symbolic link into the github tree, and of course, I'll have to add a .gitignore for the .ipynb.

# ## Comment Out
#
# The following cell has meta data which is supposed to comment it out in either the .ipynb or the .py version.
#
# I can show that by adding
# ```
# { "active" : "ipynb" }
# ```
# to the cell metadata (see advanced Tools in Tools side tab).   
# Then the .py version of the file has the `print()` function all commented out with #.  However, I cannot make the cell unexecutable (<shift><enter>) with "active":"py"

# + active="py" inactive="ipynb"
print("'comment out' with tag")
# -




