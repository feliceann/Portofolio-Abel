from flask import Blueprint, request, jsonify
from model import Database
from config import Config
from Backend.admin.login import token_required
import resend
from html import escape

contacts_bp = Blueprint('contacts', __name__)


def send_resend_email(name, email, message):
    if not Config.RESEND_API_KEY:
        return False, 'RESEND_API_KEY belum diisi pada file .env'

    target_email = Config.CONTACT_RECEIVER_EMAIL
    if not target_email:
        profiles = Database().execute_query(
            """
            SELECT p.email
            FROM profiles p
            JOIN users u ON p.user_id = u.id
            WHERE u.role = 'admin' AND p.email IS NOT NULL AND p.email != ''
            ORDER BY p.id ASC
            LIMIT 1
            """,
            fetch=True
        )
        target_email = profiles[0]['email'] if profiles else ''

    if not target_email:
        return False, 'Email penerima belum tersedia. Isi CONTACT_RECEIVER_EMAIL atau email profil admin.'

    resend.api_key = Config.RESEND_API_KEY
    resend.Emails.send({
        'from': Config.RESEND_FROM_EMAIL,
        'to': [target_email],
        'subject': f'Pesan portofolio dari {name}',
        'reply_to': email,
        'html': f"""
            <h2>Pesan Baru dari Website Portofolio</h2>
            <p><strong>Nama:</strong> {escape(name)}</p>
            <p><strong>Email:</strong> {escape(email)}</p>
            <p><strong>Pesan:</strong></p>
            <p>{escape(message)}</p>
        """
    })
    return True, 'Pesan berhasil dikirim'


@contacts_bp.route('/contact', methods=['POST'])
def create_contact():
    try:
        data = request.get_json() or {}
        name = (data.get('name') or '').strip()
        email = (data.get('email') or '').strip()
        message = (data.get('message') or '').strip()

        if not name or not email or not message:
            return jsonify({'error': 'Nama, email, dan pesan wajib diisi'}), 400

        db = Database()
        db.execute_query(
            """
            INSERT INTO contacts (name, email, message, status)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, message, 'new')
        )

        sent, note = send_resend_email(name, email, message)
        if not sent:
            return jsonify({
                'success': True,
                'message': 'Pesan tersimpan, tetapi email belum terkirim',
                'email_status': note
            }), 202

        return jsonify({'success': True, 'message': 'Pesan berhasil dikirim'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@contacts_bp.route('/contacts', methods=['GET'])
@token_required
def get_contacts(current_user):
    try:
        db = Database()
        result = db.execute_query(
            "SELECT * FROM contacts ORDER BY created_at DESC",
            fetch=True
        )
        return jsonify({'success': True, 'data': result or []}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@contacts_bp.route('/contacts/<int:id>', methods=['PUT'])
@token_required
def update_contact(current_user, id):
    try:
        data = request.get_json() or {}
        status = data.get('status')
        if status not in ['new', 'read', 'archived']:
            return jsonify({'error': 'Status tidak valid'}), 400

        db = Database()
        db.execute_query("UPDATE contacts SET status = %s WHERE id = %s", (status, id))
        return jsonify({'success': True, 'message': 'Status kontak berhasil diperbarui'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@contacts_bp.route('/contacts/<int:id>', methods=['DELETE'])
@token_required
def delete_contact(current_user, id):
    try:
        db = Database()
        db.execute_query("DELETE FROM contacts WHERE id = %s", (id,))
        return jsonify({'success': True, 'message': 'Kontak berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
