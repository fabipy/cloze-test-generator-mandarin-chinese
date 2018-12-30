1) Extract the cwn_dirty.csv from the ZIP archive and place it in the same folder as run.py
2) Move the cwn.py file to your Python3's site-packages folder.
3) pip install the following Python packages: hanziconv, pynlpir & immediately after installing use: pynlpir update
5) Usage: "python run.py text.txt" -> The output text file result text.txt will be written into the same directory

Notes: The source text file needs to contain a Chinese text resource. The text file requires to only have a single line!
The line allows for multiple texts separated by the pipe symbol "|" as the delimiter (See example text files)
