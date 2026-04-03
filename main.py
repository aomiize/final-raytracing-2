import RT_utility as rtu
import RT_camera as rtc
import RT_renderer as rtren
import RT_material as rtm
import RT_scene as rts
import RT_object as rto
import RT_integrator as rti
import RT_texture as rtt
import RT_light as rtl


def renderJapanScene():

    main_camera = rtc.Camera()

    # ---------- render quality ----------
    main_camera.aspect_ratio = 16.0/9.0
    main_camera.img_width = 1920
    main_camera.samples_per_pixel = 128
    main_camera.max_depth = 8

    main_camera.vertical_fov = 35

    main_camera.look_from = rtu.Vec3(0,2,7)
    main_camera.look_at = rtu.Vec3(0,1,0)
    main_camera.vec_up = rtu.Vec3(0,1,0)

    aperture = 0.1
    focus_distance = 7

    main_camera.init_camera(aperture, focus_distance)

    world = rts.Scene()

    # ---------- ground ----------

    checker = rtt.CheckerTexture(
        0.5,
        rtu.Color(0.15,0.15,0.15),
        rtu.Color(0.7,0.7,0.7)
    )

    ground_mat = rtm.TextureColor(checker)

    world.add_object(
        rto.Sphere(
            rtu.Vec3(0,-1000,0),
            1000,
            ground_mat
        )
    )

    # ---------- Mt Fuji background ----------

    fuji_tex = rtt.ImageTexture("textures/fuji.jpg")
    fuji_mat = rtm.TextureColor(fuji_tex)

    world.add_object(
        rto.Sphere(
            rtu.Vec3(0,6,-20),
            7,
            fuji_mat
        )
    )

    # ---------- convenience store ----------

    store_tex = rtt.ImageTexture("textures/store.jpg")
    store_mat = rtm.TextureColor(store_tex)

    world.add_object(
        rto.Sphere(
            rtu.Vec3(0,1,-3),
            1.6,
            store_mat
        )
    )

    # ---------- neon sign ----------

    neon_light = rtl.Diffuse_light(
        rtu.Color(12,4,3)
    )

    world.add_object(
        rto.Sphere(
            rtu.Vec3(0,2.2,-3),
            0.35,
            neon_light
        )
    )

    # ---------- window light ----------

    window_light = rtl.Diffuse_light(
        rtu.Color(6,6,4)
    )

    world.add_object(
        rto.Sphere(
            rtu.Vec3(-0.6,1.2,-2.6),
            0.25,
            window_light
        )
    )

    world.add_object(
        rto.Sphere(
            rtu.Vec3(0.6,1.2,-2.6),
            0.25,
            window_light
        )
    )

    # ---------- street light ----------

    street_light = rtl.Diffuse_light(
        rtu.Color(8,7,5)
    )

    world.add_object(
        rto.Sphere(
            rtu.Vec3(-2,3,-2),
            0.6,
            street_light
        )
    )

    # ---------- integrator ----------

    integrator = rti.Integrator(bSkyBG=False)

    renderer = rtren.Renderer(
        main_camera,
        integrator,
        world
    )

    renderer.render_jittered()

    renderer.write_img2png("japan_fuji_scene.png")


if __name__ == "__main__":
    renderJapanScene()