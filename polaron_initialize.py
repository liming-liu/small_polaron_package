#!/usr/env/python
'''
To initialize polaron topology.
by Liming Liu
'''

import numpy as np
import matplotlib.pyplot as plt

poscar = open('CONTCAR', 'r')

# parse head info
head = []
for i in range(9):
  head.append(poscar.readline())
scale_para = float(head[1])
latt = np.zeros([3,3])
for i in range(3):
  latt[i] = np.array(head[i+2].split(), dtype=float)
ele = head[5].split()
ele_num = np.array(head[6].split(), dtype=float)
N = ele_num.sum()
head[8]='Cart'+'\n'

# output head
out = open('head', 'w+')
out.write(''.join(head))
out.close()


# parse coordinates and dynamic tags
data = [[ None for x in range(6)] for y in range(int(N))]
for i in range(int(N)):
  data[i] = poscar.readline().split()

# output coordinates and dynamic tags
out = open('data', 'w+')
out.write(str(data))
out.close()

# seperate coordinates from dynamic tags
coor = np.zeros([int(N), 3])
fftt = [[ None for x in range(3)] for y in range(int(N))]
for i in range(int(N)):
  coor[i] = np.array(data[i][0:3], dtype=float)
  fftt[i] = data[i][3:6]
np.savetxt('coor', coor)
out = open('fftt', 'w+')
out.write(str(fftt))
out.close()

# seperate coordinates according elements
sum = 0
for i in range(len(ele)):
  ele_coor = np.zeros([int(ele_num[i]), 3])
  ele_coor = coor[sum: sum+int(ele_num[i]), :]
  sum = sum + int(ele_num[i])
  vars()[ele[i]] = np.dot(ele_coor, latt.T)
#  np.savetxt('%s' % ele[i], ele[i], fmt="%10.5f")

# distorition function
def distortion(center):
  "To enlongate bonds around selected center atom"
  for j in range(O.shape[0]):
    v = O[j] - Ti[center]
    d = np.sqrt(np.dot(v, v.T))
    u = v / d
    if d < 2.1:
      print(j)
      print(O[j])
      O[j] = O[j] + 0.1 * u
      print(O[j])
      print("\n")


# get input from keyboard
center_Ti = input("Input center atom number in array form:\n").split()
for i in center_Ti:
  distortion(int(i)-1)

out = open('POSCAR', 'w+')
out.write(''.join(head))
for i in range(O.shape[0]):
  out.write(' '.join(str(x) for x in O[i]) +' ' + str(' '.join(fftt[i]))+ '\n')
for i in range(Ti.shape[0]):
  out.write(' '.join(str(x) for x in Ti[i]) + ' ' + str(' '.join(fftt[i+O.shape[0]])) + '\n')
for i in range(H_O.shape[0]):
  out.write(' '.join(str(x) for x in H_O[i]) + ' ' + str(' '.join(fftt[i+O.shape[0]+Ti.shape[0]])) + '\n')
for i in range(H_Ti.shape[0]):
  out.write(' '.join(str(x) for x in H_Ti[i]) + ' ' + str(' '.join(fftt[i+O.shape[0]+Ti.shape[0]+H_O.shape[0]])) + '\n')
out.close()
