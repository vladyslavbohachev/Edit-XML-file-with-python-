
**Aufgaben import anpassung**

Set word directories

```python
rootdir = r'X:/'
importdir = r'X:/import'

moddir = r'X:/modified'
candir = r'X:/cancelled'
acpdir = r'X:/BackupRAW'
nowdir = 'X:/BackupRAW/' + str(datetime.date.today())
```

***rootdir*** - main direcrory  
***importdir*** - direcrory for final editing xml datasets complete for import  

***moddir*** - direcrory for modified xml datasets  
***candir*** - direcrory for cancelled xml datasets  
***acpdir*** - directory for accepted xml datasets
***nowdir*** - directory for backup of the accepted ROW datasets per day

```python
def check_dir():
    directoryList = [importdir, moddir, candir, acpdir, nowdir]
    for items in directoryList:
        os.makedirs(items, exist_ok=True)
```
Check directory - is a function to check if the needed directory exists, if not the function will create one.

```python
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
```
Function Clear data - will move everything what we don't need to the specified folders.
```python
def setup():
    for root, directories, filenames in os.walk(rootdir):
```
Function *Configure* - is the main part of the code, we start here with the looping throu the whole directory.
```python
for filename in filenames:
	if filename.endswith('.xml'):
```
Here we select all files in the directory that match the criteria end with ".xml"
```python
tree = ET.parse(os.path.join(rootdir,filename))
root = tree.getroot()
```
Now we parse every file
```python
 getExternnumber = []
 	for getExternnumberToText in root.findall('NK/AK/SD/EXTNR'):
       		getExternnumber.append(getExternnumberToText.text)
                if str(getExternnumber).startswith('010') and str(getExternnumber).__contains__('0104') or str(getExternnumber).__contains__('0105'):
                	continue
```
Than we check if the file had beed edited previously, in our case we check if the numer contains the digits "*0104*" 
becese after running the code thet returns this number in this field.
```python
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
```
As next we have to set unique id's to the fields for our purposes, in case when we run thou the whole xml we will get 
any fields with this name. When the id's are setted we dump it to the xml tree.
```python
#count shipments in order
getAllShipments = [(x.find('NR')) for x in tree.findall('.//NR/..')]
```
Now we set an increment to measure how meny fields we have to change, the value of the number tell us this.
```python
 # Splits
SplitStellplaetze = []
SplitTransportnummer = []
	for splitcounter in root.findall('NK/AK/SD/INFO/ABSINFO1'):
        	splitone = splitcounter.text.split('fp')[0].split('Stellplätze: ')[1]
                splittwo = splitcounter.text.split('Transportnummer: ')[1].split('\\nSAP')[0]
                SplitStellplaetze.append(splitone)
                SplitTransportnummer.append(splittwo)
```

Here we split the data that we need for our fields in this case that are the number of pallets that have been separated
from the info text.


