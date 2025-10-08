set -euo pipefail
claims=$(grep -Rho '\\label{clm:[^}]*}' sections tex | sed 's/.*{clm:\([^}]*\)}/\1/' | grep -v '^#')
for c in $claims; do
  if ! grep -R "clm:$c" -n sections tex | grep -q "ValidationMatrix"; then
    echo "Missing in Validation Matrix: clm:$c" >&2
    exit 1
  fi

done
