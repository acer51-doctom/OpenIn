#!/bin/bash

echo "Installing native host..."

ID="com.acer51-doctom.openurl"
HOST_PATH="$(pwd)/native_app.py"
MANIFEST_PATH="$HOME/.config/google-chrome/NativeMessagingHosts/$ID.json"

mkdir -p "$(dirname "$MANIFEST_PATH")"

cat > "$MANIFEST_PATH" <<EOF
{
  "name": "$ID",
  "description": "Open URLs in external browsers",
  "path": "$HOST_PATH",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://__EXTENSION_ID__/"
  ]
}
EOF

chmod +x "$HOST_PATH"
echo "Done. Don't forget to replace __EXTENSION_ID__ in the manifest."
