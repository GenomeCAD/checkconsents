# CheckConsents Tool

## Installation

`CheckConsents` tool requires Python 3.12+.

`CheckConsents` tool requires `convert` from [ImageMagick software](https://imagemagick.org/index.php).

```bash
$ convert --version
Version: ImageMagick 7.1.1-15 Q16-HDRI x86_64 21298 https://imagemagick.org
Copyright: (C) 1999 ImageMagick Studio LLC
License: https://imagemagick.org/script/license.php
Features: Cipher DPC HDRI Modules OpenMP(4.5) 
Delegates (built-in): bzlib cairo djvu fftw fontconfig freetype gslib gvc heic jbig jng jp2 jpeg jxl lcms lqr ltdl lzma openexr pangocairo png ps raqm raw rsvg tiff webp wmf x xml zip zlib
Compiler: gcc (13.2)
```

CheckConsents tool use `Tesseract` to detect orientation of pages.

To work, it requires to have `osd.traineddata` file available in `resources` folder.
You can download it at: https://github.com/tesseract-ocr/tessdata/raw/3.04.00/osd.traineddata

You may need to set TESSDATA_PREFIX env var.

```bash
export TESSDATA_PREFIX="/path/to/folder/which/contains/traineddata_files"
```

## Usage

```bash
$ ./checkconsents.py  --help
usage: checkconsents.py [-h] [-v] -i INPUT_FOLDER [-w WORKING_DIR]
                        [--configfile CONFIGFILE]
                        [--log_level {ERROR,error,WARNING,warning,INFO,info,DEBUG,debug}]
                        [--log_file LOG_FILE]

Check consent checkboxes into consent forms (pdf format)

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Inputs:
  -i INPUT_FOLDER, --input_folder INPUT_FOLDER
                        path of input directory (default: None)
  -w WORKING_DIR, --working_dir WORKING_DIR
                        Directory use to generate intermediates (default:
                        /tmp)

Config:
  --configfile CONFIGFILE
                        configfile filepath (default:
                        ./checkconsents_config.yml)

Logger:
  --log_level {ERROR,error,WARNING,warning,INFO,info,DEBUG,debug}
                        log level (default: INFO)
  --log_file LOG_FILE   log file (use the stderr by default) (default: None)
```

```bash
$ mkdir target
$ ./checkconsents.py  --input_folder ./tests/resources/initial_data --configfile resources/checkconsents_config.yml -w ./target
```

```bash
$ docker run --rm \
             -v ./target:/code/target  \
             -v ./resources:/code/resources  \
             -v ./tests/resources:/code/tests/resources cad/checkconsents:1.0.0 \
                                                        --input_folder ./tests/resources/initial_data  \
                                                        --configfile resources/checkconsents_config.yml  \
                                                        -w /code/target

```

### Outputs

`CheckConsents` tool creates an output folder (like `CheckConsents_20231102-141811`) into the working directory.
Inside this directory, `CheckConsents` tool generates a json file with all results.
If some forms have not been resolved a debugging image is generated for an human review. In this specific case, `CheckConsents` exits with code = 3.

The debug level, enabled by adding `--log_level debug` to the command line, increases the verbosity of logs and generates by default all final debugging images.

### Config file

You can use the config file is to define all templates to use and adding/change value for some parameters.

You have an example here: [resources/checkconsents_config.yml] (resources/checkconsents_config.yml).

| var                                                                                                                                                                                                      | description                                                                                 | default value                  |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|--------------------------------|
| intermediates                                                                                                                                                                                            | keep intermediate files                                                                     | False                          |
| parsing_header_limit                                                                                                                                                                                     | max of lines read (correspond to the max size of title). Must be an integer greater than 0. | 5                              |
| <dl><dt>conversion:</dt><dd>density: 300</dd><dd>opt_args: "..."</dd></dl>                                                                                                                               | Define specific parameter for pdf conversion to png                                         | density = 300<br>opt_args=None |
| <dl><dt>templates:</dt><dd>mytemplatename: "name of template"</dd><dd>pattern: "sentence you want to catch"</dd><dd>path: path/to/your/template.svg</dd><dd>priority: <integer greater than 0></dd></dl> | Dict to describe all your templates                                                         | None                           |
| <dl><dt>pages:</dt><dd>recherche: "phrase"</dd></dl>                                                                                                                                                     | describe the patterns to identify the right page to analyse                                 | None                           |

### Exit codes

| code | description                                             |
|------|---------------------------------------------------------|
| 0    | Success                                                 |
| 1    | input directory does not exist                          |
| 2    | error during pdf conversion to png                      |
| 3    | Some form can be resolved. See logs for further details |

## Development 

You can use virtualenv locally or use the docker compose file: `compose-dev.yml`.

### Setup virtualenv

```bash
$ python -m venv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

### Docker dev env

It requires Dockre and Docker compose installed. 
All folders and files form the repository are available into `/code` directory.

```bash
$ docker compose -f compose-dev.yml
$ docker compose -f compose-dev.yml ps
$ docker exec -it checkconsents-app-1 /bin/bash 
cad@853796383c04:/code$ source dev.docker.bashrc      # load aliases (optional but recommended)
[cad@docker-853796383c04 /code] [07.11.2023 09:25:52] $
```

### Tests

#### Unit/Functional tests

We use PyTest to define and run our tests.

Run all tests (in dev container):

```bash
[cad@docker-853796383c04 /code] [07.11.2023 09:25:52] $ pytest
```

Run test of a specific submodule (in dev container):

```bash
[cad@docker-853796383c04 /code] [07.11.2023 09:25:52] $ # pytest tests/test_<submodule name>.py
[cad@docker-853796383c04 /code] [07.11.2023 09:25:52] $ pytest tests/test_templates.py

# list data used for tests
[cad@docker-853796383c04 /code] [07.11.2023 09:35:42] $ ll /tmp/pytest-of-cad/pytest-current/datacurrent/
total 8984
drwx------. 1 cad cad     226 Nov  7 09:34 .
drwx------. 1 cad cad     140 Nov  7 09:34 ..
-rw-r--r--. 1 cad cad 2781876 Nov  7 09:34 functests_consent-0.png
-rw-r--r--. 1 cad cad 1354738 Nov  7 09:34 functests_consent-1.png
-rw-r--r--. 1 cad cad 1348930 Nov  7 09:34 functests_consent-2.png
-rw-r--r--. 1 cad cad 2130168 Nov  7 09:34 functests_consent-3.png
-rw-r--r--. 1 cad cad 1571076 Nov  7 09:34 functests_consent.pdf
```

Compute test coverage (in dev container):

```bash
[cad@docker-853796383c04 /code] [30.11.2023 14:53:29] $ pytest --cov=consentforms
```

Generate a test report (in dev container):

```bash
[cad@docker-853796383c04 /code] [30.11.2023 14:53:29] $ pytest --html=report.html

# with test coverage
[cad@docker-853796383c04 /code] [30.11.2023 14:53:29] $ pytest --html=report.html --cov=consentforms

# with test coverage report
[cad@docker-853796383c04 /code] [30.11.2023 14:53:29] $ pytest --html=report.html --cov=consentforms --cov-report html
```

#### Running Tests

Using local virtualenv:

```bash
(env) $ python checkconsents.py --input_folder ./tests/resources --configfile resources/checkconsents_config.yml --log_level debug -w ./target

(env) $ python -m pdb checkconsents.py --input_folder ./tests/resources --configfile resources/checkconsents_config.yml --log_level debug -w ./target
```

Analyse all example files from `tests/resources/initial_data` :

```bash
$ mkdir target
$ docker run --rm \
             -v /etc/localtime:/etc/localtime:ro \
             -v ./target:/code/target \
             -v ./resources:/code/resources \
             -v ./tests/resources:/code/tests/resources \
             cad/checkconsents:1.0.0 \
                      --input_folder ./tests/resources/initial_data \
                      --configfile resources/checkconsents_config.yml \
                      --working_dir /code/target

# NB if you have timezone setted on your host add the followwing docker option : -v /etc/timezone:/etc/timezone:ro 
```


#### Debugging using docker image:

```bash
$ docker build -t cad/checkconsents:test .

$ docker run --rm \
             -v ./target:/code/target \
             -v ./checkconsents.py:/code/checkconsents.py \
             -v ./resources:/code/resources \
             -v ./tests/resources:/code/tests/resources cad/checkconsents:test \
                --input_folder ./tests/resources \
                --configfile resources/checkconsents_config.yml \
                --log_level debug \
                -w /code/target

# debug
$ docker run --rm -it --entrypoint python \
             -v ./target:/code/target \
             -v ./checkconsents.py:/code/checkconsents.py \
             -v ./resources:/code/resources \
             -v ./tests/resources:/code/tests/resources cad/checkconsents:test \
                -m pdb /code/checkconsents.py \
                --input_folder ./tests/resources \
                --configfile resources/checkconsents_config.yml \
                --log_level debug \
                -w /code/target

```

## Documentation

### Generate documentation

This project uses Sphinx to generate the documentation

```bash
$ python -m venv env_doc
$ source env_doc/bin/activate
$ pip install -U sphinx
```
## Docker

A development image can be build from the available `Dockerfile`.
This image is base on `python:3.12-slim` image.

### Build docker image

We define a dockerfile to setup the perfect environment for `CheckConsents` tool without installing any dependencies on your machine.
This image is not production ready. We recommend to use it only for dev and testing purpose.

```bash
$ docker build -t cad/checkconsents:1.0.0 .
```

```bash
$ docker run --rm cad/checkconsents:1.0.0
usage: checkconsents.py [-h] [-v] -i INPUT_FOLDER [-w WORKING_DIR]
                        [--configfile CONFIGFILE]
                        [--log_level {ERROR,error,WARNING,warning,INFO,info,DEBUG,debug}]
                        [--log_file LOG_FILE]

Check consent checkboxes into consent forms (pdf format)

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Inputs:
  -i INPUT_FOLDER, --input_folder INPUT_FOLDER
                        path of input directory (default: None)
  -w WORKING_DIR, --working_dir WORKING_DIR
                        Directory use to generate intermediates (default:
                        /tmp)

Config:
  --configfile CONFIGFILE
                        configfile filepath (default:
                        /code/checkconsents_config.yml)

Logger:
  --log_level {ERROR,error,WARNING,warning,INFO,info,DEBUG,debug}
                        log level (default: INFO)
  --log_file LOG_FILE   log file (use the stderr by default) (default: None)
```

### Known vulnerabilities

```
$ grype cad/checkconsents:1.0.0
 ✔ Vulnerability DB                [updated]  
 ✔ Loaded image                                                                                                                                                                                                                                                                                      cad/checkconsents:1.0.0
 ✔ Parsed image                                                                                                                                                                                                                                      sha256:0783c28c9a929d73605dabdb6f17f59a5c64b8dd0cee7054ff52dacdc426ceaa
 ✔ Cataloged packages              [442 packages]  
 ✔ Scanned for vulnerabilities     [496 vulnerability matches]  
   ├── by severity: 2 critical, 48 high, 117 medium, 13 low, 306 negligible (10 unknown)
   └── by status:   0 fixed, 496 not-fixed, 0 ignored 
NAME                       INSTALLED                FIXED-IN     TYPE    VULNERABILITY     SEVERITY   
apt                        2.6.1                                 deb     CVE-2011-3374     Negligible  
binutils                   2.40-2                                deb     CVE-2023-1972     Negligible  
binutils                   2.40-2                                deb     CVE-2021-32256    Negligible  
binutils                   2.40-2                                deb     CVE-2018-9996     Negligible  
binutils                   2.40-2                                deb     CVE-2018-20712    Negligible  
binutils                   2.40-2                                deb     CVE-2018-20673    Negligible  
binutils                   2.40-2                                deb     CVE-2018-18483    Negligible  
binutils                   2.40-2                                deb     CVE-2017-13716    Negligible  
binutils-common            2.40-2                                deb     CVE-2023-1972     Negligible  
binutils-common            2.40-2                                deb     CVE-2021-32256    Negligible  
binutils-common            2.40-2                                deb     CVE-2018-9996     Negligible  
binutils-common            2.40-2                                deb     CVE-2018-20712    Negligible  
binutils-common            2.40-2                                deb     CVE-2018-20673    Negligible  
binutils-common            2.40-2                                deb     CVE-2018-18483    Negligible  
binutils-common            2.40-2                                deb     CVE-2017-13716    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                deb     CVE-2023-1972     Negligible  
binutils-x86-64-linux-gnu  2.40-2                                deb     CVE-2021-32256    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                deb     CVE-2018-9996     Negligible  
binutils-x86-64-linux-gnu  2.40-2                                deb     CVE-2018-20712    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                deb     CVE-2018-20673    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                deb     CVE-2018-18483    Negligible  
binutils-x86-64-linux-gnu  2.40-2                                deb     CVE-2017-13716    Negligible  
bsdutils                   1:2.38.1-5+b1                         deb     CVE-2022-0563     Negligible  
coreutils                  9.1-1                    (won't fix)  deb     CVE-2016-2781     Low         
coreutils                  9.1-1                                 deb     CVE-2017-18018    Negligible  
cpp-12                     12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
cpp-12                     12.2.0-14                             deb     CVE-2022-27943    Negligible  
ffmpeg                     7:5.1.3-1                (won't fix)  deb     CVE-2022-4907     High        
gcc-12                     12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
gcc-12                     12.2.0-14                             deb     CVE-2022-27943    Negligible  
gcc-12-base                12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
gcc-12-base                12.2.0-14                             deb     CVE-2022-27943    Negligible  
ghostscript                10.0.0~dfsg-11+deb12u2                deb     CVE-2023-38560    Negligible  
ghostscript                10.0.0~dfsg-11+deb12u2                deb     CVE-2022-1350     Negligible  
gpgv                       2.2.40-1.1                            deb     CVE-2022-3219     Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2021-3610     High        
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-3428     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-34151    Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-3195     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-2157     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1906     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1289     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-3213     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-1115     Medium      
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-34152    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2021-20311    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2018-15607    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-7275     Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11755    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11754    Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2016-8678     Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2008-3134     Negligible  
imagemagick                8:6.9.11.60+dfsg-1.6                  deb     CVE-2005-0406     Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2021-3610     High        
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-3428     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-34151    Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-3195     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-2157     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1906     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1289     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-3213     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-1115     Medium      
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-34152    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2021-20311    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2018-15607    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-7275     Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11755    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11754    Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2016-8678     Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2008-3134     Negligible  
imagemagick-6-common       8:6.9.11.60+dfsg-1.6                  deb     CVE-2005-0406     Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2021-3610     High        
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-3428     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-34151    Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-3195     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-2157     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1906     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1289     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-3213     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-1115     Medium      
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-34152    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2021-20311    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2018-15607    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-7275     Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11755    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11754    Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2016-8678     Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2008-3134     Negligible  
imagemagick-6.q16          8:6.9.11.60+dfsg-1.6                  deb     CVE-2005-0406     Negligible  
libaom3                    3.6.0-1                  (won't fix)  deb     CVE-2023-39616    High        
libapt-pkg6.0              2.6.1                                 deb     CVE-2011-3374     Negligible  
libarchive-dev             3.6.2-1                  (won't fix)  deb     CVE-2023-30571    Medium      
libarchive13               3.6.2-1                  (won't fix)  deb     CVE-2023-30571    Medium      
libasan8                   12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libasan8                   12.2.0-14                             deb     CVE-2022-27943    Negligible  
libatomic1                 12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libatomic1                 12.2.0-14                             deb     CVE-2022-27943    Negligible  
libavahi-client3           0.8-10                   (won't fix)  deb     CVE-2023-38473    Medium      
libavahi-client3           0.8-10                   (won't fix)  deb     CVE-2023-38472    Medium      
libavahi-client3           0.8-10                   (won't fix)  deb     CVE-2023-38471    Medium      
libavahi-client3           0.8-10                   (won't fix)  deb     CVE-2023-38470    Medium      
libavahi-client3           0.8-10                   (won't fix)  deb     CVE-2023-38469    Medium      
libavahi-common-data       0.8-10                   (won't fix)  deb     CVE-2023-38473    Medium      
libavahi-common-data       0.8-10                   (won't fix)  deb     CVE-2023-38472    Medium      
libavahi-common-data       0.8-10                   (won't fix)  deb     CVE-2023-38471    Medium      
libavahi-common-data       0.8-10                   (won't fix)  deb     CVE-2023-38470    Medium      
libavahi-common-data       0.8-10                   (won't fix)  deb     CVE-2023-38469    Medium      
libavahi-common3           0.8-10                   (won't fix)  deb     CVE-2023-38473    Medium      
libavahi-common3           0.8-10                   (won't fix)  deb     CVE-2023-38472    Medium      
libavahi-common3           0.8-10                   (won't fix)  deb     CVE-2023-38471    Medium      
libavahi-common3           0.8-10                   (won't fix)  deb     CVE-2023-38470    Medium      
libavahi-common3           0.8-10                   (won't fix)  deb     CVE-2023-38469    Medium      
libavcodec59               7:5.1.3-1                (won't fix)  deb     CVE-2022-4907     High        
libavdevice59              7:5.1.3-1                (won't fix)  deb     CVE-2022-4907     High        
libavfilter8               7:5.1.3-1                (won't fix)  deb     CVE-2022-4907     High        
libavformat59              7:5.1.3-1                (won't fix)  deb     CVE-2022-4907     High        
libavutil57                7:5.1.3-1                (won't fix)  deb     CVE-2022-4907     High        
libbinutils                2.40-2                                deb     CVE-2023-1972     Negligible  
libbinutils                2.40-2                                deb     CVE-2021-32256    Negligible  
libbinutils                2.40-2                                deb     CVE-2018-9996     Negligible  
libbinutils                2.40-2                                deb     CVE-2018-20712    Negligible  
libbinutils                2.40-2                                deb     CVE-2018-20673    Negligible  
libbinutils                2.40-2                                deb     CVE-2018-18483    Negligible  
libbinutils                2.40-2                                deb     CVE-2017-13716    Negligible  
libblkid1                  2.38.1-5+b1                           deb     CVE-2022-0563     Negligible  
libc-bin                   2.36-9+deb12u3                        deb     CVE-2019-9192     Negligible  
libc-bin                   2.36-9+deb12u3                        deb     CVE-2019-1010025  Negligible  
libc-bin                   2.36-9+deb12u3                        deb     CVE-2019-1010024  Negligible  
libc-bin                   2.36-9+deb12u3                        deb     CVE-2019-1010023  Negligible  
libc-bin                   2.36-9+deb12u3                        deb     CVE-2019-1010022  Negligible  
libc-bin                   2.36-9+deb12u3                        deb     CVE-2018-20796    Negligible  
libc-bin                   2.36-9+deb12u3                        deb     CVE-2010-4756     Negligible  
libc-dev-bin               2.36-9+deb12u3                        deb     CVE-2019-9192     Negligible  
libc-dev-bin               2.36-9+deb12u3                        deb     CVE-2019-1010025  Negligible  
libc-dev-bin               2.36-9+deb12u3                        deb     CVE-2019-1010024  Negligible  
libc-dev-bin               2.36-9+deb12u3                        deb     CVE-2019-1010023  Negligible  
libc-dev-bin               2.36-9+deb12u3                        deb     CVE-2019-1010022  Negligible  
libc-dev-bin               2.36-9+deb12u3                        deb     CVE-2018-20796    Negligible  
libc-dev-bin               2.36-9+deb12u3                        deb     CVE-2010-4756     Negligible  
libc6                      2.36-9+deb12u3                        deb     CVE-2019-9192     Negligible  
libc6                      2.36-9+deb12u3                        deb     CVE-2019-1010025  Negligible  
libc6                      2.36-9+deb12u3                        deb     CVE-2019-1010024  Negligible  
libc6                      2.36-9+deb12u3                        deb     CVE-2019-1010023  Negligible  
libc6                      2.36-9+deb12u3                        deb     CVE-2019-1010022  Negligible  
libc6                      2.36-9+deb12u3                        deb     CVE-2018-20796    Negligible  
libc6                      2.36-9+deb12u3                        deb     CVE-2010-4756     Negligible  
libc6-dev                  2.36-9+deb12u3                        deb     CVE-2019-9192     Negligible  
libc6-dev                  2.36-9+deb12u3                        deb     CVE-2019-1010025  Negligible  
libc6-dev                  2.36-9+deb12u3                        deb     CVE-2019-1010024  Negligible  
libc6-dev                  2.36-9+deb12u3                        deb     CVE-2019-1010023  Negligible  
libc6-dev                  2.36-9+deb12u3                        deb     CVE-2019-1010022  Negligible  
libc6-dev                  2.36-9+deb12u3                        deb     CVE-2018-20796    Negligible  
libc6-dev                  2.36-9+deb12u3                        deb     CVE-2010-4756     Negligible  
libcaca0                   0.99.beta20-3                         deb     CVE-2022-0856     Negligible  
libcairo-gobject2          1.16.0-7                 (won't fix)  deb     CVE-2019-6462     Low         
libcairo-gobject2          1.16.0-7                 (won't fix)  deb     CVE-2019-6461     Low         
libcairo-gobject2          1.16.0-7                 (won't fix)  deb     CVE-2018-18064    Low         
libcairo-gobject2          1.16.0-7                 (won't fix)  deb     CVE-2017-7475     Low         
libcairo2                  1.16.0-7                 (won't fix)  deb     CVE-2019-6462     Low         
libcairo2                  1.16.0-7                 (won't fix)  deb     CVE-2019-6461     Low         
libcairo2                  1.16.0-7                 (won't fix)  deb     CVE-2018-18064    Low         
libcairo2                  1.16.0-7                 (won't fix)  deb     CVE-2017-7475     Low         
libcc1-0                   12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libcc1-0                   12.2.0-14                             deb     CVE-2022-27943    Negligible  
libctf-nobfd0              2.40-2                                deb     CVE-2023-1972     Negligible  
libctf-nobfd0              2.40-2                                deb     CVE-2021-32256    Negligible  
libctf-nobfd0              2.40-2                                deb     CVE-2018-9996     Negligible  
libctf-nobfd0              2.40-2                                deb     CVE-2018-20712    Negligible  
libctf-nobfd0              2.40-2                                deb     CVE-2018-20673    Negligible  
libctf-nobfd0              2.40-2                                deb     CVE-2018-18483    Negligible  
libctf-nobfd0              2.40-2                                deb     CVE-2017-13716    Negligible  
libctf0                    2.40-2                                deb     CVE-2023-1972     Negligible  
libctf0                    2.40-2                                deb     CVE-2021-32256    Negligible  
libctf0                    2.40-2                                deb     CVE-2018-9996     Negligible  
libctf0                    2.40-2                                deb     CVE-2018-20712    Negligible  
libctf0                    2.40-2                                deb     CVE-2018-20673    Negligible  
libctf0                    2.40-2                                deb     CVE-2018-18483    Negligible  
libctf0                    2.40-2                                deb     CVE-2017-13716    Negligible  
libcups2                   2.4.2-3+deb12u4                       deb     CVE-2014-8166     Negligible  
libdav1d6                  1.0.0-2                  (won't fix)  deb     CVE-2023-32570    Medium      
libde265-0                 1.0.11-1                 (won't fix)  deb     CVE-2023-27103    High        
libde265-0                 1.0.11-1                 (won't fix)  deb     CVE-2023-27102    Medium      
libgcc-12-dev              12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libgcc-12-dev              12.2.0-14                             deb     CVE-2022-27943    Negligible  
libgcc-s1                  12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libgcc-s1                  12.2.0-14                             deb     CVE-2022-27943    Negligible  
libgcrypt20                1.10.1-3                              deb     CVE-2018-6829     Negligible  
libgfortran5               12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libgfortran5               12.2.0-14                             deb     CVE-2022-27943    Negligible  
libgif7                    5.2.1-2.5                             deb     CVE-2023-39742    Negligible  
libgif7                    5.2.1-2.5                             deb     CVE-2022-28506    Negligible  
libgif7                    5.2.1-2.5                             deb     CVE-2021-40633    Negligible  
libgif7                    5.2.1-2.5                             deb     CVE-2020-23922    Negligible  
libglib2.0-0               2.74.6-2                              deb     CVE-2012-0039     Negligible  
libgnutls30                3.7.9-2                               deb     CVE-2011-3389     Negligible  
libgomp1                   12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libgomp1                   12.2.0-14                             deb     CVE-2022-27943    Negligible  
libgprofng0                2.40-2                                deb     CVE-2023-1972     Negligible  
libgprofng0                2.40-2                                deb     CVE-2021-32256    Negligible  
libgprofng0                2.40-2                                deb     CVE-2018-9996     Negligible  
libgprofng0                2.40-2                                deb     CVE-2018-20712    Negligible  
libgprofng0                2.40-2                                deb     CVE-2018-20673    Negligible  
libgprofng0                2.40-2                                deb     CVE-2018-18483    Negligible  
libgprofng0                2.40-2                                deb     CVE-2017-13716    Negligible  
libgs-common               10.0.0~dfsg-11+deb12u2                deb     CVE-2023-38560    Negligible  
libgs-common               10.0.0~dfsg-11+deb12u2                deb     CVE-2022-1350     Negligible  
libgs10                    10.0.0~dfsg-11+deb12u2                deb     CVE-2023-38560    Negligible  
libgs10                    10.0.0~dfsg-11+deb12u2                deb     CVE-2022-1350     Negligible  
libgs10-common             10.0.0~dfsg-11+deb12u2                deb     CVE-2023-38560    Negligible  
libgs10-common             10.0.0~dfsg-11+deb12u2                deb     CVE-2022-1350     Negligible  
libgssapi-krb5-2           1.20.1-2+deb12u1                      deb     CVE-2018-5709     Negligible  
libharfbuzz0b              6.0.0+dfsg-3             (won't fix)  deb     CVE-2023-25193    High        
libheif1                   1.15.1-1                 (won't fix)  deb     CVE-2023-29659    Medium      
libitm1                    12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libitm1                    12.2.0-14                             deb     CVE-2022-27943    Negligible  
libjansson4                2.14-2                                deb     CVE-2020-36325    Negligible  
libjbig0                   2.1-6.1                               deb     CVE-2017-9937     Negligible  
libjbig2dec0               0.19-3                   (won't fix)  deb     CVE-2023-46361    Unknown     
libjxl0.7                  0.7.0-10                 (won't fix)  deb     CVE-2023-0645     Critical    
libjxl0.7                  0.7.0-10                 (won't fix)  deb     CVE-2023-35790    High        
libjxl0.7                  0.7.0-10                              deb     CVE-2021-36691    Negligible  
libk5crypto3               1.20.1-2+deb12u1                      deb     CVE-2018-5709     Negligible  
libkrb5-3                  1.20.1-2+deb12u1                      deb     CVE-2018-5709     Negligible  
libkrb5support0            1.20.1-2+deb12u1                      deb     CVE-2018-5709     Negligible  
libldap-2.5-0              2.5.13+dfsg-5            (won't fix)  deb     CVE-2023-2953     High        
libldap-2.5-0              2.5.13+dfsg-5                         deb     CVE-2020-15719    Negligible  
libldap-2.5-0              2.5.13+dfsg-5                         deb     CVE-2017-17740    Negligible  
libldap-2.5-0              2.5.13+dfsg-5                         deb     CVE-2017-14159    Negligible  
libldap-2.5-0              2.5.13+dfsg-5                         deb     CVE-2015-3276     Negligible  
libllvm15                  1:15.0.6-4+b1                         deb     CVE-2023-29942    Negligible  
libllvm15                  1:15.0.6-4+b1                         deb     CVE-2023-29941    Negligible  
libllvm15                  1:15.0.6-4+b1                         deb     CVE-2023-29939    Negligible  
libllvm15                  1:15.0.6-4+b1                         deb     CVE-2023-29935    Negligible  
libllvm15                  1:15.0.6-4+b1                         deb     CVE-2023-29934    Negligible  
libllvm15                  1:15.0.6-4+b1                         deb     CVE-2023-29933    Negligible  
libllvm15                  1:15.0.6-4+b1                         deb     CVE-2023-29932    Negligible  
libllvm15                  1:15.0.6-4+b1                         deb     CVE-2023-26924    Negligible  
liblsan0                   12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
liblsan0                   12.2.0-14                             deb     CVE-2022-27943    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2021-3610     High        
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-3428     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-34151    Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-3195     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-2157     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1906     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1289     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-3213     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-1115     Medium      
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-34152    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2021-20311    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2018-15607    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-7275     Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11755    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11754    Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2016-8678     Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2008-3134     Negligible  
libmagickcore-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2005-0406     Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2021-3610     High        
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-3428     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-34151    Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-3195     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-2157     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1906     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2023-1289     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-3213     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6     (won't fix)  deb     CVE-2022-1115     Medium      
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2023-34152    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2021-20311    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2018-15607    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-7275     Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11755    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2017-11754    Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2016-8678     Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2008-3134     Negligible  
libmagickwand-6.q16-6      8:6.9.11.60+dfsg-1.6                  deb     CVE-2005-0406     Negligible  
libmbedcrypto7             2.28.3-1                              deb     CVE-2023-43615    Negligible  
libmbedcrypto7             2.28.3-1                              deb     CVE-2018-1000520  Negligible  
libmount1                  2.38.1-5+b1                           deb     CVE-2022-0563     Negligible  
libnghttp2-14              1.52.0-1                              deb     CVE-2023-44487    Negligible  
libnss3                    2:3.87.1-1                            deb     CVE-2017-11698    Negligible  
libnss3                    2:3.87.1-1                            deb     CVE-2017-11697    Negligible  
libnss3                    2:3.87.1-1                            deb     CVE-2017-11696    Negligible  
libnss3                    2:3.87.1-1                            deb     CVE-2017-11695    Negligible  
libnss3                    2:3.87.1-1               (won't fix)  deb     CVE-2023-5388     Unknown     
libopenjp2-7               2.5.0-2                  (won't fix)  deb     CVE-2021-3575     High        
libopenjp2-7               2.5.0-2                  (won't fix)  deb     CVE-2019-6988     Low         
libopenjp2-7               2.5.0-2                               deb     CVE-2018-20846    Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2018-16376    Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2018-16375    Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2017-17479    Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2016-9581     Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2016-9580     Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2016-9117     Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2016-9116     Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2016-9115     Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2016-9114     Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2016-9113     Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2016-10506    Negligible  
libopenjp2-7               2.5.0-2                               deb     CVE-2016-10505    Negligible  
libperl5.36                5.36.0-7                 (won't fix)  deb     CVE-2023-31484    High        
libperl5.36                5.36.0-7                              deb     CVE-2023-31486    Negligible  
libperl5.36                5.36.0-7                              deb     CVE-2011-4116     Negligible  
libpixman-1-0              0.42.2-1                 (won't fix)  deb     CVE-2023-37769    Medium      
libpng16-16                1.6.39-2                              deb     CVE-2021-4214     Negligible  
libpostproc56              7:5.1.3-1                (won't fix)  deb     CVE-2022-4907     High        
libpython3.11-minimal      3.11.2-6                 (won't fix)  deb     CVE-2023-41105    High        
libpython3.11-minimal      3.11.2-6                 (won't fix)  deb     CVE-2023-24329    High        
libpython3.11-minimal      3.11.2-6                              deb     CVE-2023-40217    Medium      
libpython3.11-minimal      3.11.2-6                 (won't fix)  deb     CVE-2023-27043    Medium      
libpython3.11-minimal      3.11.2-6                              deb     CVE-2023-24535    Negligible  
libpython3.11-stdlib       3.11.2-6                 (won't fix)  deb     CVE-2023-41105    High        
libpython3.11-stdlib       3.11.2-6                 (won't fix)  deb     CVE-2023-24329    High        
libpython3.11-stdlib       3.11.2-6                              deb     CVE-2023-40217    Medium      
libpython3.11-stdlib       3.11.2-6                 (won't fix)  deb     CVE-2023-27043    Medium      
libpython3.11-stdlib       3.11.2-6                              deb     CVE-2023-24535    Negligible  
libquadmath0               12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libquadmath0               12.2.0-14                             deb     CVE-2022-27943    Negligible  
librabbitmq4               0.11.0-1+b1              (won't fix)  deb     CVE-2023-35789    Medium      
libsmartcols1              2.38.1-5+b1                           deb     CVE-2022-0563     Negligible  
libsndfile1                1.2.0-1                  (won't fix)  deb     CVE-2022-33065    High        
libsndfile1                1.2.0-1                  (won't fix)  deb     CVE-2022-33064    High        
libsqlite3-0               3.40.1-2                              deb     CVE-2021-45346    Negligible  
libssl3                    3.0.11-1~deb12u2                      deb     CVE-2010-0928     Negligible  
libssl3                    3.0.11-1~deb12u2                      deb     CVE-2007-6755     Negligible  
libstdc++6                 12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libstdc++6                 12.2.0-14                             deb     CVE-2022-27943    Negligible  
libswresample4             7:5.1.3-1                (won't fix)  deb     CVE-2022-4907     High        
libswscale6                7:5.1.3-1                (won't fix)  deb     CVE-2022-4907     High        
libsystemd0                252.17-1~deb12u1                      deb     CVE-2023-31439    Negligible  
libsystemd0                252.17-1~deb12u1                      deb     CVE-2023-31438    Negligible  
libsystemd0                252.17-1~deb12u1                      deb     CVE-2023-31437    Negligible  
libsystemd0                252.17-1~deb12u1                      deb     CVE-2013-4392     Negligible  
libtiff6                   4.5.0-6                               deb     CVE-2023-41175    Medium      
libtiff6                   4.5.0-6                               deb     CVE-2023-40745    Medium      
libtiff6                   4.5.0-6                  (won't fix)  deb     CVE-2023-3618     Medium      
libtiff6                   4.5.0-6                               deb     CVE-2023-3576     Medium      
libtiff6                   4.5.0-6                  (won't fix)  deb     CVE-2023-3316     Medium      
libtiff6                   4.5.0-6                  (won't fix)  deb     CVE-2023-2908     Medium      
libtiff6                   4.5.0-6                  (won't fix)  deb     CVE-2023-26966    Medium      
libtiff6                   4.5.0-6                  (won't fix)  deb     CVE-2023-26965    Medium      
libtiff6                   4.5.0-6                  (won't fix)  deb     CVE-2023-25433    Medium      
libtiff6                   4.5.0-6                               deb     CVE-2023-3164     Negligible  
libtiff6                   4.5.0-6                               deb     CVE-2023-1916     Negligible  
libtiff6                   4.5.0-6                               deb     CVE-2022-1210     Negligible  
libtiff6                   4.5.0-6                               deb     CVE-2018-10126    Negligible  
libtiff6                   4.5.0-6                               deb     CVE-2017-9117     Negligible  
libtiff6                   4.5.0-6                               deb     CVE-2017-5563     Negligible  
libtiff6                   4.5.0-6                               deb     CVE-2017-17973    Negligible  
libtiff6                   4.5.0-6                               deb     CVE-2017-16232    Negligible  
libtsan2                   12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libtsan2                   12.2.0-14                             deb     CVE-2022-27943    Negligible  
libubsan1                  12.2.0-14                (won't fix)  deb     CVE-2023-4039     Medium      
libubsan1                  12.2.0-14                             deb     CVE-2022-27943    Negligible  
libudev1                   252.17-1~deb12u1                      deb     CVE-2023-31439    Negligible  
libudev1                   252.17-1~deb12u1                      deb     CVE-2023-31438    Negligible  
libudev1                   252.17-1~deb12u1                      deb     CVE-2023-31437    Negligible  
libudev1                   252.17-1~deb12u1                      deb     CVE-2013-4392     Negligible  
libuuid1                   2.38.1-5+b1                           deb     CVE-2022-0563     Negligible  
libvpx7                    1.12.0-1+deb12u2                      deb     CVE-2017-0641     Negligible  
libxml2                    2.9.14+dfsg-1.3~deb12u1  (won't fix)  deb     CVE-2023-45322    Medium      
libxml2                    2.9.14+dfsg-1.3~deb12u1  (won't fix)  deb     CVE-2023-39615    Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-5717     High        
linux-libc-dev             6.1.55-1                              deb     CVE-2023-5633     High        
linux-libc-dev             6.1.55-1                              deb     CVE-2023-5345     High        
linux-libc-dev             6.1.55-1                              deb     CVE-2023-5178     High        
linux-libc-dev             6.1.55-1                              deb     CVE-2023-3640     High        
linux-libc-dev             6.1.55-1                              deb     CVE-2023-35827    High        
linux-libc-dev             6.1.55-1                              deb     CVE-2023-3397     High        
linux-libc-dev             6.1.55-1                              deb     CVE-2023-2176     High        
linux-libc-dev             6.1.55-1                              deb     CVE-2021-3864     High        
linux-libc-dev             6.1.55-1                              deb     CVE-2021-3847     High        
linux-libc-dev             6.1.55-1                 (won't fix)  deb     CVE-2019-19814    High        
linux-libc-dev             6.1.55-1                 (won't fix)  deb     CVE-2019-19449    High        
linux-libc-dev             6.1.55-1                 (won't fix)  deb     CVE-2013-7445     High        
linux-libc-dev             6.1.55-1                              deb     CVE-2023-5197     Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-5158     Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-4133     Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-4010     Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-37454    Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-37453    Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-31083    Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-31082    Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-23005    Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-21264    Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-1193     Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-1192     Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-0597     Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2023-0160     Medium      
linux-libc-dev             6.1.55-1                 (won't fix)  deb     CVE-2022-4543     Medium      
linux-libc-dev             6.1.55-1                              deb     CVE-2020-36694    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)  deb     CVE-2020-14304    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)  deb     CVE-2019-20794    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)  deb     CVE-2019-16089    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)  deb     CVE-2019-15213    Medium      
linux-libc-dev             6.1.55-1                 (won't fix)  deb     CVE-2018-12928    Low         
linux-libc-dev             6.1.55-1                              deb     CVE-2023-4134     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2023-39191    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2023-31085    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2023-31081    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2023-26242    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2023-23039    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-45888    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-45885    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-45884    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-44034    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-44033    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-44032    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-41848    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-3238     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-2961     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-25265    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-1247     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2022-0400     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2021-3714     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2021-26934    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2020-35501    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2020-11725    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-19378    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-19070    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-16234    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-16233    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-16232    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-16231    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-16230    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-16229    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-12456    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-12455    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-12382    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-12381    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-12380    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-12379    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-12378    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2019-11191    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2018-17977    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2018-1121     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2017-13694    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2017-13693    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2017-0630     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2016-8660     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2016-10723    Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2015-2877     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2014-9900     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2014-9892     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2012-4542     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2011-4917     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2011-4916     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2011-4915     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2010-5321     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2010-4563     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2008-4609     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2008-2544     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2007-3719     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2005-3660     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2004-0230     Negligible  
linux-libc-dev             6.1.55-1                              deb     CVE-2023-5090     Unknown     
linux-libc-dev             6.1.55-1                              deb     CVE-2023-47233    Unknown     
linux-libc-dev             6.1.55-1                              deb     CVE-2023-46862    Unknown     
linux-libc-dev             6.1.55-1                              deb     CVE-2023-46813    Unknown     
linux-libc-dev             6.1.55-1                              deb     CVE-2023-34324    Unknown     
login                      1:4.13+dfsg1-1+b1        (won't fix)  deb     CVE-2023-29383    Low         
login                      1:4.13+dfsg1-1+b1                     deb     CVE-2019-19882    Negligible  
login                      1:4.13+dfsg1-1+b1                     deb     CVE-2007-5686     Negligible  
login                      1:4.13+dfsg1-1+b1        (won't fix)  deb     CVE-2023-4641     Unknown     
mount                      2.38.1-5+b1                           deb     CVE-2022-0563     Negligible  
openssl                    3.0.11-1~deb12u2                      deb     CVE-2010-0928     Negligible  
openssl                    3.0.11-1~deb12u2                      deb     CVE-2007-6755     Negligible  
passwd                     1:4.13+dfsg1-1+b1        (won't fix)  deb     CVE-2023-29383    Low         
passwd                     1:4.13+dfsg1-1+b1                     deb     CVE-2019-19882    Negligible  
passwd                     1:4.13+dfsg1-1+b1                     deb     CVE-2007-5686     Negligible  
passwd                     1:4.13+dfsg1-1+b1        (won't fix)  deb     CVE-2023-4641     Unknown     
perl                       5.36.0-7                 (won't fix)  deb     CVE-2023-31484    High        
perl                       5.36.0-7                              deb     CVE-2023-31486    Negligible  
perl                       5.36.0-7                              deb     CVE-2011-4116     Negligible  
perl-base                  5.36.0-7                 (won't fix)  deb     CVE-2023-31484    High        
perl-base                  5.36.0-7                              deb     CVE-2023-31486    Negligible  
perl-base                  5.36.0-7                              deb     CVE-2011-4116     Negligible  
perl-modules-5.36          5.36.0-7                 (won't fix)  deb     CVE-2023-31484    High        
perl-modules-5.36          5.36.0-7                              deb     CVE-2023-31486    Negligible  
perl-modules-5.36          5.36.0-7                              deb     CVE-2011-4116     Negligible  
pip                        23.3.1                                python  CVE-2018-20225    High        
python3-pil                9.4.0-1.1+b1             (won't fix)  deb     CVE-2023-44271    Unknown     
python3.11                 3.11.2-6                 (won't fix)  deb     CVE-2023-41105    High        
python3.11                 3.11.2-6                 (won't fix)  deb     CVE-2023-24329    High        
python3.11                 3.11.2-6                              deb     CVE-2023-40217    Medium      
python3.11                 3.11.2-6                 (won't fix)  deb     CVE-2023-27043    Medium      
python3.11                 3.11.2-6                              deb     CVE-2023-24535    Negligible  
python3.11-minimal         3.11.2-6                 (won't fix)  deb     CVE-2023-41105    High        
python3.11-minimal         3.11.2-6                 (won't fix)  deb     CVE-2023-24329    High        
python3.11-minimal         3.11.2-6                              deb     CVE-2023-40217    Medium      
python3.11-minimal         3.11.2-6                 (won't fix)  deb     CVE-2023-27043    Medium      
python3.11-minimal         3.11.2-6                              deb     CVE-2023-24535    Negligible  
tar                        1.34+dfsg-1.2                         deb     CVE-2022-48303    Negligible  
tar                        1.34+dfsg-1.2                         deb     CVE-2005-2541     Negligible  
util-linux                 2.38.1-5+b1                           deb     CVE-2022-0563     Negligible  
util-linux-extra           2.38.1-5+b1                           deb     CVE-2022-0563     Negligible  
zlib1g                     1:1.2.13.dfsg-1                       deb     CVE-2023-45853    Critical
```

### Software Bill of Materials (SBOM)

```
$ syft cad/checkconsents:1.0.0
 ✔ Loaded image                                                                                                                                                                                                                                                                                      cad/checkconsents:1.0.0
 ✔ Parsed image                                                                                                                                                                                                                                      sha256:0783c28c9a929d73605dabdb6f17f59a5c64b8dd0cee7054ff52dacdc426ceaa
 ✔ Cataloged packages              [442 packages]  
NAME                        VERSION                         TYPE   
Deprecated                  1.2.14                          python  
Pillow                      10.1.0                          python  
Pillow                      9.4.0                           python  
PyYAML                      6.0.1                           python  
Pygments                    2.16.1                          python  
Simple Launcher Executable  1.1.0.14                        dotnet  
adduser                     3.134                           deb     
annotated-types             0.6.0                           python  
apt                         2.6.1                           deb     
attrs                       23.1.0                          python  
base-files                  12.4+deb12u2                    deb     
base-passwd                 3.6.1                           deb     
bash                        5.2.15                          binary  
bash                        5.2.15-2+b2                     deb     
binutils                    2.40-2                          deb     
binutils-common             2.40-2                          deb     
binutils-x86-64-linux-gnu   2.40-2                          deb     
bsdutils                    1:2.38.1-5+b1                   deb     
ca-certificates             20230311                        deb     
cdifflib                    1.2.6                           python  
colorful                    0.5.5                           python  
contextlib2                 21.6.0                          python  
coreutils                   9.1-1                           deb     
cpp                         4:12.2.0-3                      deb     
cpp-12                      12.2.0-14                       deb     
dash                        0.5.12-2                        deb     
debconf                     1.5.82                          deb     
debian-archive-keyring      2023.3+deb12u1                  deb     
debianutils                 5.7-0.5~deb12u1                 deb     
diffutils                   1:3.8-4                         deb     
dpkg                        1.21.22                         deb     
e2fsprogs                   1.47.0-2                        deb     
ffmpeg                      7:5.1.3-1                       deb     
findutils                   4.9.0-4                         deb     
fontconfig                  2.14.1-4                        deb     
fontconfig-config           2.14.1-4                        deb     
fonts-dejavu-core           2.37-6                          deb     
fonts-urw-base35            20200910-7                      deb     
gcc                         4:12.2.0-3                      deb     
gcc-12                      12.2.0-14                       deb     
gcc-12-base                 12.2.0-14                       deb     
ghostscript                 10.0.0~dfsg-11+deb12u2          deb     
gpgv                        2.2.40-1.1                      deb     
grep                        3.8-5                           deb     
gzip                        1.12-1                          deb     
hicolor-icon-theme          0.17-2                          deb     
hostname                    3.23+nmu1                       deb     
imagemagick                 8:6.9.11.60+dfsg-1.6            deb     
imagemagick-6-common        8:6.9.11.60+dfsg-1.6            deb     
imagemagick-6.q16           8:6.9.11.60+dfsg-1.6            deb     
imutils                     0.5.4                           python  
init-system-helpers         1.65.2                          deb     
jsonschema                  4.19.2                          python  
jsonschema-specifications   2023.7.1                        python  
libacl1                     2.3.1-3                         deb     
libaom3                     3.6.0-1                         deb     
libapt-pkg6.0               2.6.1                           deb     
libarchive-dev              3.6.2-1                         deb     
libarchive13                3.6.2-1                         deb     
libasan8                    12.2.0-14                       deb     
libasound2                  1.2.8-1+b1                      deb     
libasound2-data             1.2.8-1                         deb     
libass9                     1:0.17.1-1                      deb     
libasyncns0                 0.8-6+b3                        deb     
libatomic1                  12.2.0-14                       deb     
libattr1                    1:2.5.1-4                       deb     
libaudit-common             1:3.0.9-1                       deb     
libaudit1                   1:3.0.9-1                       deb     
libavahi-client3            0.8-10                          deb     
libavahi-common-data        0.8-10                          deb     
libavahi-common3            0.8-10                          deb     
libavc1394-0                0.5.4-5                         deb     
libavcodec59                7:5.1.3-1                       deb     
libavdevice59               7:5.1.3-1                       deb     
libavfilter8                7:5.1.3-1                       deb     
libavformat59               7:5.1.3-1                       deb     
libavutil57                 7:5.1.3-1                       deb     
libbinutils                 2.40-2                          deb     
libblas3                    3.11.0-2                        deb     
libblkid1                   2.38.1-5+b1                     deb     
libbluray2                  1:1.3.4-1                       deb     
libbrotli1                  1.0.9-2+b6                      deb     
libbs2b0                    3.1.0+dfsg-7                    deb     
libbsd0                     0.11.7-2                        deb     
libbz2-1.0                  1.0.8-5+b1                      deb     
libc-bin                    2.36-9+deb12u3                  deb     
libc-dev-bin                2.36-9+deb12u3                  deb     
libc6                       2.36-9+deb12u3                  deb     
libc6-dev                   2.36-9+deb12u3                  deb     
libcaca0                    0.99.beta20-3                   deb     
libcairo-gobject2           1.16.0-7                        deb     
libcairo2                   1.16.0-7                        deb     
libcap-ng0                  0.8.3-1+b3                      deb     
libcap2                     1:2.66-4                        deb     
libcc1-0                    12.2.0-14                       deb     
libcdio-cdda2               10.2+2.0.1-1                    deb     
libcdio-paranoia2           10.2+2.0.1-1                    deb     
libcdio19                   2.1.0-4                         deb     
libchromaprint1             1.5.1-2+b1                      deb     
libcjson1                   1.7.15-1                        deb     
libcodec2-1.0               1.0.5-1                         deb     
libcom-err2                 1.47.0-2                        deb     
libcrypt-dev                1:4.4.33-2                      deb     
libcrypt1                   1:4.4.33-2                      deb     
libctf-nobfd0               2.40-2                          deb     
libctf0                     2.40-2                          deb     
libcups2                    2.4.2-3+deb12u4                 deb     
libcurl3-nss                7.88.1-10+deb12u4               deb     
libcurl4                    7.88.1-10+deb12u4               deb     
libcurl4-nss-dev            7.88.1-10+deb12u4               deb     
libdatrie1                  0.2.13-2+b1                     deb     
libdav1d6                   1.0.0-2                         deb     
libdb5.3                    5.3.28+dfsg2-1                  deb     
libdbus-1-3                 1.14.10-1~deb12u1               deb     
libdc1394-25                2.2.6-4                         deb     
libde265-0                  1.0.11-1                        deb     
libdebconfclient0           0.270                           deb     
libdecor-0-0                0.1.1-2                         deb     
libdeflate0                 1.14-1                          deb     
libdrm-amdgpu1              2.4.114-1+b1                    deb     
libdrm-common               2.4.114-1                       deb     
libdrm-intel1               2.4.114-1+b1                    deb     
libdrm-nouveau2             2.4.114-1+b1                    deb     
libdrm-radeon1              2.4.114-1+b1                    deb     
libdrm2                     2.4.114-1+b1                    deb     
libedit2                    3.1-20221030-2                  deb     
libelf1                     0.188-2.1                       deb     
libepoxy0                   1.5.10-1                        deb     
libexpat1                   2.5.0-1                         deb     
libext2fs2                  1.47.0-2                        deb     
libffi8                     3.4.4-1                         deb     
libfftw3-double3            3.3.10-1                        deb     
libflac12                   1.4.2+ds-2                      deb     
libflite1                   2.2-5                           deb     
libfontconfig1              2.14.1-4                        deb     
libfontenc1                 1:1.1.4-1                       deb     
libfreetype6                2.12.1+dfsg-5                   deb     
libfribidi0                 1.0.8-2.1                       deb     
libgbm1                     22.3.6-1+deb12u1                deb     
libgcc-12-dev               12.2.0-14                       deb     
libgcc-s1                   12.2.0-14                       deb     
libgcrypt20                 1.10.1-3                        deb     
libgdbm-compat4             1.23-3                          deb     
libgdbm6                    1.23-3                          deb     
libgdk-pixbuf-2.0-0         2.42.10+dfsg-1+b1               deb     
libgdk-pixbuf2.0-common     2.42.10+dfsg-1                  deb     
libgfortran5                12.2.0-14                       deb     
libgif7                     5.2.1-2.5                       deb     
libgl1                      1.6.0-1                         deb     
libgl1-mesa-dri             22.3.6-1+deb12u1                deb     
libglapi-mesa               22.3.6-1+deb12u1                deb     
libglib2.0-0                2.74.6-2                        deb     
libglvnd0                   1.6.0-1                         deb     
libglx-mesa0                22.3.6-1+deb12u1                deb     
libglx0                     1.6.0-1                         deb     
libgme0                     0.6.3-6                         deb     
libgmp10                    2:6.2.1+dfsg1-1.1               deb     
libgnutls30                 3.7.9-2                         deb     
libgomp1                    12.2.0-14                       deb     
libgpg-error0               1.46-1                          deb     
libgprofng0                 2.40-2                          deb     
libgraphite2-3              1.3.14-1                        deb     
libgs-common                10.0.0~dfsg-11+deb12u2          deb     
libgs10                     10.0.0~dfsg-11+deb12u2          deb     
libgs10-common              10.0.0~dfsg-11+deb12u2          deb     
libgsm1                     1.0.22-1                        deb     
libgssapi-krb5-2            1.20.1-2+deb12u1                deb     
libharfbuzz0b               6.0.0+dfsg-3                    deb     
libheif1                    1.15.1-1                        deb     
libhogweed6                 3.8.1-2                         deb     
libhwy1                     1.0.3-3+deb12u1                 deb     
libice6                     2:1.0.10-1                      deb     
libicu72                    72.1-3                          deb     
libidn12                    1.41-1                          deb     
libidn2-0                   2.3.3-1+b1                      deb     
libiec61883-0               1.2.0-6+b1                      deb     
libijs-0.35                 0.35-15                         deb     
libimagequant0              2.17.0-1                        deb     
libisl23                    0.25-1                          deb     
libitm1                     12.2.0-14                       deb     
libjack-jackd2-0            1.9.21~dfsg-3                   deb     
libjansson4                 2.14-2                          deb     
libjbig0                    2.1-6.1                         deb     
libjbig2dec0                0.19-3                          deb     
libjpeg62-turbo             1:2.1.5-2                       deb     
libjxl0.7                   0.7.0-10                        deb     
libk5crypto3                1.20.1-2+deb12u1                deb     
libkeyutils1                1.6.3-2                         deb     
libkrb5-3                   1.20.1-2+deb12u1                deb     
libkrb5support0             1.20.1-2+deb12u1                deb     
liblapack3                  3.11.0-2                        deb     
liblcms2-2                  2.14-2                          deb     
libldap-2.5-0               2.5.13+dfsg-5                   deb     
liblept5                    1.82.0-3+b3                     deb     
libleptonica-dev            1.82.0-3+b3                     deb     
liblerc4                    4.0.0+ds-2                      deb     
liblilv-0-0                 0.24.14-1                       deb     
libllvm15                   1:15.0.6-4+b1                   deb     
liblqr-1-0                  0.4.2-2.1                       deb     
liblsan0                    12.2.0-14                       deb     
libltdl7                    2.4.7-5                         deb     
liblz4-1                    1.9.4-1                         deb     
liblzma5                    5.4.1-0.2                       deb     
libmagickcore-6.q16-6       8:6.9.11.60+dfsg-1.6            deb     
libmagickwand-6.q16-6       8:6.9.11.60+dfsg-1.6            deb     
libmbedcrypto7              2.28.3-1                        deb     
libmd0                      1.0.4-2                         deb     
libmfx1                     22.5.4-1                        deb     
libmount1                   2.38.1-5+b1                     deb     
libmp3lame0                 3.100-6                         deb     
libmpc3                     1.3.1-1                         deb     
libmpfr6                    4.2.0-1                         deb     
libmpg123-0                 1.31.2-1                        deb     
libmysofa1                  1.3.1~dfsg0-1                   deb     
libncursesw6                6.4-4                           deb     
libnettle8                  3.8.1-2                         deb     
libnghttp2-14               1.52.0-1                        deb     
libnorm1                    1.5.9+dfsg-2                    deb     
libnsl-dev                  1.3.0-2                         deb     
libnsl2                     1.3.0-2                         deb     
libnspr4                    2:4.35-1                        deb     
libnss3                     2:3.87.1-1                      deb     
libnuma1                    2.0.16-1                        deb     
libogg0                     1.3.5-3                         deb     
libopenal-data              1:1.19.1-2                      deb     
libopenal1                  1:1.19.1-2                      deb     
libopenjp2-7                2.5.0-2                         deb     
libopenmpt0                 0.6.9-1                         deb     
libopus0                    1.3.1-3                         deb     
libp11-kit0                 0.24.1-2                        deb     
libpam-modules              1.5.2-6+deb12u1                 deb     
libpam-modules-bin          1.5.2-6+deb12u1                 deb     
libpam-runtime              1.5.2-6+deb12u1                 deb     
libpam0g                    1.5.2-6+deb12u1                 deb     
libpango-1.0-0              1.50.12+ds-1                    deb     
libpangocairo-1.0-0         1.50.12+ds-1                    deb     
libpangoft2-1.0-0           1.50.12+ds-1                    deb     
libpaper1                   1.1.29                          deb     
libpciaccess0               0.17-2                          deb     
libpcre2-8-0                10.42-1                         deb     
libperl5.36                 5.36.0-7                        deb     
libpgm-5.3-0                5.3.128~dfsg-2                  deb     
libpixman-1-0               0.42.2-1                        deb     
libplacebo208               4.208.0-3                       deb     
libpng16-16                 1.6.39-2                        deb     
libpocketsphinx3            0.8+5prealpha+1-15              deb     
libpostproc56               7:5.1.3-1                       deb     
libpsl5                     0.21.2-1                        deb     
libpulse0                   16.1+dfsg1-2+b1                 deb     
libpython3-stdlib           3.11.2-1+b1                     deb     
libpython3.11-minimal       3.11.2-6                        deb     
libpython3.11-stdlib        3.11.2-6                        deb     
libquadmath0                12.2.0-14                       deb     
librabbitmq4                0.11.0-1+b1                     deb     
libraqm0                    0.7.0-4.1                       deb     
librav1e0                   0.5.1-6                         deb     
libraw1394-11               2.1.2-2                         deb     
libreadline8                8.2-1.3                         deb     
librist4                    0.2.7+dfsg-1                    deb     
librsvg2-2                  2.54.7+dfsg-1~deb12u1           deb     
librtmp1                    2.4+20151223.gitfa8646d.1-2+b2  deb     
librubberband2              3.1.2+dfsg0-1                   deb     
libsamplerate0              0.2.2-3                         deb     
libsasl2-2                  2.1.28+dfsg-10                  deb     
libsasl2-modules-db         2.1.28+dfsg-10                  deb     
libsdl2-2.0-0               2.26.5+dfsg-1                   deb     
libseccomp2                 2.5.4-1+b3                      deb     
libselinux1                 3.4-1+b6                        deb     
libsemanage-common          3.4-1                           deb     
libsemanage2                3.4-1+b5                        deb     
libsensors-config           1:3.6.0-7.1                     deb     
libsensors5                 1:3.6.0-7.1                     deb     
libsepol2                   3.4-2.1                         deb     
libserd-0-0                 0.30.16-1                       deb     
libshine3                   3.1.1-2                         deb     
libslang2                   2.3.3-3                         deb     
libsm6                      2:1.2.3-1                       deb     
libsmartcols1               2.38.1-5+b1                     deb     
libsnappy1v5                1.1.9-3                         deb     
libsndfile1                 1.2.0-1                         deb     
libsndio7.0                 1.9.0-0.3+b2                    deb     
libsodium23                 1.0.18-1                        deb     
libsord-0-0                 0.16.14+git221008-1             deb     
libsoxr0                    0.1.3-4                         deb     
libspeex1                   1.2.1-2                         deb     
libsphinxbase3              0.8+5prealpha+1-16              deb     
libsqlite3-0                3.40.1-2                        deb     
libsratom-0-0               0.6.14-1                        deb     
libsrt1.5-gnutls            1.5.1-1                         deb     
libss2                      1.47.0-2                        deb     
libssh-gcrypt-4             0.10.5-2                        deb     
libssh2-1                   1.10.0-3+b1                     deb     
libssl3                     3.0.11-1~deb12u2                deb     
libstdc++6                  12.2.0-14                       deb     
libsvtav1enc1               1.4.1+dfsg-1                    deb     
libswresample4              7:5.1.3-1                       deb     
libswscale6                 7:5.1.3-1                       deb     
libsystemd0                 252.17-1~deb12u1                deb     
libtasn1-6                  4.19.0-2                        deb     
libtesseract-dev            5.3.0-2                         deb     
libtesseract5               5.3.0-2                         deb     
libthai-data                0.1.29-1                        deb     
libthai0                    0.1.29-1                        deb     
libtheora0                  1.1.1+dfsg.1-16.1+b1            deb     
libtiff6                    4.5.0-6                         deb     
libtinfo6                   6.4-4                           deb     
libtirpc-common             1.3.3+ds-1                      deb     
libtirpc-dev                1.3.3+ds-1                      deb     
libtirpc3                   1.3.3+ds-1                      deb     
libtsan2                    12.2.0-14                       deb     
libtwolame0                 0.4.0-2                         deb     
libubsan1                   12.2.0-14                       deb     
libudev1                    252.17-1~deb12u1                deb     
libudfread0                 1.1.2-1                         deb     
libunistring2               1.0-2                           deb     
libusb-1.0-0                2:1.0.26-1                      deb     
libuuid1                    2.38.1-5+b1                     deb     
libva-drm2                  2.17.0-1                        deb     
libva-x11-2                 2.17.0-1                        deb     
libva2                      2.17.0-1                        deb     
libvdpau1                   1.5-2                           deb     
libvidstab1.1               1.1.0-2+b1                      deb     
libvorbis0a                 1.3.7-1                         deb     
libvorbisenc2               1.3.7-1                         deb     
libvorbisfile3              1.3.7-1                         deb     
libvpx7                     1.12.0-1+deb12u2                deb     
libvulkan1                  1.3.239.0-1                     deb     
libwayland-client0          1.21.0-1                        deb     
libwayland-cursor0          1.21.0-1                        deb     
libwayland-egl1             1.21.0-1                        deb     
libwayland-server0          1.21.0-1                        deb     
libwebp7                    1.2.4-0.2+deb12u1               deb     
libwebpdemux2               1.2.4-0.2+deb12u1               deb     
libwebpmux3                 1.2.4-0.2+deb12u1               deb     
libx11-6                    2:1.8.4-2+deb12u2               deb     
libx11-data                 2:1.8.4-2+deb12u2               deb     
libx11-xcb1                 2:1.8.4-2+deb12u2               deb     
libx264-164                 2:0.164.3095+gitbaee400-3       deb     
libx265-199                 3.5-2+b1                        deb     
libxau6                     1:1.0.9-1                       deb     
libxcb-dri2-0               1.15-1                          deb     
libxcb-dri3-0               1.15-1                          deb     
libxcb-glx0                 1.15-1                          deb     
libxcb-present0             1.15-1                          deb     
libxcb-randr0               1.15-1                          deb     
libxcb-render0              1.15-1                          deb     
libxcb-shape0               1.15-1                          deb     
libxcb-shm0                 1.15-1                          deb     
libxcb-sync1                1.15-1                          deb     
libxcb-xfixes0              1.15-1                          deb     
libxcb1                     1.15-1                          deb     
libxcursor1                 1:1.2.1-1                       deb     
libxdmcp6                   1:1.1.2-3                       deb     
libxext6                    2:1.3.4-1+b1                    deb     
libxfixes3                  1:6.0.0-2                       deb     
libxi6                      2:1.8-1+b1                      deb     
libxkbcommon0               1.5.0-1                         deb     
libxml2                     2.9.14+dfsg-1.3~deb12u1         deb     
libxrandr2                  2:1.5.2-2+b1                    deb     
libxrender1                 1:0.9.10-1.1                    deb     
libxshmfence1               1.3-1                           deb     
libxss1                     1:1.2.3-1                       deb     
libxt6                      1:1.2.1-1.1                     deb     
libxv1                      2:1.0.11-1.1                    deb     
libxvidcore4                2:1.3.7-1                       deb     
libxxf86vm1                 1:1.1.4-1+b2                    deb     
libxxhash0                  0.8.1-1                         deb     
libz3-4                     4.8.12-3.1                      deb     
libzimg2                    3.0.4+ds1-1                     deb     
libzmq5                     4.3.4-6                         deb     
libzstd1                    1.5.4+dfsg2-5                   deb     
libzvbi-common              0.2.41-1                        deb     
libzvbi0                    0.2.41-1                        deb     
linux-libc-dev              6.1.55-1                        deb     
login                       1:4.13+dfsg1-1+b1               deb     
logsave                     1.47.0-2                        deb     
lxml                        4.9.3                           python  
mailcap                     3.70+nmu1                       deb     
mawk                        1.3.4.20200120-3.1              deb     
media-types                 10.0.0                          deb     
mime-support                3.66                            deb     
mount                       2.38.1-5+b1                     deb     
ncurses-base                6.4-4                           deb     
ncurses-bin                 6.4-4                           deb     
netbase                     6.4                             deb     
nss-plugin-pem              1.0.8+1-1                       deb     
numpy                       1.26.1                          python  
ocl-icd-libopencl1          2.3.1-1                         deb     
opencv-python               4.8.1.78                        python  
openssl                     3.0.11-1~deb12u2                deb     
packaging                   23.2                            python  
passwd                      1:4.13+dfsg1-1+b1               deb     
perl                        5.36.0-7                        deb     
perl-base                   5.36.0-7                        deb     
perl-modules-5.36           5.36.0-7                        deb     
pip                         23.3.1                          python  
poppler-data                0.4.12-1                        deb     
prettyprinter               0.18.0                          python  
pydantic                    2.4.2                           python  
pydantic_core               2.10.1                          python  
pytesseract                 0.3.10                          python  
python                      3.12.0                          binary  
python3                     3.11.2-1+b1                     deb     
python3-minimal             3.11.2-1+b1                     deb     
python3-pil                 9.4.0-1.1+b1                    deb     
python3.11                  3.11.2-6                        deb     
python3.11-minimal          3.11.2-6                        deb     
readline-common             8.2-1.3                         deb     
referencing                 0.30.2                          python  
rpcsvc-proto                1.4.3-1                         deb     
rpds-py                     0.12.0                          python  
schema                      0.7.5                           python  
scipy                       1.11.3                          python  
sed                         4.9-1                           deb     
sensible-utils              0.0.17+nmu1                     deb     
setuptools                  68.2.2                          python  
shared-mime-info            2.2-1                           deb     
sysvinit-utils              3.06-4                          deb     
tar                         1.34+dfsg-1.2                   deb     
tesseract-ocr               5.3.0-2                         deb     
tesseract-ocr-eng           1:4.1.0-2                       deb     
tesseract-ocr-osd           1:4.1.0-2                       deb     
tesseract-ocr-script-latn   1:4.1.0-2                       deb     
typing_extensions           4.8.0                           python  
tzdata                      2023c-5                         deb     
ucf                         3.0043+nmu1                     deb     
usr-is-merged               35                              deb     
util-linux                  2.38.1-5+b1                     deb     
util-linux-extra            2.38.1-5+b1                     deb     
wheel                       0.41.3                          python  
wrapt                       1.15.0                          python  
x11-common                  1:7.7+23                        deb     
xfonts-encodings            1:1.0.4-2.2                     deb     
xfonts-utils                1:7.7+6                         deb     
xkb-data                    2.35.1-1                        deb     
zlib1g                      1:1.2.13.dfsg-1                 deb
```


## License

GNU General Public License v3

See [Licence](consentforms/LICENSE) for further details.
