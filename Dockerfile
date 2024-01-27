FROM public.ecr.aws/lambda/python:3.12

COPY Pipfile* ${LAMBDA_TASK_ROOT}

RUN pip install pipenv

RUN pipenv requirements > requirements.txt

RUN pip install -r requirements.txt

COPY main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]
