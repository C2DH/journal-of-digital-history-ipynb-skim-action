FROM python:3-slim AS builder

WORKDIR /app

ADD skim.py /app/skim.py

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app fire

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/skim.py"]