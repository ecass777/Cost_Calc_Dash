FROM python:3.11-slim

WORKDIR /Cost_Calc_Dash

COPY requirements.txt /Cost_Calc_Dash/requirements.txt

RUN pip install --no-cache-dir -r /Cost_Calc_Dash/requirements.txt

COPY . /Cost_Calc_Dash

EXPOSE 10000

CMD ["python", "index.py"]