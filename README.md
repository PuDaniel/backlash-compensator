# backlash-compensator
Simple x- and y-axis backlash compensation for a G-Code file

### Usage:
```
python3 remove_backlash.py [-h] [-x BACKLASH_X] [-y BACKLASH_Y] [-t TOLERANCE] in_file [out_file]

positional arguments:
  in_file               Input G-code file
  out_file              Output G-code file, default in_file_nobacklash.nc

optional arguments:
  -h, --help            show this help message and exit
  -x BACKLASH_X, --backlash_x BACKLASH_X
                        Backlash in x-direction, default 0.1 mm
  -y BACKLASH_Y, --backlash_y BACKLASH_Y
                        Backlash in y-direction, default 0.1 mm
  -t TOLERANCE, --tolerance TOLERANCE
                        Tolerance against rounding errors, default 0.005 mm
```
Specify the machine's x- and y-backlash with ``-x`` and ``-y`` input options.  
If no output file is given, a new file is created automatically named: "inputfile_nobacklash.nc"

### Limitations:
Only works for G90 (absolute coordinates) and G17 (X-Y plane).
Only compensates G00, G01, G02 and G03 commands.
