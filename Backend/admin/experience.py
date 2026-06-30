from flask import Blueprint, request, jsonify
from model import Database
from Backend.admin.login import token_required

experience_bp = Blueprint('experience', __name__)


@experience_bp.route('/experiences', methods=['GET'])
def get_experiences():
    try:
        db = Database()
        result = db.execute_query(
            """
            SELECT e.*, u.username
            FROM experiences e
            JOIN users u ON e.user_id = u.id
            WHERE u.role = 'admin'
            ORDER BY e.created_at DESC
            """,
            fetch=True
        )
        return jsonify({'success': True, 'data': result or []}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@experience_bp.route('/experiences/<int:id>', methods=['GET'])
def get_experience_by_id(id):
    try:
        db = Database()
        result = db.execute_query("SELECT * FROM experiences WHERE id = %s", (id,), fetch=True)
        if not result:
            return jsonify({'error': 'Experience tidak ditemukan'}), 404
        return jsonify({'success': True, 'data': result[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@experience_bp.route('/experiences', methods=['POST'])
@token_required
def create_experience(current_user):
    try:
        data = request.get_json() or {}
        for field in ['posisi', 'perusahaan', 'durasi']:
            if not data.get(field):
                return jsonify({'error': f'{field} wajib diisi'}), 400

        db = Database()
        new_id = db.execute_query(
            """
            INSERT INTO experiences (user_id, posisi, perusahaan, durasi, deskripsi)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                current_user,
                data.get('posisi'),
                data.get('perusahaan'),
                data.get('durasi'),
                data.get('deskripsi')
            )
        )
        return jsonify({'success': True, 'message': 'Experience berhasil dibuat', 'id': new_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@experience_bp.route('/experiences/<int:id>', methods=['PUT'])
@token_required
def update_experience(current_user, id):
    try:
        data = request.get_json() or {}
        db = Database()
        existing = db.execute_query(
            "SELECT id FROM experiences WHERE id = %s AND user_id = %s",
            (id, current_user),
            fetch=True
        )
        if not existing:
            return jsonify({'error': 'Experience tidak ditemukan atau bukan milik Anda'}), 404

        allowed_fields = ['posisi', 'perusahaan', 'durasi', 'deskripsi']
        updates = []
        values = []
        for field in allowed_fields:
            if field in data:
                updates.append(f"{field} = %s")
                values.append(data[field])

        if not updates:
            return jsonify({'error': 'Tidak ada data yang diupdate'}), 400

        values.append(id)
        db.execute_query(f"UPDATE experiences SET {', '.join(updates)} WHERE id = %s", tuple(values))
        return jsonify({'success': True, 'message': 'Experience berhasil diupdate'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@experience_bp.route('/experiences/<int:id>', methods=['DELETE'])
@token_required
def delete_experience(current_user, id):
    try:
        db = Database()
        existing = db.execute_query(
            "SELECT id FROM experiences WHERE id = %s AND user_id = %s",
            (id, current_user),
            fetch=True
        )
        if not existing:
            return jsonify({'error': 'Experience tidak ditemukan atau bukan milik Anda'}), 404

        db.execute_query("DELETE FROM experiences WHERE id = %s", (id,))
        return jsonify({'success': True, 'message': 'Experience berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
