import numpy as np
import parser

good_file = './data/alice_1575256526.bin'
bad_file = './data/alice_1575617692.bin'

good_t, good_p = parser.read(good_file)
bad_t, bad_p = parser.read(bad_file)

print('len(good_t)', len(good_t))
print('good_t[0:100]', good_t[0:50])
print('len(bad_t)', len(bad_t))
print('bad_t[0:100]', bad_t[0:50])