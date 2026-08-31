/**
 * Kwankhao Sivasomboon - AI Engineer Portfolio & Web CV
 * Interactive Application Engine (Zero-dependency Vanilla JS)
 */

document.addEventListener('DOMContentLoaded', () => {
  // Global App State
  const state = {
    theme: localStorage.getItem('theme') || 'dark',
    activeCategory: 'all',
    searchQuery: '',
    selectedSkill: null,
    projects: window.PORTFOLIO_DATA?.projects || [],
    resume: window.PORTFOLIO_DATA?.resume || {},
    categories: window.PORTFOLIO_DATA?.categories || [],
    startupLearnings: window.PORTFOLIO_DATA?.startupLearnings || []
  };

  // Init Components
  initTheme();
  initNeuralCanvas();
  initNavigation();
  initSkillsMatrix();
  initStartupLearnings();
  initCategoryFilters();
  initProjectSearch();
  renderProjects();
  initExperienceTimeline();
  initEducation();
  initCounters();
  initModals();

  /* ==========================================================================
     1. Theme Management (Dark / Light)
     ========================================================================== */
  function initTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    const themeBtn = document.getElementById('theme-toggle-btn');
    
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        state.theme = state.theme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', state.theme);
        localStorage.setItem('theme', state.theme);
        showToast(`Switched to ${state.theme === 'dark' ? 'Dark' : 'Light'} Mode`);
      });
    }
  }

  /* ==========================================================================
     2. Interactive Neural Canvas Background
     ========================================================================== */
  function initNeuralCanvas() {
    const canvas = document.getElementById('neural-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = Math.min(Math.floor(window.innerWidth / 22), 60);
    const mouse = { x: null, y: null, radius: 140 };

    window.addEventListener('mousemove', (e) => {
      mouse.x = e.x;
      mouse.y = e.y;
    });

    window.addEventListener('mouseleave', () => {
      mouse.x = null;
      mouse.y = null;
    });

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 2 + 1
      });
    }

    function animate() {
      ctx.clearRect(0, 0, width, height);

      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const nodeColor = isDark ? 'rgba(0, 242, 254, 0.4)' : 'rgba(2, 132, 199, 0.35)';
      const lineColor = isDark ? 'rgba(79, 172, 254, 0.08)' : 'rgba(2, 132, 199, 0.06)';

      particles.forEach((p, index) => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        // Draw particle node
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = nodeColor;
        ctx.fill();

        // Connect with nearby particles
        for (let j = index + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 120) {
            ctx.beginPath();
            ctx.strokeStyle = lineColor;
            ctx.lineWidth = 1 - dist / 120;
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }

        // Connect with mouse cursor
        if (mouse.x && mouse.y) {
          const dx = p.x - mouse.x;
          const dy = p.y - mouse.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < mouse.radius) {
            ctx.beginPath();
            ctx.strokeStyle = isDark ? 'rgba(0, 242, 254, 0.2)' : 'rgba(2, 132, 199, 0.15)';
            ctx.lineWidth = 1.2 * (1 - dist / mouse.radius);
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.stroke();
          }
        }
      });

      requestAnimationFrame(animate);
    }
    animate();
  }

  /* ==========================================================================
     3. Navigation & Scroll Watcher
     ========================================================================== */
  function initNavigation() {
    const navbar = document.getElementById('navbar');
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const mobileDrawer = document.getElementById('mobile-drawer');
    const closeDrawerBtn = document.getElementById('close-drawer-btn');
    const mobileLinks = document.querySelectorAll('.mobile-nav-link');

    // Sticky navbar shadow on scroll
    window.addEventListener('scroll', () => {
      if (window.scrollY > 30) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });

    // Mobile Drawer open/close
    if (mobileBtn && mobileDrawer) {
      mobileBtn.addEventListener('click', () => mobileDrawer.classList.add('open'));
      closeDrawerBtn.addEventListener('click', () => mobileDrawer.classList.remove('open'));
      mobileLinks.forEach(link => {
        link.addEventListener('click', () => mobileDrawer.classList.remove('open'));
      });
    }

    // Update project count badge
    const badge = document.getElementById('project-count-badge');
    if (badge) badge.textContent = state.projects.length;
  }

  /* ==========================================================================
     4. Technical Skills Matrix
     ========================================================================== */
  function initSkillsMatrix() {
    const container = document.getElementById('skills-matrix-container');
    if (!container || !state.resume?.skills) return;

    const domainConfigs = [
      {
        key: 'computer_vision',
        title: 'Computer Vision & Edge AI',
        icon: 'fa-eye',
        skills: state.resume.skills.computer_vision
      },
      {
        key: 'genai_rag',
        title: 'GenAI, LLMs & Hybrid RAG',
        icon: 'fa-brain-circuit',
        skills: state.resume.skills.genai_rag
      },
      {
        key: 'backend_cloud',
        title: 'Backend, Cloud & Microservices',
        icon: 'fa-server',
        skills: state.resume.skills.backend_cloud
      },
      {
        key: 'qa_automation',
        title: 'Multi-Agent & QA Automation',
        icon: 'fa-robot',
        skills: state.resume.skills.qa_automation
      },
      {
        key: 'geospatial_3d',
        title: 'Geospatial AI & 3D Analytics',
        icon: 'fa-earth-americas',
        skills: state.resume.skills.geospatial_3d
      }
    ];

    container.innerHTML = domainConfigs.map(domain => `
      <div class="skill-domain-card">
        <div class="skill-domain-header">
          <div class="domain-icon"><i class="fa-solid ${domain.icon}"></i></div>
          <h3 class="domain-title">${domain.title}</h3>
        </div>
        <div class="skill-tags-wrap">
          ${domain.skills.map(skill => `
            <button class="skill-tag" data-skill="${skill}" title="Click to filter projects using ${skill}">
              ${skill}
            </button>
          `).join('')}
        </div>
      </div>
    `).join('');

    // Add interactive filter on skill click
    container.querySelectorAll('.skill-tag').forEach(btn => {
      btn.addEventListener('click', () => {
        const skill = btn.getAttribute('data-skill');
        if (state.selectedSkill === skill) {
          state.selectedSkill = null;
          btn.classList.remove('active');
          state.searchQuery = '';
          document.getElementById('project-search-input').value = '';
        } else {
          container.querySelectorAll('.skill-tag').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          state.selectedSkill = skill;
          state.searchQuery = skill;
          document.getElementById('project-search-input').value = skill;
        }
        renderProjects();
        // Scroll smoothly to projects section
        const projSec = document.getElementById('projects');
        if (projSec) projSec.scrollIntoView({ behavior: 'smooth' });
      });
    });
  }

  /* ==========================================================================
     4.1 Startup Experience & Soft Skills Section
     ========================================================================== */
  function initStartupLearnings() {
    const container = document.getElementById('startup-learnings-container');
    if (!container || !state.startupLearnings) return;

    container.innerHTML = state.startupLearnings.map(item => `
      <div class="startup-card">
        <div>
          <div class="startup-card-top">
            <div class="startup-icon-wrap"><i class="fa-solid ${item.icon}"></i></div>
            <span class="badge badge-sub">${item.tag}</span>
          </div>
          <h3 class="startup-title">${item.title}</h3>
          <p class="startup-desc">${item.description}</p>
        </div>
      </div>
    `).join('');
  }

  /* ==========================================================================
     5. Category Filters & Project Search
     ========================================================================== */
  function initCategoryFilters() {
    const container = document.getElementById('category-filters-container');
    if (!container) return;

    container.innerHTML = state.categories.map(cat => `
      <button class="filter-btn ${cat.id === state.activeCategory ? 'active' : ''}" data-category="${cat.id}">
        ${cat.icon ? `<i class="fa-solid fa-${cat.icon}"></i>` : ''}
        ${cat.label}
      </button>
    `).join('');

    container.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.activeCategory = btn.getAttribute('data-category');
        renderProjects();
      });
    });

    const resetBtn = document.getElementById('reset-filter-btn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        state.activeCategory = 'all';
        state.searchQuery = '';
        state.selectedSkill = null;
        document.getElementById('project-search-input').value = '';
        document.querySelectorAll('.skill-tag').forEach(b => b.classList.remove('active'));
        container.querySelectorAll('.filter-btn').forEach(b => {
          b.classList.toggle('active', b.getAttribute('data-category') === 'all');
        });
        renderProjects();
      });
    }
  }

  function initProjectSearch() {
    const input = document.getElementById('project-search-input');
    const clearBtn = document.getElementById('search-clear-btn');
    if (!input) return;

    input.addEventListener('input', (e) => {
      state.searchQuery = e.target.value.trim().toLowerCase();
      if (clearBtn) {
        clearBtn.style.display = state.searchQuery ? 'block' : 'none';
      }
      renderProjects();
    });

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        input.value = '';
        state.searchQuery = '';
        clearBtn.style.display = 'none';
        renderProjects();
      });
    }
  }

  /* ==========================================================================
     6. Render Projects Grid
     ========================================================================== */
  function renderProjects() {
    const container = document.getElementById('projects-grid-container');
    const countText = document.getElementById('results-count-text');
    const resetBtn = document.getElementById('reset-filter-btn');
    if (!container) return;

    // Filter projects
    const filtered = state.projects.filter(project => {
      // Category check
      const matchesCategory = state.activeCategory === 'all' || project.category === state.activeCategory;
      if (!matchesCategory) return false;

      // Search query check
      if (state.searchQuery) {
        const query = state.searchQuery.toLowerCase();
        const searchable = [
          project.title,
          project.shortSummary,
          project.fullDescription,
          project.impact,
          ...(project.techStack || []),
          ...(project.highlights || [])
        ].join(' ').toLowerCase();

        return searchable.includes(query);
      }

      return true;
    });

    // Update Results Bar
    if (countText) {
      countText.textContent = `Showing ${filtered.length} of ${state.projects.length} projects ${state.searchQuery ? `for "${state.searchQuery}"` : ''}`;
    }
    if (resetBtn) {
      if (state.activeCategory !== 'all' || state.searchQuery) {
        resetBtn.classList.remove('hidden');
      } else {
        resetBtn.classList.add('hidden');
      }
    }

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px;">
          <div style="font-size: 3rem; color: var(--text-muted); margin-bottom: 16px;"><i class="fa-solid fa-folder-open"></i></div>
          <h3 style="font-size: 1.3rem; margin-bottom: 8px;">No projects matched your criteria</h3>
          <p style="color: var(--text-muted); margin-bottom: 20px;">Try searching for a different keyword like "YOLO", "RAG", "FastAPI", or "OpenVINO".</p>
          <button class="btn btn-primary" onclick="document.getElementById('reset-filter-btn').click();">Reset Search</button>
        </div>
      `;
      return;
    }

    container.innerHTML = filtered.map(project => `
      <div class="project-card" data-id="${project.id}">
        <div>
          ${project.image ? `
            <div class="project-card-image-wrap">
              <img src="${project.image}" alt="${project.title}" class="project-card-image" loading="lazy" onerror="this.parentElement.style.display='none'">
            </div>
          ` : ''}

          <div class="project-card-header">
            <div class="project-card-badges">
              <span class="badge">${project.categoryLabel || project.category}</span>
              ${project.badge ? `<span class="badge badge-sub">${project.badge}</span>` : ''}
            </div>
          </div>

          <h3 class="project-card-title">${project.title}</h3>
          <div class="project-card-impact"><i class="fa-solid fa-sparkles"></i> ${project.impact}</div>
          <p class="project-card-desc">${project.shortSummary}</p>

          ${project.metrics && project.metrics.length > 0 ? `
            <div class="project-metrics-strip">
              ${project.metrics.slice(0, 2).map(m => `
                <div class="metric-item">
                  <span class="metric-val">${m.value}</span>
                  <span class="metric-lbl">${m.label}</span>
                </div>
              `).join('')}
            </div>
          ` : ''}

          <div class="project-tech-badges">
            ${(project.techStack || []).slice(0, 6).map(tech => `
              <span class="tech-chip">${tech}</span>
            `).join('')}
            ${(project.techStack || []).length > 6 ? `<span class="tech-chip">+${project.techStack.length - 6}</span>` : ''}
          </div>
        </div>

        <div class="project-card-footer">
          <button class="btn btn-sm btn-primary open-project-modal-btn" data-id="${project.id}">
            <i class="fa-solid fa-network-wired"></i> Deep Dive & Architecture
          </button>
        </div>
      </div>
    `).join('');

    // Attach click listeners to cards
    container.querySelectorAll('.open-project-modal-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-id');
        openProjectModal(id);
      });
    });
  }

  /* ==========================================================================
     7. Project Deep Dive Modal
     ========================================================================== */
  function openProjectModal(projectId) {
    const project = state.projects.find(p => p.id === projectId);
    if (!project) return;

    const modal = document.getElementById('project-modal');
    const catBadge = document.getElementById('modal-category-badge');
    const tagBadge = document.getElementById('modal-badge-tag');
    const body = document.getElementById('modal-body-content');

    if (catBadge) catBadge.textContent = project.categoryLabel || project.category;
    if (tagBadge) tagBadge.textContent = project.badge || 'Deep Dive';

    body.innerHTML = `
      <div>
        <h2 class="modal-project-title">${project.title}</h2>
        <p class="modal-project-impact" style="margin-top: 6px;"><i class="fa-solid fa-bolt"></i> ${project.impact}</p>
      </div>

      ${project.image ? `
        <div>
          <img src="${project.image}" alt="${project.title}" class="modal-image-preview">
        </div>
      ` : ''}

      <div>
        <h4 class="modal-section-title"><i class="fa-solid fa-align-left"></i> Overview & Implementation Summary</h4>
        <p style="color: var(--text-secondary); line-height: 1.7;">${project.fullDescription}</p>
      </div>

      ${project.architecture ? `
        <div>
          <h4 class="modal-section-title"><i class="fa-solid fa-diagram-project"></i> System Architecture & Data Flow</h4>
          <div class="modal-architecture-box">
            <pre><code>${project.architecture.trim()}</code></pre>
          </div>
        </div>
      ` : ''}

      ${project.metrics && project.metrics.length > 0 ? `
        <div>
          <h4 class="modal-section-title"><i class="fa-solid fa-chart-line"></i> Validated Benchmarks & Metrics</h4>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px;">
            ${project.metrics.map(m => `
              <div style="background: var(--bg-tertiary); padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
                <div style="font-size: 1.4rem; font-weight: 800; color: var(--accent-cyan); font-family: 'JetBrains Mono';">${m.value}</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-primary); margin-top: 2px;">${m.label}</div>
                <div style="font-size: 0.75rem; color: var(--text-muted);">${m.sub}</div>
              </div>
            `).join('')}
          </div>
        </div>
      ` : ''}

      ${project.innovations && project.innovations.length > 0 ? `
        <div>
          <h4 class="modal-section-title"><i class="fa-solid fa-lightbulb"></i> Engineering Notes & Key Solutions</h4>
          <ul class="modal-innovations-list">
            ${project.innovations.map(inn => `
              <li>${inn.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</li>
            `).join('')}
          </ul>
        </div>
      ` : ''}

      ${project.codeSnippet ? `
        <div>
          <h4 class="modal-section-title"><i class="fa-solid fa-code"></i> Implementation Code Highlight</h4>
          <div class="code-viewer-container">
            <div class="code-viewer-header">
              <span class="code-title"><i class="fa-solid fa-file-code"></i> ${project.codeSnippet.title}</span>
              <button class="copy-code-btn" id="modal-copy-code-btn">
                <i class="fa-solid fa-copy"></i> Copy Code
              </button>
            </div>
            <div class="code-block-content">
              <pre><code>${escapeHtml(project.codeSnippet.code.trim())}</code></pre>
            </div>
          </div>
        </div>
      ` : ''}

      <div>
        <h4 class="modal-section-title"><i class="fa-solid fa-cubes"></i> Technologies Used</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          ${(project.techStack || []).map(t => `
            <span class="skill-tag" style="cursor: default;">${t}</span>
          `).join('')}
        </div>
      </div>
    `;

    // Hook code copy button
    const copyBtn = document.getElementById('modal-copy-code-btn');
    if (copyBtn && project.codeSnippet) {
      copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(project.codeSnippet.code);
        showToast('Code snippet copied to clipboard!');
      });
    }

    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  /* ==========================================================================
     8. Experience Timeline
     ========================================================================== */
  function initExperienceTimeline() {
    const container = document.getElementById('experience-timeline-container');
    if (!container || !state.resume?.experience) return;

    container.innerHTML = state.resume.experience.map(exp => `
      <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-card">
          <div class="timeline-header">
            <div>
              <h3 class="timeline-role">${exp.role}</h3>
              <div class="timeline-company">${exp.company} · <span style="color: var(--text-muted); font-size: 0.9rem;">${exp.location}</span></div>
            </div>
            <span class="timeline-period">${exp.period}</span>
          </div>
          <ul class="timeline-achievements">
            ${exp.achievements.map(ach => `
              <li>${ach.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</li>
            `).join('')}
          </ul>
        </div>
      </div>
    `).join('');
  }

  /* ==========================================================================
     9. Education & Competitions
     ========================================================================== */
  function initEducation() {
    const container = document.getElementById('education-grid-container');
    if (!container) return;

    const eduItems = state.resume?.education || [];
    const compItems = state.resume?.competitions || [];

    const eduHtml = eduItems.map(edu => `
      <div class="edu-card">
        <div class="edu-icon-wrap"><i class="fa-solid fa-graduation-cap"></i></div>
        <h3 class="edu-title">${edu.degree}</h3>
        <div class="edu-institution">${edu.institution}</div>
        <div class="edu-period">${edu.period}</div>
        ${edu.coursework ? `
          <div style="font-size: 0.82rem; font-weight: 600; color: var(--text-muted); margin-top: 10px;">Relevant Coursework:</div>
          <div class="coursework-list">
            ${edu.coursework.map(c => `<span class="course-badge">${c}</span>`).join('')}
          </div>
        ` : ''}
      </div>
    `).join('');

    const compHtml = compItems.map(comp => `
      <div class="edu-card">
        <div class="edu-icon-wrap" style="background: rgba(16, 185, 129, 0.12); color: var(--accent-emerald);">
          <i class="fa-solid fa-trophy"></i>
        </div>
        <h3 class="edu-title">${comp.name}</h3>
        <div class="edu-institution" style="color: var(--accent-emerald);">${comp.role}</div>
        <p style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 8px;">${comp.description}</p>
      </div>
    `).join('');

    container.innerHTML = eduHtml + compHtml;
  }

  /* ==========================================================================
     10. Modals Management (Project & Resume)
     ========================================================================== */
  function initModals() {
    const projectModal = document.getElementById('project-modal');
    const projectCloseBtn = document.getElementById('modal-close-btn');
    const resumeModal = document.getElementById('resume-modal');
    const resumeCloseBtn = document.getElementById('resume-modal-close-btn');
    const openResumeBtn = document.getElementById('open-resume-modal-btn');

    function closeModal(modal) {
      if (!modal) return;
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    if (projectCloseBtn) {
      projectCloseBtn.addEventListener('click', () => closeModal(projectModal));
    }
    if (resumeCloseBtn) {
      resumeCloseBtn.addEventListener('click', () => closeModal(resumeModal));
    }

    [projectModal, resumeModal].forEach(m => {
      if (m) {
        m.addEventListener('click', (e) => {
          if (e.target === m) closeModal(m);
        });
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeModal(projectModal);
        closeModal(resumeModal);
      }
    });

    if (openResumeBtn && resumeModal) {
      openResumeBtn.addEventListener('click', () => {
        renderResumeContent();
        resumeModal.classList.add('active');
        resumeModal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
      });
    }
  }

  function renderResumeContent() {
    const body = document.getElementById('resume-modal-body');
    if (!body || !state.resume) return;

    const r = state.resume;
    body.innerHTML = `
      <div class="resume-paper">
        <div class="resume-header-block">
          <h2>${r.name}</h2>
          <div class="resume-role">${r.headline || r.title}</div>
          <div class="resume-meta-links">
            <span><i class="fa-solid fa-phone"></i> ${r.contact.phone}</span>
            <span><i class="fa-solid fa-envelope"></i> ${r.contact.email}</span>
            <span><i class="fa-brands fa-linkedin"></i> linkedin.com/in/kwankhao-sivasomboon</span>
            <span><i class="fa-brands fa-github"></i> github.com/Kwankhao-Sivasomboon</span>
          </div>
        </div>

        <div>
          <h3 style="font-size: 1.1rem; border-bottom: 2px solid var(--border-color); padding-bottom: 6px; margin-bottom: 12px; color: var(--accent-cyan);">
            PROFESSIONAL SUMMARY
          </h3>
          <p style="font-size: 0.95rem; line-height: 1.6; color: var(--text-secondary);">${r.summary}</p>
        </div>

        <div>
          <h3 style="font-size: 1.1rem; border-bottom: 2px solid var(--border-color); padding-bottom: 6px; margin-bottom: 12px; color: var(--accent-cyan);">
            TECHNICAL SKILLS
          </h3>
          <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.9rem;">
            <div><strong>Programming & Data:</strong> ${(r.skills.programming || []).join(', ')}</div>
            <div><strong>AI/ML & Computer Vision:</strong> ${(r.skills.computer_vision || []).join(', ')}</div>
            <div><strong>GenAI & Retrieval (RAG):</strong> ${(r.skills.genai_rag || []).join(', ')}</div>
            <div><strong>Backend, Cloud & DevOps:</strong> ${(r.skills.backend_cloud || []).join(', ')}</div>
          </div>
        </div>

        <div>
          <h3 style="font-size: 1.1rem; border-bottom: 2px solid var(--border-color); padding-bottom: 6px; margin-bottom: 12px; color: var(--accent-cyan);">
            WORK EXPERIENCE
          </h3>
          <div style="display: flex; flex-direction: column; gap: 20px;">
            ${(r.experience || []).map(exp => `
              <div>
                <div style="display: flex; justify-content: space-between; font-weight: 700;">
                  <span>${exp.company} | ${exp.role}</span>
                  <span style="color: var(--text-muted);">${exp.period}</span>
                </div>
                <ul style="padding-left: 20px; margin-top: 8px; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6;">
                  ${exp.achievements.map(a => `<li>${a.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</li>`).join('')}
                </ul>
              </div>
            `).join('')}
          </div>
        </div>

        <div>
          <h3 style="font-size: 1.1rem; border-bottom: 2px solid var(--border-color); padding-bottom: 6px; margin-bottom: 12px; color: var(--accent-cyan);">
            EDUCATION
          </h3>
          ${(r.education || []).map(edu => `
            <div>
              <div style="display: flex; justify-content: space-between; font-weight: 700;">
                <span>${edu.institution}</span>
                <span style="color: var(--text-muted);">${edu.period}</span>
              </div>
              <div style="color: var(--accent-cyan); font-size: 0.9rem;">${edu.degree}</div>
              <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Relevant Coursework: ${(edu.coursework || []).join(', ')}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  /* ==========================================================================
     11. Animated Stat Counters
     ========================================================================== */
  function initCounters() {
    const counters = document.querySelectorAll('.counter');
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const counter = entry.target;
          const target = +counter.getAttribute('data-target');
          let count = 0;
          const step = Math.max(Math.floor(target / 40), 1);

          const updateCounter = () => {
            count += step;
            if (count < target) {
              counter.innerText = count;
              setTimeout(updateCounter, 30);
            } else {
              counter.innerText = target;
            }
          };
          updateCounter();
          obs.unobserve(counter);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
  }

  /* ==========================================================================
     12. Toast Feedback Notification
     ========================================================================== */
  window.showToast = function(message) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fa-solid fa-circle-check" style="color: var(--accent-emerald);"></i> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  };

  function escapeHtml(text) {
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
});
