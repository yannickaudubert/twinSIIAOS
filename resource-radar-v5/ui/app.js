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
    'expert-fit': 'Expert / Adéquation',
    'expert-compare': 'Expert / Comparateur',
    'expert-evidence': 'Expert / Preuves',
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

  const stateExplanations = {
    observed: 'Faits publics vérifiés. Cela ne signifie pas que la ressource a été testée localement.',
    candidate: 'Option jugée assez pertinente pour mériter une qualification ou une comparaison.',
    installed: 'La ressource a été installée dans un environnement identifié, sans préjuger de sa performance.',
    tested: 'Un protocole ou cas d’usage a produit des résultats vérifiables dans un environnement déclaré.',
    qualified: 'Les preuves disponibles soutiennent une conclusion dans un contexte explicitement décrit.',
    target: 'Ressource ou état retenu comme cible d’architecture, sous réserve des décisions et preuves associées.',
    deprecated: 'Ressource ou usage déprécié ; conservé pour l’historique, la migration ou la compréhension de l’existant.',
    retired: 'Ressource retirée des choix courants, mais potentiellement conservée pour l’historique.',
  };

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
      dataset: 'Jeu de données',
      service: 'Service',
      tool: 'Outil',
      database: 'Base de données',
      framework: 'Framework',
      platform: 'Plateforme',
      application: 'Application',
      library: 'Bibliothèque',
      protocol: 'Protocole',
      connector: 'Connecteur',
      hub: 'Hub / registre',
      reference: 'Ressource de référence',
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
    const expert = item?.expert_available || {};
    const declared = Number(expert.evidence_count || 0);
    const benchmark = expert.benchmark === true ? 1 : 0;
    return declared + benchmark;
  }

  function gapCount(item) {
    return Array.isArray(item.known_gaps) ? item.known_gaps.length : 0;
  }

  function resourceDestination(item) {
    const query = new URLSearchParams();
    query.set('id', String(item.id || ''));
    if (app.fixtureMode) query.set('fixture', '1');
    return `./resource.html?${query.toString()}`;
  }

  function replaceOwnText(element, text) {
    if (!element) return;
    const textNode = [...element.childNodes].find((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim());
    if (textNode) textNode.textContent = ` ${text} `;
  }

  function humanizeStaticShell() {
    replaceOwnText(document.querySelector('[data-view="expert-fit"]'), 'Adéquation');
    replaceOwnText(document.querySelector('[data-view="expert-evidence"]'), 'Preuves');

    const sidebarSmall = document.querySelector('.sidebar-small');
    if (sidebarSmall) sidebarSmall.textContent = 'Sources vérifiées · preuves datées · publication maîtrisée.';

    const topbarKicker = document.querySelector('.topbar-kicker');
    if (topbarKicker) topbarKicker.textContent = 'Intelligence technologique';

    const demoBanner = document.getElementById('demo-banner');
    if (demoBanner) {
      demoBanner.innerHTML = '<strong>Données de démonstration.</strong> Cet aperçu sert uniquement à vérifier l’interface. Il ne constitue ni une qualification publiée ni une recommandation.';
    }

    const candidateCard = document.getElementById('metric-candidates')?.closest('.metric-card');
    if (candidateCard) {
      const note = candidateCard.querySelector('.metric-note');
      if (note) note.textContent = 'observé ou candidat, à tester ou qualifier';
    }

    const evidenceCard = document.getElementById('metric-evidence')?.closest('.metric-card');
    if (evidenceCard) {
      const label = evidenceCard.querySelector('.metric-label');
      const note = evidenceCard.querySelector('.metric-note');
      if (label) label.textContent = 'Preuves signalées';
      if (note) note.textContent = 'preuves ou benchmarks existants, détails selon publication';
    }

    const empty = document.getElementById('resource-empty');
    if (empty) {
      const note = empty.querySelector('span');
      if (note) note.textContent = 'Aucune donnée publique n’est publiée pour cette vue. Le Radar reste vide plutôt que d’inventer du contenu.';
    }

    const expertCallout = document.querySelector('.expert-callout p');
    if (expertCallout) expertCallout.textContent = 'Le Pass Conseil ouvre l’adéquation au contexte, les preuves détaillées, les architectures et les arbitrages de mission — pas davantage de liens publics.';
  }

  function ensureHumanUx() {
    if (!document.querySelector('link[href="./human.css"]')) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = './human.css';
      document.head.append(link);
    }

    humanizeStaticShell();

    const actions = document.querySelector('.topbar-actions');
    if (actions && !actions.querySelector('.human-help-links')) {
      const help = document.createElement('div');
      help.className = 'human-help-links';
      help.setAttribute('aria-label', 'Aide');
      help.innerHTML = '<a href="./start.html">Commencer</a><a href="./guide.html">Mode d’emploi</a><a href="./lexique.html">Lexique</a>';
      actions.prepend(help);
    }

    const radar = document.querySelector('[data-view-panel="radar"]');
    const heading = radar?.querySelector('.page-heading');
    if (radar && heading && !radar.querySelector('.human-orientation-strip')) {
      const strip = document.createElement('nav');
      strip.className = 'human-orientation-strip';
      strip.setAttribute('aria-label', 'Choisir un point de départ');
      strip.innerHTML = '<strong>Je pars de :</strong><a href="#radar">une solution connue</a><a href="#capabilities">un besoin</a><a href="#landscapes">une comparaison</a><a href="#expert-evidence">une décision à justifier</a><a href="./lexique.html">un terme à comprendre</a>';
      heading.before(strip);
    }

    const tableWrap = document.querySelector('.resource-table-wrap');
    if (tableWrap && !document.getElementById('resource-mobile-list')) {
      const mobile = document.createElement('div');
      mobile.id = 'resource-mobile-list';
      mobile.className = 'resource-mobile-list';
      mobile.setAttribute('aria-label', 'Ressources, vue mobile');
      tableWrap.after(mobile);
    }
  }

  async function loadProjection() {
    const source = app.fixtureMode ? './fixtures/radar-public.demo.json' : '../projections/radar-public.json';
    try {
      const response = await fetch(source, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (!data || data.schema !== 'siiaos.radar-public.v1' || !Array.isArray(data.items)) {
        throw new Error('Données publiques incompatibles');
      }
      app.projection = data;
      document.getElementById('projection-dot')?.classList.add('ok');
      document.getElementById('projection-status').textContent = app.fixtureMode ? 'Données de démonstration chargées' : 'Données publiques chargées';
    } catch (error) {
      console.warn('Radar public data unavailable:', error);
      document.getElementById('projection-status').textContent = 'Aucune donnée publique chargée';
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
      const explanation = item.public_explanation || {};
      const haystack = [
        item.title,
        item.summary,
        item.kind,
        explanation.plain_language,
        explanation.primary_role,
        ...(Array.isArray(explanation.solves) ? explanation.solves : []),
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
    const mobile = document.getElementById('resource-mobile-list');
    if (!tbody || !empty || !count) return;

    count.textContent = `${items.length} ressource${items.length > 1 ? 's' : ''}`;
    tbody.innerHTML = items.map((item) => {
      const state = normalizeState(item.state);
      const capabilities = Array.isArray(item.capabilities) ? item.capabilities : [];
      const role = item.public_explanation?.primary_role || capabilities[0] || kindLabel(item.kind);
      return `<tr data-resource-id="${escapeHtml(item.id)}" tabindex="0" aria-label="Ouvrir la fiche ${escapeHtml(item.title || item.id)}">
        <td><div class="resource-name"><strong>${escapeHtml(item.title || item.id)}</strong><small>${escapeHtml(item.public_explanation?.plain_language || item.summary || item.source_url || '')}</small></div></td>
        <td>${escapeHtml(role)}</td>
        <td><span class="pill ${escapeHtml(state)} state-help" title="${escapeHtml(stateExplanations[state] || '')}">${escapeHtml(stateLabel(state))}</span></td>
        <td>${trendMarkup(item)}</td>
        <td>${escapeHtml(formatDate(item.last_verified_at || item.updated_at || item.last_activity))}</td>
      </tr>`;
    }).join('');

    if (mobile) {
      mobile.innerHTML = items.map((item) => {
        const state = normalizeState(item.state);
        const capabilities = Array.isArray(item.capabilities) ? item.capabilities : [];
        const role = item.public_explanation?.primary_role || capabilities[0] || kindLabel(item.kind);
        return `<article class="resource-mobile-card">
          <div class="resource-mobile-card-head"><h3>${escapeHtml(item.title || item.id)}</h3><span class="pill ${escapeHtml(state)}" title="${escapeHtml(stateExplanations[state] || '')}">${escapeHtml(stateLabel(state))}</span></div>
          <p>${escapeHtml(item.public_explanation?.plain_language || item.summary || 'Aucun résumé public disponible.')}</p>
          <div class="resource-mobile-meta"><span>${escapeHtml(kindLabel(item.kind))}</span><span>${escapeHtml(role)}</span><span>vérifié ${escapeHtml(formatDate(item.last_verified_at || item.updated_at || item.last_activity))}</span></div>
          <div class="resource-mobile-actions"><a href="${escapeHtml(resourceDestination(item))}">Comprendre la fiche →</a><span>${trendMarkup(item)}</span></div>
        </article>`;
      }).join('');
    }

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
      board.innerHTML = '<div class="empty-state"><strong>Aucune capacité publiée.</strong><span>Cette vue se remplira lorsque des ressources publiques seront disponibles.</span></div>';
      return;
    }
    board.innerHTML = entries.map(([name, meta]) => `<article class="capability-card">
      <div class="eyebrow">Capacité</div>
      <h2>${escapeHtml(name)}</h2>
      <p>${meta.count} ressource${meta.count > 1 ? 's' : ''} actuellement reliée${meta.count > 1 ? 's' : ''} à cette capacité.</p>
      <footer><span>${escapeHtml([...meta.kinds].slice(0, 3).join(' · '))}</span><span>états : ${escapeHtml([...meta.states].map(stateLabel).join(', '))}</span></footer>
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
      target.innerHTML = '<div class="empty-state"><strong>Aucun signal public.</strong><span>L’Hyperveille reste vide tant qu’aucune observation publiable n’est disponible.</span></div>';
      return;
    }
    target.innerHTML = sorted.map((item) => {
      const state = normalizeState(item.state);
      const expert = item.expert_available || {};
      const decisionSignal = expert.fit || expert.contextual_position || expert.benchmark || Number(expert.evidence_count || 0) > 0
        ? 'analyse approfondie disponible'
        : 'observation publique';
      return `<article class="timeline-item">
        <div class="timeline-meta"><span>${escapeHtml(formatDate(item.updated_at || item.last_verified_at || item.last_activity))}</span><span>${escapeHtml(kindLabel(item.kind))}</span><span title="${escapeHtml(stateExplanations[state] || '')}">${escapeHtml(stateLabel(state))}</span><span>${escapeHtml(decisionSignal)}</span></div>
        <h2>${escapeHtml(item.title || item.id)}</h2>
        <p>${escapeHtml(item.public_explanation?.plain_language || item.summary || 'Observation publiée sans commentaire supplémentaire.')}</p>
      </article>`;
    }).join('');
  }

  function updateFreshness() {
    const target = document.getElementById('freshness-label');
    if (!target) return;
    if (!app.projection.generatedAt) {
      target.textContent = app.fixtureMode ? 'Données de démonstration' : 'Aucune donnée publique';
      return;
    }
    target.textContent = `${app.fixtureMode ? 'Démonstration' : 'Données publiques'} · ${formatDate(app.projection.generatedAt)}`;
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

  function openResourceFromRow(row) {
    const id = row?.dataset?.resourceId;
    if (!id) return;
    const item = app.projection.items.find((entry) => String(entry.id) === String(id));
    if (!item) return;
    window.location.href = resourceDestination(item);
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
    document.getElementById('resource-table-body')?.addEventListener('click', (event) => {
      const row = event.target.closest('tr[data-resource-id]');
      if (row) openResourceFromRow(row);
    });
    document.getElementById('resource-table-body')?.addEventListener('keydown', (event) => {
      if (!['Enter', ' '].includes(event.key)) return;
      const row = event.target.closest('tr[data-resource-id]');
      if (!row) return;
      event.preventDefault();
      openResourceFromRow(row);
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

  ensureHumanUx();
  bindEvents();
  activateView(viewFromHash());
  loadProjection();
})();
