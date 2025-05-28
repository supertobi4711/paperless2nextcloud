#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timezone, time
import pytz
import sys

NEXTCLOUD_URL = XXX #please specify
NEXTCLOUD_USER = XXX  #please specify
NEXTCLOUD_APP_PASSWORD = XXX #please specify
# Paperless API
api_url = "http://192.168.1.130:8000/api/documents/" #please specify
params = {"has_custom_fields": "true"}
auth = HTTPBasicAuth("username", "password")  #please specify

try:
    response = requests.get(api_url, params=params, auth=auth)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"❌ Error retrieving documents: {e}")
    sys.exit(1)

data = response.json()
print(f"📄 {data['count']} document(s) found.")

for doc in data.get("results", []):
    doc_id = doc["id"]
    title = doc["title"]
    url = f"http://192.168.1.130:8000/documents/{doc_id}/"

    for field in doc.get("custom_fields", []):
        try:
            local_tz = pytz.timezone("Europe/Berlin")

            # parse due date
            #due_date = datetime.fromisoformat(field["value"]).date()

            value = field.get("value")

            if not isinstance(value, str):
                print(f"⚠️  custom field is no string for document {doc_id}: {value} ({type(value)})")
                continue  

            try:
                due_date = datetime.fromisoformat(value).date()
            except ValueError as e:
                print(f"⚠️  invalid date format for document {doc_id}: {value}")
                continue

            # always use 7:30 pm local time
            local_due = local_tz.localize(datetime.combine(due_date, time(19, 30)))
            due_dt = local_due.astimezone(timezone.utc)
            due_str = due_dt.strftime("%Y%m%dT%H%M%SZ")
            uid = f"task-{doc_id}"
            ics_path = f"{uid}.ics"
            dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            description = f"Document from paperless\\n\\nLink: {url}"

            # prepare ICS
            new_ics = "\n".join([
                "BEGIN:VCALENDAR",
                "VERSION:2.0",
                "PRODID:-//Paperless Fristexport//EN",
                "BEGIN:VTODO",
                f"UID:{uid}",
                f"DTSTAMP:{dtstamp}",
                f"SUMMARY:{title}",
                f"DESCRIPTION:{description}",
                f"DUE:{due_str}",
                f"URL:{url}",
                "STATUS:NEEDS-ACTION",
                "END:VTODO",
                "END:VCALENDAR"
            ])

            # check for existing entry
            get_url = f"{NEXTCLOUD_URL}{ics_path}"
            existing = requests.get(get_url, auth=(NEXTCLOUD_USER, NEXTCLOUD_APP_PASSWORD))

            # if exists: compare due date
            if existing.status_code == 200 and "DUE:" in existing.text:
                for line in existing.text.splitlines():
                    if line.startswith("DUE:"):
                        existing_due = line.strip().split(":", 1)[1]
                        if existing_due == due_str:
                            print(f"⏩ No change for document {uid} ({due_str}) – skipped.")
                            break
                else:
                    # no due date found
                    pass
            else:
                # file doesn't exist
                pass

            put_url = f"{NEXTCLOUD_URL}{ics_path}"
            res = requests.put(
                put_url,
                data=new_ics,
                headers={"Content-Type": "text/calendar"},
                auth=(NEXTCLOUD_USER, NEXTCLOUD_APP_PASSWORD)
            )

            if res.status_code in (200, 201, 204):
                print(f"✅ Updated: {uid} → {title}")
            else:
                print(f"❌ Error {res.status_code} for {uid}: {res.text}")

        except Exception as e:
            print(f"⚠️ Errot in document {doc_id}: {e}")
