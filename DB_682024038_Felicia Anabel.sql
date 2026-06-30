CREATE DATABASE IF NOT EXISTS felicia_anabel
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE felicia_anabel;

DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS experiences;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin', 'user') NOT NULL DEFAULT 'admin',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profiles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  nama_lengkap VARCHAR(150) NOT NULL,
  nama_panggilan VARCHAR(100),
  tempat_lahir VARCHAR(100),
  tanggal_lahir DATE,
  email VARCHAR(150),
  telepon VARCHAR(50),
  universitas VARCHAR(150),
  fakultas VARCHAR(150),
  prodi VARCHAR(150),
  semester INT,
  alamat TEXT,
  foto_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_profiles_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE skills (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  nama_skill VARCHAR(120) NOT NULL,
  icon_class VARCHAR(120),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_skills_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE experiences (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  posisi VARCHAR(150) NOT NULL,
  perusahaan VARCHAR(150) NOT NULL,
  durasi VARCHAR(100) NOT NULL,
  deskripsi TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_experiences_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  judul VARCHAR(150) NOT NULL,
  deskripsi TEXT NOT NULL,
  gambar_url TEXT,
  link_project TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_projects_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE contacts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  email VARCHAR(150) NOT NULL,
  message TEXT NOT NULL,
  status ENUM('new', 'read', 'archived') NOT NULL DEFAULT 'new',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password_hash, role)
VALUES
  ('admin', 'pbkdf2:sha256:1000000$portfolioadmin$7b9eae37a68b357c9cf0a9b2c2744604bf9b894fee320a4c934f45abf4176fce', 'admin');

INSERT INTO profiles (
  user_id, nama_lengkap, nama_panggilan, tempat_lahir, tanggal_lahir,
  email, telepon, universitas, fakultas, prodi, semester, alamat, foto_url
)
VALUES (
  1,
  'Felicia Anabel',
  'Abel',
  'Jakarta',
  '2006-02-08',
  'feliciaanabel8226@gmail.com',
  '089644852606',
  'Universitas Kristen Satya Wacana',
  'Fakultas Teknologi Informasi',
  'Sistem Informasi',
  NULL,
  'Jakarta, Indonesia',
  ''
);

INSERT INTO skills (user_id, nama_skill, icon_class)
VALUES
  (1, 'Photographer', 'fas fa-camera'),
  (1, 'Adobe Illustrator', 'fab fa-python'),
  (1, 'Graphic Design', 'fas fa-paint-brush'),
  (1, 'MySQL dan TiDB', 'fas fa-database');

INSERT INTO experiences (user_id, posisi, perusahaan, durasi, deskripsi)
VALUES
  (1, 'Mahasiswa Sistem Informasi', 'Universitas Kristen Satya Wacana', '2024 - Sekarang', 'Mempelajari pengembangan sistem informasi, database, analisis proses bisnis, dan teknologi web.'),
  (1, 'ISACA Student Group UKSW', 'Secretary', '2025 - 2026', 'Menjadi fungsionaris ISG UKSW selama 2 tahun, mempelajari tata kelola serta Audit TI.');

INSERT INTO projects (user_id, judul, deskripsi, gambar_url, link_project)
VALUES
  (1, 'Website Portofolio Felicia Anabel', 'Aplikasi portofolio berbasis Flask yang menampilkan profil, skill, pengalaman, proyek, dan form kontak dari database.', '', 'https://github.com/'),
  (1, 'Dashboard Admin Portfolio', 'Dashboard admin untuk mengelola data profil, skill, pengalaman, proyek, upload gambar, dan pesan kontak.', '', 'https://github.com/');
