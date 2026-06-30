from flask import Blueprint, request, jsonify
from model import Database
from Backend.admin.login import token_required

skills_bp = Blueprint('skills', __name__)


@skills_bp.route('/skills', methods=['GET'])
def get_skills():
    try:
        db = Database()
        result = db.execute_query(
            """
            SELECT s.*, u.username
            FROM skills s
            JOIN users u ON s.user_id = u.id
            WHERE u.role = 'admin'
            ORDER BY s.id DESC
            """,
            fetch=True
        )
        return jsonify({'success': True, 'data': result or []}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@skills_bp.route('/skills/<int:id>', methods=['GET'])
def get_skill_by_id(id):
    try:
        db = Database()
        result = db.execute_query("SELECT * FROM skills WHERE id = %s", (id,), fetch=True)
        if not result:
            return jsonify({'error': 'Skill tidak ditemukan'}), 404
        return jsonify({'success': True, 'data': result[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@skills_bp.route('/skills', methods=['POST'])
@token_required
def create_skill(current_user):
    try:
        data = request.get_json() or {}
        if not data.get('nama_skill'):
            return jsonify({'error': 'nama_skill wajib diisi'}), 400

        db = Database()
        new_id = db.execute_query(
            "INSERT INTO skills (user_id, nama_skill, icon_class) VALUES (%s, %s, %s)",
            (current_user, data.get('nama_skill'), data.get('icon_class'))
        )
        return jsonify({'success': True, 'message': 'Skill berhasil dibuat', 'id': new_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@skills_bp.route('/skills/<int:id>', methods=['PUT'])
@token_required
def update_skill(current_user, id):
    try:
        data = request.get_json() or {}
        db = Database()
        existing = db.execute_query(
            "SELECT id FROM skills WHERE id = %s AND user_id = %s",
            (id, current_user),
            fetch=True
        )
        if not existing:
            return jsonify({'error': 'Skill tidak ditemukan atau bukan milik Anda'}), 404

        allowed_fields = ['nama_skill', 'icon_class']
        updates = []
        values = []
        for field in allowed_fields:
            if field in data:
                updates.append(f"{field} = %s")
                values.append(data[field])

        if not updates:
            return jsonify({'error': 'Tidak ada data yang diupdate'}), 400

        values.append(id)
        db.execute_query(f"UPDATE skills SET {', '.join(updates)} WHERE id = %s", tuple(values))
        return jsonify({'success': True, 'message': 'Skill berhasil diupdate'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@skills_bp.route('/skills/<int:id>', methods=['DELETE'])
@token_required
def delete_skill(current_user, id):
    try:
        db = Database()
        existing = db.execute_query(
            "SELECT id FROM skills WHERE id = %s AND user_id = %s",
            (id, current_user),
            fetch=True
        )
        if not existing:
            return jsonify({'error': 'Skill tidak ditemukan atau bukan milik Anda'}), 404

        db.execute_query("DELETE FROM skills WHERE id = %s", (id,))
        return jsonify({'success': True, 'message': 'Skill berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
