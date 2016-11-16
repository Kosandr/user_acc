#!/usr/bin/python3

#sudo pip3 install libsass sh
#run from root of project:
#./pywatch.py sass "scsc" "./sass/watchsass.py" -d

import sass, sh

sass_src_path = './sass/'
#sass_out_dir = './sass/output'
sass_out_dir = './static-nginx/autogen'

def get_files(path='.'):
   raw_files = str(sh.ls(path))
   raw_files = raw_files.replace('\t', ' ').replace('\n', ' ')
   files_str = ' '.join(raw_files.split())
   files_lst = files_str.split(' ')
   return files_lst

def is_sass(name):
   return name[-5:] == '.scsc'

file_paths = filter(is_sass, get_files(sass_src_path))

for fname in file_paths:
   fname_no_ext = fname[:-5]
   fname_out = fname_no_ext + '.css'
   with open(sass_src_path + '/' + fname, 'r') as f:
      file_data = f.read()
      out_data = sass.compile(string=file_data)
      with open(sass_out_dir + '/' + fname_out, 'w') as fout:
         fout.write(out_data)

