# Password Migration Tools

## 1Password to Pass Migration
- Using 1password2pass.rb script from password-store repository
- Source: https://git.zx2c4.com/password-store/tree/contrib/importers/1password2pass.rb

### Key Script Options:
- `-f` (--force): Overwrite existing passwords
- `-d` (--default [FOLDER]): Place passwords into specific folder
- `-n` (--name [PASS-NAME]): Select field to use as pass-name (title or URL)
- `-m` (--meta): Import metadata and insert it below the password

### Prerequisites:
- Requires both `pass` and Ruby installed
- GPG key setup required
- Requires 1Password export in either .1pif or CSV format