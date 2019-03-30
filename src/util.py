import itertools

def hexdump(data, start_address = 0):
    blocks = [data[i:i + 16] for i in range(0, len(data), 16)]
    for (i, block) in enumerate(blocks):
        print("0x{:06X} | ".format(start_address + i * 16) + " ".join("{:02X}".format(n) for n in block))

