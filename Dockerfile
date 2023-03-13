FROM python:latest

COPY . . 

RUN pip install selenium openpyxl webdriver-manager

CMD ["python", "project/__main__.py"]