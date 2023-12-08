FROM python:3.12.0-slim

####### METADATA #######
LABEL authors="Adrien Josso Rigonato <adrien.josso-rigonato@genomecad.fr>, David Salgado <david.salgado@genomecad.fr>"
LABEL base.image="python:3.12.0-slim"
LABEL version="1.0.0"
LABEL software="checkconsents"
LABEL software.version="1.0.0"
LABEL license="GLP 3"
LABEL about.tags="OMR"

RUN /bin/sh -c 'set e  ; \
                apt-get update -y ; \
                apt-get upgrade -y ; \
                apt-get install -y --no-install-recommends imagemagick \
                                                           ghostscript \
                                                           gcc \
                                                           libc-dev \
                                                           ffmpeg \
                                                           libsm6 \
                                                           libxext6 \
                                                           tesseract-ocr \
                                                           libleptonica-dev \
                                                           libtesseract-dev \
                                                           python3-pil \
                                                           tesseract-ocr-eng \
                                                           tesseract-ocr-script-latn ; \
                apt-get clean autoclean ; \
                apt-get autoremove -y ; \
                rm -rf /var/lib/apt/lists/* ; \
                pip install --upgrade pip ; \
                sed -i '/"PDF"/d' /etc/ImageMagick-6/policy.xml'


# RUN /bin/sh -c 'set e  ; \
#                 apt-get update -y ; \
#                 apt-get upgrade -y ;'
# RUN /bin/sh -c 'set e  ; \
#                 apt-get install -y --no-install-recommends imagemagick \
#                                                            ghostscript \
#                                                            gcc \
#                                                            libc-dev \
#                                                            ffmpeg \
#                                                            libsm6 \
#                                                            libxext6 \
#                                                            tesseract-ocr ;'
# RUN /bin/sh -c 'set e  ; \
#                 apt-get install -y --no-install-recommends libleptonica-dev libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn' 
# RUN /bin/sh -c 'set e  ; \
#                 apt-get clean autoclean ; \
#                 apt-get autoremove -y ; \
#                 rm -rf /var/lib/apt/lists/* ; \
#                 pip install --upgrade pip ; \
#                 sed -i '/"PDF"/d' /etc/ImageMagick-6/policy.xml'

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt

RUN adduser --disabled-password --no-create-home --quiet cad
USER cad

ENTRYPOINT [ "/code/entrypoint.sh" ]
CMD [ "--help" ]
