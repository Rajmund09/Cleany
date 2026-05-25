import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')
    
    # Upload and processing directories
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    RAW_FOLDER = os.path.join(UPLOAD_FOLDER, 'raw')
    CLEANED_FOLDER = os.path.join(UPLOAD_FOLDER, 'cleaned')
    TEMP_FOLDER = os.path.join(UPLOAD_FOLDER, 'temp')
    
    # Reports directories
    REPORTS_FOLDER = os.path.join(BASE_DIR, 'reports')
    PDF_REPORTS = os.path.join(REPORTS_FOLDER, 'pdf')
    EXCEL_REPORTS = os.path.join(REPORTS_FOLDER, 'excel')
    CHART_REPORTS = os.path.join(REPORTS_FOLDER, 'charts')
    
    # Allowed extensions
    ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
    
    # Database
    DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'database.db')}"

    @staticmethod
    def init_app(app):
        # Create necessary directories
        directories = [
            Config.RAW_FOLDER, Config.CLEANED_FOLDER, Config.TEMP_FOLDER,
            Config.PDF_REPORTS, Config.EXCEL_REPORTS, Config.CHART_REPORTS,
            os.path.join(Config.BASE_DIR, 'database')
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
