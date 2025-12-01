from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Importações locais do seu projeto
from database import Base, engine, get_db
import models
import auth  # O arquivo de segurança que criamos
from routers import users, patients, evolutions, appointments, finance

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FisioManager API")

# ==========================================
# 1. CONFIGURAÇÃO DE CORS (OPÇÃO NUCLEAR)
# ==========================================
# Isso resolve o erro "blocked by CORS policy" e o problema do redirecionamento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Libera para QUALQUER site (Frontend, Localhost, etc)
    allow_credentials=True,
    allow_methods=["*"],  # Libera GET, POST, DELETE, PUT, OPTIONS
    allow_headers=["*"],  # Libera todos os cabeçalhos
)

# ==========================================
# 2. ROTAS DE AUTENTICAÇÃO
# ==========================================

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Busca o usuário pelo username
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    # 2. Verifica se o usuário existe e se a senha bate
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Gera o token de acesso
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/create-admin")
def create_admin(db: Session = Depends(get_db)):
    # Verifica se já existe
    user = db.query(models.User).filter(models.User.username == "admin").first()
    if user:
        return {"message": "Admin já existe"}
    
    # Cria usuário admin com senha hash
    hashed_pwd = auth.hash_password("123456")
    new_user = models.User(username="admin", hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "Admin criado com sucesso!", "username": "admin"}

# ==========================================
# 3. ROTA DE EMERGÊNCIA (RESET BANCO)
# ==========================================
@app.get("/reset-database-force")
def reset_database():
    # CUIDADO: Apaga tudo e recria as tabelas
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return {"message": "Banco de dados RESETADO e tabelas RECRIADAS com sucesso!"}

@app.get("/")
def root():
    return {"message": "API FisioManager está rodando! 🚀"}

# ==========================================
# 4. INCLUINDO OS ROTEADORES (MODULARIZAÇÃO)
# ==========================================
app.include_router(users.router)
app.include_router(patients.router)
# Se der erro nestes dois abaixo, é porque você ainda não criou os arquivos. 
# Se existirem, deixe descomentado:
app.include_router(evolutions.router) 
app.include_router(appointments.router)
app.include_router(finance.router)

