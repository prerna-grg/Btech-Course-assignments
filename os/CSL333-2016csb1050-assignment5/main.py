from simulate import simulate
import numpy as np

vas = int(input("Enter Virtual Address Size in bits: "))
ps = int(input("Enter Page size in KB: "))
rs = int(input("Enter RAM size in MB: "))
ar = int(input("Enter number of addresses to generate: "))
ref_addresses = list(np.random.randint( (2**vas-1) , size=ar))

print("Using FIFO")
print(simulate(vas, ps, rs, 'FIFO', ref_addresses ))
print("Using LFU")
print(simulate(vas, ps, rs, 'LFU', ref_addresses ))
print("Using MFU")
print(simulate(vas, ps, rs, 'MFU', ref_addresses ))
