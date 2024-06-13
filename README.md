python -m venv venv
source venv/bin/activate
pip install kivy buildozer bleak cython setuptools
buildozer android debug

don't forget between changes:
buildozer android clean

