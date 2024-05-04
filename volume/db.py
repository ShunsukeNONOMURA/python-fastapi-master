from sqlalchemy import Boolean, Column, Integer, String, DATETIME, ForeignKey, create_engine, select, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy_utils import create_view
from datetime import datetime

SQLALCHEMY_DATABASE_URI = "sqlite:///./dev.sqlite3"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False}, 
    echo=True
)
# DB接続用のセッションクラス インスタンスが作成されると接続する
SessionLocal = sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False
)

Base = declarative_base()

# DB接続のセッションを各エンドポイントの関数に渡す
from contextlib import contextmanager
@contextmanager
def create_session():
    session = SessionLocal()  # def __enter__
    try:
        yield session  # with asでsessionを渡す
        session.commit()  # 何も起こらなければcommit()
    except:
        print("rollback transaction")
        session.rollback()  # errorが起こればrollback()
        raise
    finally:
        print("closing connection")
        session.close()  # どちらにせよ最終的にはclose()

table_args = {}
# table_args = {'schema': 'app'}

# Userテーブルの定義
class TUser(Base):
    __table_args__ = table_args
    __tablename__ = 't_user'
    user_id = Column(String(20), primary_key = True, comment='ユーザID')
    user_name = Column(String(20), nullable=False)
    user_password = Column(String(20), nullable=False)
    user_creation_datetime = Column(DATETIME, default=datetime.now, nullable=False)
    user_update_datetime = Column(DATETIME, default=datetime.now, nullable=False)
    user_role_code = Column(String(2), ForeignKey('m_user_role.user_role_code'), nullable=False)
    
# Userロールの定義
class MUserRole(Base):
    __table_args__ = table_args
    __tablename__ = 'm_user_role'
    user_role_code = Column(String(2), primary_key = True)
    user_role_name = Column(String(20), nullable=False)
    user = relationship('TUser')

class VUser(Base):
    __table__ = create_view(
        'v_user', 
        select(
            TUser.user_id,
            TUser.user_name,
            TUser.user_password,
            TUser.user_creation_datetime,
            TUser.user_update_datetime,
            TUser.user_role_code,
            MUserRole.user_role_name
        ).select_from(TUser.__table__.outerjoin(MUserRole, MUserRole.user_role_code == TUser.user_role_code)),
        metadata = Base.metadata,
        cascade_on_drop=False,
        # replace = True
    )

# RDBの初期化
def init_db(drop_all=True):
    if drop_all:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)

    with create_session() as session:
        user_role = MUserRole(user_role_code='00', user_role_name='admin')
        session.add(user_role)
        user_role = MUserRole(user_role_code='99', user_role_name='guest')
        session.add(user_role)
        user = TUser(
            user_id = 'admin',
            user_name = 'admin',
            user_password = 'admin',
            user_role_code = '00'
        )
        session.add(user)
        user = TUser(
            user_id = 'guest',
            user_name = 'guest',
            user_password = 'guest',
            user_role_code = '99'
        )
        session.add(user)
        session.commit()

# テーブル作成
if __name__ == '__main__':
    init_db()