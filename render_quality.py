"""
Render Quality Presets
======================
ระบบปรับคุณภาพรูปภาพแบบหลายระดับ

วิธีใช้:
1. เลือก QUALITY_PRESET ที่ต้องการ
2. ใส่ใน main() ก่อน camera.init_camera()
"""

import RT_camera as rtc

# ========================================
# QUALITY PRESETS
# ========================================

QUALITY_PRESETS = {
    
    # ========================================
    # PREVIEW QUALITY (ดูคร่าวๆ)
    # ========================================
    'preview': {
        'name': 'Preview Quality',
        'description': 'ดูคร่าวๆ ทดสอบ composition',
        'img_width': 480,
        'samples_per_pixel': 4,
        'max_depth': 3,
        'render_time': '3-5 นาที',
        'file_size': '~500 KB',
        'use_case': 'ทดสอบมุมกล้อง, แสง, องค์ประกอบ'
    },
    
    # ========================================
    # DRAFT QUALITY (ดูรายละเอียดคร่าวๆ)
    # ========================================
    'draft': {
        'name': 'Draft Quality',
        'description': 'ดูรายละเอียดคร่าวๆ มี noise เล็กน้อย',
        'img_width': 640,
        'samples_per_pixel': 16,
        'max_depth': 5,
        'render_time': '8-12 นาที',
        'file_size': '~1 MB',
        'use_case': 'ทดสอบรายละเอียด, วัสดุ, สี'
    },
    
    # ========================================
    # LOW QUALITY (คุณภาพต่ำ)
    # ========================================
    'low': {
        'name': 'Low Quality',
        'description': 'คุณภาพต่ำ แต่ใช้เวลาน้อย',
        'img_width': 960,
        'samples_per_pixel': 100,
        'max_depth': 6,
        'render_time': '40-60 นาที',
        'file_size': '~3 MB',
        'use_case': 'ตรวจสอบก่อนส่งงาน'
    },
    
    # ========================================
    # MEDIUM QUALITY (คุณภาพกลาง)
    # ========================================
    'medium': {
        'name': 'Medium Quality (HD)',
        'description': 'คุณภาพกลาง เหมาะดูบนจอ',
        'img_width': 1920,
        'samples_per_pixel': 256,
        'max_depth': 8,
        'render_time': '2-4 ชั่วโมง',
        'file_size': '~8 MB',
        'use_case': 'สำหรับดูบนจอ Full HD'
    },
    
    # ========================================
    # HIGH QUALITY (คุณภาพสูง)
    # ========================================
    'high': {
        'name': 'High Quality (Full HD+)',
        'description': 'คุณภาพสูง ภาพเนียนมาก',
        'img_width': 2560,
        'samples_per_pixel': 512,
        'max_depth': 10,
        'render_time': '6-10 ชั่วโมง',
        'file_size': '~15 MB',
        'use_case': 'สำหรับส่งงาน คุณภาพดี'
    },
    
    # ========================================
    # ULTRA QUALITY (คุณภาพสูงสุด - 4K)
    # ========================================
    'ultra': {
        'name': 'Ultra Quality (4K)',
        'description': 'คุณภาพสูงสุด ภาพสวยที่สุด',
        'img_width': 3840,
        'samples_per_pixel': 1024,
        'max_depth': 12,
        'render_time': '12-20 ชั่วโมง',
        'file_size': '~25 MB',
        'use_case': 'ส่งงานคุณภาพสูงสุด, พิมพ์ขนาดใหญ่'
    },
    
    # ========================================
    # EXTREME QUALITY (สำหรับผลงานระดับ production)
    # ========================================
    'extreme': {
        'name': 'Extreme Quality (8K)',
        'description': 'สำหรับ production ระดับมืออาชีพ',
        'img_width': 7680,
        'samples_per_pixel': 2048,
        'max_depth': 15,
        'render_time': '48-72 ชั่วโมง',
        'file_size': '~100 MB',
        'use_case': 'Production ระดับสูง, โฆษณา, ภาพยนตร์'
    },
    
    # ========================================
    # CUSTOM (กำหนดเอง)
    # ========================================
    'custom': {
        'name': 'Custom Quality',
        'description': 'กำหนดค่าเองทุกอย่าง',
        'img_width': 1920,  # แก้ได้
        'samples_per_pixel': 256,  # แก้ได้
        'max_depth': 8,  # แก้ได้
        'render_time': 'ขึ้นกับการตั้งค่า',
        'file_size': 'ขึ้นกับการตั้งค่า',
        'use_case': 'ปรับแต่งเอง'
    }
}


