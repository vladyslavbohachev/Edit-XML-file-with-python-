
**Aufgaben import anpassung**

Set the directories

```python
rootdir = 'X:/'  
moddir = 'X:/1_modified'  
candir = 'X:/1_cancelled'  
importdir = 'X:/1_import'  
```


***moddir*** - is the direcrory for modified xml datasets  
***candir*** - is the direcrory for modified xml cancelled  
***rootdir*** - is the main direcrory  
***importdir*** - is the direcrory for final editing xml datasets complete for import  

```python
def check_dir():
    if not os.path.exists(moddir):
        os.makedirs(moddir)
    if not os.path.exists(candir):
        os.makedirs(candir)
    if not os.path.exists(importdir):
        os.makedirs(importdir)
```
Check directory - is a function to check if the needed directory exists, if not the function will create one.

```python
def clear_data():
    filterMod = [filename for filename in os.listdir(rootdir) if filename.__contains__('modified')]
    filterCan = [filename for filename in os.listdir(rootdir) if filename.__contains__('cancelled')]
    for filename in filterMod:
        path_to_file = os.path.join(rootdir, filename)
        shutil.move(path_to_file, moddir)
    for filename in filterCan:
        path_to_file = os.path.join(rootdir, filename)
        shutil.move(path_to_file, candir)
```
Function Clear data - will move everything what we don't need to the specified folders.
```python
def configure():
    for root, directories, filenames in os.walk(rootdir):
```
Function *Configure* - is the main part of the code, we start here with the looping throu the whole directory.\
```python
for filename in filenames:
	if filename.endswith('.xml'):
```
Here we select all files in the directory that match the criteria end with ".xml"\
```python
tree = ET.parse(os.path.join(rootdir,filename))
	root = tree.getroot()
```
Now we parse every file
```python
extner = []
	for geext in root.findall('NK/AK/SD/EXTNR'):
		extner.append(geext.text)
		if str(extner).__contains__('0104'):
			continue
```
Than we check if the file had beed edited previously, in our case we check if the numer contains the digits "*0104*" 
becese after running the code thet returns this number in this field.
```python
else:
	for (id, METER1) in enumerate(root.findall('NK/AK/SD/FD/METER1')):
		METER1.set('ID', str(id))
	tree.write(os.path.join(rootdir, filename))
	for (id_n, EXTNER) in enumerate(root.findall('NK/AK/SD/EXTNR')):
		EXTNER.set('NR', str(id_n))
	tree.write(os.path.join(rootdir, filename))
	for (id_exttarn, tarn) in enumerate(root.findall('NK/AK/SD/EXTTANR')):
		tarn.set('ANR', str(id_exttarn))
	tree.write(os.path.join(rootdir, filename))
	for eml in root.findall('NK/AK/SD/EXTTANR'):
		newval = ET.SubElement(eml, None)
		newval.text = ''
	ET.dump(tree)
```
As next we have to set unique id's to the fields for our purposes, in case when we run thou the whole xml we will get 
any fields with this name. When the id's are setted we dump it to the xml tree.
```python
find_nr = [(x.find('NR')) for x in tree.findall('.//NR/..')]
```
Now we set an increment to measure how meny fields we have to change, the value of the number tell us this.
```python
info = []
	for j in root.findall('NK/AK/SD/INFO/ABSINFO1'):
		split = j.text.split('fp')[0].split('Stellplätze: ')[1]
		info.append(split)
```
Here we split the data that we need for our fields in this case that are the number of pallets that have been separated \
from the info text.
```python
for i in root.findall('NK/AK/SD/FD/METER1'):
	meter1.append(i.text)
	test = tree.findall('NK/AK/SD/FD/METER1[@ID]')
	for counter in range(len(find_nr)):
		print(f'OK - - - {filename}: ist', test[counter].text, ' soll', info[counter])
		if test[counter].text != info[counter] or test[counter] == '0.000':
			test[counter].text = str(info[counter])
			tree.write(os.path.join(rootdir, filename))
```
Now we apply the data from Meter1 that are our pallets to our field Meter1 (the field Meter1 have an generated id, becase \
there can be more than 1 field for editing and also it can be more fields with our values.)\
```python
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
			tree.write(os.path.join(rootdir, filename))
```
Here we do the same thing as before
```python
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
```
The same thing too, but for other values and fields.
```python
for id in root.findall('NK/AK/SD/FD/METER1'):
	del (id.attrib['ID'])
tree.write(os.path.join(rootdir, filename))
for id in root.findall('NK/AK/SD/EXTNR'):
	del (id.attrib['NR'])
tree.write(os.path.join(rootdir, filename))
for id in root.findall('NK/AK/SD/EXTTANR'):
	del (id.attrib['ANR'])
tree.write(os.path.join(rootdir, filename))
```
As one of the last things we do, is the clear out the xml, here we remove all given id's.
```python
filterfinal = [filename for filename in os.listdir(rootdir) if filename.__contains__('accepted')]
	for filename in filterfinal:
		path_to_import = os.path.join(rootdir, filename)
		shutil.move(path_to_import, importdir)
```
And the last, but not list thing that we do in our code, we move the modified data to our import folder.

.... AND thats all Folks ....



