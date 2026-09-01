/**
 * Kwankhao Sivasomboon - Junior AI Engineer Portfolio & Web CV
 * Interactive Application Engine (Zero-dependency Vanilla JS)
 */

document.addEventListener('DOMContentLoaded', () => {
  // Global App State
  const state = {
    theme: localStorage.getItem('theme') || 'dark',
    activeCategory: 'all',      // 'all' | 'cv-edge' | 'genai-rag' | etc.
    searchQuery: '',
    selectedSkill: null,
    projects: window.PORTFOLIO_DATA?.projects || [],
    companyProjects: window.PORTFOLIO_DATA?.companyProjects || [],
    personalProjects: window.PORTFOLIO_DATA?.personalProjects || [],
    resume: window.PORTFOLIO_DATA?.resume || {},
    categories: window.PORTFOLIO_DATA?.categories || [],
    startupLearnings: window.PORTFOLIO_DATA?.startupLearnings || []
  };

  // Init Components
  initTheme();
  initNeuralCanvas();
  initNavigation();
  initCollapsibleSections();
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

    // Auto-unfold collapsible section when clicking any anchor link
    document.querySelectorAll('a[href^="#"]').forEach(link => {
      link.addEventListener('click', (e) => {
        const hash = link.getAttribute('href');
        if (hash && hash.length > 1) {
          const targetId = hash.substring(1);
          window.openCollapsibleSection(targetId);
        }
      });
    });
  }

  /* ==========================================================================
     3.1 Collapsible Section Accordions (Folded by default)
     ========================================================================== */
  function initCollapsibleSections() {
    const sections = document.querySelectorAll('.collapsible-section');
    const expandAllBtn = document.getElementById('expand-all-btn');
    const collapseAllBtn = document.getElementById('collapse-all-btn');

    sections.forEach(section => {
      const header = section.querySelector('.collapsible-header');
      const toggleText = section.querySelector('.toggle-text');

      if (!header) return;

      header.addEventListener('click', () => {
        const isOpen = section.classList.toggle('is-open');
        header.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        if (toggleText) toggleText.textContent = isOpen ? 'Fold' : 'Expand';
      });

      // Keyboard accessibility (Enter or Space)
      header.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          header.click();
        }
      });
    });

    // Expand All Button
    if (expandAllBtn) {
      expandAllBtn.addEventListener('click', () => {
        sections.forEach(sec => {
          sec.classList.add('is-open');
          const header = sec.querySelector('.collapsible-header');
          const toggleText = sec.querySelector('.toggle-text');
          if (header) header.setAttribute('aria-expanded', 'true');
          if (toggleText) toggleText.textContent = 'Fold';
        });
        showToast('All sections expanded');
      });
    }

    // Collapse All Button
    if (collapseAllBtn) {
      collapseAllBtn.addEventListener('click', () => {
        sections.forEach(sec => {
          sec.classList.remove('is-open');
          const header = sec.querySelector('.collapsible-header');
          const toggleText = sec.querySelector('.toggle-text');
          if (header) header.setAttribute('aria-expanded', 'false');
          if (toggleText) toggleText.textContent = 'Expand';
        });
        showToast('All sections folded');
      });
    }
  }

  window.openCollapsibleSection = function(sectionId) {
    const sec = document.getElementById(sectionId);
    if (sec && sec.classList.contains('collapsible-section')) {
      sec.classList.add('is-open');
      const header = sec.querySelector('.collapsible-header');
      const toggleText = sec.querySelector('.toggle-text');
      if (header) header.setAttribute('aria-expanded', 'true');
      if (toggleText) toggleText.textContent = 'Fold';
    }
  };

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
        icon: 'fa-brain',
        skills: state.resume.skills.genai_rag
      },
      {
        key: 'backend_cloud',
        title: 'Backend, Cloud & Microservices',
        icon: 'fa-server',
        skills: state.resume.skills.backend_cloud
      },
      {
        key: 'data_automation',
        title: 'Automation & Testing',
        icon: 'fa-robot',
        skills: state.resume.skills.data_automation || state.resume.skills.qa_automation || []
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
          const clearBtn = document.getElementById('search-clear-btn');
          if (clearBtn) clearBtn.style.display = 'none';
        } else {
          container.querySelectorAll('.skill-tag').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          state.selectedSkill = skill;
          state.searchQuery = skill;
          
          // Auto-reset category to 'all' so skill search isn't blocked by previous category tab
          state.activeCategory = 'all';
          document.querySelectorAll('.filter-btn').forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-category') === 'all');
          });

          const input = document.getElementById('project-search-input');
          if (input) input.value = skill;
          const clearBtn = document.getElementById('search-clear-btn');
          if (clearBtn) clearBtn.style.display = 'block';
        }
        renderProjects();
        // Unfold and scroll smoothly to projects section
        window.openCollapsibleSection('projects');
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
        ${cat.icon ? `<i class="fa-solid ${cat.icon}"></i>` : ''}
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
     6. Smart Search Tokenizer & Render Projects
     ========================================================================== */
  function extractSearchTokens(rawQuery) {
    if (!rawQuery) return [];
    const normalized = rawQuery.toLowerCase().trim();

    // Map common multi-word skills to high-recall search triggers
    const aliasMap = {
      'groq whisper': ['whisper', 'groq', 'audio', 'speech'],
      'google gemini': ['gemini', 'vlm'],
      'hybrid rag': ['hybrid', 'rag', 'rrf', 'bm25'],
      'structured outputs': ['pydantic', 'schema', 'structured'],
      'llm evaluation': ['evaluation', 'judge', 'eval'],
      'reciprocal rank fusion (rrf)': ['reciprocal', 'rrf', 'bm25', 'fusion'],
      'ctc loss': ['ctc'],
      'resnet-crnn': ['crnn', 'resnet'],
      'yolo11-pose': ['yolo', 'pose'],
      'openvino (fp16)': ['openvino'],
      'insightface / arcface': ['insightface', 'arcface'],
      'contour analysis': ['contour', 'crack'],
      'satellite remote sensing (ndvi / evi)': ['satellite', 'remote sensing', 'ndvi', 'spectral', 'crop'],
      'drone aerial imagery': ['drone', 'aerial', 'crack'],
      'lidar analysis': ['lidar', 'geospatial'],
      'three.js 3d web': ['three.js', '3d', 'room'],
      'open3d / trimesh': ['open3d', 'trimesh', 'mesh', '3d'],
      'esp32 ble iot': ['esp32', 'raspberry pi', 'iot']
    };

    if (aliasMap[normalized]) {
      return aliasMap[normalized];
    }

    // Default: split punctuation and parentheses
    return normalized
      .replace(/[()\/,+&._-]/g, ' ')
      .split(/\s+/)
      .filter(token => token.length > 1 && !['1.5', '2.5', 'fp16', 'v11', 'v8'].includes(token));
  }

  function renderProjects() {
    const companyGrid = document.getElementById('company-projects-grid');
    const personalGrid = document.getElementById('personal-projects-grid');
    const companyPart = document.getElementById('company-projects-part');
    const personalPart = document.getElementById('personal-projects-part');
    const partDivider = document.getElementById('projects-part-divider');
    const countText = document.getElementById('results-count-text');
    const resetBtn = document.getElementById('reset-filter-btn');

    if (!companyGrid || !personalGrid) return;

    const queryTokens = extractSearchTokens(state.searchQuery);

    // Filter helper
    const filterItem = (project) => {
      // 1. Category Filter
      if (state.activeCategory !== 'all' && project.category !== state.activeCategory) {
        return false;
      }

      // 2. Search / Skill Query Token Matching
      if (queryTokens.length > 0) {
        const searchableText = [
          project.title,
          project.shortSummary,
          project.fullDescription,
          project.impact,
          project.typeLabel || '',
          project.companyName || '',
          ...(project.techStack || []),
          ...(project.highlights || []),
          ...(project.innovations || [])
        ].join(' ').toLowerCase();

        // Check if ANY meaningful token from the search query matches the project
        const hasTokenMatch = queryTokens.some(token => searchableText.includes(token));
        if (!hasTokenMatch) return false;
      }

      return true;
    };

    const filteredCompany = state.companyProjects.filter(filterItem);
    const filteredPersonal = state.personalProjects.filter(filterItem);
    const totalShown = filteredCompany.length + filteredPersonal.length;

    // Update Results Bar
    if (countText) {
      countText.textContent = `Showing ${totalShown} of ${state.projects.length} projects (${filteredCompany.length} Industry, ${filteredPersonal.length} Independent) ${state.searchQuery ? `for "${state.searchQuery}"` : ''}`;
    }

    if (resetBtn) {
      if (state.activeCategory !== 'all' || state.searchQuery) {
        resetBtn.classList.remove('hidden');
      } else {
        resetBtn.classList.add('hidden');
      }
    }

    // Render Section 1: Company / Industry Projects (Top Priority)
    if (filteredCompany.length > 0) {
      companyPart.style.display = 'block';
      companyGrid.innerHTML = filteredCompany.map(project => renderCardHTML(project, false)).join('');
    } else {
      if (filteredPersonal.length > 0) {
        companyPart.style.display = 'none';
      } else {
        companyPart.style.display = 'block';
        companyGrid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; padding: 40px 20px;">
            <div style="font-size: 2rem; color: var(--text-muted); margin-bottom: 10px;"><i class="fa-solid fa-building"></i></div>
            <p style="color: var(--text-muted);">No industry systems matched the selected filter.</p>
          </div>
        `;
      }
    }

    // Render Section 2: Personal / Independent Projects
    if (filteredPersonal.length > 0) {
      personalPart.style.display = 'block';
      personalGrid.innerHTML = filteredPersonal.map(project => renderCardHTML(project, true)).join('');
    } else {
      if (filteredCompany.length > 0) {
        personalPart.style.display = 'none';
      } else {
        personalPart.style.display = 'block';
        personalGrid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; padding: 40px 20px;">
            <div style="font-size: 2rem; color: var(--text-muted); margin-bottom: 10px;"><i class="fa-solid fa-flask"></i></div>
            <p style="color: var(--text-muted);">No independent research projects matched the selected filter.</p>
          </div>
        `;
      }
    }

    // Divider visibility
    if (partDivider) {
      partDivider.style.display = (filteredCompany.length > 0 && filteredPersonal.length > 0) ? 'flex' : 'none';
    }

    // Attach click listeners to cards
    document.querySelectorAll('.open-project-modal-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-id');
        openProjectModal(id);
      });
    });
  }

  function renderCardHTML(project, isPersonal) {
    const badgeClass = isPersonal ? 'badge-personal' : 'badge-company';
    const badgeIcon = isPersonal ? 'fa-flask' : 'fa-briefcase';
    const badgeText = isPersonal ? 'Independent Project' : (project.companyName || 'Industry Experience');

    return `
      <div class="project-card ${isPersonal ? 'personal-card' : 'company-card'}" data-id="${project.id}">
        <div>
          <div class="project-card-header">
            <div class="project-card-badges">
              <span class="badge ${badgeClass}"><i class="fa-solid ${badgeIcon}"></i> ${badgeText}</span>
              <span class="badge">${project.categoryLabel || project.category}</span>
            </div>
          </div>

          <h3 class="project-card-title">${project.title}</h3>
          <div class="project-card-impact"><i class="fa-solid fa-code-commit"></i> ${project.impact}</div>
          
          ${project.image ? `
            <div style="position: relative; width: 100%; height: 160px; border-radius: var(--radius-md); overflow: hidden; margin-bottom: 14px; border: 1px solid var(--border-color);">
              <img src="${project.image}" alt="${project.title}" style="width: 100%; height: 100%; object-fit: cover; display: block;" loading="lazy">
            </div>
          ` : ''}

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
          <button class="btn btn-sm ${isPersonal ? 'btn-primary' : 'btn-secondary'} open-project-modal-btn" data-id="${project.id}">
            ${isPersonal ? '<i class="fa-solid fa-code"></i> Deep Dive & Code' : '<i class="fa-solid fa-layer-group"></i> System Overview'}
          </button>
        </div>
      </div>
    `;
  }

  /* ==========================================================================
     7. Project Deep Dive & System Overview Modal
     ========================================================================== */
  function openProjectModal(projectId) {
    const project = state.projects.find(p => p.id === projectId);
    if (!project) return;

    const modal = document.getElementById('project-modal');
    const catBadge = document.getElementById('modal-category-badge');
    const tagBadge = document.getElementById('modal-badge-tag');
    const body = document.getElementById('modal-body-content');
    const isPersonal = project.type === 'personal';

    if (catBadge) catBadge.textContent = project.categoryLabel || project.category;
    if (tagBadge) tagBadge.textContent = isPersonal ? 'Independent Deep Dive' : (project.companyName || 'Industry Experience');

    body.innerHTML = `
      <div>
        <div style="margin-bottom: 8px;">
          <span class="badge ${isPersonal ? 'badge-personal' : 'badge-company'}">
            <i class="fa-solid ${isPersonal ? 'fa-flask' : 'fa-briefcase'}"></i>
            ${isPersonal ? 'Independent Project (Source Code & Architecture Open)' : `Production System · ${project.companyName || 'Yourhome'}`}
          </span>
        </div>
        <h2 class="modal-project-title">${project.title}</h2>
        <p class="modal-project-impact" style="margin-top: 6px;"><i class="fa-solid fa-bolt"></i> ${project.impact}</p>
      </div>

      ${project.image ? `
        <div style="position: relative; width: 100%; border-radius: var(--radius-md); overflow: hidden; border: 1px solid var(--border-color); background: #050811;">
          <img src="${project.image}" alt="${project.title}" style="width: 100%; max-height: 300px; object-fit: contain; display: block; margin: 0 auto;">
        </div>
      ` : ''}

      <div>
        <h4 class="modal-section-title"><i class="fa-solid fa-align-left"></i> ${isPersonal ? 'Project Overview' : 'System Overview & Engineering Role'}</h4>
        <p style="color: var(--text-secondary); line-height: 1.7;">${project.fullDescription}</p>
      </div>

      ${project.highlights && project.highlights.length > 0 ? `
        <div>
          <h4 class="modal-section-title"><i class="fa-solid fa-list-check"></i> Key Engineering Highlights</h4>
          <ul class="modal-innovations-list">
            ${project.highlights.map(h => `
              <li>${h.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</li>
            `).join('')}
          </ul>
        </div>
      ` : ''}

      ${project.architecture ? `
        <div>
          <h4 class="modal-section-title"><i class="fa-solid fa-diagram-project"></i> System Architecture & Pipeline</h4>
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
        <h4 class="modal-section-title"><i class="fa-solid fa-cubes"></i> Technologies & Libraries</h4>
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

    container.innerHTML = state.resume.experience.map((exp, idx) => `
      <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-card ${idx === 0 ? 'expanded' : ''}" data-idx="${idx}">
          <div class="timeline-header" style="cursor: pointer;" title="Click to expand/collapse achievements">
            <div>
              <h3 class="timeline-role">${exp.role}</h3>
              <div class="timeline-company">${exp.company} · <span style="color: var(--text-muted); font-size: 0.9rem;">${exp.location}</span></div>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
              <span class="timeline-period">${exp.period}</span>
              <span class="timeline-toggle-icon" style="color: var(--accent-cyan); font-size: 0.85rem;">
                <i class="fa-solid fa-chevron-${idx === 0 ? 'up' : 'down'}"></i>
              </span>
            </div>
          </div>
          <ul class="timeline-achievements" style="display: ${idx === 0 ? 'flex' : 'none'};">
            ${exp.achievements.map(ach => `
              <li>${ach.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</li>
            `).join('')}
          </ul>
        </div>
      </div>
    `).join('');

    // Attach click listener to toggle achievements
    container.querySelectorAll('.timeline-card').forEach(card => {
      const header = card.querySelector('.timeline-header');
      const list = card.querySelector('.timeline-achievements');
      const icon = card.querySelector('.timeline-toggle-icon i');

      header.addEventListener('click', () => {
        const isClosed = list.style.display === 'none';
        list.style.display = isClosed ? 'flex' : 'none';
        icon.className = isClosed ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down';
        card.classList.toggle('expanded', isClosed);
      });
    });
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
