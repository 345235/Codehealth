import os


#walk script 
for root, dirs, files in os.walk('.'):
    print("Current directory:", root)
    print("Subdirectories:", dirs)
    print("Files:", files)
    print('----------------')
  




file = open (files, "r")

content = file.read()
print(content)

file.close()
