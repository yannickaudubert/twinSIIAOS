(() => {
  'use strict';

  const app = {
    projection: { schema: 'siiaos.radar-public.v1', generatedAt: '', items: [] },
    fixtureMode: new URLSearchParams(window.location.search).get('fixture') === '1',
    activeView: 'radar',
  };

  const labels = {
    radar: 'Radar',
    capabilities: 'Capacités',
    approaches: 'Approches',
    landscapes: 'Paysages',
    watch: 'Hyperveille',
    acquire: 'Acquérir',
    method: 'Méthode',
    'expert-fit': 'Expert / Fit',
    'expert-compare': 'Expert / Comparateur',
    'expert-evidence': 'Expert / Evidence',
    'expert-architecture': 'Expert / Architecture',
    'expert-decisions': 'Expert / Décisions',
  };

  const landscapeDefinitions = [
    {
      code: 'L01',
      title: 'Serving et runtimes IA',
      description: 'Distinguer runtime local, serveur GPU, gateway et couche de compatibilité API.',
      options: [
        ['Local interactif', 'Priorité à la simplicité, au packaging et aux formats quantifiés.'],
        ['Serving GPU', 'Priorité au batching, débit, parallélisme et observabilité.'],
        ['Gateway', 'Priorité au routage, politiques, quotas, coûts et compatibilité fournisseurs.'],
      ],
    },
    {
      code: 'L02',
      title: 'RAG, retrieval et contexte',
      description: 'Ne pas comparer directement une base vectorielle, un framework de retrieval et un agent documentaire.',
      options: [
        ['Stockage vectoriel', 'Index, filtres, recherche hybride, réplication et exploitation.'],
        ['Retrieval / contexte', 'Pipelines, routing, memory, ingestion et orchestration.'],
        ['Document agents', 'Parsing, OCR, compréhension documentaire et boucles agentiques.'],
      ],
    },
    {
      code: 'L03',
      title: 'Agents et workflows durables',
      description: 'Séparer builder low-code, framework agentique et moteur de durable execution.',
      options: [
        ['Builder', 'Assemblage rapide, connecteurs, UX de workflow.'],
        ['Framework agentique', 'Contrôle code-first, états, outils, mémoire, graphe.'],
        ['Durable execution', 'Reprise après erreur, états longs, garanties d’exécution.'],
      ],
    },
    {
      code: 'L04',
      title: 'Observabilité et évaluation IA',
      description: 'Tracer, évaluer, red-teamer et gouverner les changements ne relèvent pas du même outil.',
      options: [
        ['Runtime traces', 'Latence, tokens, coûts, spans et erreurs.'],
        ['Evaluation', 'Datasets, métriques, évaluateurs et expériences.'],
        ['Red team / CI gates', 'Tests adversariaux et contrôle avant promotion.'],
      ],
    },
  ];

  function escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function normalizeState(value) {
    const known = ['observed', 'candidate', 'installed', 'tested', 'qualified', 'target', 'deprecated', 'retired'];
    return known.includes(value) ? value : 'observed';
  }

  function stateLabel(value) {
    const map = {
      observed: 'Observé',
      candidate: 'Candidat',
      installed: 'Installé',
      tested: 'Testé',
      qualified: 'Qualifié',
      target: 'Cible',
      deprecated: 'Déprécié',
      retired: 'Retiré',
    };
    return map[value] || 'Observé';
  }

  function kindLabel(value) {
    const map = {
      system: 'Système',
      model: 'Modèle',
      approach: 'Approche',
      agent: 'Agent',
      runtime: 'Runtime',
      source: 'Source',
      dataset: 'Dataset',
      service: 'Service',
      tool: 'Outil',
      database: 'Base de données',
      framework: 'Framework',
      platform: 'Plateforme',
      application: 'Application',
    };
    return map[value] || value || 'Ressource';
  }

  function formatDate(value) {
    if (!value) return '—';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return String(value).slice(0, 10);
    return new Intl.DateTimeFormat('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' }).format(date);
  }

  function trendValue(item) {
    const raw = item?.trend?.delta_30d;
    return typeof raw === 'number' ? raw : null;
  }

  function trendMarkup(item) {
    const value = trendValue(item);
    if (value === null) return '<span class="trend-neutral">—</span>';
    const className = value > 0 ? 'trend-positive' : value < 0 ? 'trend-negative' : 'trend-neutral';
    const sign = value > 0 ? '+' : '';
    return `<span class="${className}">${sign}${escapeHtml(value)}</span>`;
  }

  function evidenceCount(item) {
    const ids = Array.isArray(item.evidence_ids) ? item.evidence_ids.length : 0;
    return ids + (item.benchmark_summary ? 1 : 0);
  }

  function gapCount(item) {
    return Array.isArray(item.known_gaps) ? item.known_gaps.length : 0;
  }

  async function loadProjection() {
    const source = app.fixtureMode ? './fixtures/radar-public.demo.json' : '../projections/radar-public.json';
    try {
      const response = await fetch(source, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (!data || data.schema !== 'siiaos.radar-public.v1' || !Array.isArray(data.items)) {
        throw new Error('Projection incompatible');
      }
      app.projection = data;
      document.getElementById('projection-dot')?.classList.add('ok');
      document.getElementById('projection-status').textContent = app.fixtureMode ? 'Fixture de revue chargée' : 'Projection publique chargée';
    } catch (error) {
      console.warn('Radar projection unavailable:', error);
      document.getElementById('projection-status').textContent = 'Projection vide';
    }

    const demoBanner = document.getElementById('demo-banner');
    if (demoBanner) demoBanner.hidden = !app.fixtureMode;
    renderAll();
  }

  function renderMetrics(items) {
    const candidates = items.filter((item) => ['observed', 'candidate'].includes(normalizeState(item.state))).length;
    const evidence = items.reduce((sum, item) => sum + evidenceCount(item), 0);
    const gaps = items.reduce((sum, item) => sum + gapCount(item), 0);
    document.getElementById('metric-resources').textContent = String(items.length);
    document.getElementById('metric-candidates').textContent = String(candidates);
    document.getElementById('metric-evidence').textContent = String(evidence);
    document.getElementById('metric-gaps').textContent = String(gaps);
  }

  function currentFilteredItems() {
    const q = (document.getElementById('radar-search')?.value || '').trim().toLowerCase();
    const state = document.getElementById('state-filter')?.value || '';
    const kind = document.getElementById('kind-filter')?.value || '';
    return app.projection.items.filter((item) => {
      const haystack = [
        item.title,
        item.summary,
        item.kind,
        ...(Array.isArray(item.capabilities) ? item.capabilities : []),
        ...(Array.isArray(item.approaches) ? item.approaches : []),
      ].filter(Boolean).join(' ').toLowerCase();
      return (!q || haystack.includes(q)) && (!state || normalizeState(item.state) === state) && (!kind || item.kind === kind);
    });
  }

  function renderKindOptions(items) {
    const select = document.getElementById('kind-filter');
    if (!select) return;
    const previous = select.value;
    const kinds = [...new Set(items.map((item) => item.kind).filter(Boolean))].sort();
    select.innerHTML = '<option value="">Tous</option>' + kinds.map((kind) => `<option value="${escapeHtml(kind)}">${escapeHtml(kindLabel(kind))}</option>`).join('');
    if (kinds.includes(previous)) select.value = previous;
  }

  function renderTable() {
    const items = currentFilteredItems();
    const tbody = document.getElementById('resource-table-body');
    const empty = document.getElementById('resource-empty');
    const count = document.getElementById('result-count');
    if (!tbody || !empty || !count) return;

    count.textContent = `${items.length} ressource${items.length > 1 ? 's' : ''}`;
    tbody.innerHTML = items.map((item) => {
      const state = normalizeState(item.state);
      const capabilities = Array.isArray(item.capabilities) ? item.capabilities : [];
      const role = capabilities[0] || kindLabel(item.kind);
      return `<tr data-resource-id="${escapeHtml(item.id)}" tabindex="0">
        <td><div class="resource-name"><strong>${escapeHtml(item.title || item.id)}</strong><small>${escapeHtml(item.summary || item.source_url || '')}</small></div></td>
        <td>${escapeHtml(role)}</td>
        <td><span class="pill ${escapeHtml(state)}">${escapeHtml(stateLabel(state))}</span></td>
        <td>${trendMarkup(item)}</td>
        <td>${escapeHtml(formatDate(item.last_verified_at || item.updated_at || item.last_activity))}</td>
      </tr>`;
    }).join('');
    empty.hidden = items.length > 0;
  }

  function renderCapabilities(items) {
    const board = document.getElementById('capability-board');
    if (!board) return;
    const counter = new Map();
    items.forEach((item) => {
      (Array.isArray(item.capabilities) ? item.capabilities : []).forEach((capability) => {
        const bucket = counter.get(capability) || { count: 0, states: new Set(), kinds: new Set() };
        bucket.count += 1;
        bucket.states.add(normalizeState(item.state));
        bucket.kinds.add(kindLabel(item.kind));
        counter.set(capability, bucket);
      });
    });
    const entries = [...counter.entries()].sort((a, b) => b[1].count - a[1].count);
    if (!entries.length) {
      board.innerHTML = '<div class="empty-state"><strong>Aucune capacité publiée.</strong><span>La vue se remplira à partir de la projection publique versionnée.</span></div>';
      return;
    }
    board.innerHTML = entries.map(([name, meta]) => `<article class="capability-card">
      <div class="eyebrow">Capacité</div>
      <h2>${escapeHtml(name)}</h2>
      <p>${meta.count} ressource${meta.count > 1 ? 's' : ''} actuellement reliée${meta.count > 1 ? 's' : ''} à cette capacité dans la projection.</p>
      <footer><span>${escapeHtml([...meta.kinds].slice(0, 3).join(' · '))}</span><span>états : ${escapeHtml([...meta.states].join(', '))}</span></footer>
    </article>`).join('');
  }

  function renderLandscapes() {
    const target = document.getElementById('landscape-detail-grid');
    if (!target) return;
    target.innerHTML = landscapeDefinitions.map((landscape) => `<article class="landscape-detail">
      <div>
        <div class="eyebrow">${escapeHtml(landscape.code)}</div>
        <h2>${escapeHtml(landscape.title)}</h2>
        <p>${escapeHtml(landscape.description)}</p>
      </div>
      <div class="landscape-options">
        ${landscape.options.map(([title, note]) => `<div class="landscape-option"><strong>${escapeHtml(title)}</strong><small>${escapeHtml(note)}</small></div>`).join('')}
      </div>
    </article>`).join('');
  }

  function renderWatch(items) {
    const target = document.getElementById('watch-timeline');
    if (!target) return;
    const sorted = [...items].sort((a, b) => String(b.updated_at || b.last_verified_at || b.last_activity || '').localeCompare(String(a.updated_at || a.last_verified_at || a.last_activity || ''))).slice(0, 12);
    if (!sorted.length) {
      target.innerHTML = '<div class="empty-state"><strong>Aucun signal public.</strong><span>L’Hyperveille reste vide tant qu’aucune observation versionnée n’est projetée.</span></div>';
      return;
    }
    target.innerHTML = sorted.map((item) => {
      const state = normalizeState(item.state);
      const position = item.competitive_position && item.competitive_position !== 'unknown' ? item.competitive_position : 'non classé';
      return `<article class="timeline-item">
        <div class="timeline-meta"><span>${escapeHtml(formatDate(item.updated_at || item.last_verified_at || item.last_activity))}</span><span>${escapeHtml(kindLabel(item.kind))}</span><span>${escapeHtml(stateLabel(state))}</span><span>${escapeHtml(position)}</span></div>
        <h2>${escapeHtml(item.title || item.id)}</h2>
        <p>${escapeHtml(item.summary || 'Observation publiée sans commentaire éditorial supplémentaire.')}</p>
      </article>`;
    }).join('');
  }

  function updateFreshness() {
    const target = document.getElementById('freshness-label');
    if (!target) return;
    if (!app.projection.generatedAt) {
      target.textContent = app.fixtureMode ? 'Fixture de démonstration' : 'Projection vide';
      return;
    }
    target.textContent = `${app.fixtureMode ? 'Fixture' : 'Projection'} · ${formatDate(app.projection.generatedAt)}`;
  }

  function renderAll() {
    const items = app.projection.items || [];
    renderKindOptions(items);
    renderMetrics(items);
    renderTable();
    renderCapabilities(items);
    renderLandscapes();
    renderWatch(items);
    updateFreshness();
  }

  function activateView(view) {
    if (!labels[view]) view = 'radar';
    app.activeView = view;
    document.querySelectorAll('[data-view-panel]').forEach((panel) => {
      panel.classList.toggle('is-visible', panel.dataset.viewPanel === view);
    });
    document.querySelectorAll('[data-view]').forEach((link) => {
      link.classList.toggle('is-active', link.dataset.view === view);
    });
    const topbar = document.getElementById('topbar-view');
    if (topbar) topbar.textContent = labels[view];
    document.body.classList.remove('nav-open');
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  function viewFromHash() {
    const raw = window.location.hash.replace(/^#/, '');
    return labels[raw] ? raw : 'radar';
  }

  function bindEvents() {
    window.addEventListener('hashchange', () => activateView(viewFromHash()));
    document.getElementById('mobile-menu')?.addEventListener('click', () => document.body.classList.toggle('nav-open'));
    document.getElementById('focus-search')?.addEventListener('click', () => document.getElementById('radar-search')?.focus());
    ['radar-search', 'state-filter', 'kind-filter'].forEach((id) => {
      const element = document.getElementById(id);
      if (!element) return;
      element.addEventListener(element.tagName === 'INPUT' ? 'input' : 'change', renderTable);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') document.body.classList.remove('nav-open');
      if (event.key === '/' && document.activeElement?.tagName !== 'INPUT') {
        event.preventDefault();
        activateView('radar');
        document.getElementById('radar-search')?.focus();
      }
    });
  }

  bindEvents();
  activateView(viewFromHash());
  loadProjection();
})();
