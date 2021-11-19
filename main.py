import os
import shutil
import xml.etree.ElementTree as ET

moddir = '1_modified'
candir = '1_cancelled'
rootdir = 'mainData'

def check_dir():
    isExistMod = os.path.exists(moddir)
    isExistCan = os.path.exists(candir)

    if not isExistMod:
        os.makedirs(moddir)
    if not isExistCan:
        os.makedirs(candir)

def clear_data():
    filterMod = [filename for filename in os.listdir(rootdir) if filename.__contains__('modified')]
    filterCan = [filename for filename in os.listdir(rootdir) if filename.__contains__('cancelled')]

    for filename in filterMod:
        path_to_file = os.path.join(rootdir,filename)
        shutil.move(path_to_file, moddir)
    for filename in filterCan:
        path_to_file = os.path.join(rootdir, filename)
        shutil.move(path_to_file, candir)

def configure():
    for root, directories, filenames in os.walk(rootdir):
        for filename in filenames:
            if filename.endswith('.xml'):
                tree = ET.parse(os.path.join(rootdir,filename))
                root = tree.getroot()
                for (id, METER1) in enumerate(root.findall('NK/AK/SD/FD/METER1')):
                    METER1.set('ID',str(id))
                tree.write(os.path.join(rootdir, filename))

                for (id_n, EXTNER) in enumerate(root.findall('NK/AK/SD/EXTNR')):
                    EXTNER.set('NR', str(id_n))
                tree.write(os.path.join(rootdir,filename))

                for (id_exttarn, tarn) in enumerate(root.findall('NK/AK/SD/EXTTANR')):
                    tarn.set('ANR', str(id_exttarn))
                tree.write(os.path.join(rootdir,filename))
                for eml in root.findall('NK/AK/SD/EXTTANR'):
                    newval = ET.SubElement(eml, None)
                    newval.text = ''
                ET.dump(tree)
                find_nr = [(x.find('NR')) for x in tree.findall('.//NR/..')]
                info = []
                for j in root.findall('NK/AK/SD/INFO/ABSINFO1'):
                    split = j.text.split('fp')[0].split('Stellplätze: ')[1]
                    info.append(split)
                meter1 = []
                for i in root.findall('NK/AK/SD/FD/METER1'):
                    meter1.append(i.text)
                test = tree.findall('NK/AK/SD/FD/METER1[@ID]')
                for counter in range(len(find_nr)):
                    print(f'OK - - - {filename}: ist', test[counter].text, ' soll', info[counter])
                    if test[counter].text != info[counter] or test[counter] == '0.000':
                        test[counter].text = str(info[counter])
                        tree.write(os.path.join(rootdir,filename))

                EXTNR_1 = []
                for d in root.findall('NK/AK/SD/EXTNR'):
                    EXTNR_1.append(d.text)

                exttarn = []
                for s in root.findall('NK/AK/SD/EXTTANR'):
                    exttarn.append(s)
                tarn = tree.findall('NK/AK/SD/EXTTANR[@ANR]')

                for counter in range(len(find_nr)):
                    print('Das ist EXTTARN', tarn[counter].text, ' soll', EXTNR_1[counter])
                    if tarn[counter] == exttarn[counter].text:
                        continue
                    else:
                        tarn[counter].text = str(EXTNR_1[counter])
                        tree.write(os.path.join(rootdir,filename))
                extner = []
                for l in root.findall('NK/AK/SD/EXTNR'):
                    extner.append(l.text)
                num = []
                for q in root.findall('NK/AK/SD/INFO/ABSINFO1'):
                    split_num = q.text.split('Transportnummer: ')[1].split('\\nSAP')[0]
                    num.append(split_num)
                num_list = tree.findall('NK/AK/SD/EXTNR[@NR]')
                for counter in range(len(find_nr)):
                    print('Das ist die EXTNR', num_list[counter].text, ' soll', num[counter])
                    if num_list[counter].text != num[counter]:
                        num_list[counter].text = str(num[counter])
                        tree.write(os.path.join(rootdir, filename))

                for id in root.findall('NK/AK/SD/FD/METER1'):
                    del (id.attrib['ID'])
                tree.write(os.path.join(rootdir,filename))
                for id in root.findall('NK/AK/SD/EXTNR'):
                    del (id.attrib['NR'])
                tree.write(os.path.join(rootdir,filename))
                for id in root.findall('NK/AK/SD/EXTTANR'):
                    del (id.attrib['ANR'])
                tree.write(os.path.join(rootdir,filename))
def main ():
    check_dir()
    clear_data()
    configure()

if __name__ == '__main__':
    main()
