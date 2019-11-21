import adtypes
import sys, uuid
from bluepy.btle import Scanner, DefaultDelegate

def twos_complement(hexstr, bits):
    value = int(hexstr,16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

def beacon_parser(raw_data, rssi):
    tmp = list(raw_data[0:4])
    VID = ''.join([tmp[2], tmp[3], tmp[0], tmp[1]])
    UUID = uuid.UUID(raw_data[4:36])
    HW = raw_data[36:38]
    SW = raw_data[38:40]
    BATT = raw_data[40:42]
    MAJOR = raw_data[42:46]
    MINOR = raw_data[46:50]
    RSSI_1M = raw_data[-2:]
    return [UUID, HW, SW, twos_complement(BATT, 8), MAJOR, MINOR, RSSI_1M, rssi]
    # print(UUID, HW, SW, BATT, MAJOR, MINOR, twos_complement(RSSI_1M, 8))

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr == dest_addr:
            for (adtype, desc, value) in dev.getScanData():
                if desc == 'Manufacturer':
                    res = beacon_parser(value, dev.rssi)
                    print(res)
                    print('\x1b[%dA' % (2))


print('======\nusage: python3 blescan blescan.py MAC_ADDR\nfor example:python3 blescan.py aa:bb:cc:dd:ee:00\n=====')
if len(sys.argv) != 2:
    print('command usage error')
    sys.exit()

dest_addr = sys.argv[1]
scanner = Scanner(0).withDelegate(ScanDelegate())

while True:
    try:
        devices = scanner.scan(20)
    except:
        scanner = Scanner(0).withDelegate(ScanDelegate())