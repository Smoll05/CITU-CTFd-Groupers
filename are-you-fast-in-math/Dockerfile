FROM pwn.red/jail
COPY --from=python@sha256:85e668ed5c6219f9fd1a70d12103b6c8b2cfbdca971d045cdafc301c061c049d / /srv

USER root
COPY chal.py /srv/app/run
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=20M
ENV JAIL_TIME=1000000