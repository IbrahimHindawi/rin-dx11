"""Screenshots of the built lessons, taken from outside them: launch a lesson,
wait, optionally press keys, capture its window with PrintWindow, close it.
The lessons need no test code of their own. Needs Pillow.

    python tools/screenshot.py                      every lesson in build/cmake
    python tools/screenshot.py hdr bloom:T@4        some, with keys and a wait

name[:keys][@seconds]: keys are sent as WM_KEYDOWN in order, "T" for Tab;
the wait defaults to 2.5 seconds. Pictures go to shots/<name>[_keys].png.
"""
import ctypes, ctypes.wintypes as wt, subprocess, sys, time, pathlib
from PIL import Image

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
user32.SetProcessDPIAware()
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "shots"
OUT.mkdir(exist_ok=True)

WM_KEYDOWN, WM_KEYUP, WM_CLOSE = 0x100, 0x101, 0x10
EnumProc = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)

def find_window(pid):
    found = []
    def cb(hwnd, _):
        p = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value == pid and user32.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True
    user32.EnumWindows(EnumProc(cb), 0)
    return found[0] if found else None

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wt.DWORD), ("biWidth", wt.LONG), ("biHeight", wt.LONG), ("biPlanes", wt.WORD),
                ("biBitCount", wt.WORD), ("biCompression", wt.DWORD), ("biSizeImage", wt.DWORD),
                ("biXPelsPerMeter", wt.LONG), ("biYPelsPerMeter", wt.LONG), ("biClrUsed", wt.DWORD), ("biClrImportant", wt.DWORD)]

def capture(hwnd):
    rect = wt.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    w, h = rect.right, rect.bottom
    hdc = user32.GetDC(hwnd)
    mem = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(mem, bmp)
    user32.PrintWindow(hwnd, mem, 3)   # PW_CLIENTONLY | PW_RENDERFULLCONTENT
    bi = BITMAPINFOHEADER(ctypes.sizeof(BITMAPINFOHEADER), w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mem, bmp, 0, h, buf, ctypes.byref(bi), 0)
    gdi32.DeleteObject(bmp); gdi32.DeleteDC(mem); user32.ReleaseDC(hwnd, hdc)
    return Image.frombuffer("RGB", (w, h), buf, "raw", "BGRX", 0, 1)

def shoot(spec):
    name, keys, wait = spec, "", 2.5
    if "@" in name: name, t = name.split("@"); wait = float(t)
    if ":" in name: name, keys = name.split(":")
    exe = ROOT / "build/cmake" / f"{name}.exe"
    proc = subprocess.Popen([str(exe)], cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    hwnd, deadline = None, time.time() + 60
    while hwnd is None and time.time() < deadline and proc.poll() is None:
        time.sleep(0.1); hwnd = find_window(proc.pid)
    if hwnd is None:
        out = proc.stdout.read().decode(errors="replace") if proc.poll() is not None else "no window"
        print(f"FAIL {name}: {out.strip()[:300]}"); proc.kill(); return
    for k in keys:
        vk = 0x09 if k == "T" else ord(k)
        user32.PostMessageW(hwnd, WM_KEYDOWN, vk, 0); user32.PostMessageW(hwnd, WM_KEYUP, vk, 0)
        time.sleep(0.2)
    time.sleep(wait)
    if proc.poll() is not None:
        print(f"FAIL {name}: exited early: {proc.stdout.read().decode(errors='replace').strip()[:300]}"); return
    tag = name + (f"_{keys}" if keys else "")
    capture(hwnd).save(OUT / f"{tag}.png")
    user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
    try: proc.wait(10)
    except subprocess.TimeoutExpired: proc.kill()
    print(f"ok   {tag}")

specs = sys.argv[1:] or [p.stem for p in sorted((ROOT / "build/cmake").glob("*.exe"))]
for s in specs: shoot(s)
