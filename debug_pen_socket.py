#!/usr/bin/env python3
"""
Pen Socket Detection Debug Script

This script attempts multiple methods to detect when a pen/stylus
is removed from its socket on a Windows laptop (Lenovo Y1 Yoga).

Methods tested:
1. Windows WM_TABLET_ADDED/REMOVED messages
2. USB HID device monitoring
3. Windows Management Instrumentation (WMI)
4. Registry monitoring for tablet input devices
5. Polling for pen device presence
"""

import sys
import time
import threading
import ctypes
from ctypes import wintypes, POINTER, WINFUNCTYPE, c_int, c_void_p, Structure
import subprocess

print("\n" + "="*70)
print("PEN SOCKET DETECTION DEBUG TOOL")
print("="*70)
print("This tool will attempt to detect pen removal from socket.")
print("Remove and insert your pen while this script is running.\n")

# Windows message constants
WM_DEVICECHANGE = 0x0219
DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEREMOVECOMPLETE = 0x8004
DBT_DEVTYP_DEVICEINTERFACE = 0x00000005

# Tablet PC Input constants
TABLET_DISABLE_PRESSANDHOLD = 0x00000001
TABLET_DISABLE_PENTAPFEEDBACK = 0x00000008
TABLET_DISABLE_PENBARRELFEEDBACK = 0x00000010
TABLET_DISABLE_TOUCHUIFORCEON = 0x00000100
TABLET_DISABLE_TOUCHUIFORCEOFF = 0x00000200
TABLET_DISABLE_TOUCHSWITCH = 0x00008000
TABLET_DISABLE_FLICKS = 0x00010000


class DEV_BROADCAST_HDR(Structure):
    _fields_ = [
        ("dbch_size", wintypes.DWORD),
        ("dbch_devicetype", wintypes.DWORD),
        ("dbch_reserved", wintypes.DWORD),
    ]


class DEV_BROADCAST_DEVICEINTERFACE(Structure):
    _fields_ = [
        ("dbcc_size", wintypes.DWORD),
        ("dbcc_devicetype", wintypes.DWORD),
        ("dbcc_reserved", wintypes.DWORD),
        ("dbcc_classguid", ctypes.c_byte * 16),
        ("dbcc_name", ctypes.c_wchar * 256),
    ]


