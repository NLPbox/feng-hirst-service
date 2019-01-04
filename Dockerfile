FROM nlpbox/feng-hirst-rst-parser:2019-01-04

RUN apk add py3-pip && \
    pip3 install hug==2.4.0 pexpect==4.5.0 pytest==3.5.1 sh==1.12.14

ADD feng_hug_api.py test_api.py input_*.txt /opt/feng-hirst-service/

WORKDIR /opt/feng-hirst-service

EXPOSE 8080
ENTRYPOINT ["hug"]
CMD ["-f", "feng_hug_api.py"]

