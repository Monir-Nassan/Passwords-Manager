# Password manager
Password manager software using the Symmetric AES Cipher for passwords encryption and SHA-256 hash to store The Master Key, Sqlite as a Database, PyQt5 For the Gui


## Security
**Please do Your research on the best way to store passwords.**

The software is completely offline and even if Some got the database it's completely useless it works as follows :

- The MasterKey used for the encryption is the password You provide to create The account
- The Masterkey hash is stored in the database.
- when logging in The hash of the Masterkey provided is being evaluated with the hash stored in the database.
**The issue here is The Masterkey is being stored in memory, so the app can use it for the encryption/decryption of the passwords. Improvements are incoming! If you have any suggestions Please PR**

## Installation
```sh
git clone https://github.com/Monir-Nassan/Passwords-Manager.git
cd Passwords-Manager
```

#### create virtual enviroment
```sh
py -m venv env
```


#### activate the virtual envirment
```sh
.\env\Scripts\activate.bat
```

#### install the dependencies
```sh
py -m pip install -r requirements.txt
```

#### run the app
```sh
py app.py
```



