from flask import Flask, request, jsonify
from services.user_service import UserService
from repositories.postgres_user_repo import PostgresUserRepository
import traceback  # Добавьте эту строку

app = Flask(__name__)
app.config['DEBUG'] = True  # Добавьте эту строку

# Инициализация зависимостей
repo = PostgresUserRepository()
service = UserService(repo)


@app.route('/health')
def health():
    return {"status": "ok"}


@app.route('/users', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

        user = service.register_user(name, email)
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Добавьте детальную информацию об ошибке
        error_details = traceback.format_exc()
        print(f"Internal error: {error_details}")  # Для просмотра в консоли
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = service.list_all_users()
        return jsonify([{
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "created_at": u.created_at.isoformat()
        } for u in users])
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Internal error: {error_details}")
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Добавьте debug=True