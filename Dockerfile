FROM pytorch/pytorch

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# nltk package's extra
RUN python -m nltk.downloader punkt

COPY . ./

CMD [ "python", "chat.py" ]