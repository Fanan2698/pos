# Bagaimana cara berkontibusi pada projek ini

## Membuat Milestone
Milestone digunakan untuk track issue dan merge request untuk mencapai goals/tujuan dalam periode waktu tertentu. Milestone juga bisa sebagai Agile Sprint atau Release. Jika Milestone sebagai Agile Sprint, atur judul dari Milestone berdasarkan periode waktu, misal `Sprint Agustus 2020`, Namun jika milestone sebagai Release maka atur judul dari Milestone menjadi nomor versi, misal `Version 3.2`

## Membuat issue
Dalam membuat issue, kita dapat mengkategorikan menjadi 3 kategori besar yaitu :
- Task
Kita dapat membuat sebuah issue task dengan format '<create/edit/delete> <modules/pages>'
- Bug
Kita dapat membuat sebuah issue task dengan format '<error/failed/http error code> ketika mengakses <module/pages>'
- User Stories
Kita dapat membuat sebuah issue task dengan format 'sebagai <user/role> saya ingin <needs/wish> agar <goals>'

### Issue berkaitan dengan desain
_Rekomendasi_ : Jika issue berkaitan dengan design seperti user role workflow, wireframe maka figma sudah menyediakan fitur integrasi dengan gitlab secara otomatis dengan cara seperti [panduan ini](https://gitlab.com/gitlab-org/gitlab-figma-plugin/-/wikis/home) (Instalasi, integrasi, publish)

_Tidak Rekomendasi_ : Atau dengan mengupload secara manual desain pada issue 

##### Catatan
Issue dengan _attach image_ berbeda dengan issue dengan _upload design_. Issue dengan _attach image_ sangat berguna ketika menunjukan bukti dari hasil program/aplikasi yang berjalan/error. Sedangkan issue dengan _upload design_ berguna untuk saat perancangan / development contohnya seperti wireframe

## Menautkan label
Saat membuat issue pastikan menautkan _assignment_, _label_, _milestone_, _start date_, _end date_

## Melakukan add/commit/push
Saat menambahkan file baru yang belum di tracking oleh git, kita bisa melakukannya dengan cara :

```bash
# jika file tertentu
$ git add <nama file>

# jika semua file
$ git add .
```
Setelah itu, lakukan commit.

Saat melakukan commit agar perubahan dapat terkait ke issue, pastikan lakukan commit dengan menyertakan nomor issue, contoh perintah sebagai berikut :

```bash
$ git commit -am "#12, Closes #2, Related to #7"
```

- #12 Menautkan commit dengan issue nomor 12
- Closes #2 Menautkan commit dengan issue nomer 2 dan Close issue status pada gitlab
- Related to #7 Menautkan commit yang berkaitan dengan issue nomor 7

Setelah itu, lakukan push.

Saat melakukan push, dapaat dilakukan dengan perintah sebagai berikut :

```bash
$ git push
# atau
$ git push origin <nama branch>
```

Atau jika ingin melakukan push kode + push branch, lakukand dengan cara :

```bash
$ git push --set-upstream origin <nama branch>
```

## Meeting dengan zoom
Saat ada issue yang sudah dibuat dan ingin dibahas bersama dengan melakukan video/voice call, kita dapat menautkan zoom pada setiap issue dengan menggukanan quick action seperti contoh berikut ini:
```bash
/zoom <zoom_url>
```