# Method 1: Windows Message Monitoring
def method1_windows_messages():
    """Monitor Windows device change messages."""
    print("\n[Method 1] Windows Device Change Messages")
    print("-" * 70)
    
    try:
        # Create a hidden window to receive messages
        user32 = ctypes.windll.user32
        
        # Define window procedure
        WNDPROC = WINFUNCTYPE(c_int, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
        
        def wnd_proc(hwnd, msg, wparam, lparam):
            if msg == WM_DEVICECHANGE:
                if wparam == DBT_DEVICEARRIVAL:
                    print(f"  ✓ Device arrival detected! Time: {time.strftime('%H:%M:%S')}")
                    try:
                        hdr = ctypes.cast(lparam, POINTER(DEV_BROADCAST_HDR)).contents
                        if hdr.dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE:
                            print("    -> Type: Device Interface (possibly pen!)")
                    except:
                        pass
                elif wparam == DBT_DEVICEREMOVECOMPLETE:
                    print(f"  ✓ Device removal detected! Time: {time.strftime('%H:%M:%S')}")
                    try:
                        hdr = ctypes.cast(lparam, POINTER(DEV_BROADCAST_HDR)).contents
                        if hdr.dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE:
                            print("    -> Type: Device Interface (possibly pen!)")
                    except:
                        pass
            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
        
        wnd_proc_func = WNDPROC(wnd_proc)
        
        # Register window class
        class_name = "PenDetectorWindow"
        wndclass = ctypes.wintypes.WNDCLASSW()
        wndclass.lpfnWndProc = wnd_proc_func
        wndclass.lpszClassName = class_name
        wndclass.hInstance = ctypes.windll.kernel32.GetModuleHandleW(None)
        
        class_atom = user32.RegisterClassW(ctypes.byref(wndclass))
        if not class_atom:
            print("  ✗ Failed to register window class")
            return
        
        # Create window
        hwnd = user32.CreateWindowExW(
            0, class_atom, "Pen Detector", 0,
            0, 0, 0, 0, None, None, wndclass.hInstance, None
        )
        
        if not hwnd:
            print("  ✗ Failed to create window")
            return
        
        print("  ✓ Message monitor started")
        print("  → Listening for device changes...")
        
        # Message loop
        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
    
    except Exception as e:
        print(f"  ✗ Error: {e}")


# Method 2: HID Device Enumeration
def method2_hid_devices():
    """Enumerate HID devices and look for pen/digitizer."""
    print("\n[Method 2] HID Device Enumeration")
    print("-" * 70)
    
    try:
        import win32api
        import win32con
        import win32gui
        
        # This would require pywin32 which might not be installed
        print("  ⚠ Requires pywin32 package (pip install pywin32)")
        print("  → Skipping this method")
    except ImportError:
        print("  ⚠ pywin32 not installed (pip install pywin32)")
        print("  → Skipping this method")


# Method 3: WMI Monitoring
def method3_wmi_monitoring():
    """Use Windows Management Instrumentation to monitor devices."""
    print("\n[Method 3] WMI Device Monitoring")
    print("-" * 70)
    
    try:
        import wmi
        print("  ✓ WMI available")
        
        c = wmi.WMI()
        
        # List current pointing devices
        print("\n  Current Pointing Devices:")
        for device in c.Win32_PointingDevice():
            print(f"    - {device.Name} ({device.DeviceID})")
            if "pen" in device.Name.lower() or "stylus" in device.Name.lower():
                print("      ★ PEN DETECTED!")
        
        print("\n  → Monitoring for device changes...")
        print("  → (This method may not catch pen socket events)")
        
    except ImportError:
        print("  ⚠ WMI not installed (pip install WMI)")
        print("  → Skipping this method")
    except Exception as e:
        print(f"  ✗ Error: {e}")


# Method 4: Registry Monitoring
def method4_registry_monitoring():
    """Monitor registry for tablet input changes."""
    print("\n[Method 4] Registry Monitoring")
    print("-" * 70)
    
    try:
        import winreg
        
        # Check tablet PC settings
        paths = [
            r"SOFTWARE\Microsoft\Wisp\Pen",
            r"SOFTWARE\Microsoft\TabletTip",
            r"SYSTEM\CurrentControlSet\Enum\HID",
        ]
        
        print("  ✓ Checking registry keys:")
        for path in paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ)
                subkey_count = winreg.QueryInfoKey(key)[0]
                print(f"    - {path}: {subkey_count} subkeys")
                winreg.CloseKey(key)
            except WindowsError:
                print(f"    - {path}: Not accessible")
        
        print("\n  → Registry monitoring requires more complex implementation")
        print("  → Pen socket events may not be reflected in registry")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")


