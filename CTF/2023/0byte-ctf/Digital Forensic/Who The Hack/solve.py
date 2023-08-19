from collections import defaultdict

log_file_path = 'access.log'

# --- Analyse - get the suspicious IPs ---
# suspicious_ip = defaultdict(list)

# with open(log_file_path, 'r') as log_file:
#     for line in log_file:
#         fields = line.split()
        
#         if fields[8] == '403':
#             suspicious_ip[fields[0]].append(f"Access to forbidden file: {fields[6]}")
#         if fields[8] == '401':
#             suspicious_ip[fields[0]].append(f"Failed login attempt: {fields[6]}")

# print()
# for ip, activities in suspicious_ip.items():
#     print(f"Suspicious IP: {ip}")
#     for activity in activities:
#         print(f"  - {activity}")

# --- get all requests urls with spesific ip ---
# ip = "178.19.45.123"
# url = []
# with open(log_file_path, 'r') as log_file:
#     for line in log_file:
#         fields = line.split()
        
#         if ip in fields[0]:
#             url.append(fields[6])

# for i in url:
#     print(i)


# --- get flag ---
ip = "178.19.45.123"
url = []
with open(log_file_path, 'r') as log_file:
    for line in log_file:
        fields = line.split()
        
        if ip in fields[0]:
            url.append(fields[6])

for i in url:
    if "/%" in i and len(i.strip()) <= 4:
        print(bytes.fromhex(i.strip()[2:]).decode(), end="")