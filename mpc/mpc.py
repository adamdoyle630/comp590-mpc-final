import os
import math
from typing import List, Self, Tuple

class MPC_Functions:
    # Biggest prime that fits in 31 bits
    P = 2**31-1

    @classmethod
    def generate_shares(self: Self, value: int, party_count: int) -> List[int]:

        if party_count < 2:
            raise ValueError("Need more than one share")
        
        random_bytes = [os.urandom(math.ceil(math.log2(self.P))) for _ in range(party_count - 1)]
        random_shares = [int.from_bytes(bytes) % self.P for bytes in random_bytes]

        random_shares.append((value - sum(random_shares) + self.P) % self.P)

        return random_shares
    
    @classmethod
    def calculate_sum_of_shares(self: Self, shares: List[int]) -> int:
        # TODO: Is there a better way to handle negative values (that become overflow)
        if sum(shares) % self.P > 2**30-1:
            return (self.P - sum(shares) % self.P) * -1
            
        return sum(shares) % self.P
    
    @classmethod
    def calculate_mean(self: Self, server_shares: List[int], count: int) -> float:
        return sum(server_shares) % self.P / count
    
    @classmethod
    def generate_beavers(self: Self, party_count: int) -> Tuple[List[int], List[int], List[int]]:
        
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
    def generate_beaver_mask(self: Self, x_share: int, y_share: int, a_share: int, b_share: int) -> Tuple[int, int]:
        e_share = (x_share - a_share) % self.P
        d_share = (y_share - b_share) % self.P

        return (d_share, e_share)
    
    @classmethod
    def beaver_compute(self: Self, x_share: int, y_share: int, a_shares: int, b_shares: int, c_share: int, d_shares: List[int], e_shares: List[int], first_party=False) -> int:
        e_share = (x_share - a_shares) % self.P
        d_share = (y_share - b_shares) % self.P

        e = (e_share + sum(e_shares)) % self.P
        d = (d_share + sum(d_shares)) % self.P

        z = (c_share + x_share * d + y_share * e) % self.P

        if first_party:
            ed = e * d % self.P
            z = (z - ed) % self.P

        return z
    

s1 = MPC_Functions.generate_shares(10, 4)
s2 = MPC_Functions.generate_shares(20, 4)
s3 = MPC_Functions.generate_shares(30, 4)
s4 = MPC_Functions.generate_shares(100, 4)
s5 = MPC_Functions.generate_shares(50, 4)
s6 = MPC_Functions.generate_shares(2, 4)

message_shares = [s1, s2, s3, s4, s5, s6]
server1 = []
server2 = []
server3 = []
server4 = []

for message in message_shares:
    server1.append(message[0])
    server2.append(message[1])
    server3.append(message[2])
    server4.append(message[3])

server1_sum = MPC_Functions.calculate_sum_of_shares(server1)
server2_sum = MPC_Functions.calculate_sum_of_shares(server2)
server3_sum = MPC_Functions.calculate_sum_of_shares(server3)
server4_sum = MPC_Functions.calculate_sum_of_shares(server4)

mean = int(MPC_Functions.calculate_mean([server1_sum, server2_sum, server3_sum, server4_sum], len(message_shares)))

print(f"Mean: {mean}")

a_shares, b_shares, c_shares = MPC_Functions.generate_beavers(4)

servers = [server1, server2, server3, server4]
server1_zshares = []
server2_zshares = []
server3_zshares = []
server4_zshares = []
zshares = [server1_zshares, server2_zshares, server3_zshares, server4_zshares]

for i in range(len(server1)):
    d_shares = []
    e_shares = []

    for index, server in enumerate(servers):
        if index == 0:
            d_share, e_share = MPC_Functions.generate_beaver_mask(server[i] - mean, server[i] - mean, a_shares[index], b_shares[index])
            d_shares.append(d_share)
            e_shares.append(e_share)
            continue

        d_share, e_share = MPC_Functions.generate_beaver_mask(server[i], server[i], a_shares[index], b_shares[index])
        d_shares.append(d_share)
        e_shares.append(e_share)

    z_shares = []

    for index, server in enumerate(servers):
        curr_d_shares = d_shares[:index] + d_shares[index + 1:]
        curr_e_shares = e_shares[:index] + e_shares[index + 1:]

        if index == 0:
            z = MPC_Functions.beaver_compute(server[i] - mean, server[i] - mean, a_shares[index], b_shares[index], c_shares[index], curr_d_shares, curr_e_shares, True)
            z_shares.append(z)
            continue

        z = MPC_Functions.beaver_compute(server[i], server[i], a_shares[index], b_shares[index], c_shares[index], curr_d_shares, curr_e_shares)
        z_shares.append(z)

    for index, server in enumerate(zshares):
        server.append(z_shares[index])

server_sums = []
for share in zshares:
    server_sums.append(MPC_Functions.calculate_sum_of_shares(share))

print(math.sqrt(MPC_Functions.calculate_sum_of_shares(server_sums)/len(message_shares)))

# standard_devation = math.sqrt(sum(squared_differences)/len(message_shares))
# print(f"Standard Deviation: {math.sqrt(sum(squared_differences)/len(message_shares))}")

# TODO: Is this way of calculating z-score secure
# z_scores = []

# for i in range(len(server1)):
#     shares = []
#     for server in servers:
#         shares.append(server[i])

#     shares[0] = (shares[0] - mean) % MPC_Functions.P

#     z_scores.append(MPC_Functions.calculate_sum_of_shares(shares) / standard_devation)

# print(z_scores)
# print(sum(z_scores))