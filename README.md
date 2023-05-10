<a name="readme-top"></a>
<h1 align="center">Implementasi Makalah</h1>

## Setup MongoDB

1. Download dan install mongodb signed dan mongodb compass
2. Setup environment jika diperlukan di bagian path
3. Sesuaikan nama db pada kode program dengan nama db yang dibuat

## Kode program

1. Download zip kode ini di halaman ini atau clone file dengan command:
  ```sh
  git clone https://github.com/MAINSETS/Makalah
  ```
2. Lakukan instalasi library Crypto pada terminal (jika belum)
  ```sh
  pip install Crypto
  ```
3. Lakukan instalasi library pymongo pada terminal (jika belum)
  ```sh
  pip install pymongo
  ```
4. Run program praktik.py
5. apabila terjadi error *ModuleNotFoundError: No module named 'Crypto'*, biasanya terjadi karena os windows tidak sengaja me-lowercase-kan folder library Crypto. Solusinya, cek library Crypto pada direktori site-packages python,
biasanya terdapat pada C:\Users\NamaUser\AppData\Roaming\Python\Python38\site-packages. Ubah folder yang bernama "crypto" menjadi uppercase "Crypto", dan jalankan kembali main.py
