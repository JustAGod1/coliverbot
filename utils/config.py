from environs import Env, EnvError

env = Env()
env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")
LOGGING_LEVEL: int = env.int("LOGGING_LEVEL", 10)
prefix = ""
pg_prefix = "POSTGRES_"
fsm_prefix = "FDMREDIS_"
if env.bool("INSIDE_A_DOCKER", default=False):
    prefix += "DOCKER_"

with env.prefixed("POSTGRES_"):
    PG_USER: str = env.str("USER")
    PG_PASSWORD: str = env.str("PASSWORD")
    PG_DATABASE: str = env.str("DATABASE")

with env.prefixed("FSMREDIS_"):
    FSM_PASSWORD: str = env.str("PASSWORD")

with env.prefixed(prefix + "POSTGRES_"):
    PG_HOST: str = env.str("HOST")
    PG_PORT: int = env.int("PORT")

with env.prefixed(prefix + "FSMREDIS_"):
    FSM_HOST: str = env.str("HOST")
    FSM_PORT: int = env.int("PORT")

DB_URL: str = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
