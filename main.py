"""
Scene 1: DEPTH OF FIELD - ชัดตรงกลาง เบลอข้างๆ
==============================================
ใช้ Aperture ใหญ่ + Focus ที่ภาพกลาง
→ ภาพกลาง (Mona Lisa) ชัด
→ ภาพข้างๆ เบลอ
→ ม้านั่งข้างหน้าเบลอ

⚡ Settings: 960×540, 64 SPP, 2-3 นาที
"""

import sys
import io
import RT_utility as rtu
import RT_camera as rtc
import RT_renderer as rtren
import RT_material as rtm
import RT_scene as rts
import RT_object as rto
import RT_integrator as rti
import RT_texture as rtt
import RT_light as rtl
import math

if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except:
        pass


def safe_print(msg):
    try:
        print(msg)
    except:
        pass


def main():
    
    camera = rtc.Camera()
    camera.aspect_ratio = 16.0 / 9.0
    
    # ========================================
    # SETTINGS
    # ========================================
    camera.img_width = 960
    camera.samples_per_pixel = 64    # Jittered sampling
    camera.max_depth = 5
    # ========================================
    
    # ========================================
    # CAMERA - DEPTH OF FIELD
    # ========================================
    camera.vertical_fov = 50
    camera.look_from = rtu.Vec3(0, 1.8, -10)
    camera.look_at = rtu.Vec3(0, 2.5, -30)     # มองไปที่ภาพกลาง
    camera.vec_up = rtu.Vec3(0, 1, 0)
    
    # ⭐ KEY: Aperture ใหญ่ = DOF ตื้น (เบลอมาก)
    aperture = 0.3              # ← ใหญ่มาก (0.3) = เบลอมาก
                                # ลด 0.1 = เบลอน้อยลง
                                
    # ⭐ Focus ที่ภาพกลาง (ระยะห่างจากกล้องถึงภาพ)
    focus_distance = 39.5       # ← ระยะจาก camera ถึงภาพกลาง
                                # ภาพอยู่ที่ z=-49.5, camera อยู่ที่ z=-10
                                # ระยะ = 49.5 - 10 = 39.5
    
    camera.init_camera(aperture, focus_distance)
    
    safe_print("=" * 70)
    safe_print("📷 DEPTH OF FIELD SETTINGS")
    safe_print("=" * 70)
    safe_print(f"Aperture:        {aperture} (large = more blur)")
    safe_print(f"Focus Distance:  {focus_distance} (distance to center painting)")
    safe_print(f"Result:          Center painting SHARP, others BLURRED")
    safe_print("=" * 70)
    safe_print("")
    
    # ========================================
    # SCENE
    # ========================================
    
    scene = rts.Scene(rtu.Color(0.02, 0.02, 0.03))
    
    # Materials
    floor_mat = rtm.Lambertian(rtu.Color(0.15, 0.15, 0.17))
    wall_mat = rtm.Lambertian(rtu.Color(0.15, 0.15, 0.16))
    ceiling_mat = rtm.Lambertian(rtu.Color(0.08, 0.08, 0.09))
    
    # Room
    scene.add_object(rto.Quad(rtu.Vec3(-30, 0, -50), rtu.Vec3(60, 0, 0), rtu.Vec3(0, 0, 100), floor_mat))
    scene.add_object(rto.Quad(rtu.Vec3(-30, 0, -50), rtu.Vec3(60, 0, 0), rtu.Vec3(0, 8, 0), wall_mat))
    scene.add_object(rto.Quad(rtu.Vec3(-30, 0, -50), rtu.Vec3(0, 0, 100), rtu.Vec3(0, 8, 0), wall_mat))
    scene.add_object(rto.Quad(rtu.Vec3(30, 0, -50), rtu.Vec3(0, 0, 100), rtu.Vec3(0, 8, 0), wall_mat))
    scene.add_object(rto.Quad(rtu.Vec3(-30, 8, -50), rtu.Vec3(60, 0, 0), rtu.Vec3(0, 0, 100), ceiling_mat))
    
    # ========================================
    # PAINTINGS (ตำแหน่งเดียวกันทุกภาพ z=-49.5)
    # ========================================
    
    # ภาพซ้าย (จะเบลอ)
    girl_texture = rtt.ImageTexture('textures/1665_Girl_with_a_Pearl_Earring.jpg')
    girl_mat = rtm.TextureColor(girl_texture)
    scene.add_object(rto.Quad(
        rtu.Vec3(-10 - 1.0, 2.8 - 1.2, -49.5),
        rtu.Vec3(2.0, 0, 0),
        rtu.Vec3(0, 2.4, 0),
        girl_mat
    ))
    
    # ภาพกลาง (จะชัด ⭐)
    mona_texture = rtt.ImageTexture('textures/Mona_Lisa.jpg')
    mona_mat = rtm.TextureColor(mona_texture)
    scene.add_object(rto.Quad(
        rtu.Vec3(0 - 0.9, 3.0 - 1.35, -49.5),
        rtu.Vec3(1.8, 0, 0),
        rtu.Vec3(0, 2.7, 0),
        mona_mat
    ))
    
    # ภาพขวา (จะเบลอ)
    portrait_texture = rtt.ImageTexture('textures/Self-portrait-with-Straw-Hat.jpg')
    portrait_mat = rtm.TextureColor(portrait_texture)
    scene.add_object(rto.Quad(
        rtu.Vec3(10 - 1.0, 2.8 - 1.2, -49.5),
        rtu.Vec3(2.0, 0, 0),
        rtu.Vec3(0, 2.4, 0),
        portrait_mat
    ))
    
    # ========================================
    # FRAMES (กรอบทอง)
    # ========================================
    
    frame_mat = rtm.Metal(rtu.Color(1.0, 0.84, 0.0), 0.2)
    
    for px, py, pw, ph in [(-10, 2.8, 2.0, 2.4), (0, 3.0, 1.8, 2.7), (10, 2.8, 2.0, 2.4)]:
        for dx, dy in [(-pw/2, ph/2), (pw/2, ph/2), (-pw/2, -ph/2), (pw/2, -ph/2)]:
            scene.add_object(rto.Sphere(rtu.Vec3(px + dx, py + dy, -49.2), 0.1, frame_mat))
    
    # ========================================
    # CHANDELIER (โคมไฟ - ลดความสว่าง)
    # ========================================
    
    chandelier_mat = rtl.TemperatureLight(2700, 1.5)  # ลดจาก 3.0 → 1.5
    
    for i in range(8):
        angle = (i / 8.0) * 2 * math.pi
        x = 0.8 * math.cos(angle)
        z = -25 + 0.8 * math.sin(angle)
        scene.add_object(rto.Sphere(rtu.Vec3(x, 6.5, z), 0.12, chandelier_mat))  # เล็กลง 0.15→0.12
    
    # ========================================
    # BENCHES (ม้านั่ง - จะเบลอเพราะอยู่ใกล้)
    # ========================================
    
    bench_mat = rtm.Lambertian(rtu.Color(0.4, 0.1, 0.1))
    
    for x in [-10, 0, 10]:
        scene.add_object(rto.Sphere(rtu.Vec3(x, 0.5, -35), 0.4, bench_mat))
    
    # ========================================
    # LIGHTS - แบบภาพอ้างอิง
    # ========================================
    
    # 💡 Spotlights หลัก 3 ดวง บนภาพ (สว่างชัดเจน)
    for x in [-10, 0, 10]:
        scene.add_object(rto.Sphere(
            rtu.Vec3(x, 6.8, -47),       # ขยับไปข้างหน้าเล็กน้อย
            0.25,                         # ใหญ่ขึ้นเล็กน้อย
            rtl.TemperatureLight(3200, 8.0)  # อุ่น + สว่างมาก
        ))
    
    # 🌟 Ambient ceiling lights (นุ่มนวล, กระจายทั่วห้อง)
    ambient_positions = [
        # แถวหน้า
        (-15, 7.0, -15),
        (0, 7.0, -15),
        (15, 7.0, -15),
        # แถวกลาง
        (-15, 7.0, -30),
        (15, 7.0, -30),
        # แถวหลัง (ข้างๆ ภาพ)
        (-20, 7.0, -45),
        (20, 7.0, -45),
    ]
    
    for x, y, z in ambient_positions:
        scene.add_object(rto.Sphere(
            rtu.Vec3(x, y, z),
            0.15,
            rtl.TemperatureLight(3000, 0.6)  # อุ่น + ไม่สว่างมาก
        ))
    
    # 🔆 Fill light เบาๆ (เติมแสงในส่วนที่มืด)
    scene.add_object(rto.Sphere(
        rtu.Vec3(0, 6.5, -20),
        0.3,
        rtl.TemperatureLight(2800, 1.2)  # อุ่นมาก + ไม่สว่างมาก
    ))
    
    # ========================================
    # RENDER
    # ========================================
    
    integrator = rti.Integrator(bDlight=True, bSkyBG=False)
    renderer = rtren.Renderer(camera, integrator, scene)
    
    safe_print("🎨 Rendering Scene 1 - DEPTH OF FIELD + REALISTIC LIGHTING")
    safe_print(f"Resolution:   {camera.img_width} × {camera.img_height}")
    safe_print(f"Samples:      {camera.samples_per_pixel} SPP (Jittered)")
    safe_print(f"Max Depth:    {camera.max_depth}")
    safe_print("")
    safe_print("Lighting Setup (like reference image):")
    safe_print("  💡 3× Spotlights (3200K, bright) - directly above paintings")
    safe_print("  🌟 7× Ambient lights (3000K, soft) - ceiling spread")
    safe_print("  🔆 1× Fill light (2800K, warm) - center")
    safe_print("  💫 8× Chandelier (2700K, dim) - decorative")
    safe_print("")
    safe_print("Depth of Field:")
    safe_print("  ✓ Center painting (Mona Lisa) - SHARP")
    safe_print("  ✓ Side paintings - BLURRED")
    safe_print("  ✓ Benches (foreground) - BLURRED")
    safe_print("")
    safe_print("Expected: 2-3 minutes")
    safe_print("=" * 70)
    safe_print("")
    
    # ใช้ jittered sampling
    renderer.render_jittered()
    
    renderer.write_img2png('scene1_depth_of_field.png')
    
    safe_print("")
    safe_print("=" * 70)
    safe_print("✅ Done!")
    safe_print("=" * 70)
    safe_print("Output: scene1_depth_of_field.png")
    safe_print("")
    safe_print("📷 Depth of Field Effect:")
    safe_print("  • Aperture 0.3 = Large aperture = Shallow DOF")
    safe_print("  • Focus at center painting (z=-49.5)")
    safe_print("  • Objects at different depths appear blurred")
    safe_print("=" * 70)


if __name__ == '__main__':
    main()