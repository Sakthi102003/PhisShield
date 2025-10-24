# PhishShield Scripts

This folder contains utility scripts for running and managing PhishShield.

## 📜 Available Scripts

### Windows Scripts (.bat)

#### `run_backend_admin.bat`
Starts the backend Flask server in administrator mode.
```cmd
scripts\run_backend_admin.bat
```

#### `run_frontend_admin.bat`
Starts the frontend development server in administrator mode.
```cmd
scripts\run_frontend_admin.bat
```

#### `setup_backend.bat`
Sets up the backend environment (installs dependencies, creates database).
```cmd
scripts\setup_backend.bat
```

### Unix/Linux Scripts (.sh)

#### `build.sh`
Builds both frontend and backend for production deployment.
```bash
bash scripts/build.sh
```

## 🚀 Quick Start

### Windows Users

1. **First Time Setup**:
   ```cmd
   scripts\setup_backend.bat
   ```

2. **Run Backend**:
   ```cmd
   scripts\run_backend_admin.bat
   ```

3. **Run Frontend** (in new terminal):
   ```cmd
   scripts\run_frontend_admin.bat
   ```

### Linux/Mac Users

1. **Make scripts executable**:
   ```bash
   chmod +x scripts/build.sh
   ```

2. **Build for production**:
   ```bash
   bash scripts/build.sh
   ```

## 📝 Creating New Scripts

When adding new scripts:
1. Place them in this `scripts/` folder
2. Use `.bat` extension for Windows scripts
3. Use `.sh` extension for Unix/Linux scripts
4. Make Unix scripts executable: `chmod +x script.sh`
5. Update this README with script documentation

## 🔒 Security Notes

- Scripts with "admin" in the name may require administrator privileges
- Always review scripts before running them
- Keep sensitive credentials in environment variables, not in scripts
