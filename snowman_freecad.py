#!/usr/bin/env python3
"""
Snowman 3D Model for FreeCAD
Three spheres for body, two cylinders for hat, cone for nose, hemispheres for eyes and buttons
Plus a jaunty corn-cob pipe
"""

import FreeCAD
import Part
import math

# Create a new document
doc = FreeCAD.newDocument("Snowman")

# Sphere sizes (descending)
body_radius = 50
chest_radius = 38
head_radius = 28

# Sphere positions (z-aligned, intersecting)
body_z = body_radius
chest_z = body_z + body_radius * 0.7 + chest_radius * 0.7
head_z = chest_z + chest_radius * 0.7 + head_radius * 0.7

# Hat parameters
hat_pipe_radius = head_radius * 0.6
hat_pipe_height = head_radius * 1.2
hat_brim_radius = head_radius * 0.9
hat_brim_height = 3
hat_z = head_z + head_radius * 0.85

# Nose parameters
nose_radius = 6
nose_length = 25

# Eye and button parameters
eye_radius = 4
button_radius = 5

# Corn-cob pipe parameters
pipe_bowl_radius = 6
pipe_bowl_height = 12
pipe_bowl_inner_radius = 4
pipe_bowl_inner_depth = 8
pipe_stem_radius = 2.5
pipe_stem_length = 25


def make_hemisphere(radius):
    """Create a hemisphere (half sphere) by cutting a sphere with a box."""
    sphere = Part.makeSphere(radius)
    box = Part.makeBox(2*radius, 2*radius, radius,
                       FreeCAD.Vector(-radius, -radius, -radius))
    hemisphere = sphere.cut(box)
    return hemisphere


def make_cone(base_radius, height):
    """Create a cone pointing in +Z direction."""
    return Part.makeCone(base_radius, 0, height)


# Body (bottom sphere) - white
body = Part.makeSphere(body_radius)
body.translate(FreeCAD.Vector(0, 0, body_z))
body_obj = doc.addObject("Part::Feature", "Body")
body_obj.Shape = body
body_obj.ViewObject.ShapeColor = (1.0, 1.0, 1.0)  # white

# Chest (middle sphere) - white
chest = Part.makeSphere(chest_radius)
chest.translate(FreeCAD.Vector(0, 0, chest_z))
chest_obj = doc.addObject("Part::Feature", "Chest")
chest_obj.Shape = chest
chest_obj.ViewObject.ShapeColor = (1.0, 1.0, 1.0)  # white

# Head (top sphere) - white
head = Part.makeSphere(head_radius)
head.translate(FreeCAD.Vector(0, 0, head_z))
head_obj = doc.addObject("Part::Feature", "Head")
head_obj.Shape = head
head_obj.ViewObject.ShapeColor = (1.0, 1.0, 1.0)  # white

# Hat - Stovepipe (tall cylinder) - black
hat_pipe = Part.makeCylinder(hat_pipe_radius, hat_pipe_height)
hat_pipe.translate(FreeCAD.Vector(0, 0, hat_z))
hat_pipe_obj = doc.addObject("Part::Feature", "HatPipe")
hat_pipe_obj.Shape = hat_pipe
hat_pipe_obj.ViewObject.ShapeColor = (0.0, 0.0, 0.0)  # black

# Hat - Brim (flat thin cylinder) - black
hat_brim = Part.makeCylinder(hat_brim_radius, hat_brim_height)
hat_brim.translate(FreeCAD.Vector(0, 0, hat_z))
hat_brim_obj = doc.addObject("Part::Feature", "HatBrim")
hat_brim_obj.Shape = hat_brim
hat_brim_obj.ViewObject.ShapeColor = (0.0, 0.0, 0.0)  # black

# Nose (cone) - pointing forward (negative Y direction) - orange
nose = make_cone(nose_radius, nose_length)
# Rotate to point in -Y direction (90 degrees around X axis)
nose.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)
nose.translate(FreeCAD.Vector(0, -head_radius, head_z))
nose_obj = doc.addObject("Part::Feature", "Nose")
nose_obj.Shape = nose
nose_obj.ViewObject.ShapeColor = (1.0, 0.5, 0.0)  # orange

