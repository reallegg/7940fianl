FROM python
COPY  chatbot.py .
COPY  requirements.txt .
ENV ACCESS_TOKEN  6003544672:AAFYUCXaALM9fgFtPZ9rHXz_Ft5r4z7OzAk
ENV LOCAL host.docker.internal
ENV USER root
ENV PASSWORD  hemi7940
ENV DB 7940
ENV PORT  3306
RUN pip install -r requirements.txt
CMD python chatbot.py