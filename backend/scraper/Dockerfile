FROM python:3.13-slim

WORKDIR /app/scraper

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-m", "scraper.scrape" ]