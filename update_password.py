# update_password.py
import sys
import argparse
import getpass
from werkzeug.security import generate_password_hash
from app import app, db
from models.user import User

def main():
    parser = argparse.ArgumentParser(
        description="Update (or create) a Spaklean user password in the database."
    )
    parser.add_argument("--email", required=True, help="User email to update")
    parser.add_argument(
        "--password",
        help="New password. If omitted, you'll be prompted securely."
    )
    parser.add_argument(
        "--create-if-missing",
        action="store_true",
        help="Create the user if it doesn't exist (with provided --role)."
    )
    parser.add_argument(
        "--role",
        default="Custodian",
        help="Role to use if creating a missing user (default: Custodian)."
    )
    parser.add_argument(
        "--first-name",
        default="Temp",
        help="First name to use if creating a missing user (default: Temp)."
    )
    parser.add_argument(
        "--last-name",
        default="User",
        help="Last name to use if creating a missing user (default: User)."
    )
    args = parser.parse_args()

    password = args.password or getpass.getpass("Enter new password: ")
    if len(password) < 6:
        print("❌ Password must be at least 6 characters.")
        sys.exit(1)

    with app.app_context():
        user = User.query.filter_by(email=args.email).first()

        if not user:
            if not args.create_if_missing:
                print(f"❌ User not found: {args.email}. Use --create-if-missing to create.")
                sys.exit(1)
            # Create a new user
            user = User(
                first_name=args.first_name,
                last_name=args.last_name,
                email=args.email,
                role=args.role,
                password_hash=generate_password_hash(password),
            )
            db.session.add(user)
            db.session.commit()
            print(f"✅ Created user {args.email} with role '{args.role}'")
            return

        # Update existing user's password
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        print(f"✅ Updated password for {args.email}")

if __name__ == "__main__":
    main()
