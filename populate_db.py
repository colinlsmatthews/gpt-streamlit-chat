import sqlite3
import EAGPT_lib as eagpt
import os
import glob

for file in eagpt.get_profile_files():
    print(file)

for name in eagpt.get_filtered_profile_list():
    print(name)

print(eagpt.get_profile_files())
