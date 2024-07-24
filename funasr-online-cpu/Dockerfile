FROM registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.10
LABEL maintainer="elegant.Chen <telegant@qq.com>"
ENV TZ=Asia/Shanghai
EXPOSE 10095/tcp 10095/tcp
COPY run.sh /run.sh
ENTRYPOINT ["/run.sh"]
