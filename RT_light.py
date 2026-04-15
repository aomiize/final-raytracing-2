# Enhanced Light Classes
# รองรับ: SpotLight, TemperatureLight, SoftLight, GradientLight, FlickerLight

import RT_utility as rtu
import RT_material as rtm
import math

class Light(rtm.Material):
    def __init__(self) -> None:
        pass

    def scattering(self, rRayIn, hHinfo):
        return None

    def emitting(self):
        return rtu.Color(0,0,0)

    def is_light(self):
        return True


class Diffuse_light(Light):
    """แสงกระจายทั่วไป (Basic light)"""
    def __init__(self, cAlbedo) -> None:
        super().__init__()
        self.light_color = cAlbedo

    def scattering(self, rRayIn, hHinfo):
        return None

    def emitting(self):
        return self.light_color


class TemperatureLight(Light):
    """
    แสงตามอุณหภูมิ Kelvin (Color Temperature)
    
    Parameters:
    -----------
    temperature : float
        อุณหภูมิสีในหน่วย Kelvin
        - 1850K: แสงเทียน (Candle)
        - 2700K: หลอดไส้ (Incandescent)
        - 3000K: แสงอบอุ่น (Warm White)
        - 3500K: แสงนุ่ม (Soft White)
        - 4000K: แสงกลาง (Neutral White)
        - 5000K: แสงกลางวัน (Daylight)
        - 5500K: แสงแดดเที่ยง (Noon Daylight)
        - 6500K: แสงขาวเย็น (Cool White)
        - 10000K: ท้องฟ้าสีน้ำเงิน (Blue Sky)
    
    intensity : float
        ความเข้มแสง (1.0 = ปกติ, >1.0 = สว่างขึ้น)
    """
    
    def __init__(self, temperature=5000, intensity=1.0):
        super().__init__()
        self.temperature = temperature
        self.intensity = intensity
        self.light_color = self._kelvin_to_rgb(temperature)
    
    def _kelvin_to_rgb(self, kelvin):
        """แปลงอุณหภูมิ Kelvin เป็นสี RGB"""
        
        # Clamp temperature
        temp = max(1000, min(40000, kelvin))
        temp = temp / 100.0
        
        # Calculate Red
        if temp <= 66:
            red = 255
        else:
            red = temp - 60
            red = 329.698727446 * math.pow(red, -0.1332047592)
            red = max(0, min(255, red))
        
        # Calculate Green
        if temp <= 66:
            green = temp
            green = 99.4708025861 * math.log(green) - 161.1195681661
        else:
            green = temp - 60
            green = 288.1221695283 * math.pow(green, -0.0755148492)
        green = max(0, min(255, green))
        
        # Calculate Blue
        if temp >= 66:
            blue = 255
        else:
            if temp <= 19:
                blue = 0
            else:
                blue = temp - 10
                blue = 138.5177312231 * math.log(blue) - 305.0447927307
                blue = max(0, min(255, blue))
        
        # Normalize to 0-1 range
        return rtu.Color(red / 255.0, green / 255.0, blue / 255.0)
    
    def scattering(self, rRayIn, hHinfo):
        return None
    
    def emitting(self):
        return self.light_color * self.intensity


class SpotLight(Light):
    """
    แสงแบบ Spotlight (แสงกรวย)
    
    Parameters:
    -----------
    color : Color
        สีของแสง
    cone_angle : float
        มุมกรวยของแสง (degrees) - ยิ่งเล็กยิ่งแคบ
        เช่น 15 = แคบมาก, 45 = กว้างปานกลาง
    falloff : float
        การลดทอนของแสงที่ขอบกรวย (0-1)
        0 = ขอบคมชัด, 1 = ขอบนุ่ม
    intensity : float
        ความเข้มแสง
    """
    
    def __init__(self, color, cone_angle=30, falloff=0.8, intensity=1.0):
        super().__init__()
        self.base_color = color
        self.cone_angle = cone_angle
        self.falloff = falloff
        self.intensity = intensity
    
    def scattering(self, rRayIn, hHinfo):
        return None
    
    def emitting(self):
        # สำหรับ spotlight เราใช้สีพื้นฐาน
        # การคำนวณทิศทางจะทำใน integrator
        return self.base_color * self.intensity


