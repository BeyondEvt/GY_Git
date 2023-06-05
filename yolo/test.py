q=[1,1,2]
q.pop(0)
# q.append(3)
# print(q)
# import time
# import numpy as np
# start_0 = time.time()
# for i in range(100000):
#     i += 1
# #
# # now = time.time()
# # end = time.time()
# # if now - start_0 in dict:
# # print(now - start)
# # print(np.floor(now- start))
# dict = {"1.0": [[1,2],[2,3]]}
# if 1.0 in dict:
#     print("1")
# if 1 in dict:
#     print("2")
# if str(1.0) in dict:
#     print("3")
# if str(1) in dict:
#     print("4")
# dict={"0.0":[]}
# count = 0
# from get_standard_data import *
# give_standard(0, 6, 7, 0, 0, 0, np.pi/6, 0.0, 9.0)
# give_standard(6, 0, 0, 0, 0, 0, 2*np.pi/3, 0.0, 9.0)
# give_standard(8, 0, 0, 0, 0, 0, 2*np.pi/3, 0.0, 9.0)
# give_standard(5, 0, 0, 0, 0, 0, np.pi/3, 0.0, 9.0)
# give_standard(7, 0, 0, 0, 0, 0, np.pi/3, 0.0, 9.0)
import time
start = time.time()
i = 0
for i in range(100000):
    i += 1
end = time.time()
print(end-start)