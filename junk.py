def foo(x):
    bitSize = x.bit_length()-1
    print(bitSize)
    return (x & ((1<<bitSize) - 1)) - (x & (1<<bitSize))

print(bin(23))
#print(foo(bin(23)))
#print(foo(0b11111111111111111))
