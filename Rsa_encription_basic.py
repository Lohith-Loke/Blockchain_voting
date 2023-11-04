import sympy
import random 
import math
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

keys=rsa.generate_private_key(public_exponent=65537, key_size=2048)

p=keys.private_numbers().p
q=keys.private_numbers().q
d=keys.private_numbers().d
e=keys.public_key().public_numbers().e
n=keys.public_key().public_numbers().n

print(f"publick key <{e},{n}>")

print(f"private key  <{d},{n}>")

message = b" hello "
digest=hashes.Hash(hashes.SHA3_256())
digest.update(message)

message_hash = digest.finalize()

message_hash_int = int.from_bytes(message_hash, byteorder='big')

print(q)

print(message_hash_int)

if message_hash_int>n:
    print('{message} must be smaller than n')
    raise Exception('assertion failed', 'Messege < N')
# The numerical representation of the message should be smaller than the modulus (n).
C = pow(message_hash_int,e) % n # encription 
print(f'{message_hash_int} ---> {C}')


original_messege =pow(C,d) % n
print(f'{C}---->{original_messege}')