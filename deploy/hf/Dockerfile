# Imagem do jogo Arena SVM para o Hugging Face Spaces (SDK Docker, porta 7860)
FROM python:3.12-slim

# O Spaces executa o contêiner com o usuário de id 1000
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH PYTHONUNBUFFERED=1
WORKDIR /home/user/app

COPY --chown=user requirements-deploy.txt .
RUN pip install --no-cache-dir -r requirements-deploy.txt

COPY --chown=user . .

EXPOSE 7860
# Um único processo: as salas ficam na memória e precisam ser compartilhadas entre as requisições.
CMD ["gunicorn", "--chdir", "app", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "16", "--timeout", "120", "servidor:app"]
