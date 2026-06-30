const state = {
  skills: [],
  experiences: [],
  projects: [],
  contacts: []
};

document.addEventListener('DOMContentLoaded', async () => {
  if (!localStorage.getItem('portfolio_token')) {
    window.location.href = '/admin/login.html';
    return;
  }

  document.getElementById('logoutBtn').addEventListener('click', logout);
  document.querySelectorAll('[data-reset]').forEach((button) => {
    button.addEventListener('click', () => document.getElementById(button.dataset.reset).reset());
  });

  bindForms();
  bindUploads();
  await loadAll();
});

function bindForms() {
  document.getElementById('profileForm').addEventListener('submit', saveProfile);
  document.getElementById('skillForm').addEventListener('submit', saveSkill);
  document.getElementById('experienceForm').addEventListener('submit', saveExperience);
  document.getElementById('projectForm').addEventListener('submit', saveProject);
}

function bindUploads() {
  document.getElementById('uploadProfileBtn').addEventListener('click', async () => {
    const url = await uploadImage(document.getElementById('profileImage').files[0]);
    if (url) document.getElementById('foto_url').value = url;
  });
  document.getElementById('uploadProjectBtn').addEventListener('click', async () => {
    const url = await uploadImage(document.getElementById('projectImage').files[0]);
    if (url) document.getElementById('gambar_url').value = url;
  });
}

async function loadAll() {
  try {
    const [stats, profile, skills, experiences, projects, contacts] = await Promise.all([
      apiRequest('/dashboard/stats'),
      apiRequest('/profiles'),
      apiRequest('/skills'),
      apiRequest('/experiences'),
      apiRequest('/projects'),
      apiRequest('/contacts')
    ]);

    renderStats(stats.data);
    fillForm('profileForm', profile.data || {});
    state.skills = skills.data || [];
    state.experiences = experiences.data || [];
    state.projects = projects.data || [];
    state.contacts = contacts.data || [];
    renderTables();
  } catch (error) {
    toast(error.message);
  }
}

function renderStats(stats) {
  const items = [
    ['Pengalaman', stats.experiences_count || 0],
    ['Proyek', stats.projects_count || 0],
    ['Skill', stats.skills_count || 0],
    ['Kontak', stats.contacts_count || 0]
  ];
  document.getElementById('statsGrid').innerHTML = items.map(([label, value]) => `
    <div class="stat-card"><strong>${value}</strong><span>${label}</span></div>
  `).join('');
}

function renderTables() {
  table('skillsTable', ['Skill', 'Icon', 'Aksi'], state.skills.map((item) => [
    item.nama_skill,
    item.icon_class || '-',
    actions('skill', item.id)
  ]));

  table('experiencesTable', ['Posisi', 'Instansi', 'Durasi', 'Aksi'], state.experiences.map((item) => [
    item.posisi,
    item.perusahaan,
    item.durasi,
    actions('experience', item.id)
  ]));

  table('projectsTable', ['Judul', 'Link', 'Aksi'], state.projects.map((item) => [
    item.judul,
    item.link_project ? `<a href="${escapeHtml(item.link_project)}" target="_blank">Buka</a>` : '-',
    actions('project', item.id)
  ]));

  table('contactsTable', ['Nama', 'Email', 'Status', 'Pesan', 'Aksi'], state.contacts.map((item) => [
    item.name,
    item.email,
    item.status,
    item.message,
    `<button onclick="markContact(${item.id}, 'read')">Tandai Dibaca</button><button onclick="removeItem('contact', ${item.id})">Hapus</button>`
  ]));
}

function table(id, headers, rows) {
  document.getElementById(id).innerHTML = `
    <thead><tr>${headers.map((header) => `<th>${header}</th>`).join('')}</tr></thead>
    <tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${cell || '-'}</td>`).join('')}</tr>`).join('')}</tbody>
  `;
}

function actions(type, id) {
  return `<button onclick="editItem('${type}', ${id})">Edit</button><button onclick="removeItem('${type}', ${id})">Hapus</button>`;
}

async function saveProfile(event) {
  event.preventDefault();
  try {
    await apiRequest('/profiles', { method: 'PUT', body: JSON.stringify(formData('profileForm')) });
    toast('Profil berhasil disimpan');
    await loadAll();
  } catch (error) {
    toast(error.message);
  }
}

async function saveSkill(event) {
  event.preventDefault();
  await saveEntity('skillForm', '/skills', 'Skill');
}

async function saveExperience(event) {
  event.preventDefault();
  await saveEntity('experienceForm', '/experiences', 'Pengalaman');
}

async function saveProject(event) {
  event.preventDefault();
  await saveEntity('projectForm', '/projects', 'Proyek');
}

async function saveEntity(formId, endpoint, label) {
  try {
    const data = formData(formId);
    const id = data.id;
    delete data.id;
    await apiRequest(id ? `${endpoint}/${id}` : endpoint, {
      method: id ? 'PUT' : 'POST',
      body: JSON.stringify(data)
    });
    document.getElementById(formId).reset();
    toast(`${label} berhasil disimpan`);
    await loadAll();
  } catch (error) {
    toast(error.message);
  }
}

function editItem(type, id) {
  const map = {
    skill: ['skillForm', state.skills],
    experience: ['experienceForm', state.experiences],
    project: ['projectForm', state.projects]
  };
  const [formId, list] = map[type];
  const item = list.find((row) => row.id === id);
  fillForm(formId, item || {});
  document.getElementById(formId).scrollIntoView({ behavior: 'smooth', block: 'center' });
}

async function removeItem(type, id) {
  if (!confirm('Hapus data ini?')) return;
  const endpoint = type === 'contact' ? '/contacts' : type === 'skill' ? '/skills' : type === 'experience' ? '/experiences' : '/projects';
  try {
    await apiRequest(`${endpoint}/${id}`, { method: 'DELETE' });
    toast('Data berhasil dihapus');
    await loadAll();
  } catch (error) {
    toast(error.message);
  }
}

async function markContact(id, status) {
  try {
    await apiRequest(`/contacts/${id}`, { method: 'PUT', body: JSON.stringify({ status }) });
    toast('Status kontak diperbarui');
    await loadAll();
  } catch (error) {
    toast(error.message);
  }
}

async function uploadImage(file) {
  if (!file) {
    toast('Pilih file gambar terlebih dahulu');
    return '';
  }
  const data = new FormData();
  data.append('file', file);
  try {
    const result = await apiRequest('/upload/image', { method: 'POST', body: data });
    toast('Gambar berhasil diupload ke Cloudinary');
    return result.url;
  } catch (error) {
    toast(error.message);
    return '';
  }
}

function formData(formId) {
  const data = {};
  new FormData(document.getElementById(formId)).forEach((value, key) => {
    data[key] = value;
  });
  return data;
}

function fillForm(formId, data) {
  const form = document.getElementById(formId);
  Object.entries(data || {}).forEach(([key, value]) => {
    const input = form.elements[key];
    if (input && value !== null && value !== undefined) input.value = value;
  });
}

async function logout() {
  try {
    await apiRequest('/logout', { method: 'POST' });
  } finally {
    localStorage.removeItem('portfolio_token');
    window.location.href = '/admin/login.html';
  }
}

function toast(message) {
  const el = document.getElementById('toast');
  el.textContent = message;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 3000);
}

function escapeHtml(text) {
  if (text === null || text === undefined) return '';
  return String(text).replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  }[char]));
}
