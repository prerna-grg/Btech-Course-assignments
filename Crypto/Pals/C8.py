from collections import defaultdict

def repeated_blocks(buffer, block_length=8):
    reps = defaultdict(lambda: -1) # initialise every possible value with -1
    for i in range(0, len(buffer), block_length):
        block = bytes(buffer[i:i + block_length])
        reps[block] += 1 # will count the number of times this particular 16 bytes occurs
    return sum(reps.values())

max_reps = 0
ecb_ciphertext = None

for ciphertext in list(open("8.txt", "r")):
    ciphertext = ciphertext.rstrip()
    ciphertext = bytes(ciphertext, 'utf-8')
    reps = repeated_blocks(ciphertext)
    if reps > max_reps:
        max_reps = reps
        ecb_ciphertext = ciphertext

print("ECB encryption has been done for:")
print(ecb_ciphertext)
