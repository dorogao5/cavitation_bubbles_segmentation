from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from jose import JWTError, jwt  # pip install python-jose
from datetime import datetime, timedelta
import shutil
import os
import uuid

from src.video_processing import VideoProcessor
from settings import get_settings, Settings

# Получаем настройки (включая username и password из .env)
settings = get_settings()

# Константы для JWT
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
         expire = datetime.utcnow() + expires_delta
    else:
         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, stored_password: str) -> bool:
    # Здесь простое сравнение строк, в продакшене рекомендуется использовать хэширование
    return plain_password == stored_password

def authenticate_user(username: str, password: str):
    if username == settings.username and verify_password(password, settings.password):
         return {"username": username}
    return None

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Incorrect username or password",
             headers={"WWW-Authenticate": "Bearer"},
         )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
         data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Could not validate credentials",
         headers={"WWW-Authenticate": "Bearer"},
    )
    try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         username: str = payload.get("sub")
         if username is None:
             raise credentials_exception
    except JWTError:
         raise credentials_exception
    return {"username": username}

# Определяем папки для хранения файлов с уникальными именами
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Инициализируем VideoProcessor (укажите корректный путь к модели)
MODEL_PATH = "hf_model_repo/model.pt"
video_processor = VideoProcessor(MODEL_PATH)

@app.post("/process_video/")
async def process_video_endpoint(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # Генерируем уникальное имя для загружаемого файла
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    input_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    with open(input_path, "wb") as buffer:
         shutil.copyfileobj(file.file, buffer)

    output_video_path = os.path.join(OUTPUT_FOLDER, f"processed_{unique_filename}")
    csv_path = os.path.join(OUTPUT_FOLDER, f"data_{unique_filename.split('.')[0]}.csv")
    hist_folder = OUTPUT_FOLDER  # можно использовать отдельную папку или уникальный идентификатор

    speed_hist_file, area_hist_file = video_processor.process_video(
         input_path, output_video_path, csv_path, hist_folder
    )
    return {
         "output_video": output_video_path,
         "csv_file": csv_path,
         "speed_hist_file": speed_hist_file,
         "area_hist_file": area_hist_file
    }

@app.get("/download/")
async def download_file(path: str, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return FileResponse(path, filename=os.path.basename(path))
