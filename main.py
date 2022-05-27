import datetime
import os
import shutil
import xml.etree.ElementTree as Et

rootdir = r'X:/'
importdir = r'X:/import'
modifiedDir = r'X:/modified'
cancelledDir = r'X:/cancelled'
acceptedDir = r'X:/BackupRAW'
dailyBackupDir = 'X:/BackupRAW/' + str(datetime.date.today())


def check_dir():
    directorylist = [importdir, modifiedDir, cancelledDir, acceptedDir, dailyBackupDir]
    for items in directorylist:
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
        if rootdir is None:
            exit(0)
        else:
            for filename in files:
                if filename.endswith('.xml'):
                    tree = Et.parse(os.path.join(rootdir, filename))
                    root = tree.getroot()
                    getexternnumber = []
                    for getexternnumberToText in root.findall('NK/AK/SD/EXTNR'):
                        getexternnumber.append(getexternnumberToText.text)
                        if str(getexternnumber).startswith('010'):
                            continue
                        else:
                            rootlist = ['NK/AK/SD/FD/METER1', 'NK/AK/SD/EXTNR', 'NK/AK/SD/EXTTANR']
                            setidlist = ['setStellplaetzeID', 'setExternemummerID', 'setExternetransportnummerID']
                            idlist = ['SID', 'EID', 'ENID']
                            rootid = ['sid', 'eid', 'enid']
                            for i in range(len(rootlist)):
                                for (rootid[i], setidlist[i]) in enumerate(root.findall(rootlist[i])):
                                    setidlist[i].set(idlist[i], str(rootid[i]))
                                tree.write(os.path.join(rootdir, filename))
                            for eml in root.findall('NK/AK/SD/EXTTANR'):
                                newval = Et.SubElement(eml, None)
                                newval.text = ''
                            tree.write(os.path.join(rootdir, filename))
                            splitstp = []
                            splittransnum = []
                            for splitcounter in root.findall('NK/AK/SD/INFO/ABSINFO1'):
                                splitone = splitcounter.text.split('fp')[0].split('Stellplätze: ')[1]
                                splittwo = splitcounter.text.split('Transportnummer: ')[1].split('\\nSAP')[0]
                                splitstp.append(splitone)
                                splittransnum.append(splittwo)
                            getexternemummerdata = []
                            for i in root.findall('NK/AK/SD/EXTNR'):
                                getexternemummerdata.append(i.text)
                            getexternetransportnummerdata = []
                            for j in root.findall('NK/AK/SD/EXTTANR'):
                                getexternetransportnummerdata.append(j)
                            getstpeid = tree.findall('NK/AK/SD/FD/METER1[@SID]')
                            getexttransnumid = tree.findall('NK/AK/SD/EXTTANR[@ENID]')
                            getextnemid = tree.findall('NK/AK/SD/EXTNR[@EID]')
                            for counter in range(len([(x.find('NR')) for x in tree.findall('.//NR/..')])):
                                if getstpeid[counter].text != splitstp[counter] or getstpeid[counter] == '0.000' \
                                        and getexttransnumid[counter] != getexternetransportnummerdata[counter].text \
                                        and getextnemid[counter].text != splittransnum[counter]:
                                    getstpeid[counter].text = str(splitstp[counter])
                                    getexttransnumid[counter].text = str(getexternemummerdata[counter])
                                    getextnemid[counter].text = str(splittransnum[counter])
                                    tree.write(os.path.join(rootdir, filename))
                            for i in range(len(rootlist)):
                                for delid in root.findall(rootlist[i]):
                                    del (delid.attrib[idlist[i]])
                                tree.write(os.path.join(rootdir, filename))
            for filename in [filename for filename in os.listdir(rootdir) if filename.__contains__(str('accepted'))]:
                shutil.move(os.path.join(rootdir, filename), os.path.join(importdir, filename))
        return None


def main():
    check_dir()
    clear_data()
    setup()


if __name__ == '__main__':
    main()
