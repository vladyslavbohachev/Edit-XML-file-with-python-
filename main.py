import os
import xml.etree.ElementTree as ET

def configure():
    #Get document directory
    rootdir = 'path_to_your_data'

    #run thru whole directory and search files with the .xml ending
    for filenames in os.walk(rootdir):
        for filename in filenames:
            if filename.endswith('.xml'):
                #initialize the Etree
                tree = ET.parse(os.path.join(rootdir, filename))
                root = tree.getroot()
                #there are many same tags in the xml and we need to select only specific
                #for this case we create id's for the tags and write it to the xml
                for (id, METER1) in enumerate(root.findall('NK/AK/SD/FD/METER1')):
                    METER1.set('ID', str(id))
                tree.write(os.path.join(rootdir, filename))
                #search for how many sendings are inside the order
                find_nr = [(x.find('NR')) for x in tree.findall('.//NR/..')]
                #Search for the information we neet and split it for our purposes
                # and print it out to an array list
                info = []
                for j in root.findall('NK/AK/SD/INFO/ABSINFO1'):
                    split = j.text.split('fp')[0].split('Stellplätze: ')[1]
                    info.append(split)

                # we search for our id's and put this in to a list

                meter1 = []
                for i in root.findall('NK/AK/SD/FD/METER1'):
                    meter1.append(i.text)
                test = tree.findall('NK/AK/SD/FD/METER1[@ID]')
                #create loop for replacement of the selected tags
                for counter in range(len(find_nr)):
                    print(f' OK - - - {filename}: ist', test[counter].text, ' soll', info[counter])
                    if test[counter].text != info[counter] or test[counter] == '0.000':
                        test[counter].text = str(info[counter])
                        tree.write(os.path.join(rootdir, filename))
                #for perfectionists we remove all id's
                for id in root.findall('NK/AK/SD/FD/METER1'):
                    del (id.attrib['ID'])
                tree.write(os.path.join(rootdir, filename))
def main():
    configure()


if __name__ == '__main__':
    main()