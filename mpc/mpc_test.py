from mpc import MPC_Functions
import math

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

print("Server 1 Sum:", server1_sum)
print("Server 2 Sum:", server2_sum)
print("Server 3 Sum:", server3_sum)
print("Server 4 Sum:", server4_sum)

print("Mean: ", MPC_Functions.calculate_mean([server1_sum, server2_sum, server3_sum, server4_sum], len(message_shares)))


# a_shares, b_shares, c_shares = MPC_Functions.generate_beavers(3)
# a = sum(a_shares) % MPC_Functions.P
# b = sum(b_shares) % MPC_Functions.P
# c = sum(c_shares) % MPC_Functions.P

# print(f"a: {a}, b: {b}, c: {c}")
# print(f"a * b = {a * b % MPC_Functions.P}")

# x_shares = MPC_Functions.generate_shares(10, 3)
# y_shares = MPC_Functions.generate_shares(10, 3)

# # x_shares[0] -= 1
# # y_shares[0] -= 1

# d0_share, e0_share = MPC_Functions.generate_beaver_mask(x_shares[0], y_shares[0], a_shares[0], b_shares[0])
# d1_share, e1_share = MPC_Functions.generate_beaver_mask(x_shares[1], y_shares[1], a_shares[1], b_shares[1])
# d2_share, e2_share = MPC_Functions.generate_beaver_mask(x_shares[2], y_shares[2], a_shares[2], b_shares[2])

# z0 = MPC_Functions.beaver_compute(x_shares[0], y_shares[0], a_shares[0], b_shares[0], c_shares[0], [d1_share, d2_share], [e1_share, e2_share], True)
# z1 = MPC_Functions.beaver_compute(x_shares[1], y_shares[1], a_shares[1], b_shares[1], c_shares[1], [d0_share, d2_share], [e0_share, e2_share])
# z2 = MPC_Functions.beaver_compute(x_shares[1], y_shares[1], a_shares[1], b_shares[1], c_shares[1], [d0_share, d1_share], [e0_share, e1_share])

# print(MPC_Functions.calculate_sum_of_shares([z0, z1, z2]))


# a_shares, b_shares, c_shares = MPC_Functions.generate_beavers(3)

# x = MPC_Functions.generate_shares(10, 3)
# y = MPC_Functions.generate_shares(20, 3)

# message_shares = [x, y]
# server1 = []
# server2 = []
# server3 = []

# for message in message_shares:
#     server1.append(message[0])
#     server2.append(message[1])
#     server3.append(message[2])

# print(x, y)
# print(server1, server2, server3)

# d_shares = []
# e_shares = []

# servers = [server1, server2, server3]

# for index, server in enumerate(servers):
#     if index == 0:
#         d_share, e_share = MPC_Functions.generate_beaver_mask(server[0] - 2, server[1] - 2, a_shares[index], b_shares[index])
#         d_shares.append(d_share)
#         e_shares.append(e_share)
#         continue

#     d_share, e_share = MPC_Functions.generate_beaver_mask(server[0], server[1], a_shares[index], b_shares[index])
#     d_shares.append(d_share)
#     e_shares.append(e_share)

# z_shares = []

# for index, server in enumerate(servers):
#     curr_d_shares = d_shares[:index] + d_shares[index + 1:]
#     curr_e_shares = e_shares[:index] + e_shares[index + 1:]

#     if index == 0:
#         z = MPC_Functions.beaver_compute(server[0] - 2, server[1] - 2, a_shares[index], b_shares[index], c_shares[index], curr_d_shares, curr_e_shares, True)
#         z_shares.append(z)
#         continue

#     z = MPC_Functions.beaver_compute(server[0], server[1], a_shares[index], b_shares[index], c_shares[index], curr_d_shares, curr_e_shares)
#     z_shares.append(z)

# print(MPC_Functions.calculate_sum_of_shares(z_shares))



# s1 = MPC_Functions.generate_shares(10, 4)
# s2 = MPC_Functions.generate_shares(20, 4)
# s3 = MPC_Functions.generate_shares(30, 4)
# s4 = MPC_Functions.generate_shares(100, 4)
# s5 = MPC_Functions.generate_shares(50, 4)
# s6 = MPC_Functions.generate_shares(2, 4)

# message_shares = [s1, s2, s3, s4, s5, s6]
# server1 = []
# server2 = []
# server3 = []
# server4 = []

# for message in message_shares:
#     server1.append(message[0])
#     server2.append(message[1])
#     server3.append(message[2])
#     server4.append(message[3])

# server1_sum = MPC_Functions.calculate_sum_of_shares(server1)
# server2_sum = MPC_Functions.calculate_sum_of_shares(server2)
# server3_sum = MPC_Functions.calculate_sum_of_shares(server3)
# server4_sum = MPC_Functions.calculate_sum_of_shares(server4)

# mean = int(MPC_Functions.calculate_mean([server1_sum, server2_sum, server3_sum, server4_sum], len(message_shares)))

# print(f"Mean: {mean}")

# a_shares, b_shares, c_shares = MPC_Functions.generate_beavers(4)

# servers = [server1, server2, server3, server4]
# squared_differences = []

# for i in range(len(server1)):
#     d_shares = []
#     e_shares = []

#     for index, server in enumerate(servers):
#         if index == 0:
#             d_share, e_share = MPC_Functions.generate_beaver_mask(server[i] - mean, server[i] - mean, a_shares[index], b_shares[index])
#             d_shares.append(d_share)
#             e_shares.append(e_share)
#             continue

#         d_share, e_share = MPC_Functions.generate_beaver_mask(server[i], server[i], a_shares[index], b_shares[index])
#         d_shares.append(d_share)
#         e_shares.append(e_share)

#     z_shares = []

#     for index, server in enumerate(servers):
#         curr_d_shares = d_shares[:index] + d_shares[index + 1:]
#         curr_e_shares = e_shares[:index] + e_shares[index + 1:]

#         if index == 0:
#             z = MPC_Functions.beaver_compute(server[i] - mean, server[i] - mean, a_shares[index], b_shares[index], c_shares[index], curr_d_shares, curr_e_shares, True)
#             z_shares.append(z)
#             continue

#         z = MPC_Functions.beaver_compute(server[i], server[i], a_shares[index], b_shares[index], c_shares[index], curr_d_shares, curr_e_shares)
#         z_shares.append(z)

#     squared_differences.append(MPC_Functions.calculate_sum_of_shares(z_shares))

# print(squared_differences)
# print(f"Standard Deviation: {math.sqrt(sum(squared_differences)/len(message_shares))}")