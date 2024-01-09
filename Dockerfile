FROM rockylinux:9

RUN dnf -y install 'dnf-command(config-manager)'
RUN dnf config-manager --set-enabled crb
RUN dnf -y install epel-release
RUN dnf -y install ffmpeg-free awscli https://cdn.azul.com/zulu/bin/zulu21.30.15-ca-jre21.0.1-linux.$(uname -p).rpm

WORKDIR /app
RUN curl -LO https://github.com/yt-dlp/yt-dlp/releases/download/2023.12.30/yt-dlp_linux_$(uname -p)  \
    && mv yt-dlp_linux_$(uname -p) /usr/bin/yt-dlp  \
    && chmod +x /usr/bin/yt-dlp

ENTRYPOINT [ "/usr/bin/java", "-cp", "./*", "com.amazonaws.services.lambda.runtime.api.client.AWSLambda" ]

CMD ["xyz.omnigrove.App::helloWorld"]
