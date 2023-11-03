## Gold
import random
import math
from typing import Tuple
from cryptography.hazmat.primitives.asymmetric import rsa
from sympy import mod_inverse

class Keys:
    def __init__(self,key=None) -> None:
        if not key:
            print("expected privatekey ")
        self.p = key.private_numbers().p
        self.q = key.private_numbers().q
        self.d = key.private_numbers().d
        self.e = key.public_key().public_numbers().e
        self.n = key.public_key().public_numbers().n

    def get_pub(self) ->  Tuple[int,int]:
        return (self.e, self.n)

    def get_prv(self) -> int:
        return self.d
    
    def sign(self,m_1) -> int:
        return pow(m_1, self.d, self.n)
    
def blind(m, pub_k) -> Tuple[int,int]:
    ''' throws value error if m < n'''
    e_a, n_a = pub_k
    if m >= n_a:
        raise ValueError('Message must be smaller than n')


    while True:
        r = random.randint(2, n_a - 1)
        if math.gcd(r, n_a) == 1:
            break
    r_1 = mod_inverse(r, n_a)

    m_1 = (m * pow(r, e_a, n_a)) % n_a
    
    return m_1, r_1

def sign(m_1, prv_k, pub_k):
    d = prv_k
    _,n_a=pub_k
    return pow(m_1, d, n_a)

def verify(m, sign, pub_k):
    e_a, n_a = pub_k
    if m == (pow(sign, e_a, n_a))%n_a:
        return True
    else:
        return False

if __name__=="__main__":
    m = 100
    bank_keys = Keys()

    # Generate blind message from the original message
    m_1, r_1 = blind(
        m, 
        bank_keys.get_pub()
    )

    print(m_1)
    # Pass blind message for signing by the bank
    sign_b_m_1 = bank_keys.sign(m_1)

    # Verify the blind signature
    x=verify(
        m=m_1,
        sign=sign_b_m_1,
        pub_k=bank_keys.get_pub()
    )
    if x:
        print("m_1 signed by bank keys")
    else:
        print("blind messege signature verification failure ")

    sign_m = (r_1*sign_b_m_1)%bank_keys.n

    x=verify(
        m=m,
        sign=sign_m,
        pub_k=bank_keys.get_pub()
    )

    if x :
        print("recovered sighn of bank on m")
    else:
        print('sign recovery failed ')
