const API = {
  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  },

  async fetch(url, options = {}) {
    options.headers = options.headers || {};
    options.headers['X-CSRFToken'] = this.getCookie('csrftoken') || '';
    if (!options.headers['Content-Type'] && !(options.body instanceof FormData)) {
      options.headers['Content-Type'] = 'application/json';
    }

    try {
      const response = await fetch(url, options);
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.error || data.detail || 'API error');
      }
      return data;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },

  showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const id = 'toast-' + Date.now();
    const bg = type === 'success' ? 'bg-success text-white' : type === 'error' ? 'bg-danger text-white' : 'bg-dark text-white';
    container.insertAdjacentHTML('beforeend', `
      <div id="${id}" class="toast align-items-center ${bg} border-0 show mb-2" role="alert">
        <div class="d-flex">
          <div class="toast-body font-weight-bold">${message}</div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
      </div>
    `);
    setTimeout(() => { const el = document.getElementById(id); if (el) el.remove(); }, 3500);
  },

  async enrollInCourse(courseId) {
    try {
      const res = await this.fetch(`/api/courses/${courseId}/enroll`, { method: 'POST' });
      this.showToast(res.message, 'success');
      setTimeout(() => window.location.href = `/player/${courseId}/`, 800);
    } catch (err) {
      if (err.message.includes('Authentication credentials')) {
        window.location.href = `/login/?next=/courses/${courseId}/`;
      } else {
        this.showToast(err.message, 'error');
      }
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.js-logout-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      try {
        await API.fetch('/api/auth/logout', { method: 'POST' });
      } catch (err) {}
      window.location.href = '/';
    });
  });
});