# Eyes (hemispheres on head) - black
eye_angle = 20  # degrees from center
eye_height_offset = head_radius * 0.2
eye_angle_rad = math.radians(eye_angle)

# Right eye
right_eye = make_hemisphere(eye_radius)
right_eye.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)
right_eye.translate(FreeCAD.Vector(
    head_radius * math.sin(eye_angle_rad),
    -head_radius * math.cos(eye_angle_rad) * 0.95,
    head_z + eye_height_offset
))
right_eye_obj = doc.addObject("Part::Feature", "RightEye")
right_eye_obj.Shape = right_eye
right_eye_obj.ViewObject.ShapeColor = (0.0, 0.0, 0.0)  # black

# Left eye
left_eye = make_hemisphere(eye_radius)
left_eye.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)
left_eye.translate(FreeCAD.Vector(
    -head_radius * math.sin(eye_angle_rad),
    -head_radius * math.cos(eye_angle_rad) * 0.95,
    head_z + eye_height_offset
))
left_eye_obj = doc.addObject("Part::Feature", "LeftEye")
left_eye_obj.Shape = left_eye
left_eye_obj.ViewObject.ShapeColor = (0.0, 0.0, 0.0)  # black

# Buttons (3 hemispheres on chest) - black
button_spacing = chest_radius * 0.35

for i, offset in enumerate([button_spacing, 0, -button_spacing]):
    button = make_hemisphere(button_radius)
    button.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)
    button.translate(FreeCAD.Vector(
        0,
        -chest_radius * 0.98,
        chest_z + offset
    ))
    button_obj = doc.addObject("Part::Feature", f"Button{i+1}")
    button_obj.Shape = button
    button_obj.ViewObject.ShapeColor = (0.0, 0.0, 0.0)  # black

# Corn-cob pipe
mouth_x = head_radius * 0.4
mouth_y = -head_radius * 0.95
mouth_z = head_z - head_radius * 0.35

# Create pipe stem
pipe_stem = Part.makeCylinder(pipe_stem_radius, pipe_stem_length)
# Rotate to point in -Y direction
pipe_stem.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)

# Create pipe bowl (hollow cylinder)
pipe_bowl_outer = Part.makeCylinder(pipe_bowl_radius, pipe_bowl_height)
pipe_bowl_inner = Part.makeCylinder(pipe_bowl_inner_radius, pipe_bowl_inner_depth + 1)
pipe_bowl_inner.translate(FreeCAD.Vector(0, 0, pipe_bowl_height - pipe_bowl_inner_depth))
pipe_bowl = pipe_bowl_outer.cut(pipe_bowl_inner)
pipe_bowl.translate(FreeCAD.Vector(0, -pipe_stem_length, -pipe_bowl_height * 0.3))

# Apply pipe rotations: first tilt upward (25 deg around X), then angle to side (-50 deg around Z)
# In FreeCAD we apply in reverse order
pipe_stem.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -25)
pipe_stem.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), -50)
pipe_stem.translate(FreeCAD.Vector(mouth_x, mouth_y, mouth_z))

pipe_bowl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -25)
pipe_bowl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), -50)
pipe_bowl.translate(FreeCAD.Vector(mouth_x, mouth_y, mouth_z))

pipe_stem_obj = doc.addObject("Part::Feature", "PipeStem")
pipe_stem_obj.Shape = pipe_stem
pipe_stem_obj.ViewObject.ShapeColor = (0.545, 0.271, 0.075)  # SaddleBrown

pipe_bowl_obj = doc.addObject("Part::Feature", "PipeBowl")
pipe_bowl_obj.Shape = pipe_bowl
pipe_bowl_obj.ViewObject.ShapeColor = (0.824, 0.706, 0.549)  # tan

# Recompute document
doc.recompute()

# Set up view and export image
import FreeCADGui

FreeCADGui.ActiveDocument.ActiveView.viewFront()
FreeCADGui.ActiveDocument.ActiveView.fitAll()

# Rotate view to see the snowman from a good angle (front-ish, slightly to the side)
FreeCADGui.ActiveDocument.ActiveView.viewIsometric()

# Export the image
FreeCADGui.ActiveDocument.ActiveView.saveImage("/home/jfd/prj/snowman/snowman_freecad.png", 1024, 768, "Current")

print("Snowman model created and image exported to snowman_freecad.png")
