import os
import subprocess

import uvicorn


def run_command(command: str) -> None:
    subprocess.run(
        command,
        shell=True,
        text=True,
    )

if __name__ == "__main__":
    PRODUCTION: int = int(os.environ.get("DJANGO_PRODUCTION"))    

    if PRODUCTION:
        run_command("python manage.py makemigrations")

    run_command("python manage.py migrate")
    run_command("python manage.py initialize_admin_account")
    run_command("python manage.py collectstatic --no-input")

    if PRODUCTION == 1:
        uvicorn.run(
            app="subguard.asgi:application", host="0.0.0.0", port=8000, reload=False
        )
    else:
        uvicorn.run(
            app="subguard.asgi:application", host="0.0.0.0", port=8000, reload=True
        )