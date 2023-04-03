# Read squad info from CAR file
from fixes import *
from dict import *
from func import *
import binascii, argparse

# Define classes for teams and players
class carteam():
    def __init__(self, clubname, managername):
        self.clubname = clubname
        self.managername = managername

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
parser = argparse.ArgumentParser(description='SWOS career team explorer')
parser.add_argument('carrer_save_file', metavar='car_file', help='Path to SWOS *.CAR file')
parser.add_argument('output_file', metavar='output_file', help='Path to output file')
#parser.add_argument('-a', '--amiga', help="Use this for an Amiga *.CAR file")
args = parser.parse_args()

# Actual reader code begins here
# -----------------------------------------------------------------------------------------------------
# Define starting blocks for HEXreading
tm_ofst = 0xDB85 # Club's name (up to 16 hex blocks)
mn_ofst = 0xDBA4 # Manager's name (up to 16 hex blocks)
sq_ofst = 0xDBCC # Starting address to read current CAR file squad

# Amiga HEX addresses stored below for future development (Amiga format differs by 2 bytes)
#tm_ofst = 0xDB83 # Club's name (up to 16 hex blocks)
#mn_ofst = 0xDBA2 # Manager's name (up to 16 hex blocks)
#sq_ofst = 0xDBCA # Starting address to read current CAR file squad

footballer = 0  # Number of squad players read from file
squad = [('head','number','pos','name','nat','P', 'V', 'H', 'T', 'C', 'S' ,'F', 'value')] # Declare a list for future data feed
inputfile = open(args.carrer_save_file, 'r+b').read()   # Open file in read/binary mode only
outputfile = open(args.output_file, 'w')                # Open file for outputs (write mode)
                                                        # Above may be changed as soon as GUI will be available

# Team information reader begins here
# -----------------------------------------------------------------------------------------------------
myteam = carteam(
    hex2ascii(hexcutzeros(hexpure(hexread(inputfile, tm_ofst, 16)))),
    hex2ascii(hexcutzeros(hexpure(hexread(inputfile, mn_ofst, 16))))
)

# Squad information reader begins here
# -----------------------------------------------------------------------------------------------------
while footballer < 31:
    sq_ofst_mod = sq_ofst + (38 * footballer)   # Increment basic offset each iteracion over team squad
    name_chk = hex2ascii(hexcutzeros(hexpure(hexread(inputfile, sq_ofst_mod+3, 5)))) # Get initial 5 letters of player's name
    if name_chk != '':  # If these 5 bytes are emtpy - escape the loop
        facepos_val = hex2int(hexpure(hexread(inputfile, sq_ofst_mod+26, 1)))   # Get decimal value of face/position
        facepos_val_mod = fixposition(facepos_val)                              # Run fixposition to prevent crash due to wrong face/pos numbering
        if name_chk != '*ERR*': # Player's name doesn't start with *ERR* which indicates not member of squad anymore        
            # Read skills matrix from current browsed player
            matrix = hexpure(inputfile[sq_ofst_mod+28:sq_ofst_mod+32])
            matrix = matrix[1:] # Drop initial digit as it's not needed
            gostek = player(            
                d_posfaceval[facepos_val_mod[1]][1],
                hex2int(hexcutzeros(hexpure(hexread(inputfile, sq_ofst_mod+2, 1)))),
                hex2ascii(hexcutzeros(hexpure(hexread(inputfile, sq_ofst_mod+3, 23)))),
                d_AGEdit_nation[hex2int(hexcutzeros(hexpure(hexread(inputfile, sq_ofst_mod, 1))))],
                d_posfaceval[facepos_val_mod[1]][0],
                matrix,  
                'value'
            )
            temptuple=(
                str(gostek.face),
                str(gostek.number),
                str(gostek.position),
                str(gostek.name),
                str(gostek.nation),
                str(gostek.skills[0]),
                str(gostek.skills[1]),
                str(gostek.skills[2]),
                str(gostek.skills[3]),
                str(gostek.skills[4]),
                str(gostek.skills[5]),
                str(gostek.skills[6]),
                gostek.val)            
            squad.append(temptuple)            
            footballer += 1
            gostek.reset()
        else:
            footballer += 1
            gostek.reset()
    else:
        gostek.reset()
        break

# Send all info to an output file
outputfile.write('Team name: ' + myteam.clubname + '\n' + 'Manager name ' + myteam.managername + '\n'+ '\n')
for list_entry in squad:
    list_entry_mod = str(list_entry)
    list_entry_mod = list_entry_mod.replace(',',';').replace('(','').replace(')','').replace("'",'')
    outputfile.write(list_entry_mod + '\n')
outputfile.close()

# Closing statement
print('Extract from CAR file completed.' + '\n' + 'Output file saved under: ' + args.output_file + '\n')