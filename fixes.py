# This file will contain any pieces of code that may be needed in terms of "fixing" some readings from the CAR file.

from di import d_posfaceval

def fixposition(decin):
    # Fixes some issues with wrong hex numbering for players under CAR file
    # Sensible World of EDITOR Soccer developed by Whiteulver will not read those
    # positions correctly converting positions to Goalkeepers
    postab = [0, 8, 16, 32, 40, 48, 64, 72, 80, 96, 104, 112, 128, 136, 144, 160, 168, 176, 192, 200, 208, 224, 232, 240]
    poshex = {0: '00', 8: '08', 16: '10', 32: '20', 40: '28', 48: '30', 64: '40', 72: '48', 80: '50', 96: '60',
              104: '68', 112: '70', 128:'80', 136:'88', 144:'90', 160:'a0', 168:'a8', 176:'b0', 192:'c0', 200:'c8',
              208: 'd0', 224:'e0', 232:'e8', 240:'f0'}
    step = 23
    try:
        tmpdata = d_posfaceval[decin][0]
        decout = decin
        hexout = poshex[decout]
    except:
        while step > -1:
            if decin > postab[step]:
                decin = postab[step]
                tmpdata = d_posfaceval[decin][0]
                decout = decin
                hexout = poshex[decout]
                break
            step = step - 1
    return tmpdata, decout, hexout