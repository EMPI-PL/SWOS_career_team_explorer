def hexread(file, starting_offset, hex):
    # Read HEX values from SWOS CAR file
    tmpdata = file[starting_offset:starting_offset+hex]
    return tmpdata

def hexpure(hexextract):
    # Do some cleaning in extract provided by hexread function
    tmpdata = ["{:02x}".format(b) for b in hexextract]
    tmpdata = str(tmpdata)
    tmpdata = tmpdata.replace(',', '')
    tmpdata = tmpdata.replace('[', '')
    tmpdata = tmpdata.replace(']', '')
    tmpdata = tmpdata.replace(' ', '')
    tmpdata = tmpdata.replace("'", '')
    return tmpdata

def hexcutzeros(hexdata):
    # Cuts zeros out of purified hex data
    # NOTE: This will delete double zeros no matter where they are
    tmpdata = hexdata.replace("00", "")
    return tmpdata

def hex2ascii(hexdata, code='utf-8'):
    # Converts hex data into ascii
    tmpdata = bytes.fromhex(hexdata).decode(code)    
    return tmpdata

def hex2int(hexdata):
    # Converts hex data to decimal
    tmpdata = int(hexdata, 16)
    return tmpdata