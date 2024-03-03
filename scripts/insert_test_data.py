import os
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from app.services.connectors.supabase_connector import SupabaseConnector
from app.domain.models.user import InsertUserModel, User
from app.domain.models.wallet import InsertWalletModel, Wallet
from faker import Faker
from passlib.context import CryptContext
import random

load_dotenv()
AUTH_EMAIL = os.environ.get("AUTH_EMAIL")
AUTH_PWD = os.environ.get("AUTH_PWD")

sup_obj = SupabaseConnector(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_ADMIN_KEY"))
supabase = sup_obj.get_supabase_client()
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake = Faker()

app = FastAPI()



def insert_users():
    users = []
    for _ in range(10):
        user = InsertUserModel(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            is_active_user=True,
            email=fake.email(),
            role="USER",
            password_hash="$2y$10$dmyZ/DncySzrp7QllOOBX.xR8oKu2cE.WIp19O5MoIQvuc/KI571e"
        )
        users.append(jsonable_encoder(user))
    print(users)
    data, count = supabase.table('User').insert(users).execute()
    print(data, count)

def insert_wallets(users_id):
    wallets = []
    for id in users_id:
        bcrypt_hash = password_context.hash("TESTE DE CRIPTOGRAFIA")
        wallet = InsertWalletModel(
            wallet_name=fake.word(),
            dolar_balance=fake.pydecimal(left_digits=random.randint(2, 6), right_digits=2, positive=True),
            fk_user_id=id,
            wallet_recovery_phrase_hash=bcrypt_hash #TESTE DE CRIPTOGRAFIA
        )
        wallets.append(jsonable_encoder(wallet))
    print(wallets)
    data, count = supabase.table('Wallet').insert(wallets).execute()
    
    
    

# insert_users()
# insert_wallets([12,14,1567])
wallet_result = supabase.table("Wallet").select("id").execute()
wallet_count = len(wallet_result.data)

user_result = supabase.table("User").select("id").execute()
user_count = len(user_result.data)

assert wallet_count == 0 and user_count > 0
users_id = [user["id"] for user in user_result.data]
users_id.pop(random.randint(0, len(users_id)-1)) #Remove um usuário, para teste de usuário sem carteira
print(users_id)

insert_wallets(users_id)

