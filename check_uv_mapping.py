# Check if RT_texture.py has UV flip fix

import os

print("=" * 70)
print("  Checking RT_texture.py")
print("=" * 70)
print()

if os.path.exists('RT_texture.py'):
    with open('RT_texture.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Checking UV mapping fix:")
    print()
    
    # Check for the critical line
    if '1.0 - rtu.Interval(0, 1).clamp(fv)' in content:
        print("OK: Found V coordinate flip (CORRECT)")
        print("    Line: v = 1.0 - rtu.Interval(0, 1).clamp(fv)")
    else:
        print("ERROR: V coordinate flip NOT found!")
        print()
        print("  Problem: UV mapping is incorrect")
        print("  Solution: Run command")
        print()
        print("  copy RT_texture_FINAL.py RT_texture.py")
        print()
        print("  Then run again:")
        print("  python main.py")
        print()
        print("=" * 70)
        exit()
    
    print()
    
    # Check for out of bounds protection
    if 'min(int(u * self.img.width), self.img.width - 1)' in content:
        print("OK: Out of bounds protection (CORRECT)")
    else:
        print("WARNING: No out of bounds protection")
    
    print()
    
    # Check for WEBP support
    if "self.img.mode in ('RGBA', 'LA', 'P')" in content:
        print("OK: WEBP/PNG/GIF support (CORRECT)")
    else:
        print("WARNING: No WEBP support")
    
    print()
    print("=" * 70)
    print("  Summary")
    print("=" * 70)
    print()
    
    if '1.0 - rtu.Interval(0, 1).clamp(fv)' in content:
        print("SUCCESS: RT_texture.py is correct!")
        print()
        print("If paintings still not showing, check:")
        print("1. Is main.py correct?")
        print("2. samples_per_pixel >= 16")
        print("3. max_depth >= 10")
        print()
        print("Or try running:")
        print("copy main_BLACK_CEILING.py main.py")
        print("python main.py")
    else:
        print("ERROR: RT_texture.py is NOT correct!")
        print()
        print("Run command:")
        print("copy RT_texture_FINAL.py RT_texture.py")
        print("python main.py")
    
    print()
    print("=" * 70)
    
else:
    print("ERROR: RT_texture.py not found!")
    print()
    print("Run command:")
    print("copy RT_texture_FINAL.py RT_texture.py")
    print()