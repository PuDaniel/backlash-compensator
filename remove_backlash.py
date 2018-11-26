#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  remove_backlash.py
#  
#  Copyright 2018 Daniel Pusztai
#  

import sys
import os.path

# Global variables
backlash_x = 0.202          # Backlash in x-direction
backlash_y = 0.045          # Backlash in y-direction

tol = 0.005                 # Tolerance against rounding errors

# Get the G word in a sentence (line)
def get_G(sentence):
    if ('G00 ' in sentence) or ('G0 ' in sentence):
        return 0
    elif ('G01 ' in sentence) or ('G1 ' in sentence):
        return 1
    elif ('G02 ' in sentence) or ('G2 ' in sentence):
        return 2
    elif ('G03 ' in sentence) or ('G3 ' in sentence):
        return 3
    else:
        return None
        
# Insert a whitespace in front of parameter if there isn't any
def fix_whitespace(sentence, parameter):
    pos = sentence.find(parameter)
   
    if pos > 0:
        if sentence[pos - 1] != ' ':
            sentence = sentence[0:pos] + ' ' + sentence[pos:]
    
    return sentence

# Get the X coordinate in a sentence (line)
def get_X(sentence):
    if 'X' in sentence:
        start = sentence.find('X') + 1
        end = sentence.find(' ', start)
        return float(sentence[start:end])
    else:
        return None
    
# Get the Y coordinate in a sentence (line)
def get_Y(sentence):
    if 'Y' in sentence:
        start = sentence.find('Y') + 1
        end = sentence.find(' ', start)
        return float(sentence[start:end])
    else:
        return None
    
# Get the I coordinate in a sentence (line)
def get_I(sentence):
    if 'I' in sentence:
        start = sentence.find('I') + 1
        end = sentence.find(' ', start)
        return float(sentence[start:end])
    else:
        return None
    
# Get the J coordinate in a sentence (line)
def get_J(sentence):
    if 'J' in sentence:
        start = sentence.find('J') + 1
        end = sentence.find(' ', start)
        return float(sentence[start:end])
    else:
        return None

# Get feedrate word in a sentence (line)
def get_F(sentence):
    if 'F' in sentence:
        start = sentence.find('F') + 1
        end = sentence.find(' ', start)
        return float(sentence[start:end])
    else:
        return None

# Get the starting Quadrant, the given coordinates are in, 
# with respect to circle center and rotation direction
def get_start_quadrant(G, X, Y, X_center, Y_center):
    if (X - X_center) > tol:
        if (Y - Y_center) > tol:
            return 1
        elif (Y - Y_center) < -tol:
            return 4
        else:
            if G == 2:
                return 4
            else:
                return 1
    elif (X - X_center) < -tol:
        if (Y - Y_center) > tol:
            return 2
        elif (Y - Y_center) < -tol:
            return 3
        else:
            if G == 2:
                return 2
            else:
                return 3
    else:
        if (Y - Y_center) > tol:
            if G == 2:
                return 1
            else:
                return 2
        elif (Y - Y_center) < -tol:
            if G == 2:
                return 3
            else:
                return 4
        else:
            return None

# Get the ending Quadrant, the given coordinates are in, 
# with respect to circle center and rotation direction
def get_end_quadrant(G, X, Y, X_center, Y_center):
    if (X - X_center) > tol:
        if (Y - Y_center) > tol:
            return 1
        elif (Y - Y_center) < -tol:
            return 4
        else:
            if G == 2:
                return 1
            else:
                return 4
    elif (X - X_center) < -tol:
        if (Y - Y_center) > tol:
            return 2
        elif (Y - Y_center) < -tol:
            return 3
        else:
            if G == 2:
                return 3
            else:
                return 2
    else:
        if (Y - Y_center) > tol:
            if G == 2:
                return 2
            else:
                return 1
        elif (Y - Y_center) < -tol:
            if G == 2:
                return 4
            else:
                return 3
        else:
            return None

# Replace the X coordinate value in a sentence (line)
def replace_X(sentence, value):
    if 'X' in sentence:
        start = sentence.find('X') + 1
        end = sentence.find(' ', start)
        return (sentence[0:start] + '%.3f' %value + sentence[end:])
    else:
        return sentence

# Replace the Y coordinate value in a sentence (line)
def replace_Y(sentence, value):
    if 'Y' in sentence:
        start = sentence.find('Y') + 1
        end = sentence.find(' ', start)
        return (sentence[0:start] + '%.3f' %value + sentence[end:])
    else:
        return sentence
        
# Replace the I coordinate value in a sentence (line)
def replace_I(sentence, value):
    if 'I' in sentence:
        start = sentence.find('I') + 1
        end = sentence.find(' ', start)
        return (sentence[0:start] + '%.3f' %value + sentence[end:])
    else:
        return sentence
        
