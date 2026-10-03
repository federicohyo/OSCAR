# UART client for Caravel board
# UART is on FTDI channel D (DDBUS0=rx, DDBUS1=tx) per PCB schematic
import pyftdi.serialext
from pyftdi.ftdi import Ftdi
from io import StringIO
import sys

# Discover FTDI devices
s = StringIO()
Ftdi.show_devices(out=s)
devlist = s.getvalue().splitlines()[1:-1]
gooddevs = []
for dev in devlist:
    url = dev.split('(')[0].strip()
    name = '(' + dev.split('(')[1]
    if name in ('(Single RS232-HS)', '(Quad RS232-HS)'):
        gooddevs.append(url)
if len(gooddevs) == 0:
    print('Error:  No matching FTDI devices on USB bus!')
    sys.exit(1)

# UART is on channel D (/4) — DDBUS0=rv.ser_rx, DDBUS1=rv.ser_tx
base_url = gooddevs[0].rsplit('/', 1)[0]
uart_url = base_url + '/4'
print('Using UART on FTDI channel D: ' + uart_url)

port = pyftdi.serialext.serial_for_url(uart_url, baudrate=24000, timeout=0)

print('Listening for UART data (press Ctrl+C to quit)...')
print('Tip: press the board RESET button to re-trigger "Hello World"')
print()

try:
    while True:
        c = port.read(1)
        if c == b'':
            sys.stdout.flush()
        else:
            print(c.decode("utf-8", errors="replace"), end='')
except KeyboardInterrupt:
    print('\nDone.')
finally:
    port.close()
