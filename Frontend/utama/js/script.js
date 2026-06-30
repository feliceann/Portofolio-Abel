document.addEventListener('DOMContentLoaded', async () => {
  document.getElementById('current-year').textContent = new Date().getFullYear();
  await loadPublicData();
  setupContactForm();

  const hamburger = document.getElementById('hamburger');
  const navMenu = document.getElementById('navMenu');
  if (hamburger) {
    hamburger.addEventListener('click', () => navMenu.classList.toggle('active'));
  }
});

async function loadPublicData() {
  try {
    const response = await fetch('/api/main-profile');
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    const res = await response.json();

    if (!res.success || !res.data || !res.data.nama_lengkap) {
      showError('Data profil belum tersedia.');
      return;
    }

    const profile = res.data;
    renderHero(profile);
    renderAbout(profile);
    renderSkills(profile.skills || []);
    renderExperiences(profile.experiences || []);
    renderProjects(profile.projects || []);
    renderContact(profile);
  } catch (error) {
    showError('Gagal terhubung ke server.');
  }
}

function showError(message) {
  const heroContent = document.getElementById('hero-content');
  if (heroContent) heroContent.innerHTML = `<div class="error-state">${escapeHtml(message)}</div>`;
}

function renderHero(profile) {
  document.getElementById('hero-content').innerHTML = `
    <div class="hero-copy">
      <span class="eyebrow">Information Systems Portfolio</span>
      <h1>Hi, I'm <span>${escapeHtml(profile.nama_panggilan || profile.nama_lengkap)}</span></h1>
      <h2>${escapeHtml(profile.nama_lengkap)}</h2>
      <p>${escapeHtml(profile.prodi || 'Mahasiswa')} - ${escapeHtml(profile.fakultas || 'Fakultas Teknologi Informasi')}</p>
      <div class="hero-actions">
        <a href="#projects" class="btn">Lihat Proyek <i class="fas fa-arrow-right"></i></a>
        <a href="#contact" class="btn btn-outline">Contact Me</a>
      </div>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="portrait-card">
        ${profile.foto_url
          ? `<img src="${escapeHtml(profile.foto_url)}" alt="" class="hero-photo">`
          : '<i class="fas fa-user-graduate hero-icon"></i>'}
      </div>
      <div class="floating-card card-age"><strong>${escapeHtml(profile.nama_panggilan || 'Abel')}</strong><span>Nama Panggilan</span></div>
      <div class="floating-card card-code"><i class="fas fa-code"></i></div>
    </div>
  `;
}

function renderAbout(profile) {
  const img = document.getElementById('profile-photo');
  const placeholder = document.getElementById('photo-placeholder');

  if (profile.foto_url) {
    img.src = profile.foto_url;
    img.style.display = 'block';
    placeholder.style.display = 'none';
  } else {
    img.style.display = 'none';
    placeholder.style.display = 'flex';
  }

  const age = calculateAge(profile.tanggal_lahir);
  document.getElementById('about-text').innerHTML = `
    <span class="eyebrow">About Me</span>
    <h3>${escapeHtml(profile.nama_lengkap)} - ${escapeHtml(profile.prodi || '')}</h3>
    <p>Saya ${escapeHtml(profile.nama_panggilan || 'Abel')}, mahasiswa ${escapeHtml(profile.prodi || '-')} di ${escapeHtml(profile.universitas || '-')}.</p>
    <div class="profile-details">
      <div><i class="fas fa-id-card"></i><span>Nama</span><strong>${escapeHtml(profile.nama_lengkap)}</strong></div>
      <div><i class="fas fa-cake-candles"></i><span>Lahir</span><strong>${escapeHtml(formatBirth(profile.tempat_lahir, profile.tanggal_lahir))}</strong></div>
      <div><i class="fas fa-hourglass-half"></i><span>Usia</span><strong>${age ? `${age} tahun` : '-'}</strong></div>
      <div><i class="fas fa-building-columns"></i><span>Fakultas</span><strong>${escapeHtml(profile.fakultas || '-')}</strong></div>
      <div><i class="fas fa-phone"></i><span>Telepon</span><strong>${escapeHtml(profile.telepon || '-')}</strong></div>
      <div><i class="fas fa-envelope"></i><span>Email</span><strong>${escapeHtml(profile.email || '-')}</strong></div>
    </div>
    <a href="#contact" class="btn">Hubungi Saya <i class="fas fa-paper-plane"></i></a>
  `;
}

