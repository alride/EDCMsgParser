# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

pattern = (r'^(\d)'
           r'(\d{6})'
           r'(\d{2})(\d{2})(\d{2})'
           r'(\d{2})(\d{2})(\d{2})'
           r'a(\d{3}|\d{9}|\d{8}|LUNO000)a'
           r'(.*)?'
           r'([0-9A-F]{8})\n$')

# LUNO000

# outformat = r'\1 \2 \4.\3.20\5 \6:\7:\8 \9 \10 \11'
# Full
outformat = r'\1 \2 \4.\3.20\5 \6:\7:\8 \9 \11 \10'
# Short
outformat = r'\1 \2 \4.\3.20\5 \6:\7:\8 \10'
# Short
outformat = r'\4.\3.20\5 \6:\7:\8 \10'

#          r'(a(.*))?[0-9A-F]{8}')

# MMDD-YY-HHMMSS
timestamppattern = r'^\d{7}(\d{4})(\d{2})(\d{6}).*\n$'
# YYMMDDHHMMSS
timestampformat = r'\2\1\3'

datetimeiniformat = '%d.%m.%Y %H:%M:%S'
datetimetoformat = '%y%m%d%H%M%S'

################## MAIN ####################################
import re
import sys
from datetime import datetime
import configparser
from os import path

print(f'EDC log parser v.1\n')

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} filename')
    quit()

inpfilename = path.abspath(sys.argv[1])

if not path.exists(inpfilename):
    print(f'ERROR: File {inpfilename} doesn\'t exist.')
    quit()

print(f'Using config {inpfilename}')
ConfigFileNames = inpfilename

# ini file directory
BaseDir = path.dirname(ConfigFileNames)
config = configparser.ConfigParser(allow_no_value=True)
config.read(ConfigFileNames)
filelist = config['SourceLogFiles'].get('EDCLogFiles').split(',')

TimeFilterIsSetStart = False
TimeStart = config['TimeFilter'].get('TimeStart')
if TimeStart and not TimeStart.isspace():
    TimeStart = datetime.strptime(TimeStart, datetimeiniformat).strftime(datetimetoformat)
    TimeFilterIsSetStart = True

TimeFilterIsSetEnd = False
TimeEnd = config['TimeFilter'].get('TimeEnd')
if TimeEnd and not TimeEnd.isspace():
    TimeEnd = datetime.strptime(TimeEnd, datetimeiniformat).strftime(datetimetoformat)
    TimeFilterIsSetEnd = True

outfilename = config['DestinationDirs'].get('EDCOutFile')
if outfilename and not outfilename.isspace():
    if not path.isabs(outfilename):
        outfilename = path.relpath(outfilename, start=BaseDir)
        outfilename = path.abspath(outfilename)
    print(f'Output to file {outfilename}')
    stdout = sys.stdout
    sys.stdout = open(outfilename, "w", encoding="utf-8")

if TimeStart or TimeEnd:
    print(f'# Filter Date-Time is set: {TimeStart}...{TimeEnd}') # \n

for inpfilename in filelist:
    # inpfilename = path.join(BaseDir, inpfilename)
    inpfilename = inpfilename.lstrip()
    inpfilename = path.relpath(inpfilename, start=BaseDir)
    inpfilename = path.abspath(inpfilename)
    print(f'# Source file: {inpfilename}')  # \n
    try:
        inputstream = open(inpfilename, 'r')
    except IOError:
        print(f'No such file: "{inpfilename}"')
        continue

    # with open(inpfilename, 'r') as inputstream:
    while line := inputstream.readline():
        # replacing
        timestamp = ''
        result = re.match(timestamppattern, line)
        if result:
            timestamp = result.group(2)+result.group(1)+result.group(3)

        # timestamp = re.sub(timestamppattern, timestampformat, line)

        if timestamp and ((TimeFilterIsSetStart and TimeStart > timestamp) or (TimeFilterIsSetEnd and timestamp > TimeEnd)):
            print(f'#{re.sub(pattern, outformat, line)}')
        else:
            print(re.sub(pattern, outformat, line))

    inputstream.close

if stdout:
    sys.stdout.close()
    sys.stdout = stdout

###########################################
# ATM ID - 8 symbols

###########################################
# 0 - STATUS
# 1 - TRANSACTION
# 4 - STATUS