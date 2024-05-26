import sys
from pydantic import BaseSettings
"""if sys.version_info[:2] <(3,9):
    print(sys.version_info)
    from pydantic import BaseSetting
else:
    from pydantic_setting import BaseSetting"""
    
class Setting(BaseSettings): # type: ignore
    YOUTUBE_ACTIVE_RETRY_MAX: int = 3
    
    SCOPES: list[str] = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    TOKEN: str = 'secret_fz8hGuVnnQsTbifpRhXx0SCAfNiqSSPBn7IGfZKh0ww'
    DATABASEID :str = "90cc1a489ec14a78ae14a8de4abcabb7"
    CLIENT_SECRETS_FILE: str = "./client_secret_847585282559-2v2nh29jlgrhghibmma96suoleqfkek8.apps.googleusercontent.com.json"
    HEADERS = {
        "Authorization": "Bearer{TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }
    
    
    
setting = Setting()