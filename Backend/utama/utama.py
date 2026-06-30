from flask import Blueprint, jsonify
from model import Database

utama_bp = Blueprint('utama', __name__)


@utama_bp.route('/main-profile', methods=['GET'])
def get_main_profile():
    try:
        db = Database()

        profile_query = """
            SELECT p.*
            FROM profiles p
            JOIN users u ON p.user_id = u.id
            WHERE u.role = 'admin'
            ORDER BY p.updated_at DESC, p.id ASC
            LIMIT 1
        """
        profiles = db.execute_query(profile_query, fetch=True)
        if not profiles:
            return jsonify({'success': True, 'data': {}}), 200

        profile = profiles[0]
        user_id = profile['user_id']

        skills = db.execute_query(
            "SELECT id, nama_skill, icon_class FROM skills WHERE user_id = %s ORDER BY id DESC",
            (user_id,),
            fetch=True
        )
        experiences = db.execute_query(
            """
            SELECT id, posisi, perusahaan, durasi, deskripsi
            FROM experiences
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,),
            fetch=True
        )
        projects = db.execute_query(
            """
            SELECT id, judul, deskripsi, gambar_url, link_project
            FROM projects
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,),
            fetch=True
        )

        profile['skills'] = skills or []
        profile['experiences'] = experiences or []
        profile['projects'] = projects or []

        return jsonify({'success': True, 'data': profile}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
