# object class
import RT_utility as rtu
import math

class Object:
    def __init__(self) -> None:
        pass

    def intersect(self, rRay, cInterval):
        pass

class Sphere(Object):
    def __init__(self, vCenter, fRadius, mMat=None) -> None:
        super().__init__()
        self.center = vCenter
        self.radius = fRadius
        self.material = mMat
        # additional parameters for motion blur
        self.moving_center = None       # where to the sphere moves to
        self.is_moving = False          # is it moving ?
        self.moving_dir = None          # moving direction

    def add_material(self, mMat):
        self.material = mMat

    def add_moving(self, vCenter):      # set an ability to move to the sphere
        self.moving_center = vCenter
        self.is_moving = True
        self.moving_dir = self.moving_center - self.center

    def move_sphere(self, fTime):       # move the sphere by time parameter
        return self.center + self.moving_dir*fTime

    def printInfo(self):
        self.center.printout()        
    
    def intersect(self, rRay, cInterval):        

        # check if the sphere is moving then move center of the sphere.
        sphere_center = self.center
        if self.is_moving:
            sphere_center = self.move_sphere(rRay.getTime())

        oc = rRay.getOrigin() - sphere_center
        a = rRay.getDirection().len_squared()
        half_b = rtu.Vec3.dot_product(oc, rRay.getDirection())
        c = oc.len_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c 

        if discriminant < 0:
            return None
        sqrt_disc = math.sqrt(discriminant)

        root = (-half_b - sqrt_disc) / a 
        if not cInterval.surrounds(root):
            root = (-half_b + sqrt_disc) / a 
            if not cInterval.surrounds(root):
                return None
            
        hit_t = root
        hit_point = rRay.at(root)
        hit_normal = (hit_point - sphere_center) / self.radius
        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)
        hinfo.set_face_normal(rRay, hit_normal)

        # set uv coordinates for texture mapping
        fuv = self.get_uv(hit_normal)
        hinfo.set_uv(fuv[0], fuv[1])

        return hinfo

    # return uv coordinates of the sphere at the hit point.
    def get_uv(self, vNormal):
        theta = math.acos(-vNormal.y())
        phi = math.atan2(-vNormal.z(), vNormal.x()) + math.pi

        u = phi / (2*math.pi)
        v = theta / math.pi
        return (u,v)

# Ax + By + Cz = D
class Quad(Object):
    def __init__(self, vQ, vU, vV, mMat=None) -> None:
        super().__init__()
        self.Qpoint = vQ
        self.Uvec = vU
        self.Vvec = vV
        self.material = mMat
        self.uxv = rtu.Vec3.cross_product(self.Uvec, self.Vvec)
        self.normal = rtu.Vec3.unit_vector(self.uxv)
        self.D = rtu.Vec3.dot_product(self.normal, self.Qpoint)
        self.Wvec = self.uxv / rtu.Vec3.dot_product(self.uxv, self.uxv)

    def add_material(self, mMat):
        self.material = mMat

    def intersect(self, rRay, cInterval):
        denom = rtu.Vec3.dot_product(self.normal, rRay.getDirection())
        # if parallel
        if rtu.Interval.near_zero(denom):
            return None

        # if it is hit.
        t = (self.D - rtu.Vec3.dot_product(self.normal, rRay.getOrigin())) / denom
        if not cInterval.contains(t):
            return None
        
        hit_t = t
        hit_point = rRay.at(t)
        hit_normal = self.normal

        # determine if the intersection point lies on the quad's plane.
        planar_hit = hit_point - self.Qpoint
        alpha = rtu.Vec3.dot_product(self.Wvec, rtu.Vec3.cross_product(planar_hit, self.Vvec))
        beta = rtu.Vec3.dot_product(self.Wvec, rtu.Vec3.cross_product(self.Uvec, planar_hit))
        if self.is_interior(alpha, beta) is None:
            return None

        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)
        hinfo.set_face_normal(rRay, hit_normal)

        # set uv coordinates for texture mapping
        hinfo.set_uv(alpha, beta)

        return hinfo
    
    def is_interior(self, fa, fb):
        delta = 0   
        if (fa<delta) or (1.0<fa) or (fb<delta) or (1.0<fb):
            return None

        return True


class Triangle(Object):
    def __init__(self, v0, v1, v2, mMat=None) -> None:
        super().__init__()
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.material = mMat

        self.edge1 = self.v1 - self.v0
        self.edge2 = self.v2 - self.v0
        self.normal = rtu.Vec3.unit_vector(
            rtu.Vec3.cross_product(self.edge1, self.edge2)
        )

    def intersect(self, rRay, cInterval):

        h = rtu.Vec3.cross_product(rRay.getDirection(), self.edge2)
        a = rtu.Vec3.dot_product(self.edge1, h)

        if abs(a) < 1e-8:
            return None

        f = 1.0 / a
        s = rRay.getOrigin() - self.v0
        u = f * rtu.Vec3.dot_product(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = rtu.Vec3.cross_product(s, self.edge1)
        v = f * rtu.Vec3.dot_product(rRay.getDirection(), q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * rtu.Vec3.dot_product(self.edge2, q)

        if not cInterval.contains(t):
            return None

        hit_point = rRay.at(t)

        hinfo = rtu.Hitinfo(hit_point, self.normal, t, self.material)
        hinfo.set_face_normal(rRay, self.normal)

        hinfo.set_uv(u, v)

        return hinfo
    
def bounding_sphere(self):
    return self.center, self.radius

    