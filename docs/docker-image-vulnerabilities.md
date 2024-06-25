# Known vulnerabilities

```
[adrien@fedora ~/Development/workspace/checkconsents] [13.12.2023 16:57:34] $ grype cad/checkconsents:1.0.0
 ✔ Vulnerability DB                [updated]  
 ✔ Loaded image                                                                                                                                                                                                      cad/checkconsents:1.0.0
 ✔ Parsed image                                                                                                                                                      sha256:4e16eb6478d03f8a225d430e79b8e73cb0ecf0e158efa9cdc802f61849f4cda7
 ✔ Cataloged packages              [440 packages]  
 ✔ Scanned for vulnerabilities     [544 vulnerability matches]  
   ├── by severity: 2 critical, 64 high, 137 medium, 13 low, 309 negligible (19 unknown)
   └── by status:   34 fixed, 510 not-fixed, 0 ignored 
NAME                       INSTALLED                FIXED-IN           TYPE    VULNERABILITY     SEVERITY   
apt                        2.6.1                                       deb     CVE-2011-3374     Negligible  
binutils                   2.40-2                                      deb     CVE-2023-1972     Negligible  
binutils                   2.40-2                                      deb     CVE-2021-32256    Negligible  
binutils                   2.40-2                                      deb     CVE-2018-9996     Negligible  
binutils                   2.40-2                                      deb     CVE-2018-20712    Negligible  
binutils                   2.40-2                                      deb     CVE-2018-20673    Negligible  
binutils                   2.40-2                                      deb     CVE-2018-18483    Negligible  
binutils                   2.40-2                                      deb     CVE-2017-13716    Negligible  
binutils-common            2.40-2                                      deb     CVE-2023-1972     Negligible  
binutils-common            2.40-2                                      deb     CVE-2021-32256    Negligible  
binutils-common            2.40-2                                      deb     CVE-2018-9996     Negligible  
binutils-common            2.40-2                                      deb     CVE-2018-20712    Negligible  
binutils-common            2.40-2                                      deb     CVE-2018-20673    Negligible  
binutils-common            2.40-2                                      deb     CVE-2018-18483    Negligible  
binutils-common            2.40-2                                      deb     CVE-2017-13716    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                      deb     CVE-2023-1972     Negligible  
binutils-x86-64-linux-gnu  2.40-2                                      deb     CVE-2021-32256    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                      deb     CVE-2018-9996     Negligible  
binutils-x86-64-linux-gnu  2.40-2                                      deb     CVE-2018-20712    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                      deb     CVE-2018-20673    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                      deb     CVE-2018-18483    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                      deb     CVE-2017-13716    Negligible  
bsdutils                   1:2.38.1-5+b1                               deb     CVE-2022-0563     Negligible  
coreutils                  9.1-1                    (won't fix)        deb     CVE-2016-2781     Low         
coreutils                  9.1-1                                       deb     CVE-2017-18018    Negligible  
cpp-12                     12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
cpp-12                     12.2.0-14                                   deb     CVE-2022-27943    Negligible  
ffmpeg                     7:5.1.3-1                7:5.1.4-0+deb12u1  deb     CVE-2022-4907     High        
gcc-12                     12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
gcc-12                     12.2.0-14                                   deb     CVE-2022-27943    Negligible  
gcc-12-base                12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
gcc-12-base                12.2.0-14                                   deb     CVE-2022-27943    Negligible  
ghostscript                10.0.0~dfsg-11+deb12u2                      deb     CVE-2023-46751    High        
ghostscript                10.0.0~dfsg-11+deb12u2                      deb     CVE-2023-38560    Negligible  
ghostscript                10.0.0~dfsg-11+deb12u2                      deb     CVE-2022-1350     Negligible  
gpgv                       2.2.40-1.1                                  deb     CVE-2022-3219     Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2021-3610     High        
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-5341     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-3428     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-34151    Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-3195     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-2157     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1906     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1289     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-3213     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-1115     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-34152    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2021-20311    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2018-15607    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-7275     Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11755    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11754    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2016-8678     Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2008-3134     Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                        deb     CVE-2005-0406     Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2021-3610     High        
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-5341     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-3428     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-34151    Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-3195     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-2157     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1906     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1289     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-3213     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-1115     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-34152    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2021-20311    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2018-15607    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-7275     Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11755    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11754    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2016-8678     Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2008-3134     Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                        deb     CVE-2005-0406     Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2021-3610     High        
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-5341     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-3428     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-34151    Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-3195     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-2157     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1906     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1289     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-3213     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-1115     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-34152    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2021-20311    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2018-15607    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-7275     Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11755    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11754    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2016-8678     Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2008-3134     Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                        deb     CVE-2005-0406     Negligible  
libaom3                    3.6.0-1                  (won't fix)        deb     CVE-2023-39616    High        
libapt-pkg6.0              2.6.1                                       deb     CVE-2011-3374     Negligible  
libarchive-dev             3.6.2-1                  (won't fix)        deb     CVE-2023-30571    Medium      
libarchive13               3.6.2-1                  (won't fix)        deb     CVE-2023-30571    Medium      
libasan8                   12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libasan8                   12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libatomic1                 12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libatomic1                 12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libavahi-client3           0.8-10                   (won't fix)        deb     CVE-2023-38473    Medium      
libavahi-client3           0.8-10                   (won't fix)        deb     CVE-2023-38472    Medium      
libavahi-client3           0.8-10                   (won't fix)        deb     CVE-2023-38471    Medium      
libavahi-client3           0.8-10                   (won't fix)        deb     CVE-2023-38470    Medium      
libavahi-client3           0.8-10                   (won't fix)        deb     CVE-2023-38469    Medium      
libavahi-common-data       0.8-10                   (won't fix)        deb     CVE-2023-38473    Medium      
libavahi-common-data       0.8-10                   (won't fix)        deb     CVE-2023-38472    Medium      
libavahi-common-data       0.8-10                   (won't fix)        deb     CVE-2023-38471    Medium      
libavahi-common-data       0.8-10                   (won't fix)        deb     CVE-2023-38470    Medium      
libavahi-common-data       0.8-10                   (won't fix)        deb     CVE-2023-38469    Medium      
libavahi-common3           0.8-10                   (won't fix)        deb     CVE-2023-38473    Medium      
libavahi-common3           0.8-10                   (won't fix)        deb     CVE-2023-38472    Medium      
libavahi-common3           0.8-10                   (won't fix)        deb     CVE-2023-38471    Medium      
libavahi-common3           0.8-10                   (won't fix)        deb     CVE-2023-38470    Medium      
libavahi-common3           0.8-10                   (won't fix)        deb     CVE-2023-38469    Medium      
libavcodec59               7:5.1.3-1                7:5.1.4-0+deb12u1  deb     CVE-2022-4907     High        
libavdevice59              7:5.1.3-1                7:5.1.4-0+deb12u1  deb     CVE-2022-4907     High        
libavfilter8               7:5.1.3-1                7:5.1.4-0+deb12u1  deb     CVE-2022-4907     High        
libavformat59              7:5.1.3-1                7:5.1.4-0+deb12u1  deb     CVE-2022-4907     High        
libavutil57                7:5.1.3-1                7:5.1.4-0+deb12u1  deb     CVE-2022-4907     High        
libbinutils                2.40-2                                      deb     CVE-2023-1972     Negligible  
libbinutils                2.40-2                                      deb     CVE-2021-32256    Negligible  
libbinutils                2.40-2                                      deb     CVE-2018-9996     Negligible  
libbinutils                2.40-2                                      deb     CVE-2018-20712    Negligible  
libbinutils                2.40-2                                      deb     CVE-2018-20673    Negligible  
libbinutils                2.40-2                                      deb     CVE-2018-18483    Negligible  
libbinutils                2.40-2                                      deb     CVE-2017-13716    Negligible  
libblkid1                  2.38.1-5+b1                                 deb     CVE-2022-0563     Negligible  
libc-bin                   2.36-9+deb12u3                              deb     CVE-2019-9192     Negligible  
libc-bin                   2.36-9+deb12u3                              deb     CVE-2019-1010025  Negligible  
libc-bin                   2.36-9+deb12u3                              deb     CVE-2019-1010024  Negligible  
libc-bin                   2.36-9+deb12u3                              deb     CVE-2019-1010023  Negligible  
libc-bin                   2.36-9+deb12u3                              deb     CVE-2019-1010022  Negligible  
libc-bin                   2.36-9+deb12u3                              deb     CVE-2018-20796    Negligible  
libc-bin                   2.36-9+deb12u3                              deb     CVE-2010-4756     Negligible  
libc-dev-bin               2.36-9+deb12u3                              deb     CVE-2019-9192     Negligible  
libc-dev-bin               2.36-9+deb12u3                              deb     CVE-2019-1010025  Negligible  
libc-dev-bin               2.36-9+deb12u3                              deb     CVE-2019-1010024  Negligible  
libc-dev-bin               2.36-9+deb12u3                              deb     CVE-2019-1010023  Negligible  
libc-dev-bin               2.36-9+deb12u3                              deb     CVE-2019-1010022  Negligible  
libc-dev-bin               2.36-9+deb12u3                              deb     CVE-2018-20796    Negligible  
libc-dev-bin               2.36-9+deb12u3                              deb     CVE-2010-4756     Negligible  
libc6                      2.36-9+deb12u3                              deb     CVE-2019-9192     Negligible  
libc6                      2.36-9+deb12u3                              deb     CVE-2019-1010025  Negligible  
libc6                      2.36-9+deb12u3                              deb     CVE-2019-1010024  Negligible  
libc6                      2.36-9+deb12u3                              deb     CVE-2019-1010023  Negligible  
libc6                      2.36-9+deb12u3                              deb     CVE-2019-1010022  Negligible  
libc6                      2.36-9+deb12u3                              deb     CVE-2018-20796    Negligible  
libc6                      2.36-9+deb12u3                              deb     CVE-2010-4756     Negligible  
libc6-dev                  2.36-9+deb12u3                              deb     CVE-2019-9192     Negligible  
libc6-dev                  2.36-9+deb12u3                              deb     CVE-2019-1010025  Negligible  
libc6-dev                  2.36-9+deb12u3                              deb     CVE-2019-1010024  Negligible  
libc6-dev                  2.36-9+deb12u3                              deb     CVE-2019-1010023  Negligible  
libc6-dev                  2.36-9+deb12u3                              deb     CVE-2019-1010022  Negligible  
libc6-dev                  2.36-9+deb12u3                              deb     CVE-2018-20796    Negligible  
libc6-dev                  2.36-9+deb12u3                              deb     CVE-2010-4756     Negligible  
libcaca0                   0.99.beta20-3                               deb     CVE-2022-0856     Negligible  
libcairo-gobject2          1.16.0-7                 (won't fix)        deb     CVE-2019-6462     Low         
libcairo-gobject2          1.16.0-7                 (won't fix)        deb     CVE-2019-6461     Low         
libcairo-gobject2          1.16.0-7                 (won't fix)        deb     CVE-2018-18064    Low         
libcairo-gobject2          1.16.0-7                 (won't fix)        deb     CVE-2017-7475     Low         
libcairo2                  1.16.0-7                 (won't fix)        deb     CVE-2019-6462     Low         
libcairo2                  1.16.0-7                 (won't fix)        deb     CVE-2019-6461     Low         
libcairo2                  1.16.0-7                 (won't fix)        deb     CVE-2018-18064    Low         
libcairo2                  1.16.0-7                 (won't fix)        deb     CVE-2017-7475     Low         
libcc1-0                   12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libcc1-0                   12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libctf-nobfd0              2.40-2                                      deb     CVE-2023-1972     Negligible  
libctf-nobfd0              2.40-2                                      deb     CVE-2021-32256    Negligible  
libctf-nobfd0              2.40-2                                      deb     CVE-2018-9996     Negligible  
libctf-nobfd0              2.40-2                                      deb     CVE-2018-20712    Negligible  
libctf-nobfd0              2.40-2                                      deb     CVE-2018-20673    Negligible  
libctf-nobfd0              2.40-2                                      deb     CVE-2018-18483    Negligible  
libctf-nobfd0              2.40-2                                      deb     CVE-2017-13716    Negligible  
libctf0                    2.40-2                                      deb     CVE-2023-1972     Negligible  
libctf0                    2.40-2                                      deb     CVE-2021-32256    Negligible  
libctf0                    2.40-2                                      deb     CVE-2018-9996     Negligible  
libctf0                    2.40-2                                      deb     CVE-2018-20712    Negligible  
libctf0                    2.40-2                                      deb     CVE-2018-20673    Negligible  
libctf0                    2.40-2                                      deb     CVE-2018-18483    Negligible  
libctf0                    2.40-2                                      deb     CVE-2017-13716    Negligible  
libcups2                   2.4.2-3+deb12u4                             deb     CVE-2014-8166     Negligible  
libcurl3-nss               7.88.1-10+deb12u4                           deb     CVE-2023-46218    Medium      
libcurl3-nss               7.88.1-10+deb12u4                           deb     CVE-2023-46219    Unknown     
libcurl4                   7.88.1-10+deb12u4                           deb     CVE-2023-46218    Medium      
libcurl4                   7.88.1-10+deb12u4                           deb     CVE-2023-46219    Unknown     
libcurl4-nss-dev           7.88.1-10+deb12u4                           deb     CVE-2023-46218    Medium      
libcurl4-nss-dev           7.88.1-10+deb12u4                           deb     CVE-2023-46219    Unknown     
libdav1d6                  1.0.0-2                  (won't fix)        deb     CVE-2023-32570    Medium      
libde265-0                 1.0.11-1                                    deb     CVE-2023-49468    High        
libde265-0                 1.0.11-1                                    deb     CVE-2023-49467    High        
libde265-0                 1.0.11-1                                    deb     CVE-2023-49465    High        
libde265-0                 1.0.11-1                 1.0.11-1+deb12u1   deb     CVE-2023-43887    High        
libde265-0                 1.0.11-1                 1.0.11-1+deb12u1   deb     CVE-2023-27103    High        
libde265-0                 1.0.11-1                 1.0.11-1+deb12u1   deb     CVE-2023-47471    Medium      
libde265-0                 1.0.11-1                 1.0.11-1+deb12u1   deb     CVE-2023-27102    Medium      
libgcc-12-dev              12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libgcc-12-dev              12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libgcc-s1                  12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libgcc-s1                  12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libgcrypt20                1.10.1-3                                    deb     CVE-2018-6829     Negligible  
libgfortran5               12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libgfortran5               12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libgif7                    5.2.1-2.5                                   deb     CVE-2023-48161    Negligible  
libgif7                    5.2.1-2.5                                   deb     CVE-2023-39742    Negligible  
libgif7                    5.2.1-2.5                                   deb     CVE-2022-28506    Negligible  
libgif7                    5.2.1-2.5                                   deb     CVE-2021-40633    Negligible  
libgif7                    5.2.1-2.5                                   deb     CVE-2020-23922    Negligible  
libglib2.0-0               2.74.6-2                                    deb     CVE-2012-0039     Negligible  
libgnutls30                3.7.9-2                  3.7.9-2+deb12u1    deb     CVE-2023-5981     Medium      
libgnutls30                3.7.9-2                                     deb     CVE-2011-3389     Negligible  
libgomp1                   12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libgomp1                   12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libgprofng0                2.40-2                                      deb     CVE-2023-1972     Negligible  
libgprofng0                2.40-2                                      deb     CVE-2021-32256    Negligible  
libgprofng0                2.40-2                                      deb     CVE-2018-9996     Negligible  
libgprofng0                2.40-2                                      deb     CVE-2018-20712    Negligible  
libgprofng0                2.40-2                                      deb     CVE-2018-20673    Negligible  
libgprofng0                2.40-2                                      deb     CVE-2018-18483    Negligible  
libgprofng0                2.40-2                                      deb     CVE-2017-13716    Negligible  
libgs-common               10.0.0~dfsg-11+deb12u2                      deb     CVE-2023-46751    High        
libgs-common               10.0.0~dfsg-11+deb12u2                      deb     CVE-2023-38560    Negligible  
libgs-common               10.0.0~dfsg-11+deb12u2                      deb     CVE-2022-1350     Negligible  
libgs10                    10.0.0~dfsg-11+deb12u2                      deb     CVE-2023-46751    High        
libgs10                    10.0.0~dfsg-11+deb12u2                      deb     CVE-2023-38560    Negligible  
libgs10                    10.0.0~dfsg-11+deb12u2                      deb     CVE-2022-1350     Negligible  
libgs10-common             10.0.0~dfsg-11+deb12u2                      deb     CVE-2023-46751    High        
libgs10-common             10.0.0~dfsg-11+deb12u2                      deb     CVE-2023-38560    Negligible  
libgs10-common             10.0.0~dfsg-11+deb12u2                      deb     CVE-2022-1350     Negligible  
libgssapi-krb5-2           1.20.1-2+deb12u1                            deb     CVE-2018-5709     Negligible  
libharfbuzz0b              6.0.0+dfsg-3             (won't fix)        deb     CVE-2023-25193    High        
libheif1                   1.15.1-1                 (won't fix)        deb     CVE-2023-49464    High        
libheif1                   1.15.1-1                 (won't fix)        deb     CVE-2023-49463    High        
libheif1                   1.15.1-1                 (won't fix)        deb     CVE-2023-49462    High        
libheif1                   1.15.1-1                 (won't fix)        deb     CVE-2023-49460    High        
libheif1                   1.15.1-1                 (won't fix)        deb     CVE-2023-29659    Medium      
libitm1                    12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libitm1                    12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libjansson4                2.14-2                                      deb     CVE-2020-36325    Negligible  
libjbig0                   2.1-6.1                                     deb     CVE-2017-9937     Negligible  
libjbig2dec0               0.19-3                   (won't fix)        deb     CVE-2023-46361    Medium      
libjxl0.7                  0.7.0-10                 (won't fix)        deb     CVE-2023-0645     Critical    
libjxl0.7                  0.7.0-10                 (won't fix)        deb     CVE-2023-35790    High        
libjxl0.7                  0.7.0-10                                    deb     CVE-2021-36691    Negligible  
libk5crypto3               1.20.1-2+deb12u1                            deb     CVE-2018-5709     Negligible  
libkrb5-3                  1.20.1-2+deb12u1                            deb     CVE-2018-5709     Negligible  
libkrb5support0            1.20.1-2+deb12u1                            deb     CVE-2018-5709     Negligible  
libldap-2.5-0              2.5.13+dfsg-5            (won't fix)        deb     CVE-2023-2953     High        
libldap-2.5-0              2.5.13+dfsg-5                               deb     CVE-2020-15719    Negligible  
libldap-2.5-0              2.5.13+dfsg-5                               deb     CVE-2017-17740    Negligible  
libldap-2.5-0              2.5.13+dfsg-5                               deb     CVE-2017-14159    Negligible  
libldap-2.5-0              2.5.13+dfsg-5                               deb     CVE-2015-3276     Negligible  
libllvm15                  1:15.0.6-4+b1                               deb     CVE-2023-29942    Negligible  
libllvm15                  1:15.0.6-4+b1                               deb     CVE-2023-29941    Negligible  
libllvm15                  1:15.0.6-4+b1                               deb     CVE-2023-29939    Negligible  
libllvm15                  1:15.0.6-4+b1                               deb     CVE-2023-29935    Negligible  
libllvm15                  1:15.0.6-4+b1                               deb     CVE-2023-29934    Negligible  
libllvm15                  1:15.0.6-4+b1                               deb     CVE-2023-29933    Negligible  
libllvm15                  1:15.0.6-4+b1                               deb     CVE-2023-29932    Negligible  
libllvm15                  1:15.0.6-4+b1                               deb     CVE-2023-26924    Negligible  
liblsan0                   12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
liblsan0                   12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2021-3610     High        
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-5341     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-3428     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-34151    Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-3195     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-2157     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1906     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1289     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-3213     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-1115     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-34152    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2021-20311    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2018-15607    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-7275     Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11755    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11754    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2016-8678     Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2008-3134     Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2005-0406     Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2021-3610     High        
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-5341     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-3428     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-34151    Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-3195     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-2157     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1906     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2023-1289     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-3213     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)        deb     CVE-2022-1115     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2023-34152    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2021-20311    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2018-15607    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-7275     Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11755    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2017-11754    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2016-8678     Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2008-3134     Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                        deb     CVE-2005-0406     Negligible  
libmbedcrypto7             2.28.3-1                                    deb     CVE-2023-43615    Negligible  
libmbedcrypto7             2.28.3-1                                    deb     CVE-2018-1000520  Negligible  
libmount1                  2.38.1-5+b1                                 deb     CVE-2022-0563     Negligible  
libncursesw6               6.4-4                                       deb     CVE-2023-50495    Unknown     
libnghttp2-14              1.52.0-1                 1.52.0-1+deb12u1   deb     CVE-2023-44487    Negligible  
libnss3                    2:3.87.1-1                                  deb     CVE-2017-11698    Negligible  
libnss3                    2:3.87.1-1                                  deb     CVE-2017-11697    Negligible  
libnss3                    2:3.87.1-1                                  deb     CVE-2017-11696    Negligible  
libnss3                    2:3.87.1-1                                  deb     CVE-2017-11695    Negligible  
libnss3                    2:3.87.1-1               (won't fix)        deb     CVE-2023-5388     Unknown     
libopenjp2-7               2.5.0-2                  (won't fix)        deb     CVE-2021-3575     High        
libopenjp2-7               2.5.0-2                  (won't fix)        deb     CVE-2019-6988     Low         
libopenjp2-7               2.5.0-2                                     deb     CVE-2018-20846    Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2018-16376    Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2018-16375    Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2017-17479    Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2016-9581     Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2016-9580     Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2016-9117     Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2016-9116     Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2016-9115     Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2016-9114     Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2016-9113     Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2016-10506    Negligible  
libopenjp2-7               2.5.0-2                                     deb     CVE-2016-10505    Negligible  
libperl5.36                5.36.0-7                 (won't fix)        deb     CVE-2023-31484    High        
libperl5.36                5.36.0-7                                    deb     CVE-2023-31486    Negligible  
libperl5.36                5.36.0-7                                    deb     CVE-2011-4116     Negligible  
libperl5.36                5.36.0-7                 5.36.0-7+deb12u1   deb     CVE-2023-47038    Unknown     
libpixman-1-0              0.42.2-1                                    deb     CVE-2023-37769    Negligible  
libpng16-16                1.6.39-2                                    deb     CVE-2021-4214     Negligible  
libpostproc56              7:5.1.3-1                7:5.1.4-0+deb12u1  deb     CVE-2022-4907     High        
libpython3.11-minimal      3.11.2-6                 (won't fix)        deb     CVE-2023-41105    High        
libpython3.11-minimal      3.11.2-6                 (won't fix)        deb     CVE-2023-24329    High        
libpython3.11-minimal      3.11.2-6                                    deb     CVE-2023-40217    Medium      
libpython3.11-minimal      3.11.2-6                 (won't fix)        deb     CVE-2023-27043    Medium      
libpython3.11-minimal      3.11.2-6                                    deb     CVE-2023-24535    Negligible  
libpython3.11-stdlib       3.11.2-6                 (won't fix)        deb     CVE-2023-41105    High        
libpython3.11-stdlib       3.11.2-6                 (won't fix)        deb     CVE-2023-24329    High        
libpython3.11-stdlib       3.11.2-6                                    deb     CVE-2023-40217    Medium      
libpython3.11-stdlib       3.11.2-6                 (won't fix)        deb     CVE-2023-27043    Medium      
libpython3.11-stdlib       3.11.2-6                                    deb     CVE-2023-24535    Negligible  
libquadmath0               12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libquadmath0               12.2.0-14                                   deb     CVE-2022-27943    Negligible  
librabbitmq4               0.11.0-1+b1              (won't fix)        deb     CVE-2023-35789    Medium      
libsmartcols1              2.38.1-5+b1                                 deb     CVE-2022-0563     Negligible  
libsndfile1                1.2.0-1                  (won't fix)        deb     CVE-2022-33065    High        
libsndfile1                1.2.0-1                  (won't fix)        deb     CVE-2022-33064    High        
libsqlite3-0               3.40.1-2                                    deb     CVE-2021-45346    Negligible  
libssl3                    3.0.11-1~deb12u2         (won't fix)        deb     CVE-2023-5678     Medium      
libssl3                    3.0.11-1~deb12u2                            deb     CVE-2010-0928     Negligible  
libssl3                    3.0.11-1~deb12u2                            deb     CVE-2007-6755     Negligible  
libstdc++6                 12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libstdc++6                 12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libswresample4             7:5.1.3-1                7:5.1.4-0+deb12u1  deb     CVE-2022-4907     High        
libswscale6                7:5.1.3-1                7:5.1.4-0+deb12u1  deb     CVE-2022-4907     High        
libsystemd0                252.17-1~deb12u1                            deb     CVE-2023-31439    Negligible  
libsystemd0                252.17-1~deb12u1                            deb     CVE-2023-31438    Negligible  
libsystemd0                252.17-1~deb12u1                            deb     CVE-2023-31437    Negligible  
libsystemd0                252.17-1~deb12u1                            deb     CVE-2013-4392     Negligible  
libtiff6                   4.5.0-6                  (won't fix)        deb     CVE-2023-6277     Medium      
libtiff6                   4.5.0-6                  4.5.0-6+deb12u1    deb     CVE-2023-41175    Medium      
libtiff6                   4.5.0-6                  4.5.0-6+deb12u1    deb     CVE-2023-40745    Medium      
libtiff6                   4.5.0-6                  (won't fix)        deb     CVE-2023-3618     Medium      
libtiff6                   4.5.0-6                  4.5.0-6+deb12u1    deb     CVE-2023-3576     Medium      
libtiff6                   4.5.0-6                  (won't fix)        deb     CVE-2023-3316     Medium      
libtiff6                   4.5.0-6                  (won't fix)        deb     CVE-2023-2908     Medium      
libtiff6                   4.5.0-6                  (won't fix)        deb     CVE-2023-26966    Medium      
libtiff6                   4.5.0-6                  (won't fix)        deb     CVE-2023-26965    Medium      
libtiff6                   4.5.0-6                  (won't fix)        deb     CVE-2023-25433    Medium      
libtiff6                   4.5.0-6                                     deb     CVE-2023-6228     Negligible  
libtiff6                   4.5.0-6                                     deb     CVE-2023-3164     Negligible  
libtiff6                   4.5.0-6                                     deb     CVE-2023-1916     Negligible  
libtiff6                   4.5.0-6                                     deb     CVE-2022-1210     Negligible  
libtiff6                   4.5.0-6                                     deb     CVE-2018-10126    Negligible  
libtiff6                   4.5.0-6                                     deb     CVE-2017-9117     Negligible  
libtiff6                   4.5.0-6                                     deb     CVE-2017-5563     Negligible  
libtiff6                   4.5.0-6                                     deb     CVE-2017-17973    Negligible  
libtiff6                   4.5.0-6                                     deb     CVE-2017-16232    Negligible  
libtinfo6                  6.4-4                                       deb     CVE-2023-50495    Unknown     
libtsan2                   12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libtsan2                   12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libubsan1                  12.2.0-14                (won't fix)        deb     CVE-2023-4039     Medium      
libubsan1                  12.2.0-14                                   deb     CVE-2022-27943    Negligible  
libudev1                   252.17-1~deb12u1                            deb     CVE-2023-31439    Negligible  
libudev1                   252.17-1~deb12u1                            deb     CVE-2023-31438    Negligible  
libudev1                   252.17-1~deb12u1                            deb     CVE-2023-31437    Negligible  
libudev1                   252.17-1~deb12u1                            deb     CVE-2013-4392     Negligible  
libuuid1                   2.38.1-5+b1                                 deb     CVE-2022-0563     Negligible  
libvpx7                    1.12.0-1+deb12u2                            deb     CVE-2017-0641     Negligible  
libxml2                    2.9.14+dfsg-1.3~deb12u1  (won't fix)        deb     CVE-2023-45322    Medium      
libxml2                    2.9.14+dfsg-1.3~deb12u1  (won't fix)        deb     CVE-2023-39615    Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-6610     High        
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-6606     High        
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-6111     High        
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-5717     High        
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-5633     High        
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-5345     High        
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-5178     High        
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-46813    High        
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-3640     High        
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-35827    High        
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-2176     High        
linux-libc-dev             6.1.55-1                                    deb     CVE-2021-3864     High        
linux-libc-dev             6.1.55-1                                    deb     CVE-2021-3847     High        
linux-libc-dev             6.1.55-1                 (won't fix)        deb     CVE-2019-19814    High        
linux-libc-dev             6.1.55-1                 (won't fix)        deb     CVE-2019-19449    High        
linux-libc-dev             6.1.55-1                 (won't fix)        deb     CVE-2013-7445     High        
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-6622     Medium      
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-6121     Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-6039     Medium      
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-5197     Medium      
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-5158     Medium      
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-5090     Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-50431    Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-47233    Medium      
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-46862    Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-4133     Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-4010     Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-37454    Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-3397     Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-31083    Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-31082    Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-23005    Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-21264    Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-1193     Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-1192     Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-0597     Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-0160     Medium      
linux-libc-dev             6.1.55-1                 (won't fix)        deb     CVE-2022-4543     Medium      
linux-libc-dev             6.1.55-1                                    deb     CVE-2020-36694    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)        deb     CVE-2020-14304    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)        deb     CVE-2019-20794    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)        deb     CVE-2019-16089    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)        deb     CVE-2019-15213    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)        deb     CVE-2018-12928    Low         
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-4134     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-39191    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-31085    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-31081    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-26242    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-23039    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-45888    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-45885    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-45884    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-44034    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-44033    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-44032    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-41848    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-3238     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-2961     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-25265    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-1247     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2022-0400     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2021-3714     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2021-26934    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2020-35501    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2020-11725    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-19378    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-19070    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-16234    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-16233    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-16232    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-16231    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-16230    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-16229    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-12456    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-12455    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-12382    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-12381    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-12380    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-12379    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-12378    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2019-11191    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2018-17977    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2018-1121     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2017-13694    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2017-13693    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2017-0630     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2016-8660     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2016-10723    Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2015-2877     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2014-9900     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2014-9892     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2012-4542     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2011-4917     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2011-4916     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2011-4915     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2010-5321     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2010-4563     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2008-4609     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2008-2544     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2007-3719     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2005-3660     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2004-0230     Negligible  
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-6536     Unknown     
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-6535     Unknown     
linux-libc-dev             6.1.55-1                                    deb     CVE-2023-6356     Unknown     
linux-libc-dev             6.1.55-1                 6.1.64-1           deb     CVE-2023-34324    Unknown     
login                      1:4.13+dfsg1-1+b1        (won't fix)        deb     CVE-2023-29383    Low         
login                      1:4.13+dfsg1-1+b1                           deb     CVE-2019-19882    Negligible  
login                      1:4.13+dfsg1-1+b1                           deb     CVE-2007-5686     Negligible  
login                      1:4.13+dfsg1-1+b1        (won't fix)        deb     CVE-2023-4641     Unknown     
mount                      2.38.1-5+b1                                 deb     CVE-2022-0563     Negligible  
ncurses-base               6.4-4                                       deb     CVE-2023-50495    Unknown     
ncurses-bin                6.4-4                                       deb     CVE-2023-50495    Unknown     
openssl                    3.0.11-1~deb12u2         (won't fix)        deb     CVE-2023-5678     Medium      
openssl                    3.0.11-1~deb12u2                            deb     CVE-2010-0928     Negligible  
openssl                    3.0.11-1~deb12u2                            deb     CVE-2007-6755     Negligible  
passwd                     1:4.13+dfsg1-1+b1        (won't fix)        deb     CVE-2023-29383    Low         
passwd                     1:4.13+dfsg1-1+b1                           deb     CVE-2019-19882    Negligible  
passwd                     1:4.13+dfsg1-1+b1                           deb     CVE-2007-5686     Negligible  
passwd                     1:4.13+dfsg1-1+b1        (won't fix)        deb     CVE-2023-4641     Unknown     
perl                       5.36.0-7                 (won't fix)        deb     CVE-2023-31484    High        
perl                       5.36.0-7                                    deb     CVE-2023-31486    Negligible  
perl                       5.36.0-7                                    deb     CVE-2011-4116     Negligible  
perl                       5.36.0-7                 5.36.0-7+deb12u1   deb     CVE-2023-47038    Unknown     
perl-base                  5.36.0-7                 (won't fix)        deb     CVE-2023-31484    High        
perl-base                  5.36.0-7                                    deb     CVE-2023-31486    Negligible  
perl-base                  5.36.0-7                                    deb     CVE-2011-4116     Negligible  
perl-base                  5.36.0-7                 5.36.0-7+deb12u1   deb     CVE-2023-47038    Unknown     
perl-modules-5.36          5.36.0-7                 (won't fix)        deb     CVE-2023-31484    High        
perl-modules-5.36          5.36.0-7                                    deb     CVE-2023-31486    Negligible  
perl-modules-5.36          5.36.0-7                                    deb     CVE-2011-4116     Negligible  
perl-modules-5.36          5.36.0-7                 5.36.0-7+deb12u1   deb     CVE-2023-47038    Unknown     
pip                        23.3.1                                      python  CVE-2018-20225    High        
python3-pil                9.4.0-1.1+b1             (won't fix)        deb     CVE-2023-44271    High        
python3.11                 3.11.2-6                 (won't fix)        deb     CVE-2023-41105    High        
python3.11                 3.11.2-6                 (won't fix)        deb     CVE-2023-24329    High        
python3.11                 3.11.2-6                                    deb     CVE-2023-40217    Medium      
python3.11                 3.11.2-6                 (won't fix)        deb     CVE-2023-27043    Medium      
python3.11                 3.11.2-6                                    deb     CVE-2023-24535    Negligible  
python3.11-minimal         3.11.2-6                 (won't fix)        deb     CVE-2023-41105    High        
python3.11-minimal         3.11.2-6                 (won't fix)        deb     CVE-2023-24329    High        
python3.11-minimal         3.11.2-6                                    deb     CVE-2023-40217    Medium      
python3.11-minimal         3.11.2-6                 (won't fix)        deb     CVE-2023-27043    Medium      
python3.11-minimal         3.11.2-6                                    deb     CVE-2023-24535    Negligible  
tar                        1.34+dfsg-1.2                               deb     CVE-2022-48303    Negligible  
tar                        1.34+dfsg-1.2                               deb     CVE-2005-2541     Negligible  
tar                        1.34+dfsg-1.2            (won't fix)        deb     CVE-2023-39804    Unknown     
util-linux                 2.38.1-5+b1                                 deb     CVE-2022-0563     Negligible  
util-linux-extra           2.38.1-5+b1                                 deb     CVE-2022-0563     Negligible  
zlib1g                     1:1.2.13.dfsg-1          (won't fix)        deb     CVE-2023-45853    Critical
```
