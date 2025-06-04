from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites_characters: Mapped[list['Favorite_Characters']] = relationship(
        back_populates='user', cascade='all, delete-orphan')
    favorites_starships: Mapped[list['Favorite_Starships']] = relationship(
        back_populates='user', cascade='all, delete-orphan')
    favorites_planets: Mapped[list['Favorites_Planets']] = relationship(
        back_populates='user', cascade='all, delete-orphan')


class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    birth_year: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list['Favorite_Characters']] = relationship(
        back_populates='characters', cascade='all, delete-orphan')


class Favorite_Characters(db.Model):
    __tablename__ = 'favorite_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favorites_characters')
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    characters: Mapped['Characters'] = relationship(
        back_populates='favorite_by')


class Starships(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    favorite_by: Mapped[list['Favorite_Starships']] = relationship(
        back_populates='starships', cascade='all, delete-orphan')


class Favorite_Starships(db.Model):
    __tablename__ = 'favorites_starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favorites_starships')
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'))
    starships: Mapped['Starships'] = relationship(
        back_populates='favorite_by')


class Planets (db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    population: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list['Favorites_Planets']] = relationship(
        back_populates='planets', cascade='all, delete-orphan')


class Favorites_Planets (db.Model):
    __tablename__ = 'favorites_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped[User] = relationship(back_populates='favorites_planets')
    planets_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    planets: Mapped[Planets] = relationship(back_populates='favorite_by')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
