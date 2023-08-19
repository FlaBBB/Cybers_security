from collections import defaultdict

log_file_path1 = 'Romeo.txt'
log_file_path2 = 'Dulliet.txt'

suspicious_ip = defaultdict(list)

# with open(log_file_path1, 'r') as log_file1, open(log_file_path2, 'r') as log_file2:
#     for line1, line2 in zip(log_file1, log_file2):
#         fields1 = line1.split()
#         fields2 = line2.split()

#         print(fields1)
#         if fields1[8] == '403':
#             suspicious_ip[fields1[0]].append(f"Access to forbidden file: {fields1[6]}")
#         if fields1[8] == '401':
#             suspicious_ip[fields1[0]].append(f"Failed login attempt: {fields1[6]}")
    
#         if fields2[8] == '403':
#             suspicious_ip[fields2[0]].append(f"Access to forbidden file: {fields2[6]}")
#         if fields2[8] == '401':
#             suspicious_ip[fields2[0]].append(f"Failed login attempt: {fields2[6]}")

# for ip, activities in suspicious_ip.items():
#     print(f"Suspicious IP: {ip}")
#     for activity in activities:
#         print(f"  - {activity}")

with open(log_file_path1, 'r') as log_file1, open(log_file_path2, 'r') as log_file2:
    for line1, line2 in zip(log_file1, log_file2):
        fields1 = line1.split()
        fields2 = line2.split()
        
        if len(fields1) <= 1:
            print(line1.rstrip(), end='')
        else:
            if fields1[8] == '403':
                suspicious_ip[fields1[0]].append(f"Access to forbidden file: {fields1[6]}")
            if fields1[8] == '401':
                suspicious_ip[fields1[0]].append(f"Failed login attempt: {fields1[6]}")
        
        if len(fields2) <= 1:
            print(line2.rstrip(), end='')
            pass
        else:
            if fields2[8] == '403':
                suspicious_ip[fields2[0]].append(f"Access to forbidden file: {fields2[6]}")
            if fields2[8] == '401':
                suspicious_ip[fields2[0]].append(f"Failed login attempt: {fields2[6]}")

print()
for ip, activities in suspicious_ip.items():
    print(f"Suspicious IP: {ip}")
    for activity in activities:
        print(f"  - {activity}")

