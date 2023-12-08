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

|var|description|default value|
|---|-----------|-------------|
|intermediates|keep intermediate files|False|
|parsing_header_limit|max of lines read (correspond to the max size of title). Must be an integer greater than 0.|5|
|conversion:<br>  density: 300<br>  opt_args: "..."|Define specific parameter for pdf conversion to png|density = 300<br>opt_args=None|
|templates: <br>  mytemplatename:<br>    pattern: "sentence you want to catch"<br>    path: path/to/your/template.svg<br>    priority: <integer greater than 0> | Dict to describe all your templates|None|
|pages:<br>  recherche: | describe the patterns to identify the right page to analyse|None

### Exit codes

|code|description|
|----|-----------|
|0|Success|
|1|input directory does not exist|
|2|error during pdf conversion to png|
|3|Some form can be resolved. See logs for further details|


## Developement 

### Setup env

```bash
$ python -m venv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt

```

(optional PyBuilder to manage project)
```bash
(env) $ pip install pyb
```

### Build docker image

We define a dockerfile to setup the perfect environment for `CheckConsents` tool without installing any dependencies on your machine.
This image is not production ready. We recommand to use it only for dev and testing purpose.

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

### Tests

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


## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
