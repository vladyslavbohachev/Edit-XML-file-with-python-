#!/usr/bin/python
import datetime, os
import shutil
import xml.etree.ElementTree as ET

rootdir = r'X:/'
importdir = r'X:/import'

moddir = r'X:/modified'
candir = r'X:/cancelled'
acpdir = r'X:/BackupRAW'
nowdir = 'X:/BackupRAW/' + str(datetime.date.today())

def check_dir():
    directoryList = [importdir, moddir, candir, acpdir, nowdir]
    for items in directoryList:
        os.makedirs(items, exist_ok=True)
def clear_data():
    filterMod = [filename for filename in os.listdir(rootdir) if filename.__contains__(str('modified'))]
    filterCan = [filename for filename in os.listdir(rootdir) if filename.__contains__(str('cancelled'))]
    filterAcp = [filename for filename in os.listdir(rootdir) if filename.__contains__(str('accepted'))]

    for filename in filterMod:
        path_to_file = os.path.join(rootdir, filename)
        shutil.move(path_to_file, moddir)
    for filename in filterCan:
        path_to_file = os.path.join(rootdir, filename)
        shutil.move(path_to_file, candir)
    for filename in filterAcp:
        path_to_file = os.path.join(rootdir, filename)
        shutil.copy(path_to_file, nowdir)

def setup():
    for root, directories, filenames in os.walk(rootdir):
        for filename in filenames:
            if filename.endswith('.xml'):
                tree = ET.parse(os.path.join(rootdir, filename))
                root = tree.getroot()
                getExternnumber = []
                for getExternnumberToText in root.findall('NK/AK/SD/EXTNR'):
                    getExternnumber.append(getExternnumberToText.text)
                    if str(getExternnumber).startswith('010') and str(getExternnumber).__contains__('0104') or str(getExternnumber).__contains__('0105'):
                        continue
                    else:
                        #Set ID's to relevant datasets
                        for (sid, setStellplaetzeID) in enumerate(root.findall('NK/AK/SD/FD/METER1')):
                            setStellplaetzeID.set('SID', str(sid))
                        tree.write(os.path.join(rootdir, filename))
                        for (eid, setExternemummerID) in enumerate(root.findall('NK/AK/SD/EXTNR')):
                            setExternemummerID.set('EID', str(eid))
                        tree.write(os.path.join(rootdir, filename))
                        for (enid, setExternetransportnummerID) in enumerate(root.findall('NK/AK/SD/EXTTANR')):
                            setExternetransportnummerID.set('ENID', str(enid))
                        tree.write(os.path.join(rootdir, filename))
                        for eml in root.findall('NK/AK/SD/EXTTANR'):
                            newval = ET.SubElement(eml, None)
                            newval.text = ''
                        ET.dump(tree)
                        #count shipments in order
                        getAllShipments = [(x.find('NR')) for x in tree.findall('.//NR/..')]
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
                        for counter in range(len(getAllShipments)):
                            if getStellplaetzeID[counter].text != SplitStellplaetze[counter] or getStellplaetzeID[counter] == '0.000' \
                                    and getExternetransportnummerID[counter] != getExternetransportnummerData[counter].text \
                                    and getExternemummerID[counter].text != SplitTransportnummer[counter]:
                                getStellplaetzeID[counter].text = str(SplitStellplaetze[counter])
                                getExternetransportnummerID[counter].text = str(getExternemummerData[counter])
                                getExternemummerID[counter].text = str(SplitTransportnummer[counter])
                                tree.write(os.path.join(rootdir, filename))
                        for id in root.findall('NK/AK/SD/FD/METER1'):
                            del (id.attrib['SID'])
                        tree.write(os.path.join(rootdir, filename))
                        for id in root.findall('NK/AK/SD/EXTNR'):
                            del (id.attrib['EID'])
                        tree.write(os.path.join(rootdir, filename))
                        for id in root.findall('NK/AK/SD/EXTTANR'):
                            del (id.attrib['ENID'])
                        tree.write(os.path.join(rootdir, filename))
        filterfinal = [filename for filename in os.listdir(rootdir) if filename.__contains__(str('accepted'))]
        for filename in filterfinal:
            path_to_import = os.path.join(rootdir, filename)
            shutil.move(path_to_import, importdir)
def main():
    check_dir()
    clear_data()
    setup()
if __name__ == '__main__':
    main()
