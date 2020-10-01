# Codechef Scraper
After giving a Codechef contest is it hard to find correct answers i.e. fully accepted solution not just partially accepted one and even if you find it you may not understand the solution. So using this you will get a list of users whose solutions are totally accepted so you have a wide variety of users to choose from.
## Installation
### Virtual Environement
I recommend to create a virtual environement and then install scrapy as some of the packages of scrapy can affect packages of python.
```bash
pip install pipenv
```
#### Select Directory
Now in terminal go to the disered directory using
```bash
cd <directory_path>
```
#### Create Virtual Environement
Now create a virtual environement in this directory
```bash
virtualenv .
```
#### Activate Virtual Environement
```bash
. bin/activate
```
This will activate your virtual environement.
### Install Scrapy
```bash
pip install Scrapy
```
Now chech if scrapy packages are correctly installed. There will be lot of packages most of them are dependencies. Check for the package name Scrapy if its there good to go.
```bash
pip freeze
```
## Run Scrapy
### Files
The files that are important are
```bash
codechef/codechef/spiders/codechef_spider_challenge.py
codechef/codechef/spiders/codechef_spider_question.py
```
### Contest Name
Contest codes are stored in variable
```python
url_chlng
```
Change the contest code in this variable only in both the files accordingly.
### Question Name
For a specific question use file
```bash
codechef/codechef/spiders/codechef_spider_question.py
```
In this file change the variable given below which will correspond to the question id.
```python
url_prblm
```
### Run
Save the changes now.
If you want user information on all the questions use file
```bash
codechef_spider_challenge.py
```
If you want user information on a single question use file
```bash
codechef_spider_question.py
```
Now run the disered file in terminal by
```bash
scrapy crawl <crawler_name>
```
Replace <crawler_name> with the "name" variable stored in each file which will run that respective file.
You can also save the data in a json file using the command
```bash
scrapy crawl <crawler_name> -o items.json
```
This will create "items.json" file which will have all the data in it and the directory path to this file will be
```bash
codechef/codechef/items.json
```
# PS
I am running the crawler to only two pages of correct answers as captcha is invoked if too many quick calls are done to the website.
