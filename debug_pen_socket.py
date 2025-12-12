#!/usr/bin/env python3
"""
Pen Socket Detection Debug Script (Linux)

This script attempts multiple methods to detect when a pen/stylus
is removed from its socket on a Linux laptop (Lenovo Y1 Yoga).

Methods tested:
1. /proc/bus/input/devices monitoring
2. /dev/input/ device enumeration
3. xinput command monitoring
4. udev device monitoring
5. evdev library (if available)
6. Polling for device presence
"""

import sys
import time
import os
import subprocess
import glob

print("\n" + "="*70)
print("PEN SOCKET DETECTION DEBUG TOOL (Linux)")
print("="*70)
print("This tool will attempt to detect pen removal from socket.")
print("Remove and insert your pen while this script is running.\n")
print(f"Platform: {sys.platform}")
print(f"Python: {sys.version}\n")


# Method 1: /proc/bus/input/devices
def method1_proc_devices():
    """Read /proc/bus/input/devices for pen/stylus."""
    print("\n[Method 1] /proc/bus/input/devices")
    print("-" * 70)
    
    try:
        with open('/proc/bus/input/devices', 'r') as f:
            content = f.read()
        
        devices = content.split('\n\n')
        pen_devices = []
        
        for device in devices:
            if any(keyword in device.lower() for keyword in ['pen', 'stylus', 'wacom', 'digitizer']):
                pen_devices.append(device)
        
        if pen_devices:
            print(f"  ✓ Found {len(pen_devices)} pen/stylus device(s):\n")
            for i, dev in enumerate(pen_devices, 1):
                print(f"  Device {i}:")
                for line in dev.split('\n'):
                    if line.strip():
                        print(f"    {line}")
                print()
        else:
            print("  ⚠ No pen/stylus devices found")
            print("  → Showing all input devices:\n")
            for i, device in enumerate(devices[:5], 1):
                if device.strip():
                    print(f"  Device {i}:")
                    for line in device.split('\n')[:3]:
                        if line.strip():
                            print(f"    {line}")
                    print()
    
    except FileNotFoundError:
        print("  ✗ /proc/bus/input/devices not found")
    except Exception as e:
        print(f"  ✗ Error: {e}")


# Method 2: /dev/input/ enumeration
def method2_dev_input():
    """Enumerate /dev/input/ devices."""
    print("\n[Method 2] /dev/input/ Device Enumeration")
    print("-" * 70)
    
    try:
        event_devices = glob.glob('/dev/input/event*')
        print(f"  ✓ Found {len(event_devices)} event devices:")
        
        for device in sorted(event_devices):
            try:
                # Try to get device name
                result = subprocess.run(
                    ['cat', f'/sys/class/input/{os.path.basename(device)}/device/name'],
                    capture_output=True,
                    text=True,
                    timeout=1
                )
                name = result.stdout.strip() if result.returncode == 0 else 'Unknown'
                
                is_pen = any(keyword in name.lower() for keyword in ['pen', 'stylus', 'wacom', 'digitizer'])
                marker = '★ PEN! ' if is_pen else ''
                print(f"    {marker}{device}: {name}")
            except:
                print(f"    {device}: (unable to read name)")
        
        print("\n  → These devices can be monitored for events")
    
    except Exception as e:
        print(f"  ✗ Error: {e}")


