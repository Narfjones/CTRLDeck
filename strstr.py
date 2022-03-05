#---------------------------------------------------------------------------------
#   Receive Serial data, extract slider values, and store them as strings
#---------------------------------------------------------------------------------

def serial_conversion_1(line):

    sliderlst1 = line.split("|")
    try:
        slider1str = str(sliderlst1[0])
    except IndexError:     
        slider1str = 'null'      
    return slider1str

def serial_conversion_2(line):

    sliderlst2 = line.split("|")
    try:
        slider2str = str(sliderlst2[1])
    except IndexError:
        slider2str = 'null'
    return slider2str

def serial_conversion_3(line):

    sliderlst3 = line.split("|")
    try:
        slider3str = str(sliderlst3[2])
    except IndexError:
        slider3str = 'null'
    return slider3str

def serial_conversion_4(line):

    sliderlst4 = line.split("|")
    try:
        slider4str = str(sliderlst4[3])
    except IndexError:
        slider4str = 'null'
    return slider4str
