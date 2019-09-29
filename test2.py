import sys
import os
print(sys.path[0])
print(sys.argv[0])
print(os.path.dirname(os.path.realpath(sys.executable)))
print(os.path.dirname(os.path.realpath(sys.argv[0])))
base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
b = os.path.join(base_path, "中国"+"\\")
print(b)