FROM python:3.10

ADD refactored.py . 

RUN pip install selenium openpyxl

CMD ["python", "./refactored.py"]