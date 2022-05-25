#!/usr/bin/python
import datetime, os
import shutil
import xml.etree.ElementTree as ET

rootdir = r'X:/'
importdir = r'X:/import'

modifiedDir = r'X:/modified'
cancelledDir = r'X:/cancelled'
acceptedDir = r'X:/BackupRAW'
dailyBackupDir = 'X:/BackupRAW/' + str(datetime.date.today())

def check_dir():
    directoryList = [importdir, modifiedDir, cancelledDir, acceptedDir, dailyBackupDir]
    for items in directoryList:
        os.makedirs(items, exist_ok=True)
def clear_data():
    for filename in [filename for filename in os.listdir(rootdir) if filename.__contains__(str('modified'))]:
        shutil.move(os.path.join(rootdir, filename), modifiedDir)
    for filename in [filename for filename in os.listdir(rootdir) if filename.__contains__(str('cancelled'))]:
        shutil.move(os.path.join(rootdir, filename), cancelledDir)
    for filename in [filename for filename in os.listdir(rootdir) if filename.__contains__(str('accepted'))]:
        shutil.copy(os.path.join(rootdir, filename), dailyBackupDir)
def setup():
    for root, dirs, files in os.walk(rootdir):
        print('root:', root, 'dirs:', dirs, 'files:', files)
        if(rootdir == None):
            exit(0)
        else:
            for filename in files:
                if filename.endswith('.xml'):
                    tree = ET.parse(os.path.join(rootdir,filename))
                    root = tree.getroot()
                    getExternnumber = []
                    for getExternnumberToText in root.findall('NK/AK/SD/EXTNR'):
                        getExternnumber.append(getExternnumberToText.text)
                        if str(getExternnumber).startswith('010') or \
                                str(getExternnumber).__contains__('0104') or \
                                str(getExternnumber).__contains__('0105'):
                            continue
                        else:
                            #Set ID's to relevant datasets
                            rootList = ['NK/AK/SD/FD/METER1', 'NK/AK/SD/EXTNR', 'NK/AK/SD/EXTTANR']
                            setIDList = ['setStellplaetzeID', 'setExternemummerID', 'setExternetransportnummerID']
                            idList = ['SID', 'EID', 'ENID']
                            id = ['sid', 'eid', 'enid']
                            for i in range(len(rootList)):
                                for (id[i], setIDList[i]) in enumerate(root.findall(rootList[i])):
                                    setIDList[i].set(idList[i],str(id[i]))
                                tree.write(os.path.join(rootdir, filename))

                            for eml in root.findall('NK/AK/SD/EXTTANR'):
                                newval = ET.SubElement(eml, None)
                                newval.text = ''
                            tree.write(os.path.join(rootdir, filename))
                            # Splits
                            SplitStellplaetze = []
                            SplitTransportnummer = []
                            for splitcounter in root.findall('NK/AK/SD/INFO/ABSINFO1'):
                                splitone = splitcounter.text.split('fp')[0].split('Stellplätze: ')[1]
                                splittwo = splitcounter.text.split('Transportnummer: ')[1].split('\\nSAP')[0]
                                SplitStellplaetze.append(splitone)
                                SplitTransportnummer.append(splittwo)
                            # Get Data
                            getExternemummerData = []
                            for i in root.findall('NK/AK/SD/EXTNR'):
                                getExternemummerData.append(i.text)
                            getExternetransportnummerData = []
                            for j in root.findall('NK/AK/SD/EXTTANR'):
                                getExternetransportnummerData.append(j)
                            # Get Data from ID's
                            getStellplaetzeID = tree.findall('NK/AK/SD/FD/METER1[@SID]')
                            getExternetransportnummerID = tree.findall('NK/AK/SD/EXTTANR[@ENID]')
                            getExternemummerID = tree.findall('NK/AK/SD/EXTNR[@EID]')
                            for counter in range(len([(x.find('NR')) for x in tree.findall('.//NR/..')])):
                                if getStellplaetzeID[counter].text != SplitStellplaetze[counter] or getStellplaetzeID[counter] == '0.000' \
                                        and getExternetransportnummerID[counter] != getExternetransportnummerData[counter].text \
                                        and getExternemummerID[counter].text != SplitTransportnummer[counter]:
                                    getStellplaetzeID[counter].text = str(SplitStellplaetze[counter])
                                    getExternetransportnummerID[counter].text = str(getExternemummerData[counter])
                                    getExternemummerID[counter].text = str(SplitTransportnummer[counter])
                                    tree.write(os.path.join(rootdir, filename))
                            for i in range(len(rootList)):
                                for id in root.findall(rootList[i]):
                                    del (id.attrib[idList[i]])
                                tree.write(os.path.join(rootdir, filename))

            for filename in [filename for filename in os.listdir(rootdir) if filename.__contains__(str('accepted'))]:
                shutil.move(os.path.join(rootdir, filename), importdir)
        return None
def main():
    check_dir()
    clear_data()
    setup()
if __name__ == '__main__':
    main()
