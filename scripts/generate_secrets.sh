#!/bin/bash
# Script to generate a dynamic k8s/mysql-secret.yml with custom/secure base64 values

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_FILE="$ROOT_DIR/k8s/mysql-secret.yml"

ROOT_PASS="${1:-rootpass}"
DB_USER="${2:-flaskuser}"
DB_PASS="${3:-flaskpass}"
DB_NAME="${4:-flaskdb}"

ROOT_PASS_B64=$(echo -n "$ROOT_PASS" | base64)
DB_USER_B64=$(echo -n "$DB_USER" | base64)
DB_PASS_B64=$(echo -n "$DB_PASS" | base64)
DB_NAME_B64=$(echo -n "$DB_NAME" | base64)

cat <<EOF > "$OUTPUT_FILE"
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
  namespace: assignment3
type: Opaque
data:
  mysql_root_password: $ROOT_PASS_B64
  mysql_user: $DB_USER_B64
  mysql_password: $DB_PASS_B64
  mysql_database: $DB_NAME_B64
EOF

echo "Generated $OUTPUT_FILE successfully."
