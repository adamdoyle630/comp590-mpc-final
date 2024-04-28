import os
import math
from typing import List, Tuple

class MPC_Functions:
    # Biggest prime that fits in 31 bits
    P = 2**31-1

    @classmethod
    def generate_shares(self, value: int, party_count: int) -> List[int]:

        if party_count < 2:
            raise ValueError("Need more than one share")
        
        random_bytes = [os.urandom(math.ceil(math.log2(self.P))) for _ in range(party_count - 1)]
        random_shares = [int.from_bytes(bytes) % self.P for bytes in random_bytes]

        random_shares.append((value - sum(random_shares) + self.P) % self.P)

        return random_shares
    
    @classmethod
    def calculate_sum_of_shares(self, shares: List[int]) -> int:
        if sum(shares) % self.P > 2**31-1000:
            return (self.P - sum(shares) % self.P) * -1
            
        return sum(shares) % self.P
    
    @classmethod
    def calculate_mean(self, server_shares: List[int], count: int) -> float:
        return sum(server_shares) % self.P / count
    
    @classmethod
    def generate_beavers(self, party_count: int) -> Tuple[List[int], List[int], List[int]]:
        
        if party_count < 2:
            raise ValueError("Need more than one share")    

        a_shares = [int.from_bytes(os.urandom(math.ceil(math.log2(self.P))), byteorder='big') % self.P for _ in range(party_count)]
        b_shares = [int.from_bytes(os.urandom(math.ceil(math.log2(self.P))), byteorder='big') % self.P for _ in range(party_count)]

        a = sum(a_shares) % self.P
        b = sum(b_shares) % self.P
        c = a * b % self.P

        c_shares = [int.from_bytes(os.urandom(math.ceil(math.log2(self.P))), byteorder='big') % self.P for _ in range(party_count - 1)]
        c_shares.append((c - sum(c_shares)) % self.P)

        return a_shares, b_shares, c_shares
    
    @classmethod
    def generate_beaver_mask(self, x_share: int, y_share: int, a_share: int, b_share: int) -> Tuple[int, int]:
        e_share = (x_share - a_share) % self.P
        d_share = (y_share - b_share) % self.P

        return (d_share, e_share)
    
    @classmethod
    def beaver_compute(self, x_share: int, y_share: int, c_share: int, d_shares: List[int], e_shares: List[int], first_party=False) -> int:

        e = sum(e_shares) % self.P
        d = sum(d_shares) % self.P

        z = (c_share + x_share * d + y_share * e) % self.P

        if first_party:
            ed = e * d % self.P
            z = (z - ed) % self.P

        return z