def apply_quality_preset(camera, preset_name='medium'):
    """
    ใช้ preset คุณภาพกับ camera
    
    Parameters:
    -----------
    camera : RT_camera.Camera
        Camera object
    preset_name : str
        ชื่อ preset: 'preview', 'draft', 'low', 'medium', 'high', 'ultra', 'extreme', 'custom'
    
    Returns:
    --------
    dict : ข้อมูล preset ที่ใช้
    """
    
    import sys
    
    if preset_name not in QUALITY_PRESETS:
        try:
            print(f"⚠️ ไม่พบ preset '{preset_name}' - ใช้ 'medium' แทน")
        except:
            pass
        preset_name = 'medium'
    
    preset = QUALITY_PRESETS[preset_name]
    
    # ตั้งค่า camera
    camera.img_width = preset['img_width']
    camera.samples_per_pixel = preset['samples_per_pixel']
    camera.max_depth = preset['max_depth']
    
    # คำนวณความสูงภาพ
    camera.img_height = camera.compute_img_height()
    
    # แสดงข้อมูล (ป้องกัน error ถ้า stdout ปิด)
    try:
        print("\n" + "=" * 70)
        print(f"  🎨 {preset['name']}")
        print("=" * 70)
        print(f"คำอธิบาย:     {preset['description']}")
        print(f"ความละเอียด:  {camera.img_width} × {camera.img_height} pixels")
        print(f"Samples:      {camera.samples_per_pixel} SPP")
        print(f"Max Depth:    {camera.max_depth}")
        print(f"เวลา Render:  {preset['render_time']}")
        print(f"ขนาดไฟล์:     {preset['file_size']}")
        print(f"ใช้สำหรับ:    {preset['use_case']}")
        print("=" * 70)
        print()
    except ValueError:
        # ถ้า stdout ปิดแล้ว ไม่ต้อง print
        pass
    
    return preset


def list_all_presets():
    """แสดงรายการ preset ทั้งหมด"""
    
    try:
        print("\n" + "=" * 90)
        print("  📋 RENDER QUALITY PRESETS")
        print("=" * 90)
        print()
        
        print(f"{'Preset':<12} {'Resolution':<15} {'SPP':<8} {'Depth':<7} {'Time':<20} {'Use Case':<25}")
        print("-" * 90)
        
        for key, preset in QUALITY_PRESETS.items():
            if key == 'custom':
                res = 'กำหนดเอง'
            else:
                # คำนวณความสูง (16:9)
                height = int(preset['img_width'] / (16.0/9.0))
                res = f"{preset['img_width']}×{height}"
            
            print(f"{key:<12} {res:<15} {preset['samples_per_pixel']:<8} {preset['max_depth']:<7} {preset['render_time']:<20} {preset['use_case'][:24]:<25}")
        
        print("=" * 90)
        print()
    except ValueError:
        pass


# ========================================
# COMPARISON TABLE
# ========================================

def show_quality_comparison():
    """แสดงตารางเปรียบเทียบคุณภาพ"""
    
    try:
        print("\n" + "=" * 100)
        print("  📊 QUALITY COMPARISON")
        print("=" * 100)
        print()
        
        presets_order = ['preview', 'draft', 'low', 'medium', 'high', 'ultra', 'extreme']
        
        print(f"{'Quality':<12} {'Pixels':<15} {'Megapixels':<12} {'Samples':<10} {'Total Rays':<15} {'Time':<20}")
        print("-" * 100)
        
        for preset_name in presets_order:
            preset = QUALITY_PRESETS[preset_name]
            width = preset['img_width']
            height = int(width / (16.0/9.0))
            megapixels = width * height / 1_000_000
            total_rays = width * height * preset['samples_per_pixel']
            total_rays_m = total_rays / 1_000_000
            
            print(f"{preset_name:<12} {width}×{height:<8} {megapixels:>6.2f} MP    {preset['samples_per_pixel']:<10} {total_rays_m:>10.1f}M rays   {preset['render_time']:<20}")
        
        print("=" * 100)
        print()
    except ValueError:
        pass


# ========================================
# ตัวอย่างการใช้งาน
# ========================================

if __name__ == '__main__':
    
    # แสดงรายการ presets ทั้งหมด
    list_all_presets()
    
    # แสดงตารางเปรียบเทียบ
    show_quality_comparison()
    
    # ทดสอบใช้ preset
    print("\n" + "=" * 70)
    print("  ตัวอย่างการใช้งาน")
    print("=" * 70)
    print()
    
    print("# วิธีใช้ใน main.py:")
    print()
    print("from render_quality import apply_quality_preset")
    print()
    print("def main():")
    print("    camera = rtc.Camera()")
    print("    ")
    print("    # เลือกคุณภาพที่ต้องการ")
    print("    apply_quality_preset(camera, 'high')  # ← เปลี่ยนได้")
    print("    ")
    print("    # ตั้งค่าอื่นๆ")
    print("    camera.vertical_fov = 45")
    print("    camera.look_from = rtu.Vec3(0, 1.7, -12)")
    print("    # ...")
    print("    camera.init_camera(aperture, focus_distance)")
    print()