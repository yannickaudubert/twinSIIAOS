(() => {
  'use strict';

  const params = new URLSearchParams(window.location.search);
  const fixtureMode = params.get('fixture') === '1';
  const resourceId = params.get('id') || '';

  const stateMeta = {
    observed: ['Observé', 'Faits publics vérifiés. Aucun test local ne doit être déduit de cet état.'],
    candidate: ['Candidat', 'Option assez pertinente pour mériter une qualification ou une comparaison.'],
    installed: ['Installé', 'Installé dans un environnement déclaré, sans conclusion automatique sur la qualité.'],
    tested: ['Testé', 'Un protocole ou cas d’usage a produit des résultats vérifiables.'],
    qualified: ['Qualifié', 'Les preuves soutiennent une conclusion dans un contexte explicite.'],
    target: ['Cible', 'Ressource retenue comme cible d’architecture dans un contexte défini.'],
    deprecated: ['Déprécié', 'Conservé pour l’historique ou la migration, mais plus traité comme choix courant.'],
    retired: ['Retiré', 'Sorti des choix courants ; conservé éventuellement pour historique ou migration.'],
  };

  const kindLabels = {
    system: 'Système', model: 'Modèle', approach: 'Approche', agent: 'Agent', runtime: 'Runtime', source: 'Source', dataset: 'Jeu de données',
    service: 'Service', tool: 'Outil', database: 'Base de données', framework: 'Framework', platform: 'Plateforme', application: 'Application',
    library: 'Bibliothèque', protocol: 'Protocole', connector: 'Connecteur', hub: 'Hub / registre', reference: 'Ressource de référence',
  };

  function escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function formatDate(value) {
    if (!value) return 'Non publiée';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return String(value).slice(0, 10);
    return new Intl.DateTimeFormat('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' }).format(date);
  }

  function normalizeState(value) {
    return stateMeta[value] ? value : 'observed';
  }

  function list(value) {
    return Array.isArray(value) ? value.filter(Boolean) : [];
  }

  function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  }

  function renderChips(id, items, fallback) {
    const target = document.getElementById(id);
    if (!target) return;
    if (!items.length) {
      target.innerHTML = `<span>${escapeHtml(fallback)}</span>`;
      return;
    }
    target.innerHTML = items.map((item) => `<span>${escapeHtml(item)}</span>`).join('');
  }

  function renderBulletList(id, items, fallback) {
    const target = document.getElementById(id);
    if (!target) return;
    if (!items.length) {
      target.innerHTML = `<p class="human-note">${escapeHtml(fallback)}</p>`;
      return;
    }
    target.innerHTML = `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
  }

  function renderPublicExplanation(item) {
    const section = document.getElementById('resource-explanation');
    const explanation = item.public_explanation;
    if (!section || !explanation || typeof explanation !== 'object') {
      if (section) section.hidden = true;
      return;
    }

    const primaryRole = explanation.primary_role || list(item.capabilities)[0] || kindLabels[item.kind] || item.kind || 'Rôle non publié';
    setText('resource-primary-role', primaryRole);
    setText('resource-plain-language', explanation.plain_language || item.summary || 'Aucune explication en langage simple n’est encore publiée.');

    const solves = list(explanation.solves);
    if (solves.length) setText('resource-purpose', solves.join(' · '));

    renderBulletList('resource-does-not-replace', list(explanation.does_not_replace), 'Aucune frontière fonctionnelle supplémentaire n’est encore documentée.');
    renderBulletList('resource-use-when', list(explanation.use_when), 'Aucun critère public « à regarder quand » n’est encore documenté.');
    renderBulletList('resource-avoid-when', list(explanation.avoid_when), 'Aucun critère public d’exclusion précoce n’est encore documenté.');
    renderBulletList('resource-tradeoffs', list(explanation.tradeoffs), 'Aucun compromis public n’est encore documenté.');
    renderBulletList('resource-questions', list(explanation.questions_to_ask), 'Aucune question de cadrage spécifique n’est encore publiée.');

    const operational = [
      ...list(explanation.deployment_modes).map((value) => `Déploiement : ${value}`),
      ...list(explanation.prerequisites).map((value) => `Prérequis : ${value}`),
      ...list(explanation.operations_notes).map((value) => `Exploitation : ${value}`),
      ...list(explanation.license_notes).map((value) => `Licence : ${value}`),
    ];
    renderBulletList('resource-operational', operational, 'Aucune note publique supplémentaire de déploiement, exploitation ou licence.');
    section.hidden = false;
  }

  function renderProof(item) {
    const target = document.getElementById('resource-proof');
    if (!target) return;
    const state = normalizeState(item.state);
    const expert = item.expert_available || {};
    const hasObservation = Boolean(item.last_verified_at || item.source_url || item.repo_url);
    const hasInstall = ['installed', 'tested', 'qualified'].includes(state);
    const hasTest = ['tested', 'qualified'].includes(state) || expert.benchmark === true;
    const hasQualification = state === 'qualified';

    const rows = [
      ['observed', 'Observation publique', hasObservation, hasObservation ? `Source et faits publics vérifiés${item.last_verified_at ? ` le ${formatDate(item.last_verified_at)}` : ''}.` : 'Aucune observation datée n’est publiée.'],
      ['installed', 'Installation', hasInstall, hasInstall ? 'Une installation est explicitement déclarée par l’état de preuve publié.' : 'Aucune installation n’est déclarée dans les données publiques.'],
      ['tested', 'Test / benchmark', hasTest, hasTest ? (expert.benchmark === true && !['tested', 'qualified'].includes(state) ? 'Un benchmark existe, mais l’état public de la ressource ne la déclare pas pour autant « testée » dans son ensemble.' : 'Un état testé/qualifié ou un benchmark explicite est déclaré. Vérifiez toujours le protocole et le contexte.') : 'Aucun test ou benchmark n’est déclaré dans les données publiques.'],
      ['qualified', 'Qualification', hasQualification, hasQualification ? 'Une qualification est explicitement déclarée ; lisez toujours son contexte et sa date.' : 'Aucune qualification contextualisée n’est déclarée publiquement pour cette ressource.'],
    ];

    target.innerHTML = rows.map(([cssState, label, available, note]) => `<div class="proof-row">
      <span class="pill ${available ? cssState : ''}">${available ? escapeHtml(label) : 'Non publié'}</span>
      <p>${escapeHtml(note)}</p>
      <b>${available ? 'Élément disponible' : 'Pas de conclusion'}</b>
    </div>`).join('');
  }

  function renderGaps(item) {
    const target = document.getElementById('resource-gaps');
    if (!target) return;
    const gaps = list(item.known_gaps);
    if (!gaps.length) {
      target.innerHTML = '<div class="decision-boundary"><strong>Aucun gap public déclaré.</strong><p>Cela ne signifie pas que la ressource est sans limite : seulement qu’aucun écart non sensible n’est présent dans les données publiques.</p></div>';
      return;
    }
    target.innerHTML = `<div class="reading-grid">${gaps.map((gap) => `<article class="reading-card"><span class="reading-time">À vérifier</span><h3>Gap connu</h3><p style="font-size:11px;margin:8px 0 0">${escapeHtml(gap)}</p></article>`).join('')}</div>`;
  }

  function renderRelations(item) {
    const target = document.getElementById('resource-relations');
    if (!target) return;
    const definitions = [
      ['Dépend de', list(item.depends_on), 'Aucune dépendance publiée.'],
      ['Permet', list(item.enables), 'Aucune relation « permet » publiée.'],
      ['Peut remplacer', list(item.replaces), 'Aucun remplacement publié.'],
      ['À comparer avec', list(item.competes_with), 'Aucun concurrent explicite publié.'],
    ];
    target.innerHTML = definitions.map(([title, values, fallback]) => `<article class="reading-card"><span class="reading-time">Architecture</span><h3>${escapeHtml(title)}</h3>${values.length ? `<ul>${values.map((value) => `<li>${escapeHtml(value)}</li>`).join('')}</ul>` : `<p style="font-size:10px;margin:8px 0 0">${escapeHtml(fallback)}</p>`}</article>`).join('');
  }

  function renderProvenance(item) {
    const target = document.getElementById('resource-provenance');
    if (!target) return;
    const source = item.repo_url || item.source_url || '';
    const values = [
      ['Identifiant', item.id],
      ['Source', source || 'Non publiée'],
      ['Vérifié', formatDate(item.last_verified_at)],
      ['Mis à jour', formatDate(item.updated_at || item.last_activity)],
    ];
    target.innerHTML = `<dl class="provenance">${values.map(([label, value]) => `<div><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd></div>`).join('')}</dl>`;
  }

  function renderTrend(item) {
    const value = item?.trend?.delta_30d;
    const target = document.getElementById('resource-trend');
    if (!target) return;
    if (typeof value !== 'number') {
      target.textContent = 'Aucune tendance 30 jours n’est publiée pour cette ressource.';
      return;
    }
    const direction = value > 0 ? 'positive' : value < 0 ? 'négative' : 'stable';
    target.textContent = `Tendance 30 jours publiée : ${value > 0 ? '+' : ''}${value} (${direction}). Utilisez-la comme signal de veille, jamais comme recommandation automatique.`;
  }

  function renderExpertAvailability(item) {
    const target = document.getElementById('resource-fit-public');
    if (!target) return;
    const expert = item.expert_available || {};
    const available = [];
    if (expert.fit) available.push('analyse d’adéquation');
    if (expert.benchmark) available.push('benchmark');
    if (Number(expert.evidence_count || 0) > 0) available.push(`${expert.evidence_count} preuve${expert.evidence_count > 1 ? 's' : ''}`);
    if (expert.contextual_position) available.push('position contextualisée');
    target.textContent = available.length
      ? `Le Radar indique que des éléments Expert existent (${available.join(', ')}), sans exposer leur contenu dans les données publiques.`
      : 'Aucun élément Expert n’est signalé pour le moment. Un Pass ne fabrique pas une qualification absente.';
  }

  function renderItem(item) {
    const state = normalizeState(item.state);
    const [stateLabel, stateExplanation] = stateMeta[state];
    const kind = kindLabels[item.kind] || item.kind || 'Ressource';
    const capabilities = list(item.capabilities);
    const approaches = list(item.approaches);
    const source = item.repo_url || item.source_url || '';
    const explanation = item.public_explanation || {};

    document.title = `${item.title || item.id} — SIIAOS Resource Radar`;
    setText('resource-kicker', `${kind}${capabilities[0] ? ` · ${capabilities[0]}` : ''}`);
    setText('resource-title', item.title || item.id);
    setText('resource-summary', explanation.plain_language || item.summary || 'Aucun résumé public n’est disponible pour cette ressource.');
    setText('resource-kind', kind);
    setText('resource-primary-role', explanation.primary_role || capabilities[0] || kind);
    setText('resource-state', `${stateLabel} — ${stateExplanation}`);
    setText('resource-license', item.license || 'Non publiée');
    setText('resource-verified', formatDate(item.last_verified_at));
    setText('resource-purpose', capabilities.length ? `Cette ressource contribue aux capacités suivantes : ${capabilities.join(', ')}.` : 'Aucune capacité n’est encore reliée dans les données publiques.');
    setText('resource-approach', approaches.length ? `Approche(s) publiée(s) : ${approaches.join(', ')}.` : 'Aucune approche n’est encore reliée dans les données publiques.');
    renderChips('resource-capabilities', capabilities, 'Capacités non renseignées');
    renderChips('resource-approaches', approaches, 'Approches non renseignées');

    const sourceLink = document.getElementById('resource-source');
    if (sourceLink) {
      if (source) sourceLink.href = source;
      else {
        sourceLink.removeAttribute('href');
        sourceLink.setAttribute('aria-disabled', 'true');
        sourceLink.textContent = 'Source non publiée';
      }
    }

    renderPublicExplanation(item);
    renderProof(item);
    renderGaps(item);
    renderRelations(item);
    renderProvenance(item);
    renderTrend(item);
    renderExpertAvailability(item);
  }

  async function load() {
    const loading = document.getElementById('resource-loading');
    const error = document.getElementById('resource-error');
    const content = document.getElementById('resource-content');
    const demo = document.getElementById('resource-demo');
    const back = document.getElementById('back-radar');

    if (demo) demo.hidden = !fixtureMode;
    if (back) back.href = `./index.html${fixtureMode ? '?fixture=1' : ''}#radar`;

    if (!resourceId) {
      if (loading) loading.hidden = true;
      if (error) error.hidden = false;
      return;
    }

    const source = fixtureMode ? './fixtures/radar-public.demo.json' : '../projections/radar-public.json';
    try {
      const response = await fetch(source, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const projection = await response.json();
      if (!projection || projection.schema !== 'siiaos.radar-public.v1' || !Array.isArray(projection.items)) throw new Error('Données publiques incompatibles');
      const item = projection.items.find((entry) => String(entry.id) === String(resourceId));
      if (!item) throw new Error('Ressource absente');
      renderItem(item);
      if (loading) loading.hidden = true;
      if (content) content.hidden = false;
    } catch (cause) {
      console.warn('Radar resource data unavailable:', cause);
      if (loading) loading.hidden = true;
      if (error) error.hidden = false;
    }
  }

  load();
})();
