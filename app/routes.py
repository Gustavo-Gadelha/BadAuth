from flask_smorest import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/signup", methods=["POST"])
def signup():
    pass


@auth.route("/login", methods=["POST"])
def login():
    pass


@auth.route("/recuperar-senha", methods=["POST"])
def recuperar_senha():
    pass


@auth.route("/logout", methods=["POST"])
def logout():
    pass


@auth.route("/me", methods=["POST"])
def me():
    pass
