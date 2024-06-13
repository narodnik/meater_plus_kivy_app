make sure you're using an appropriate version of java.
I had to update from openjdk 11 to 17.

python -m venv venv
source venv/bin/activate
pip install kivy buildozer bleak cython setuptools
buildozer android debug

don't forget between changes:
buildozer android clean

btw the relay station (wooden block) must be very close, especially if you're
using the oven. Otherwise it will give an error like out of range or show a
flashing red dot. For a long time I thought that meant the battery is low. Just
put the relay as close as possible (I leave mine resting on the over door
handle).

