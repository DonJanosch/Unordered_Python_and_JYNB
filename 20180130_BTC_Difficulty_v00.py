for difficulty_bits in range(256):
    target = 2 ** (256-difficulty_bits)
    hex_target = '{:08x}'.format(target)
    hex_target = '0'*(64-len(hex_target)) +str(hex_target)
    print('{} bits: {}'.format('0'*(3-len(str(difficulty_bits)))+str(difficulty_bits),hex_target))
