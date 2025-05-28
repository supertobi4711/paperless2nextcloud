# Paperless-to-Nextcloud Calendar Sync

This Python script reads documents from a [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) instance using its REST API, extracts a custom field that contains a due date, and writes calendar entries to a [Nextcloud](https://nextcloud.com/) calendar via CalDAV.

## ✨ Features

- Connects to a Paperless-ngx server via API
- Filters documents based on the exitance of custom fields (there is room for improvement here, see "TODO")
- Extracts meta data 
- Creates or updates events in a Nextcloud calendar
- Avoids duplicate entries
- Fully configurable via settings section or environment variables

## 📦 Requirements

- Python 3.8+
- A running Paperless-ngx instance with API access
- A Nextcloud calendar with CalDAV URL and credentials

### Python dependencies (install via pip):

```bash
pip install requests caldav python-dateutil
```

## ⚙️ Configuration

Edit the script:

- `api_arl`: Base URL to Paperless-ngx (e.g. `https://paperless.example.com/api`)
- `auth`: username and password for paperless-ngx
- `NEXTCLOUD_URL`: Full CalDAV URL to the calendar
- `NEXTCLOUD_USER`: Username for Nextcloud
- `NEXTCLOUD_APP_PASSWORD`: Password or app password for Nextcloud


## 🚀 Usage

```bash
python paperless_to_nextcloud.py
```

The script will:
1. Fetch documents from Paperless
2. Check each for the custom field
3. Add matching events to the Nextcloud calendar

## 🔒 Security

- It's recommended to use an [app password](https://docs.nextcloud.com/server/latest/user_manual/en/security/app_passwords.html) for Nextcloud access.
- Keep your API tokens and credentials safe and out of version control.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙌 Contributions

Pull requests and suggestions are welcome! Please open an issue for major changes or questions.

## 🛠️ TODO

- [ ] Support multiple custom fields by allowing configuration of the relevant custom field `ID`
