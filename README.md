# How to setup app

#### 1. Clone this repo
#### 2. Make sure you've got python installed
#### 3. In CMD:
##### 1. Create python virtual environment by:
#####     python3 -m venv env   // or python -m venv env
##### 2. Activate the virtualenv
#####     (MacOS & Linux):
#####         source env/bin/activate
#####     (Windows):
#####         env\Scripts\activate
#### if you see this:
##### env\Scripts\activate : File C:\path\env\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system. (...)
#### run Windows PowerShell as an Administrator
#### run this command:
#### Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
#### and then type: Y
##### 3. pip install -r requirements.txt
#### 4. run run.py and type localhost:5000 no your browser 


#### if it doesn't work check if app.run(debug=True) in run.py


# Post:
if you wish to install some packages, don't forget to:

### pip freeze > requirements.txt
to save the installed packages into the file.