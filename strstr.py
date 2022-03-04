#---------------------------------------------------------------------------------
#   Receive Serial data, extract slider values, and store them as strings
#---------------------------------------------------------------------------------

def serial_conversion_1(line):

    sliderlst1 = line.split("|")

    slider1str = str(sliderlst1[0])
               
    return slider1str

def serial_conversion_2(line):

    sliderlst2 = line.split("|")

    slider2str = str(sliderlst2[1])

    return slider2str

def serial_conversion_3(line):

    sliderlst3 = line.split("|")

    slider3str = str(sliderlst3[2])

    return slider3str

def serial_conversion_4(line):

    sliderlst4 = line.split("|")

    slider4str = str(sliderlst4[3])

    return slider4str