class SoftLight(Light):
    """
    แสงนุ่ม มีการลดทอนตามระยะทาง (Distance Falloff)
    
    Parameters:
    -----------
    color : Color
        สีของแสง
    falloff_distance : float
        ระยะที่แสงเริ่มลดลง (ยิ่งมากยิ่งส่องไกล)
    intensity : float
        ความเข้มแสง
    """
    
    def __init__(self, color, falloff_distance=10.0, intensity=1.0):
        super().__init__()
        self.light_color = color
        self.falloff_distance = falloff_distance
        self.intensity = intensity
    
    def scattering(self, rRayIn, hHinfo):
        return None
    
    def emitting(self):
        return self.light_color * self.intensity


class GradientLight(Light):
    """
    แสงไล่สี (Gradient Light)
    
    Parameters:
    -----------
    color1 : Color
        สีที่ 1
    color2 : Color
        สีที่ 2
    direction : Vec3
        ทิศทางการไล่สี
    intensity : float
        ความเข้มแสง
    """
    
    def __init__(self, color1, color2, direction=rtu.Vec3(0, 1, 0), intensity=1.0):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.direction = rtu.Vec3.unit_vector(direction)
        self.intensity = intensity
    
    def scattering(self, rRayIn, hHinfo):
        return None
    
    def emitting(self):
        # ใช้สีเฉลี่ย (สามารถปรับแต่งได้)
        avg_color = (self.color1 + self.color2) * 0.5
        return avg_color * self.intensity


class FlickerLight(Light):
    """
    แสงกระพริบ (Flicker Light) - เหมาะสำหรับเทียน, ไฟฉุกเฉิน
    
    Parameters:
    -----------
    color : Color
        สีของแสง
    base_intensity : float
        ความเข้มพื้นฐาน
    flicker_amount : float
        ปริมาณการกระพริบ (0-1)
    """
    
    def __init__(self, color, base_intensity=1.0, flicker_amount=0.3):
        super().__init__()
        self.light_color = color
        self.base_intensity = base_intensity
        self.flicker_amount = flicker_amount
    
    def scattering(self, rRayIn, hHinfo):
        return None
    
    def emitting(self):
        # สุ่มความเข้มแสง
        flicker = 1.0 + (rtu.random_double(-1, 1) * self.flicker_amount)
        intensity = self.base_intensity * max(0.1, flicker)
        return self.light_color * intensity


# ========================================
# Helper Functions
# ========================================

def create_warm_light(intensity=1.0):
    """สร้างแสงอบอุ่น (2700K - Warm White)"""
    return TemperatureLight(2700, intensity)


def create_cool_light(intensity=1.0):
    """สร้างแสงเย็น (6500K - Cool White)"""
    return TemperatureLight(6500, intensity)


def create_daylight(intensity=1.0):
    """สร้างแสงกลางวัน (5500K - Daylight)"""
    return TemperatureLight(5500, intensity)


def create_candle_light(intensity=1.0):
    """สร้างแสงเทียน (1850K - Candle)"""
    return TemperatureLight(1850, intensity)


def create_museum_spotlight(intensity=2.0):
    """สร้างไฟส่องภาพแบบพิพิธภัณฑ์"""
    return SpotLight(
        rtu.Color(1.0, 1.0, 1.05),  # สีขาวเล็กน้อยฟ้า
        cone_angle=25,
        falloff=0.9,
        intensity=intensity
    )


# ========================================
# Temperature Presets
# ========================================

TEMPERATURE_PRESETS = {
    'candle': 1850,        # เทียน
    'incandescent': 2700,  # หลอดไส้
    'warm': 3000,          # อบอุ่น
    'soft': 3500,          # นุ่ม
    'neutral': 4000,       # กลาง
    'daylight': 5000,      # กลางวัน
    'noon': 5500,          # เที่ยง
    'cool': 6500,          # เย็น
    'sky': 10000           # ท้องฟ้า
}


def create_temperature_light(preset='daylight', intensity=1.0):
    """
    สร้างแสงจาก preset ที่กำหนด
    
    Parameters:
    -----------
    preset : str
        ชื่อ preset: 'candle', 'incandescent', 'warm', 'soft', 
                      'neutral', 'daylight', 'noon', 'cool', 'sky'
    intensity : float
        ความเข้มแสง
    
    Returns:
    --------
    TemperatureLight
    """
    temp = TEMPERATURE_PRESETS.get(preset, 5000)
    return TemperatureLight(temp, intensity)