# Replace the J coordinate value in a sentence (line)
def replace_J(sentence, value):
    if 'J' in sentence:
        start = sentence.find('J') + 1
        end = sentence.find(' ', start)
        return (sentence[0:start] + '%.3f' %value + sentence[end:])
    else:
        return sentence

if __name__ == '__main__':
    # Check if there is at least one command line argument
    if len(sys.argv) < 2:
        raise Exception('Not enough input arguments!\n' 
            'Usage: remove_backlash inputfile [outputfile]')
         
    # Get the first filename (input file) and check if file exists
    input_file_name = sys.argv[1]
    if not os.path.isfile(input_file_name):
        raise Exception('%s is not a valid file!' %input_file_name)
        
    # Check if there is a second filename and set the output file
    if len(sys.argv) > 2:
        output_file_name = sys.argv[2]
    else:
        output_file_name = input_file_name.split('.')[-2] + '_nobacklash.' + input_file_name.split('.')[-1]
        
    # Open input file and read all lines
    with open(input_file_name, 'r') as input_file:
        gcode = input_file.readlines()
    
    # Check if file is already backlash compensated
    if ';--+--BACKLASH COMPENSATED--+--\n' in gcode:
        print('File has already been backlash compensated! => Nothing to do!')
        quit()
    
    # Search for some possible traps in the G-Code
    for line in range(len(gcode)):
        if 'G91' in gcode[line]:
            print('WARNING: G91 issued in line #%d' %(line + 1))
        
        if 'G18' in gcode[line]:
            print('WARNING: G18 issued in line #%d' %(line + 1))
        
        if 'G19' in gcode[line]:
            print('WARNING: G19 issued in line #%d' %(line + 1))
        
        if 'G20' in gcode[line]:
            print('WARNING: G20 issued in line #%d' %(line + 1))
    
    # Correct the whitespaces
    for line in range(len(gcode)):
        gcode[line] = fix_whitespace(gcode[line], 'X')
        gcode[line] = fix_whitespace(gcode[line], 'Y')
        gcode[line] = fix_whitespace(gcode[line], 'I')
        gcode[line] = fix_whitespace(gcode[line], 'J')
            
    # Split all arcs into quadrants
    x = 0
    y = 0
    
    line = 0
    
    while line < len(gcode):
        # Get the new coordinates
        if get_X(gcode[line]) != None:
            x_new = get_X(gcode[line])
        else:
            x_new = x
            
        if get_Y(gcode[line]) != None:
            y_new = get_Y(gcode[line])
        else:
            y_new = y
        
         # Check for arc move commands
        if (get_G(gcode[line]) == 2) or (get_G(gcode[line]) == 3):
            # Get arc center and radius
            i = get_I(gcode[line])
            j = get_J(gcode[line])
            
            x_center = x + i
            y_center = y + j
            
            r = (i**2 + j**2)**0.5
            
            # Get start and end quadrants
            start = get_start_quadrant(get_G(gcode[line]), x, y, x_center, y_center)
            
            if (x != x_new) and (y != y_new):
                end = get_end_quadrant(get_G(gcode[line]), x_new, y_new, x_center, y_center)
            else:
                # Full circle
                if get_G(gcode[line]) == 2:
                    end = (start % 4) + 1
                else:
                    end = ((start - 2) % 4) + 1
                    
            # Split the arc if it stretches over multiple quadrants
            if start != end:
                # Recover  feedrates
                if get_F(gcode[line]) != None:
                    gcode.insert(line, 'F%.1f\n' %get_F(gcode[line]))
                    line += 1
                
                if get_G(gcode[line]) == 2:
                    # Clockwise arc
                    if start == 1:
                        gcode[line] = 'G2 X%.3f Y%.3f I%.3f J%.3f\n' %(x_center + r, y_center, i, j)
                        gcode.insert(line + 1, 'G2 X%.3f Y%.3f I%.3f J%.3f\n' %(x_new, y_new, -r, 0))
                        x_new = x_center + r
                        y_new = y_center
                    elif start == 2:
                        gcode[line] = 'G2 X%.3f Y%.3f I%.3f J%.3f\n' %(x_center, y_center + r, i, j)
                        gcode.insert(line + 1, 'G2 X%.3f Y%.3f I%.3f J%.3f\n' %(x_new, y_new, 0, -r))
                        x_new = x_center
                        y_new = y_center + r
                    elif start == 3:
                        gcode[line] = 'G2 X%.3f Y%.3f I%.3f J%.3f\n' %(x_center - r, y_center, i, j)
                        gcode.insert(line + 1, 'G2 X%.3f Y%.3f I%.3f J%.3f\n' %(x_new, y_new, r, 0))
                        x_new = x_center - r
                        y_new = y_center
                    else:
                        gcode[line] = 'G2 X%.3f Y%.3f I%.3f J%.3f\n' %(x_center, y_center - r, i, j)
                        gcode.insert(line + 1, 'G2 X%.3f Y%.3f I%.3f J%.3f\n' %(x_new, y_new, 0, r))
                        x_new = x_center
                        y_new = y_center - r
                else:
                    # Counterclockwise arc
                    if start == 1:
                        gcode[line] = 'G3 X%.3f Y%.3f I%.3f J%.3f\n' %(x_center, y_center + r, i, j)
                        gcode.insert(line + 1, 'G3 X%.3f Y%.3f I%.3f J%.3f\n' %(x_new, y_new, 0, -r))
                        x_new = x_center
                        y_new = y_center + r
                    elif start == 2:
                        gcode[line] = 'G3 X%.3f Y%.3f I%.3f J%.3f\n' %(x_center - r, y_center, i, j)
                        gcode.insert(line + 1, 'G3 X%.3f Y%.3f I%.3f J%.3f\n' %(x_new, y_new, r, 0))
                        x_new = x_center - r
                        y_new = y_center
                    elif start == 3:
                        gcode[line] = 'G3 X%.3f Y%.3f I%.3f J%.3f\n' %(x_center, y_center - r, i, j)
                        gcode.insert(line + 1, 'G3 X%.3f Y%.3f I%.3f J%.3f\n' %(x_new, y_new, 0, r))
                        x_new = x_center
                        y_new = y_center - r
                    else:
                        gcode[line] = 'G3 X%.3f Y%.3f I%.3f J%.3f\n' %(x_center + r, y_center, i, j)
                        gcode.insert(line + 1, 'G3 X%.3f Y%.3f I%.3f J%.3f\n' %(x_new, y_new, -r, 0))
                        x_new = x_center + r
                        y_new = y_center
        
        # Store the new coordinates
        x = x_new
        y = y_new
        
        line += 1
    
    # Compensate the backlash in the G-Code
    x = 0
    y = 0
    i = 0
    j = 0
    
    x_dir = 1
    y_dir = 1
    
    line = 0
    
    while line < len(gcode):
        # Get the new coordinates
        if get_X(gcode[line]) != None:
            x_new = get_X(gcode[line])
        else:
            x_new = x
            
        if get_Y(gcode[line]) != None:
            y_new = get_Y(gcode[line])
        else:
            y_new = y
        
        if get_I(gcode[line]) != None:
            i = get_I(gcode[line])
            
        if get_J(gcode[line]) != None:
            j = get_J(gcode[line])
        
        # Check if there is a direction change
        if (x_new < x) and (x_dir > 0):
            # X direction changed from positive to negative
            gcode.insert(line, 'G1 X%.3f\n' %(x - backlash_x))
            x_dir = -1
            line += 1
        elif (x_new > x) and (x_dir < 0):
            # X direction changed from negative to positive
            gcode.insert(line, 'G1 X%.3f\n' %x)
            x_dir = 1
            line += 1
        
        if (y_new < y) and (y_dir > 0):
            # Y direction changed from positive to negative
            gcode.insert(line, 'G1 Y%.3f\n' %(y - backlash_y))
            y_dir = -1
            line += 1
        elif (y_new > y) and (y_dir < 0):
            # Y direction changed from negative to positive
            gcode.insert(line, 'G1 Y%.3f\n' %y)
            y_dir = 1
            line += 1
        
        # Add the backlash for negative directions
        if x_dir < 0:
            gcode[line] = replace_X(gcode[line], x_new - backlash_x)
        if y_dir < 0:
            gcode[line] = replace_Y(gcode[line], y_new - backlash_y)
        
        # Store the new coordinates
        x = x_new
        y = y_new
        
        line += 1
    
    # Add the compensation header
    gcode.insert(0, ';--+--BACKLASH COMPENSATED--+--\n')
    gcode.insert(1, '; Zero is defined when driving from negative X/Y to zero X/Y\n')
    gcode.insert(2, 'G90 G17\n')
    gcode.insert(3, 'G0 X-1 Y-1\n')
    gcode.insert(4, 'G0 X0 Y0\n')
    
    # Write the modified G-Code to the output file
    with open(output_file_name, 'w') as output_file:
        output_file.writelines(gcode)
        
    print('Backlash compensation successful!')
    print('X-Backlash: %.3fmm' %backlash_x)
    print('Y-Backlash: %.3fmm' %backlash_y)
    print('Results saved under %s' %output_file_name)
    