# Method 5: PowerShell Device Query
def method5_powershell_devices():
    """Use PowerShell to query pen devices."""
    print("\n[Method 5] PowerShell Device Query")
    print("-" * 70)
    
    try:
        # Query for HID devices
        cmd = 'Get-PnpDevice -Class "HIDClass" | Where-Object {$_.FriendlyName -like "*pen*" -or $_.FriendlyName -like "*stylus*" -or $_.FriendlyName -like "*digitizer*"} | Select-Object Status,FriendlyName,InstanceId | Format-List'
        
        print("  → Querying for pen/stylus devices...")
        result = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout.strip():
            print("  ✓ Found pen-related devices:")
            print(result.stdout)
        else:
            print("  ⚠ No pen devices found in HIDClass")
        
        # Try tablet input devices
        cmd2 = 'Get-PnpDevice | Where-Object {$_.Class -eq "Sensor" -or $_.FriendlyName -like "*touch*"} | Select-Object Status,FriendlyName | Format-Table'
        result2 = subprocess.run(
            ["powershell", "-Command", cmd2],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result2.stdout.strip():
            print("\n  Touch/Sensor devices:")
            print(result2.stdout)
    
    except subprocess.TimeoutExpired:
        print("  ✗ PowerShell query timed out")
    except Exception as e:
        print(f"  ✗ Error: {e}")


# Method 6: Continuous Polling
def method6_polling():
    """Poll for pen device presence."""
    print("\n[Method 6] Device Polling")
    print("-" * 70)
    
    try:
        print("  → Polling for pen device status changes...")
        print("  → Remove/insert pen to test detection\n")
        
        last_state = None
        poll_count = 0
        
        while poll_count < 30:  # Poll for 30 seconds
            # Try to detect pen via various APIs
            current_state = {}
            
            # Check GetSystemMetrics for pen/digitizer
            SM_DIGITIZER = 94
            SM_MAXIMUMTOUCHES = 95
            
            user32 = ctypes.windll.user32
            digitizer = user32.GetSystemMetrics(SM_DIGITIZER)
            touches = user32.GetSystemMetrics(SM_MAXIMUMTOUCHES)
            
            # Decode digitizer flags
            has_integrated_touch = bool(digitizer & 0x01)
            has_external_touch = bool(digitizer & 0x02)
            has_integrated_pen = bool(digitizer & 0x04)
            has_external_pen = bool(digitizer & 0x08)
            multi_input = bool(digitizer & 0x40)
            ready = bool(digitizer & 0x80)
            
            current_state = {
                'integrated_touch': has_integrated_touch,
                'external_touch': has_external_touch,
                'integrated_pen': has_integrated_pen,
                'external_pen': has_external_pen,
                'multi_input': multi_input,
                'ready': ready,
                'max_touches': touches
            }
            
            if last_state is None:
                print("  Initial state:")
                print(f"    Integrated Touch: {has_integrated_touch}")
                print(f"    External Touch: {has_external_touch}")
                print(f"    Integrated Pen: {has_integrated_pen}")
                print(f"    External Pen: {has_external_pen}")
                print(f"    Multi-Input: {multi_input}")
                print(f"    Ready: {ready}")
                print(f"    Max Touches: {touches}")
                print()
                last_state = current_state
            elif current_state != last_state:
                print(f"  ★ STATE CHANGE DETECTED at {time.strftime('%H:%M:%S')}!")
                for key in current_state:
                    if current_state[key] != last_state[key]:
                        print(f"    {key}: {last_state[key]} -> {current_state[key]}")
                last_state = current_state
                print()
            
            time.sleep(1)
            poll_count += 1
            
            # Show progress
            if poll_count % 5 == 0:
                print(f"  → Still monitoring... ({poll_count}/30 seconds)")
        
        print("\n  ✓ Polling completed")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")


def main():
    """Run all detection methods."""
    
    # Run synchronous tests first
    method3_wmi_monitoring()
    method4_registry_monitoring()
    method5_powershell_devices()
    method6_polling()
    
    # Method 1 needs to run in a message loop
    print("\n[Method 1] Starting Windows message monitor...")
    print("→ This will run continuously. Press Ctrl+C to exit.")
    print("→ Remove and insert your pen to test detection.\n")
    
    try:
        method1_windows_messages()
    except KeyboardInterrupt:
        print("\n\n✓ Monitoring stopped by user")
    except Exception as e:
        print(f"\n✗ Error in message monitoring: {e}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
The most reliable method for detecting pen socket removal would be:
1. Windows Device Change Messages (Method 1) - if pen appears as USB device
2. Custom driver/service monitoring tablet PC events
3. Polling GetSystemMetrics (Method 6) - may not detect socket events

Unfortunately, Windows does not provide a direct API for pen socket
detection. The pen socket is often a passive magnetic or mechanical
holder that doesn't generate system events.

However, you may see events when:
- Pen comes near the screen (proximity)
- Pen touches the screen
- Pen button is pressed

For your application, the best approach is to:
- Detect pen proximity/hover events in pygame
- Show "pen ready" status when proximity detected
- This indicates the pen is out and being used
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
