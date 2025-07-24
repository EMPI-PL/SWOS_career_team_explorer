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

def hexpurgezeros(hexdata):
    # Purge zeros out of purified hex data
    # NOTE: This will delete double zeros no matter where they are
    tmpdata = hexdata.replace("00", "")
    return tmpdata

def hexcutzeros(hexdata):
    # Cut off entire string post initial 00 position
    # NOTE: This will avoid misspelled names in squad
    tmpdata = hexdata[:hexdata.index('00')] 
    #to avoid error if last letter is "P" (i.e. "50" in hex) and hexcutzeros has truncated the last "0"
    if len(tmpdata) % 2 != 0:
        tmpdata += '0'  
    return tmpdata
    
def hex2ascii(hexdata, code='utf-8'):
    # Converts hex data into ascii
    tmpdata = bytes.fromhex(hexdata).decode(code)    
    return tmpdata

def hex2int(hexdata):
    # Converts hex data to decimal
    tmpdata = int(hexdata, 16)
    return tmpdata

def clear_4_XML(input_value):
    # In order to avoid not-well formatted issue, any special chars must be removed
    # TAG names cannot start with numbers, "xml" in any shape and/or form and also cannot contain spaces
    tmpdata = hex2ascii(input_value)        # Converts data to readable format
    tmpdata = tmpdata.replace('. ', '_')    # Takes out any dot+whitespace by repleacing with _
    tmpdata = tmpdata.replace(' ', '_')     # Takes out any remaining whitespaces by repleacing with _    
    tmpdata = tmpdata.replace("'", "")      # Takes out any ' sign
    tmpdata = tmpdata.replace("/", "")      # Takes out any / sign    
    # Add _ if starts with number
    try:
        int(tmpdata[0])
        tmpdata = '_'+tmpdata
    except:
        pass    # Literally DO NOTHING bro :-)
    return tmpdata
