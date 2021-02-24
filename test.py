import stun
import time


def get_info():
    nat_type, external_ip, external_port = stun.get_ip_info()
    print(nat_type)
    print(external_ip)
    print(external_port)
    time.sleep(3)


for _ in range(10):
    get_info()
