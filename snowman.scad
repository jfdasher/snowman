// Snowman 3D Model
// Three spheres for body, two cylinders for hat, cone for nose, hemispheres for eyes and buttons
// Plus a jaunty corn-cob pipe

$fn = 64; // Smooth curves

// Sphere sizes (descending)
body_radius = 50;
chest_radius = 38;
head_radius = 28;

// Sphere positions (z-aligned, intersecting)
body_z = body_radius;
chest_z = body_z + body_radius * 0.7 + chest_radius * 0.7;
head_z = chest_z + chest_radius * 0.7 + head_radius * 0.7;

// Hat parameters
hat_pipe_radius = head_radius * 0.6;
hat_pipe_height = head_radius * 1.2;
hat_brim_radius = head_radius * 0.9;
hat_brim_height = 3;
hat_z = head_z + head_radius * 0.85;

// Nose parameters
nose_radius = 6;
nose_length = 25;

// Eye and button parameters
eye_radius = 4;
button_radius = 5;

// Corn-cob pipe parameters
pipe_bowl_radius = 6;
pipe_bowl_height = 12;
pipe_bowl_inner_radius = 4;
pipe_bowl_inner_depth = 8;
pipe_stem_radius = 2.5;
pipe_stem_length = 25;

// Module for hemisphere
module hemisphere(r) {
    difference() {
        sphere(r);
        translate([0, 0, -r])
            cube([2*r, 2*r, 2*r], center=true);
    }
}

// Body (bottom sphere)
color("white")
translate([0, 0, body_z])
    sphere(body_radius);

// Chest (middle sphere)
color("white")
translate([0, 0, chest_z])
    sphere(chest_radius);

// Head (top sphere)
color("white")
translate([0, 0, head_z])
    sphere(head_radius);

// Hat - Stovepipe (tall cylinder)
color("black")
translate([0, 0, hat_z])
    cylinder(h=hat_pipe_height, r=hat_pipe_radius);

// Hat - Brim (flat thin cylinder)
color("black")
translate([0, 0, hat_z])
    cylinder(h=hat_brim_height, r=hat_brim_radius);

// Nose (cone) - pointing forward (negative Y direction)
color("orange")
translate([0, -head_radius, head_z])
rotate([90, 0, 0])
    cylinder(h=nose_length, r1=nose_radius, r2=0);

// Eyes (hemispheres on head, aligned tangent to head sphere)
// Eyes positioned looking forward
eye_angle = 20; // degrees from center
eye_height_offset = head_radius * 0.2;

color("black")
translate([head_radius * sin(eye_angle), -head_radius * cos(eye_angle) * 0.95, head_z + eye_height_offset])
rotate([90, 0, 0])
    hemisphere(eye_radius);

color("black")
translate([-head_radius * sin(eye_angle), -head_radius * cos(eye_angle) * 0.95, head_z + eye_height_offset])
rotate([90, 0, 0])
    hemisphere(eye_radius);

// Buttons (3 hemispheres on chest, aligned tangent to chest sphere)
button_spacing = chest_radius * 0.35;

color("black")
translate([0, -chest_radius * 0.98, chest_z + button_spacing])
rotate([90, 0, 0])
    hemisphere(button_radius);

color("black")
translate([0, -chest_radius * 0.98, chest_z])
rotate([90, 0, 0])
    hemisphere(button_radius);

color("black")
translate([0, -chest_radius * 0.98, chest_z - button_spacing])
rotate([90, 0, 0])
    hemisphere(button_radius);

// Corn-cob pipe (held jauntily)
// Mouth position is starting point, pipe extends outward
mouth_x = head_radius * 0.4;
mouth_y = -head_radius * 0.95;
mouth_z = head_z - head_radius * 0.35;

// Pipe angles outward and upward jauntily
translate([mouth_x, mouth_y, mouth_z])
rotate([0, 0, -50]) // angle to the side (away from face)
rotate([25, 0, 0]) { // tilt the whole pipe upward jauntily
    // Pipe stem (dark brown) - horizontal, extending outward from mouth
    color("SaddleBrown")
    rotate([90, 0, 0])
        cylinder(h=pipe_stem_length, r=pipe_stem_radius);

    // Pipe bowl (corn cob) - at far end of stem, pointing upward
    color("tan")
    translate([0, -pipe_stem_length, -pipe_bowl_height * 0.3])
    difference() {
        cylinder(h=pipe_bowl_height, r=pipe_bowl_radius);
        translate([0, 0, pipe_bowl_height - pipe_bowl_inner_depth])
            cylinder(h=pipe_bowl_inner_depth + 1, r=pipe_bowl_inner_radius);
    }
}
