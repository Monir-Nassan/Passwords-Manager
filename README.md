# Password manager
Password manager software using the Symetric AES Cipher for passwords encryption and SHA-256 hash to store the The Master Key, Sqlite as a Database, PyQt5 For the Gui


## Security
**Please do You'r own reasearch on the best way to store passwords.**

The software is completley offline and even if Some got the databse it's completley useless it works as follows :

- The MasterKey used for the encryption is the password You provide to create The account
- The Masterkey hash is stored in the database.
- when logging in The hash of the Masterkey provided is being evaluated with the hash stored in the database.
**The issue here is The Masterkey is being stored in memory, so the app can use it for the encryption/decryption of the passwords. Improvments inncomming ! If you have any suggestions Please PR**



