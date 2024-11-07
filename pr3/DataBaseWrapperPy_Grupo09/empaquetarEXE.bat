pyinstaller --onefile --windowed --add-data "Database-MSDOS;Database-MSDOS" --add-data "tesseract;tesseract" --add-data "templates;templates" --hidden-import "pytesseract" wrapper.py
