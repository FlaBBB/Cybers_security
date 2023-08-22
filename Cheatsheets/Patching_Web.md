# Patching Web Codes Cheatsheets

## PHP
### Native :
1. SQL Injection
```php
myslqi_real_escape_string($connection,$inputed);
```
2. XSS
```php
htmlspecialchars($inputed);
```
3. LFI
```php
realpath($inputed); 
if (strpos($inputed, '../') !== false) { die('Nope'); }
```
4. Upload File
- only Image
```php
$is_allowed = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
if($is_allowed !== false) { die('Nope'); }
```
- Specific Extension
```php
$allowed = array('png', 'jpg', 'jpeg', 'gif');
$filename = $_FILES['fileToUpload']['name'];
$ext = pathinfo($filename, PATHINFO_EXTENSION);
if(!in_array($ext,$allowed) ) { die('Nope'); }
```
5. XML External Entity
```php
libxml_disable_entity_loader(false);
$xmlfile = file_get_contents($inputed);
$dom = new DOMDocument();
$dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
$creds = simplexml_import_dom($dom);
$user = $creds->user;
$pass = $creds->pass;
```

### CI Framework :
1. SQL Injection
```php
$this->db->escape($inputed);
```
2. XSS
```php
$this->security->xss_clean($inputed);
```

### Laravel Framework: 
1. SQL Injection
```php
DB::select(DB::raw("SELECT * FROM users WHERE id = $id"));
```

## Python
1. SQL Injection
```py
cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
```
2. XSS
```py
from xml.sax.saxutils import escape
escape(inputed)
```
3. LFI
```py
from os import path
path.realpath(inputed)
if '../' in inputed:
    die('Nope')
```
4. Upload File
- only Image
```py
from PIL import Image
try:
    Image.open(inputed)
except IOError:
    die('Nope')
```
- Specific Extension
```py
allowed = ['png', 'jpg', 'jpeg', 'gif']
filename = inputed
ext = filename.split('.')[-1]
if ext not in allowed:
    die('Nope')
```
5. Check if there is any vuln code that makes SSTI

## NodeJS
1. SQL Injection
```js
const query = 'SELECT * FROM Repository WHERE TAG = ? AND public = 1'
const [rows] = await connection.query(query, [userQuery])
```
2. XSS
```js
const escape = require('escape-html');
escape(inputed);
```
3. LFI
```js
const path = require('path');
path.resolve(inputed);
if (inputed.includes('../')) { die('Nope'); }
```
4. Upload File
- only Image
```js
const fileType = require('file-type');
const imageType = await fileType.fromFile(inputed);
if (imageType.mime.split('/')[0] !== 'image') { die('Nope'); }
```
- Specific Extension
```js
const path = require('path');
const ext = path.extname(inputed);
if (ext !== '.png' && ext !== '.jpg' && ext !== '.jpeg' && ext !== '.gif') { die('Nope'); }
```
5. XML External Entity
```js
const fs = require('fs');
const xml = fs.readFileSync(inputed, 'utf8');
const DOMParser = require('xmldom').DOMParser;
const doc = new DOMParser().parseFromString(xml, 'text/xml');
const user = doc.getElementsByTagName('user')[0].childNodes[0].nodeValue;
const pass = doc.getElementsByTagName('pass')[0].childNodes[0].nodeValue;
```