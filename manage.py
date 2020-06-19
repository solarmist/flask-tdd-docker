from project.app import app, db, cli
from project.models import User  # noqa


@cli.command("recreate_db")
def recreate_db():
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
