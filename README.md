# CheckConsents Tool

## Description

## Installation

`CheckConsents` tool requires Python 3.12+.

`CheckConsents` tool requires `convert` from [ImageMagick software](https://imagemagick.org/index.php).

```Bash
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

```Bash
export TESSDATA_PREFIX="/path/to/folder/which/contains/traineddata_files"
```

It is easier to use container, see [Docker section](#docker).

## Docker

A development image can be built from the available `Dockerfile`.
This image is base on `python:3.12-slim` image.

### Build docker image

We define a dockerfile to set up the perfect environment for `CheckConsents` tool without installing any dependencies on your machine.
This image is not production ready. We recommend to use it only for dev and testing purpose.

```Bash
$ docker build -t cad/checkconsents:1.0.0 .
```

```Bash
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
                        /code/consentforms/checkconsents_config.yml)

Logger:
  --log_level {ERROR,error,WARNING,warning,INFO,info,DEBUG,debug}
                        log level (default: INFO)
  --log_file LOG_FILE   log file (use the stderr by default) (default: None)
```

### Known vulnerabilities

[Vulnerabilities scan of docker image](docs/docker-image-vulnerabilities.md)

### Software Bill of Materials (SBOM)

[SBOM description of docker image](docs/docker-image-sbom.md)


## Usage

```Bash
$ ./consentforms/checkconsents.py  --help
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

```Bash
$ mkdir target
$ ./consentforms/checkconsents.py  --input_folder ./tests/resources/initial_data --configfile resources/checkconsents_config.yml -w ./target
```

```Bash
$ docker run --rm \
             -v /etc/localtime:/etc/localtime:ro \
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
If some forms have not been resolved a debugging image is generated for a human review. In this specific case, `CheckConsents` exits with code = 3.

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


## CheckContents predictions evaluation 

| Filename            | "Research usage yes" checked     | "Research usage no" checked | Use for research agreed | Result of the automatic detection         |
| ------------------- | -------------------------------- | --------------------------- | ----------------------- | ----------------------------------------- |
| Consentement_1.pdf  | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_2.pdf  | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_3.pdf  | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#ffc000">undetermined</font> |
| Consentement_4.pdf  | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_5.pdf  | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_6.pdf  | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_7.pdf  | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_8.pdf  | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_9.pdf  | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_10.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_11.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_12.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_13.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_14.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_15.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_16.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_17.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_18.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_19.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_20.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_21.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_22.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_23.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_24.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_25.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_26.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_27.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_28.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_29.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_30.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_31.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_32.pdf | <font color="#ff0000">no</font>  | yes                         | no                      | <font color="#ff0000">no</font>           |
| Consentement_33.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |
| Consentement_34.pdf | <font color="#00b050">yes</font> | no                          | yes                     | <font color="#00b050">yes</font>          |

These predictions were obtained using default CheckConsents parameters for conversion of pdf into png with a **density of 300 dpi**, and **no colorscale transformation**.

> [!note]
> Modification of curent values of CheckConsents parameters may decrease file size of png and therefore increase execution time but may also impact accuracy of the detection. 

## Parsing the output of CheckConsents tool

The json output from checkconsents could be parsed to generate other formats or combined with other informations.

There is an example of parser which generate a csv file from the `consents.json` file.

It creates a table with the following header:

```Text
"Input directory","Input filename","Result of the automatic detection","Debug image filename","Output directory"
```

## Development

You can use virtualenv locally or use the docker compose file: `compose-dev.yml`.
We recommend to use docker which makes easier the management of environment.

### Setup virtualenv

```Bash
$ python -m venv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

### Docker dev env

It requires Docker and Docker Compose installed. 
All folders and files form the repository are available into `/code` directory.

```Bash
$ mkdir target                                        # temp folder for unit test
$ touch .env
$ docker compose -f compose-dev.yml up -d
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

Generate a test report (`report.html`, `.coverage`, `htmlcov/index.html`) (in dev container):

```bash
[cad@docker-853796383c04 /code] [30.11.2023 14:53:29] $ pytest --html=report.html

# with test coverage
[cad@docker-853796383c04 /code] [30.11.2023 14:53:29] $ pytest --html=report.html --cov=consentforms

# with test coverage report
[cad@docker-853796383c04 /code] [30.11.2023 14:53:29] $ pytest --html=report.html --cov=consentforms --cov-report html
```

> **NB**: the test `tests/test_images.py::test_sort_cnts_without_changing_crop_image` FAILED due to the last changes on version `1.1.0`.

#### Running functional Tests

Using local virtualenv:

```bash
(env) $ python consentforms/checkconsents.py --input_folder ./tests/resources --configfile resources/checkconsents_config.yml --log_level debug -w ./target

(env) $ python -m pdb consentforms/checkconsents.py --input_folder ./tests/resources --configfile resources/checkconsents_config.yml --log_level debug -w ./target
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

# NB if you have timezone set on your host add the following docker option : -v /etc/timezone:/etc/timezone:ro 
```

#### Debugging using docker image:

```bash
$ docker build -t cad/checkconsents:test .

$ docker run --rm \
             -v /etc/localtime:/etc/localtime:ro \
             -v ./target:/code/target \
             -v ./consentforms:/code/consentforms \
             -v ./resources:/code/resources \
             -v ./tests/resources:/code/tests/resources \
             cad/checkconsents:test \
                --input_folder ./tests/resources \
                --configfile resources/checkconsents_config.yml \
                --log_level debug \
                -w /code/target

# debug
$ docker run --rm -it --entrypoint python \
             -v /etc/localtime:/etc/localtime:ro \
             -v ./target:/code/target \
             -v ./consentforms:/code/consentforms \
             -v ./resources:/code/resources \
             -v ./tests/resources:/code/tests/resources \
             cad/checkconsents:test \
                -m pdb /code/consentforms/checkconsents.py \
                --input_folder ./tests/resources \
                --configfile resources/checkconsents_config.yml \
                --log_level debug \
                -w /code/target
```

## Authors

CheckConsents project is developed by David Salgado <david.salgado@inserm.fr> 
and Adrien Josso Rigonato <adrien.josso-rigonato@genomecad.fr>.
Expression of the need and test data were created by Cécile Meslier.

The project is supported by `Collecteur Analyseur de Données (CAD)`.

## License

GNU AFFERO General Public License v3

See [Licence](LICENSE) for further details.

## Acknowledgement

Checkbox detection is based on `simpleomr` script from [RescueOMR](https://github.com/EuracBiomedicalResearch/RescueOMR).

Copyright(c) 2016-2017: Yuri D'Elia <yuri.delia@eurac.edu>

Copyright(c) 2016-2017: EURAC, Institute of Genetic Medicine

Thanks to the work of Yuri D'Elia
