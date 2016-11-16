#!/usr/bin/python3

#sudo pip3 install libsass sh
#run from root of project:
#./pywatch.py jsx "jsx" "./jsx/watchjxs.py %s" -p
#./pywatch.py jsx "jsx" "./jsx/watchjsx.py" -d

import sass, sh, os, os.path

src_path = './jsx/'
#out_dir = './sass/output'
out_dir = './static-nginx/autogen'

def get_files(path='.'):
   raw_files = str(sh.ls(path))
   raw_files = raw_files.replace('\t', ' ').replace('\n', ' ')
   files_str = ' '.join(raw_files.split())
   files_lst = files_str.split(' ')
   return files_lst

def is_jsx(name):
   return name[-4:] == '.jsx'

file_paths = None
import sys
if len(sys.argv) == 1:
   file_paths = filter(is_jsx, get_files(src_path))
else:
   file_paths = [sys.argv[1]]

def compile_fname(fname):
   fname_no_ext = fname[:-4]
   fname_out = fname_no_ext + '.js'
   #with open(sass_src_path + '/' + fname, 'r') as f:
   #   file_data = f.read()
   #   out_data = sass.compile(string=file_data)
   #   with open(sass_out_dir + '/' + fname_out, 'w') as fout:
   #      fout.write(out_data)
   in_path = fname #src_path + '/' + fname ##THE OLD VERSION IS FOW WHEN WE DID THE ALL TOGETHER
   if len(sys.argv) == 1:
      in_path = src_path + '/' + fname

   out_path_base = out_dir + '/' + os.path.basename(fname)[:-4]
   out_path = out_path_base + '.js'
   if len(sys.argv) == 1:
      out_path = out_dir + '/' + fname_out

   os.system('rm %s %s.bundle.js' % (out_path, out_path_base))

   cmd = 'babel --plugins transform-react-jsx'
   cmd = '%s %s >%s' % (cmd, in_path, out_path)

   #print('======watchjsx.py: compiling %s to %s (cmd: %s)' % (in_path, out_path, cmd))
   print('======watchjsx.py: compiling %s' % (in_path, ))
   #print('======watchjsx.py: compiling %s' % (cmd, ))

   os.system(cmd)
   print('======watchjsx.py: done compiling %s. now browserifying' % out_path)

   ###this works, but doesn't convert jscloak to es2015
   #brows_cmd = 'browserify %s -o %s.bundle.js' % (out_path, out_path_base)
   #print('======watchjsx.py: brows_cmd is ' + brows_cmd)
   #os.system(brows_cmd)

   ###this should be good, but it's not
   #brows_cmd = 'browserify %s | babel >%s.bundle.js' % (out_path, out_path_base)
   #print('======watchjsx.py: brows_cmd is ' + brows_cmd)
   #os.system(brows_cmd)

   brows_cmd = 'browserify %s -o %s.bundle.tmp.js' % (out_path, out_path_base)
   print('======watchjsx.py: ', brows_cmd)
   os.system(brows_cmd)

   brows_cmd = 'babel %s.bundle.tmp.js >%s.bundle.js' % (out_path_base, out_path_base)
   print('======watchjsx.py: ', brows_cmd)
   os.system(brows_cmd)


#import _thread
import threading

threads = []
for fname in file_paths:
   #compile_fname(fname)
   #t = _thread.start_new_thread(compile_fname, (fname,))
   t = threading.Thread(target=compile_fname, args=(fname,))
   t.start()
   threads.append(t)

for thread in threads:
   thread.join()

#import sys
#print(sys.argv)

