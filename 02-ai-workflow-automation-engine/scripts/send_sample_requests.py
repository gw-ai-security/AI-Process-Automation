"""Send sample HTTP requests to the local API without extra dependencies."""

import json
from pathlib import Path
from urllib import request


BASE_URL = "http://localhost:8000"
SAMPLES_DIR = Path(__file__).resolve().parents[1] / "samples"


def send_payload(sample_name: str) -> None:
    sample_path = SAMPLES_DIR / sample_name
    payload = sample_path.read_text(encoding="utf-8")
    http_request = request.Request(
        url=f"{BASE_URL}/intake",
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(http_request) as response:
        body = json.loads(response.read().decode("utf-8"))
        print(f"{sample_name}: {response.status}")
        print(body)
        workflow_id = body.get("workflow_id")
        if workflow_id:
            with request.urlopen(f"{BASE_URL}/workflow/{workflow_id}") as workflow_response:
                print(json.loads(workflow_response.read().decode("utf-8")))


def main() -> None:
    for sample_name in ("meeting_notes.json", "support_case.json", "lead_intake.json"):
        send_payload(sample_name)


if __name__ == "__main__":
    main()
