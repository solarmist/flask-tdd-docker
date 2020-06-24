from project.api.users.models import User  # noqa
from project.app import app, cli, db  # noqa


@cli.command("recreate_db")
def recreate_db():
    print(f"DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("Dropping tables")
    db.drop_all()
    print("Re-creating tables")
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    print("Creating users")
    db.session.add(User(username="mark", email="mark@gilberta.co"))
    db.session.add(User(username="corinna", email="corinna@gilberta.co"))
    db.session.commit()


if __name__ == "__main__":
    cli()
