import os
from datetime import datetime
from typing import Any, Dict

from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

DATABASE_PATH = os.environ.get("TODO_DATABASE", "todo.db")


db = SQLAlchemy()


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    db_uri = f"sqlite:///{DATABASE_PATH}"
    if testing:
        db_uri = "sqlite:///:memory:"

    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/api/todos", methods=["GET"])
    def list_todos():
        todos = Todo.query.order_by(Todo.created_at.desc()).all()
        return jsonify([todo.to_dict() for todo in todos])

    @app.route("/api/todos", methods=["POST"])
    def create_todo():
        payload = request.get_json(force=True, silent=True) or {}
        title = (payload.get("title") or "").strip()
        if not title:
            return jsonify({"error": "title is required"}), 400

        todo = Todo(title=title, completed=bool(payload.get("completed", False)))
        db.session.add(todo)
        db.session.commit()
        return jsonify(todo.to_dict()), 201

    @app.route("/api/todos/<int:todo_id>", methods=["PATCH"])
    def update_todo(todo_id: int):
        todo = Todo.query.get_or_404(todo_id)
        payload = request.get_json(force=True, silent=True) or {}

        if "title" in payload:
            new_title = (payload.get("title") or "").strip()
            if not new_title:
                return jsonify({"error": "title cannot be empty"}), 400
            todo.title = new_title

        if "completed" in payload:
            todo.completed = bool(payload.get("completed"))

        db.session.commit()
        return jsonify(todo.to_dict())

    @app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
    def delete_todo(todo_id: int):
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return "", 204

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app


if __name__ == "__main__":
    application = create_app()
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port, debug=True)
