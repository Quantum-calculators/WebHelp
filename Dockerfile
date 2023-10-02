FROM python:3.9

EXPOSE 5000

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWTIREBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash WB && chmod 777 /opt /run

WORKDIR /WB

RUN mkdir /WB/static && mkdir /WB/media && chown -R WB:WB /WB && chmod 755 /WB

COPY --chown=WB:WB . .

RUN pip install -r requirements.txt

USER WB

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:5000"]
