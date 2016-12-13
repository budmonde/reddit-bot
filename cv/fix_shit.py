import sys
import os
import subprocess


for rnn_size in [128, 256, 512]:
  for n  in [2, 3, 4]:

    dr = "lstm"+"_"+str(rnn_size)+"_"+str(n)
    fl = dr+".out"

    os.system("cat "+dr+"/"+fl+" | grep saving > temp.out")
    with open("temp.out", "r") as f:
      for line in f.readlines():
        name  = line[24:-2]
        cmd = "mv " + name + " " + dr + "/"
        os.system(cmd)