# Method 3: xinput command
def method3_xinput():
    """Use xinput to list input devices."""
    print("\n[Method 3] xinput Command")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            ['xinput', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("  ✓ xinput output:\n")
            for line in result.stdout.split('\n'):
                is_pen = any(keyword in line.lower() for keyword in ['pen', 'stylus', 'wacom', 'digitizer', 'eraser'])
                marker = '  ★ ' if is_pen else '    '
                if line.strip():
                    print(f"{marker}{line}")
        else:
            print(f"  ✗ xinput failed: {result.stderr}")
    
    except FileNotFoundError:
        print("  ⚠ xinput not installed (sudo apt install xinput)")
    except subprocess.TimeoutExpired:
        print("  ✗ xinput command timed out")
    except Exception as e:
        print(f"  ✗ Error: {e}")


# Method 4: libinput command
def method4_libinput():
    """Use libinput to list devices."""
    print("\n[Method 4] libinput Command")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            ['libinput', 'list-devices'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("  ✓ libinput output:\n")
            devices = result.stdout.split('\n\n')
            for device in devices:
                if any(keyword in device.lower() for keyword in ['pen', 'stylus', 'wacom', 'digitizer', 'tablet']):
                    print("  ★ PEN DEVICE:")
                    for line in device.split('\n'):
                        if line.strip():
                            print(f"    {line}")
                    print()
        else:
            print(f"  ⚠ libinput requires root: sudo libinput list-devices")
    
    except FileNotFoundError:
        print("  ⚠ libinput not installed (sudo apt install libinput-tools)")
    except subprocess.TimeoutExpired:
        print("  ✗ libinput command timed out")
    except Exception as e:
        print(f"  ✗ Error: {e}")


# Method 5: evdev library
def method5_evdev():
    """Try to use python-evdev library."""
    print("\n[Method 5] python-evdev Library")
    print("-" * 70)
    
    try:
        import evdev
        
        print("  ✓ evdev library available")
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        
        print(f"\n  Found {len(devices)} input devices:")
        for device in devices:
            is_pen = any(keyword in device.name.lower() for keyword in ['pen', 'stylus', 'wacom', 'digitizer'])
            marker = '★ ' if is_pen else ''
            
            capabilities = []
            if evdev.ecodes.EV_ABS in device.capabilities():
                abs_caps = device.capabilities()[evdev.ecodes.EV_ABS]
                if any(code in abs_caps for code in [evdev.ecodes.ABS_PRESSURE, evdev.ecodes.ABS_TILT_X]):
                    capabilities.append('pressure/tilt')
            
            caps_str = f" [{', '.join(capabilities)}]" if capabilities else ""
            print(f"    {marker}{device.path}: {device.name}{caps_str}")
            
            if is_pen:
                print(f"      → Vendor: {device.info.vendor:04x}, Product: {device.info.product:04x}")
    
    except ImportError:
        print("  ⚠ evdev not installed (pip install evdev)")
        print("  → This is the best library for pen input on Linux")
    except PermissionError:
        print("  ✗ Permission denied - run as root or add user to 'input' group")
        print("    sudo usermod -a -G input $USER")
    except Exception as e:
        print(f"  ✗ Error: {e}")


# Method 6: Continuous monitoring
def method6_monitor_changes():
    """Monitor for device additions/removals."""
    print("\n[Method 6] Device Change Monitoring")
    print("-" * 70)
    print("  → Monitoring /dev/input/ for changes...")
    print("  → Remove and insert your pen now!\n")
    
    try:
        initial_devices = set(glob.glob('/dev/input/event*'))
        print(f"  Initial: {len(initial_devices)} devices")
        
        for i in range(30):
            time.sleep(1)
            current_devices = set(glob.glob('/dev/input/event*'))
            
            added = current_devices - initial_devices
            removed = initial_devices - current_devices
            
            if added:
                print(f"  ★ DEVICE ADDED at {time.strftime('%H:%M:%S')}:")
                for device in added:
                    try:
                        result = subprocess.run(
                            ['cat', f'/sys/class/input/{os.path.basename(device)}/device/name'],
                            capture_output=True,
                            text=True,
                            timeout=1
                        )
                        name = result.stdout.strip() if result.returncode == 0 else 'Unknown'
                        print(f"      {device}: {name}")
                    except:
                        print(f"      {device}")
                initial_devices = current_devices
            
            if removed:
                print(f"  ★ DEVICE REMOVED at {time.strftime('%H:%M:%S')}:")
                for device in removed:
                    print(f"      {device}")
                initial_devices = current_devices
            
            if (i + 1) % 5 == 0:
                print(f"  → Still monitoring... ({i + 1}/30 seconds)")
        
        print("\n  ✓ Monitoring completed")
    
    except Exception as e:
        print(f"  ✗ Error: {e}")


def main():
    """Run all detection methods."""
    
    # Run synchronous tests first
    method1_proc_devices()
    method2_dev_input()
    method3_xinput()
    method4_libinput()
    method5_evdev()
    method6_monitor_changes()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
The most reliable methods for detecting pen on Linux:
1. python-evdev library (Method 5) - Best for monitoring pen events
2. /dev/input/ monitoring (Method 6) - Detects device add/remove
3. xinput command (Method 3) - Lists current pen devices

For pen socket detection:
- Socket removal may or may not generate device events
- Some pens are always "connected" even when in socket
- Best approach: Monitor for pen proximity events in your app
  (when pen comes near screen, it's being used)

Recommendations:
- Install python-evdev: pip install evdev
- Add your user to 'input' group: sudo usermod -a -G input $USER
- Monitor pen events in practice.py using pygame pressure detection
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
