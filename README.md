make sure you're using an appropriate version of java.
I had to update from openjdk 11 to 17.

python -m venv venv
source venv/bin/activate
pip install kivy buildozer bleak cython setuptools
buildozer android debug

don't forget between changes:
buildozer android clean

