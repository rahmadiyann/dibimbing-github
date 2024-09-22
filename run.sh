#!/bin/bash

# Mendeklarasikan variabel
nama_default="User"
umur_default=25

# Fungsi untuk menyapa pengguna
greet() {
  local nama=$1
  local umur=$2
  echo "Hello, $nama! Anda berumur $umur tahun."
}

# Fungsi untuk menambahkan dua angka dan mengembalikan hasilnya
add_numbers() {
  local num1=$1
  local num2=$2
  local sum=$((num1 + num2))
  echo $sum
}

# Membaca input dari pengguna
echo "Masukkan nama Anda:"
read nama
echo "Masukkan umur Anda:"
read umur

# Menggunakan default values jika input kosong
if [ -z "$nama" ]; then
  nama=$nama_default
fi

if [ -z "$umur" ]; then
  umur=$umur_default
fi


# Memanggil fungsi greet
greet "$nama" "$umur"

# Membaca dua angka dari pengguna untuk ditambahkan
echo "Masukkan angka pertama:"
read angka1
echo "Masukkan angka kedua:"
read angka2

# Memanggil fungsi add_numbers dan menyimpan hasilnya dalam variabel
hasil=$(add_numbers $angka1 $angka2)

# Menampilkan hasil penjumlahan
echo "Hasil penjumlahan dari $angka1 dan $angka2 adalah: $hasil"

# Loop untuk mencetak angka dari 1 sampai 5
for i in {1..5}; do
  echo "Angka: $i"
done

# Kondisional untuk mengecek nama
if [ "$nama" = "John" ]; then
  echo "Nama Anda John"
else
  echo "Nama Anda bukan John"
fi

# Menyimpan output ke file
echo "Script ini telah dijalankan oleh $nama yang berumur $umur tahun" > output.txt

# contoh:
# chmod 777 script.sh
# ./script.sh
