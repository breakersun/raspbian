import struct

from bluepy.btle import UUID, Peripheral,DefaultDelegate

class MyDelegate(DefaultDelegate):
    def __init__(self, params):
        DefaultDelegate.__init__(self)
      
    def handleNotification(self, cHandle, data):
        s = list(data)
        print(":".join("{:02x}".format(c) for c in s))


sr_service_uuid         = UUID(0xFDEE)
sr_auth_char_uuid       = UUID(0xFD03)
sr_tx_uuid              = UUID(0xFD05)

print('target addr ' + 'ba:03:4c:3a:c3:70')

p = Peripheral('ba:03:4c:3a:c3:70', "public")
p.setDelegate(MyDelegate(p))

sr_service = p.getServiceByUUID(sr_service_uuid)

sr_tx_char = sr_service.getCharacteristics(sr_tx_uuid)[0]
sr_tx_char_value_handle = sr_tx_char.getHandle()

for desriptor in p.getDescriptors(sr_tx_char_value_handle, 0xFF):
    if (desriptor.uuid == 0x2902):
        print("SR_TX CCCD found at handle 0x"+ format(desriptor.handle,"02X"))
        sr_tx_value_cccd_handle = desriptor.handle

p.writeCharacteristic(sr_tx_value_cccd_handle, struct.pack('<bb', 0x02, 0x00))
print("Indication is turned on for TX")

sr_auth_char = sr_service.getCharacteristics(sr_auth_char_uuid)[0]
sr_auth_char_value_handle = sr_auth_char.getHandle()

p.writeCharacteristic(sr_auth_char_value_handle, struct.pack('<bbbb', 0x01, 0x02, 0x03, 0x04))

while True:
    if p.waitForNotifications(1.0):
        continue

    print("Waiting... Waited more than one sec for notification")
