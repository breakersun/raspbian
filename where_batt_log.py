import adtypes
import sys, uuid, time
from bluepy.btle import Scanner, DefaultDelegate
import datetime
import csv

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
            if desc == 'Manufacturer' and len(value) == 54:
                VID = ''.join([value[2], value[3], value[0], value[1]])
                if VID == '03f5':
                    print(str(datetime.datetime.now()) +
                          ', ' + dev.addr +
                          ', ' + str(int(''.join(value[50:52]), 16)))
                    csv_writer.writerow([datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                         dev.addr,
                                         int(''.join(value[50:52]), 16)])

timestr = time.strftime("%Y%m%d-%H%M%S")
log = open(timestr + '.csv', 'w+', newline='')
csv_writer = csv.writer(log)

scanner = Scanner(0).withDelegate(ScanDelegate())

while True:
    scanner.scan(10)
    scanner.scan(10)
    time.sleep(40)
    time.sleep(60 * 59)

