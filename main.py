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

def get_signed_internal_temp(b10, b11):
    # Get a short int from b10 b11 in little endian
    a10 = (b10 & 255) * 256 + (b11 & 255);
    if a10 >= 2048:
        return a10 | (-4096)
    return a10

def ambient_from_temperature_reading(i10, i11, i12):
    return i10 + int(max(0.0, ((i11 - min(48, i12)) * 9424) / 1487.0))

def to_celsius(i10):
    if i10 > 0:
        return (i10 + 8) / 32
    elif i10 < 0:
        return (i10 - 8) / 32
    return 0

async def monitor(root):
    try:
        async with BleakClient(ADDRESS) as client:
            while True:
                data = await client.read_gatt_char("7edda774-045e-4bbf-909b-45d1991a2876")

                internal = get_signed_internal_temp(data[1], data[0])
                ambient = get_signed_internal_temp(data[3], data[2])
                initial_ambient_offset = get_signed_internal_temp(data[5], data[4])
                lowest_ambient_offset = get_signed_internal_temp(data[5], data[4])

                ambient = 2 * max(0, ambient_from_temperature_reading(internal, ambient, initial_ambient_offset))
                internal *= 2

                tip = to_celsius(internal)
                ambient = to_celsius(ambient)

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
