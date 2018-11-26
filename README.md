# backlash-compensator
Simple x- and y-axis backlash compensation for a G-Code file

Specify the machine's x- and y-backlash at the beginning of the file

Usage: "python remove_backlash inputfile [outputfile]"

If no output file is given, a new file is created automatically named: "inputfile_nobacklash.nc"

Only works for G90 (absolute coordinates) and G17 (X-Y plane).
Only compensates G00, G01, G02 and G03 commands.
