# Snowman Project

3D snowman models in OpenSCAD and FreeCAD.

## Rendering and Verification

### OpenSCAD

Render to PNG (no display required):

```bash
openscad -o snowman.png --autocenter --viewall --imgsize=1024,768 snowman.scad
```

Template for other OpenSCAD files:

```bash
openscad -o OUTPUT.png --autocenter --viewall --imgsize=1024,768 INPUT.scad
```

### FreeCAD

FreeCAD GUI scripts require xvfb for headless rendering. Use the verification script:

```bash
./verify_freecad.sh          # 15 second timeout (default)
./verify_freecad.sh 10       # custom timeout in seconds
```

Or render manually:

```bash
# Clear any active virtual environment first
unset VIRTUAL_ENV VIRTUAL_ENV_PROMPT
export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v '\.venv' | tr '\n' ':' | sed 's/:$//')

# Create wrapper that exits cleanly (FreeCAD GUI doesn't exit on script completion)
cat > /tmp/wrapper.py << 'EOF'
import os
exec(open("snowman_freecad.py").read())
os._exit(0)
EOF

timeout 15 xvfb-run -a freecad /tmp/wrapper.py
```

Template for other FreeCAD scripts:

```bash
cat > /tmp/wrapper.py << 'EOF'
import os
exec(open("YOUR_SCRIPT.py").read())
os._exit(0)
EOF

timeout 15 xvfb-run -a freecad /tmp/wrapper.py
```

### Key Notes

- FreeCAD scripts using `FreeCADGui` require GUI mode via xvfb
- FreeCAD does not exit after script completion; use `os._exit(0)` in a wrapper
- `sys.exit()` does not work due to Qt event loop; must use `os._exit()`
- Virtual environments can interfere with FreeCAD startup; clear them before running
- OpenSCAD renders headless without xvfb

## Output Files

- `snowman.png` - OpenSCAD render
- `snowman_freecad.png` - FreeCAD render
- `snowman.scad` - OpenSCAD source
- `snowman_freecad.py` - FreeCAD Python source
