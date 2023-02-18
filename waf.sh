
#!/bin/bash

# Set threshold for number of requests per second
THRESHOLD=10

# Set ban time in seconds
BAN_TIME=10

# Set Network Interface
NET_INTERFACE='enp0s3'

# Loop forever
while true
do
    # Count the number of requests in the last second
    COUNT=$(tail -n 10000 /var/log/apache2/access.log | grep -c "$(date '+%d/%b/%Y:%H:%M:%S' --date='1 second ago')")

    # If the count exceeds the threshold, ban the IP
    if [ "$COUNT" -gt "$THRESHOLD" ]
    then
        IP=$(tail -n 10000 /var/log/apache2/access.log | grep "$(date '+%d/%b/%Y:%H:%M:%S' --date='1 second ago')" | awk '{print $1}' | sort | uniq -c | sort -nr | head -n1 | awk '{print $2}')

        # Check if IP is already banned
        if iptables -L INPUT -v -n | grep -q "$IP"
        then
            sleep 0
        else
            # Ban the IP address for the specified duration
            (echo "Banning IP address $IP for $BAN_TIME seconds" >> /var/log/banip.log
            iptables -A INPUT -p tcp -i $NET_INTERFACE -s $IP --dport 80 -j DROP
            sleep $BAN_TIME
            # Remove the IP ban after the specified duration
            echo "Unbanning IP address $IP" >> /var/log/banip.log
            while iptables -L INPUT -v -n | grep -q "$IP"
            do
                iptables -D INPUT -p tcp -i $NET_INTERFACE -s $IP --dport 80 -j DROP
            done)&
        fi
    fi
done
