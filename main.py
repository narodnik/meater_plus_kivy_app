#!/usr/bin/python
import asyncio, traceback
from bleak import BleakClient

from kivy.app import async_runTouchApp
from kivy.lang.builder import Builder

from android.permissions import request_permissions, Permission 
from android.storage import primary_external_storage_path
perms = [
    Permission.BLUETOOTH_CONNECT,
    Permission.BLUETOOTH_SCAN,
]
request_permissions(perms)

kv = '''
BoxLayout:
    orientation: 'vertical'
    Label:
        id: label
        text: 'null'
        font_size: self.width/20
'''

async def run_app(root, other_task):
    await async_runTouchApp(root, async_lib='asyncio')
    print('App done')
    other_task.cancel()

ADDRESS = "B8:1F:5E:95:64:8B"

def bytesToInt(byte0, byte1):
    return byte1*256+byte0

def convertAmbient(array): 
    tip = bytesToInt(array[0], array[1])
    ra  = bytesToInt(array[2], array[3])
    oa  = bytesToInt(array[4], array[5])
    return tip + max(
        0,
        (ra - min(48, oa)) * 16 * 589 / 1487
    )

def toCelsius(value):
    return (float(value)+8.0)/16.0

def tip_temp(array):
    tip = bytesToInt(array[0], array[1])
    return toCelsius(tip)

async def monitor(root):
    try:
        async with BleakClient(ADDRESS) as client:
            while True:
                data = await client.read_gatt_char("7edda774-045e-4bbf-909b-45d1991a2876")
                ambient = toCelsius(convertAmbient(data))
                tip = tip_temp(data)
                root.ids.label.text = f"{ambient:.2f} / {tip:.2f}"
    except:
        err = traceback.format_exc()
        print("error MeaterApp exception:", err)
        root.ids.label.text = err

root = Builder.load_string(kv)
other_task = asyncio.ensure_future(monitor(root))

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(run_app(root, other_task), other_task)
)
loop.close()
