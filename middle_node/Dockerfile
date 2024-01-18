FROM python:3
WORKDIR /app
ADD . /app
ENTRYPOINT [ "python", "./middle_node.py", "z32_middle_node","z32_overseer", "-t", "2", "-ss", "400", "500"]