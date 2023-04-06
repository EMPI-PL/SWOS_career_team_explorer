# Read squad info from CAR file
from fixes import *
from dict import *
from func import *
import binascii, argparse, subprocess

# Define classes for teams and players
class carteam():
    def __init__(self, clubname, managername, money):
        self.clubname = clubname
        self.managername = managername
        self.money = money

class player():
    def __init__(self, face, number, name, nation, position, skills, val):
        self.face = face
        self.number = number
        self.name = name
        self.nation = nation
        self.position = position
        self.skills = skills        # Individual skills replaced with MATRIX of skills
        self.val = val
    
    def reset(self):
        self.face = None
        self.number = None
        self.name = None
        self.nation = None
        self.position = None
        self.skills = None
        self.val = None

# Force path to CAR file to be given by the user
#parser = argparse.ArgumentParser(description='SWOS career team explorer')
#parser.add_argument('carrer_save_file', metavar='car_file', help='Path to SWOS *.CAR file')
#parser.add_argument('output_file', metavar='output_file', help='Path to output file')
#parser.add_argument('-a', '--amiga', help="Use this for an Amiga *.CAR file")
#args = parser.parse_args()

def readcarfile(inputfile):
    # Actual CAR file HEX reading begins here
    # -----------------------------------------------------------------------------------------------------
    # Define starting blocks for HEXreading
    tm_ofst = 0xDB85        # Club's name (up to 16 hex blocks)
    mn_ofst = 0xDBA4        # Manager's name (up to 16 hex blocks)
    sq_ofst = 0xDBCC        # Starting address to read current CAR file squad
    size_ofst = 0xE08C      # Info on how many players are actually in squad. Max is 30 = 0x1E
    sqcall_ofst = 0xDB60    # Start calling squad members from tm_ofst. Max is 30 calls to size_ofst limit
    ba_ofst = 0xD5DC        # New bank ballance (current amount of money)

    # Amiga HEX addresses stored below for future development (Amiga format differs by 2 bytes)
    #tm_ofst = 0xDB83       # Club's name (up to 16 hex blocks)
    #mn_ofst = 0xDBA2       # Manager's name (up to 16 hex blocks)
    #sq_ofst = 0xDBCA       # Starting address to read current CAR file squad

    footballer = 0  # Number of squad players read from file    
    squad = [('head','number','name','pos','nat','P', 'V', 'H', 'T', 'C', 'S' ,'F', 'value')] # Declare a list for future data feed
    open_infile = open(inputfile, 'r+b').read()                         # Open file in read/binary mode only 
    #inputfile = open(args.carrer_save_file, 'r+b').read()              # Open file in read/binary mode only
    #outputfile = open('path_to_output_file', 'w')                      # Open file for outputs (write mode)
    #outputfile = open(args.output_file, 'w')                           # Open file for outputs (write mode)

    # Team information reader begins here
    # -----------------------------------------------------------------------------------------------------
    # Calculate bank ballance from HEX
    nbb_read = (
        hex2int(hexpure(hexread(open_infile, ba_ofst, 1))),
        hex2int(hexpure(hexread(open_infile, ba_ofst+1, 1))),
        hex2int(hexpure(hexread(open_infile, ba_ofst+2, 1))),
        hex2int(hexpure(hexread(open_infile, ba_ofst+3, 1)))
    )
    bankbalance = nbb_read[0]*1 + nbb_read[1]*256 + nbb_read[2]*65536 + nbb_read[3]*16777216

    teaminfo = carteam(
        hex2ascii(hexcutzeros(hexpure(hexread(open_infile, tm_ofst, 16)))),
        hex2ascii(hexcutzeros(hexpure(hexread(open_infile, mn_ofst, 16)))),
        bankbalance
    )

    # Squad information reader begins here
    # This code definitely needs optimization and tweaking...
    # -----------------------------------------------------------------------------------------------------
    step = 0            # HEX address walker
    gk_flag = False     # Flag to indicate first keeper is already found. This prevents from printing 5 GK's at start of career.
    add_flag = False    # Flag to add data to temptuple
    while step < 30:
        call_mod = hexpure(hexread(open_infile, sqcall_ofst+step, 1))
        call = d_HEX_callplayer[call_mod]
        if call != 0x0000:  # If the call is valid (no FF in hex)
            if call != 0xDBCC:  # If the call is not for GK position
                facepos_val = hex2int(hexpure(hexread(open_infile, call+26, 1)))   # Get decimal value of face/position
                facepos_val_mod = fixposition(facepos_val)                         # Run fixposition to prevent crash due to wrong face/pos numbering
                # Read skills matrix from current browsed player
                matrix = hexpure(open_infile[call+28:call+32])
                matrix = matrix[1:] # Drop initial digit as it's not needed
                gostek = player(            
                    d_posfaceval[facepos_val_mod[1]][2],
                    hex2int(hexcutzeros(hexpure(hexread(open_infile, call+2, 1)))),
                    hex2ascii(hexcutzeros(hexpure(hexread(open_infile, call+3, 23)))),
                    d_AGEdit_nation[hex2int(hexcutzeros(hexpure(hexread(open_infile, call, 1))))],
                    d_posfaceval[facepos_val_mod[1]][0],
                    matrix,  
                    hexpure(hexread(open_infile, call+32, 1)),
                )
                add_flag = True
            elif call == 0xDBCC and gk_flag == False:   # If the call is for GK BUT no GK was spotted so far (00 in HEX)
                facepos_val = hex2int(hexpure(hexread(open_infile, call+26, 1)))   # Get decimal value of face/position
                facepos_val_mod = fixposition(facepos_val)                         # Run fixposition to prevent crash due to wrong face/pos numbering
                # Read skills matrix from current browsed player
                matrix = hexpure(open_infile[call+28:call+32])
                matrix = matrix[1:] # Drop initial digit as it's not needed
                gostek = player(            
                    d_posfaceval[facepos_val_mod[1]][2],
                    hex2int(hexcutzeros(hexpure(hexread(open_infile, call+2, 1)))),
                    hex2ascii(hexcutzeros(hexpure(hexread(open_infile, call+3, 23)))),
                    d_AGEdit_nation[hex2int(hexcutzeros(hexpure(hexread(open_infile, call, 1))))],
                    d_posfaceval[facepos_val_mod[1]][0],
                    matrix,  
                    hexpure(hexread(open_infile, call+32, 1)),
                )
                gk_flag = True  # Mark GK is here. This caused an issue at start of career with numerous slots calling GK (5 slots in HEX with 00 value)
                add_flag = True
            else:
                add_flag = False
            if add_flag == True:
                temptuple=(
                    str(gostek.face),
                    str(gostek.number),
                    str(gostek.name),
                    str(gostek.position),                    
                    str(gostek.nation),
                    str(gostek.skills[0]),
                    str(gostek.skills[1]),
                    str(gostek.skills[2]),
                    str(gostek.skills[3]),
                    str(gostek.skills[4]),
                    str(gostek.skills[5]),
                    str(gostek.skills[6]),
                    str(gostek.val)
                )            
                squad.append(temptuple)
            else:
                pass
            step += 1
            add_flag = False
        else:
            step += 1
            add_flag = False
    
    # Send all info to an output file
    #outputfile.write('Team name: ' + teaminfo.clubname + '\n' + 'Manager name ' + teaminfo.managername + '\n'+ '\n')
    #for list_entry in squad:
    #    list_entry_mod = str(list_entry)
    #    list_entry_mod = list_entry_mod.replace(',',';').replace('(','').replace(')','').replace("'",'')
    #    outputfile.write(list_entry_mod + '\n')
    #outputfile.close()

    return squad, teaminfo
    # Closing statement
    #print('Extract from CAR file completed.' + '\n' + 'Output file saved under: ' + args.output_file + '\n')