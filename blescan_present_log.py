import adtypes
import sys, uuid, time
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
	

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        for (adtype, desc, value) in dev.getScanData():
            if desc == 'Manufacturer' and len(value) == 52:
                res = beacon_parser(value, dev.rssi)
                if res[0] == uuid.UUID('5de8c210-f981-4f11-8292-631f89450e40'):
                    print(time.strftime("%Y%m%d-%H%M%S")+','+dev.addr, file=log)
                    print(time.strftime("%Y%m%d-%H%M%S")+','+dev.addr)
			
            if desc == 'Manufacturer' and len(value) == 20:
                addr = value[16:18] + ':' + value[14:16] + ':' + value[12:14] + ':' + value[10:12] + ':' + value[8:10] + ':' + value[6:8]
                if addr == dev.addr:
                    print(time.strftime("%Y%m%d-%H%M%S")+','+dev.addr, file=log)
                    print(time.strftime("%Y%m%d-%H%M%S")+','+dev.addr)
				

timestr = time.strftime("%Y%m%d-%H%M%S")
log = open(timestr, 'w+', encoding='ISO-8859-1')

scanner = Scanner(0).withDelegate(ScanDelegate())

while True:
    scanner.scan(10)

