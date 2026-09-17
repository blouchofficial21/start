import os
import sys

# Find and load the encrypted compiled module securely
try:
    so_files = [f for f in os.listdir('.') if f.endswith('.so') and 'start_core' in f]
    if so_files:
        mod_name = so_files[0][:-3]
        mod = __import__(mod_name)
        mod.main()
    else:
        print("Error: Encrypted core module missing!")
except Exception as e:
    pass