function renderSkills(skills) {
  const container = document.getElementById('skills-container');
  if (!skills.length) {
    container.innerHTML = '<p class="empty-state">Belum ada data skill.</p>';
    return;
  }

  container.innerHTML = skills.map((skill) => `
    <div class="skill-card">
      <i class="${escapeHtml(skill.icon_class || 'fas fa-code')}"></i>
      <h4>${escapeHtml(skill.nama_skill)}</h4>
      <span>Technology</span>
    </div>
  `).join('');
}

function renderExperiences(experiences) {
  const container = document.getElementById('experience-container');
  if (!experiences.length) {
    container.innerHTML = '<p class="empty-state">Belum ada pengalaman.</p>';
    return;
  }

  container.innerHTML = experiences.map((item) => `
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-content">
        <span class="timeline-date">${escapeHtml(item.durasi)}</span>
        <h3>${escapeHtml(item.posisi)}</h3>
        <h4>${escapeHtml(item.perusahaan)}</h4>
        <p>${escapeHtml(item.deskripsi || '')}</p>
      </div>
    </div>
  `).join('');
}

function renderProjects(projects) {
  const container = document.getElementById('projects-container');
  if (!projects.length) {
    container.innerHTML = '<p class="empty-state">Belum ada proyek.</p>';
    return;
  }

  container.innerHTML = projects.map((project) => `
    <div class="project-card">
      <div class="project-img-wrapper">
        ${project.gambar_url
          ? `<img src="${escapeHtml(project.gambar_url)}" alt="${escapeHtml(project.judul)}" class="project-img" loading="lazy">`
          : '<div class="project-img project-placeholder"><i class="fas fa-box-open"></i></div>'}
        <div class="project-overlay">
          <h3 class="project-title-overlay">${escapeHtml(project.judul)}</h3>
        </div>
      </div>
      <div class="project-info">
        <p>${escapeHtml((project.deskripsi || '').slice(0, 140))}${(project.deskripsi || '').length > 140 ? '...' : ''}</p>
        <div class="project-links">
          ${project.link_project ? `<a href="${escapeHtml(project.link_project)}" target="_blank" rel="noopener">Lihat Proyek <i class="fas fa-up-right-from-square"></i></a>` : ''}
        </div>
      </div>
    </div>
  `).join('');
}

function renderContact(profile) {
  const emailDisplay = document.getElementById('contact-email-display');
  if (emailDisplay && profile.email) {
    emailDisplay.innerHTML = `Tertarik berkolaborasi? Kirim pesan ke <strong>${escapeHtml(profile.email)}</strong> atau hubungi <strong>${escapeHtml(profile.telepon || '-')}</strong>.`;
  }
}

function calculateAge(dateText) {
  if (!dateText) return 20;
  const birthday = new Date(dateText);
  if (Number.isNaN(birthday.getTime())) return 20;
  const today = new Date();
  let age = today.getFullYear() - birthday.getFullYear();
  const monthDiff = today.getMonth() - birthday.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthday.getDate())) age -= 1;
  return age;
}

function formatBirth(place, dateText) {
  if (!dateText) return place || '-';
  const date = new Date(dateText);
  if (Number.isNaN(date.getTime())) return `${place || '-'}, ${dateText}`;
  return `${place || '-'}, ${date.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })}`;
}

function setupContactForm() {
  const contactForm = document.getElementById('contactForm');
  if (!contactForm) return;

  contactForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const btn = document.getElementById('sendBtn');
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Mengirim...';

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: document.getElementById('contactName').value,
          email: document.getElementById('contactEmail').value,
          message: document.getElementById('contactMessage').value
        })
      });

      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        contactForm.reset();
      } else {
        alert(result.error || 'Pesan gagal dikirim');
      }
    } catch (error) {
      alert('Terjadi kesalahan jaringan.');
    } finally {
      btn.disabled = false;
      btn.textContent = originalText;
    }
  });
}

function escapeHtml(text) {
  if (text === null || text === undefined) return '';
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return String(text).replace(/[&<>"']/g, (char) => map[char]);
}
