# Cara Menjalankan Program Scraping

Foobar is a Python library for dealing with word pluralization.

## Install Scrapy

Gunakan anaconda prompt untuk melakukan installasi package

```bash
pip install scrapy
```
atau
```bash
conda install -c conda-forge scrapy
```

## Membuat project baru

```bash
scrapy startproject [namaproject]
```

## Menjalalan project
```bash
scrapy crawl [namaquotes]
```
namaquotes harus merupakan nama variable "name" pada file didalam folder spider

## Cara agar tidak kenak banned saat melakukan scraping
Terkadang beberapa website tidak bisa dilakukan scraping karena alasan keamanan. Agar tetap bisa melakukan scraping, lakukan perubahan opsi di file settings.py dengan mengubah nama variable USER_AGENT seperti dibawah ini
```python
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1" 
```
