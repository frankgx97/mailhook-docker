FROM alpine:3.6

WORKDIR /usr/src/app

COPY . .

RUN set -ex  \
&& echo "http://mirrors.ustc.edu.cn/alpine/v3.6/main/" > /etc/apk/repositories \
&& echo "http://mirrors.ustc.edu.cn/alpine/v3.6/community/" >> /etc/apk/repositories \
&& apk add --no-cache --virtual .build-deps python py-pip \
&& pip install --no-cache-dir -r requirements.txt 

EXPOSE 5000

CMD python /usr/src/app/run.py