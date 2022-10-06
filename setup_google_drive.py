from pathlib import Path
from typing import Any, Dict

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).absolute().parent
CLIENT_SECRETS_FILE = ROOT / "secrets" / "google.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
]
API_SERVICE_NAME = "drive"
API_VERSION = "v3"
DEFAULT_TEMPLATE_ID = "1nLYIP41PKy_rQbCNNvR3QwVk6EYSccj1"


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def copy_directory_to(service, from_id, to_id, make_private=False):
    result = service.files().list(q=f"'{from_id}' in parents").execute()
    command = None
    for file in result.get("files"):
        if file.get("mimeType") == "application/vnd.google-apps.folder":
            p = make_private or file.get("name").lower() == "private"
            d = make_directory(service, file.get("name"), to_id)
            copy_directory_to(service, file.get("id"), d.get("id"), make_private=p)
            if not p:
                (
                    service.permissions()
                    .create(
                        fileId=d.get("id"),
                        body={"role": "reader", "type": "anyone"},
                    )
                    .execute()
                )
        else:
            if command is None:
                command = service.files()
            command = command.copy(
                fileId=file.get("id"),
                fields="id",
                body=dict(name=file.get("name"), parents=[to_id]),
            )
    if command is not None:
        command.execute()


def make_directory(service, name, in_id=None):
    metadata: Dict[str, Any] = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if in_id is not None:
        metadata["parents"] = [in_id]
    return service.files().create(body=metadata, fields="id,webViewLink").execute()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="The name of your event")
    parser.add_argument(
        "-t",
        "--template",
        type=str,
        default=DEFAULT_TEMPLATE_ID,
        help="The Google drive ID of the template folder that you want to copy",
    )
    args = parser.parse_args()

    service = get_authenticated_service()
    d = make_directory(service, args.name)
    copy_directory_to(service, args.template, d.get("id"))
    print(f"Drive template copied to: {d.get('webViewLink')}")
