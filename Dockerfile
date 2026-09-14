# Local / self-hosted image for the Flask version (flask_app.py).
# Hugging Face offers Docker only on a paid plan, so the public demo
# runs the Gradio app in app.py instead. This still builds and runs.
#
# Three things this image does deliberately:
#   * installs the CPU-only torch wheel - the default pulls the CUDA build,
#     roughly 800 MB of libraries that can never run on a CPU Space
#   * downloads the grammar model and the TextBlob corpora at BUILD time, so
#     the first visitor is not left waiting on an 850 MB download
#   * runs as uid 1000 with a writable cache, which is what Spaces expects;
#     as root the HF cache lands somewhere the runtime cannot write
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/home/user/.cache/huggingface \
    NLTK_DATA=/home/user/nltk_data

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /home/user/app

COPY --chown=user requirements.txt .

# CPU-only torch first, so the CUDA build is never resolved.
RUN pip install --user --no-cache-dir \
        torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu \
 && pip install --user --no-cache-dir -r requirements.txt

# Bake the model and corpora into the image.
RUN python -c "\
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; \
m='prithivida/grammar_error_correcter_v1'; \
AutoTokenizer.from_pretrained(m); \
AutoModelForSeq2SeqLM.from_pretrained(m)" \
 && python -m textblob.download_corpora

COPY --chown=user . .

EXPOSE 7860

# Two workers would load the model twice and exhaust the free tier's memory.
# One worker, and a long timeout because beam search on CPU is not quick.
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", \
     "--threads", "4", "--timeout", "180", "flask_app:app"]
