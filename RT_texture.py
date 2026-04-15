# Texture class - SUPPORTS ALL IMAGE FORMATS
import math
from PIL import Image as im
import RT_utility as rtu

class Texture:
    def __init__(self) -> None:
        pass

    def tex_value(self, fu, fv, vPoint):
        pass

class SolidColor(Texture):
    def __init__(self, cColor) -> None:
        super().__init__()
        self.solid_color = cColor

    def tex_value(self, fu, fv, vPoint):
        return self.solid_color

class CheckerTexture(Texture):
    def __init__(self, fScale, cColor1, cColor2) -> None:
        super().__init__()
        self.inv_scale = 1.0/fScale
        self.even_texture = SolidColor(cColor1)
        self.odd_texture = SolidColor(cColor2)

    def tex_value(self, fu, fv, vPoint):
        xInteger = int(math.floor(vPoint.x()*self.inv_scale))
        yInteger = int(math.floor(vPoint.y()*self.inv_scale))
        zInteger = int(math.floor(vPoint.z()*self.inv_scale))
        isEven = (xInteger + yInteger + zInteger) % 2 == 0
        if isEven:
            return self.even_texture.tex_value(fu, fv, vPoint)
        return self.odd_texture.tex_value(fu, fv, vPoint)

class ImageTexture(Texture):
    def __init__(self, strImgFilename) -> None:
        super().__init__()
        self.invalid = False
        self.img = None
        try:
            self.img = im.open(strImgFilename)
            
            # ✅ Convert WEBP/PNG with transparency to RGB
            if self.img.mode in ('RGBA', 'LA', 'P'):
                self.img = self.img.convert('RGB')
            elif self.img.mode not in ('RGB', 'L'):
                self.img = self.img.convert('RGB')
            
            try:
                print(f'✓ Loaded: {strImgFilename} ({self.img.width}x{self.img.height}, {self.img.mode})')
            except (ValueError, OSError):
                pass  # stdout ปิดแล้ว ไม่ต้อง print
            
            self.invalid = False
            
        except Exception as e:
            try:
                print(f'✗ ERROR: Could not load {strImgFilename}')
                print(f'  {e}')
            except (ValueError, OSError):
                pass  # stdout ปิดแล้ว ไม่ต้อง print
            
            self.invalid = True
            return
        
        if self.img.height <= 0 or self.img.width <= 0:
            try:
                print(f'✗ Invalid size: {self.img.size}')
            except (ValueError, OSError):
                pass
            self.invalid = True
            return

    def __del__(self):
        if self.img:
            self.img.close()

    def tex_value(self, fu, fv, vPoint):
        if self.invalid or self.img is None:
            return rtu.Color(0, 1, 1)
        
        # ✅ FIX: Flip V coordinate
        u = rtu.Interval(0, 1).clamp(fu)
        v = 1.0 - rtu.Interval(0, 1).clamp(fv)
        
        # Prevent out of bounds
        i = min(int(u * self.img.width), self.img.width - 1)
        j = min(int(v * self.img.height), self.img.height - 1)
        
        try:
            pixel = self.img.getpixel((i, j))
            
            # Handle RGB and Grayscale
            if isinstance(pixel, tuple):
                if len(pixel) >= 3:
                    scale = 1.0 / 255.0
                    return rtu.Color(pixel[0] * scale, pixel[1] * scale, pixel[2] * scale)
                elif len(pixel) == 1:
                    scale = 1.0 / 255.0
                    gray = pixel[0] * scale
                    return rtu.Color(gray, gray, gray)
            else:
                # Grayscale single value
                scale = 1.0 / 255.0
                gray = pixel * scale
                return rtu.Color(gray, gray, gray)
                
        except Exception as e:
            try:
                print(f'✗ Pixel error at ({i},{j}): {e}')
            except (ValueError, OSError):
                pass
            return rtu.Color(1, 0, 1)
        
        return rtu.Color(0, 1, 1)