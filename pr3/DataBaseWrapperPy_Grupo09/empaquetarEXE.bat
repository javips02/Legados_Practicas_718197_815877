pyinstaller --onefile --windowed --exclude-module tkinter `
            --add-data "Database-MSDOS;Database-MSDOS" `
            --add-data "tesseract;tesseract" `
            --add-data "templates;templates" `
            --hidden-import "pytesseract" `
            --hidden-import "PIL._imaging" `
            --hidden-import "PIL._imagingtk" `
            --hidden-import "PIL.Image" `
            --hidden-import "difflib" `
            --hidden-import "flask" `
            app.py
