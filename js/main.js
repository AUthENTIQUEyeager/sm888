/* SM888 — script principal (aucune dépendance). Réglages : config.js et catalogue.js. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var C = window.CONFIG, LOGO = 'assets/logo.svg'; // ← changer ici si le logo est un .png
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };
  var P = { // icônes SVG intégrées
    wa: 'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z',
    phone: 'M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z',
    menu: 'M3 6h18M3 12h18M3 18h18',
    shield: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM9 12l2 2 4-4',
    check: 'M22 11.1V12a10 10 0 11-5.9-9.1M22 4L12 14l-3-3',
    scale: 'M12 3v18M7 21h10M4 7h16M4 7l-2.5 6a3.5 3.5 0 005 0zM20 7l-2.5 6a3.5 3.5 0 005 0z',
    wrench: 'M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z',
    users: 'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8zM23 21v-2a4 4 0 00-3-3.9M16 3.1a4 4 0 010 7.8'
  };
  function ico(n) { return '<svg class="i' + (n === 'wa' ? ' f' : '') + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + P[n] + '"/></svg>'; }
  function tel(n) { return 'tel:' + n.replace(/[^\d+]/g, ''); }
  function wa(m) { return 'https://wa.me/' + C.WHATSAPP_NUMBER + '?text=' + encodeURIComponent(m); } // message encodé

  /* En-tête, pied de page, barre mobile et bouton WhatsApp : modifier ici pour changer sur toutes les pages */
  var pages = [['index.html', 'Accueil'], ['or.html', 'Or'], ['engins.html', 'Engins &amp; équipements'], ['apropos.html', 'À propos'], ['contact.html', 'Contact']];
  var cur = location.pathname.split('/').pop() || 'index.html';
  var nav = pages.map(function (p) { return '<a href="' + p[0] + '"' + (p[0] === cur ? ' aria-current="page"' : '') + '>' + p[1] + '</a>'; }).join('');
  var head = '<header class="site-h dark"><div class="wrap"><a class="logo" href="index.html" aria-label="SM888 — Accueil"><img src="' + LOGO + '" width="120" height="40" alt="SM888"></a><nav class="nav" id="nav" aria-label="Menu principal">' + nav + '</nav><a class="btn btn-wa h-wa" data-wa="general">' + ico('wa') + 'WhatsApp</a><button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu">' + ico('menu') + '</button></div></header>';
  var foot = '<footer class="site-f dark"><div class="wrap"><div class="grid"><div><img src="' + LOGO + '" width="120" height="40" alt="SM888" loading="lazy"><p>' + C.DEVISE + '</p></div><div><h3>Contact</h3><ul><li><a href="' + tel(C.PHONE_1) + '">' + C.PHONE_1 + '</a></li><li><a href="' + tel(C.PHONE_2) + '">' + C.PHONE_2 + '</a></li><li>' + C.ADRESSE + '</li>' + (C.EMAIL ? '<li><a href="mailto:' + C.EMAIL + '">' + C.EMAIL + '</a></li>' : '') + '</ul></div><div><h3>Navigation</h3><ul>' + pages.map(function (p) { return '<li><a href="' + p[0] + '">' + p[1] + '</a></li>'; }).join('') + '<li><a href="credits.html">Crédits photos</a></li></ul></div></div><p class="copy">© ' + new Date().getFullYear() + ' ' + C.NOM_ENTREPRISE + '. Tous droits réservés.</p></div></footer>';
  var bar = '<div class="mbar dark"><a class="btn btn-line" href="' + tel(C.PHONE_1) + '">' + ico('phone') + 'Appeler</a><a class="btn btn-wa" data-wa="general">' + ico('wa') + 'WhatsApp</a></div><a class="wa-float" data-wa="general" aria-label="Discuter sur WhatsApp">' + ico('wa') + '</a>';
  var skip = $('.skip');
  if (skip) skip.insertAdjacentHTML('afterend', head); else document.body.insertAdjacentHTML('afterbegin', head);
  document.body.insertAdjacentHTML('beforeend', foot + bar);

  /* Liens et textes pilotés par config.js */
  $$('[data-icon]').forEach(function (e) { e.innerHTML = ico(e.dataset.icon); });
  $$('[data-wa]').forEach(function (a) { a.href = wa(C.MESSAGES[a.dataset.wa] || C.MESSAGES.general); a.target = '_blank'; a.rel = 'noopener'; });
  $$('[data-tel]').forEach(function (a) { a.href = tel(C['PHONE_' + a.dataset.tel]); });
  $$('[data-cfg]').forEach(function (e) { var v = C[e.dataset.cfg]; if (v) e.textContent = v; else e.hidden = true; });

  /* Menu mobile */
  var b = $('.burger'), n = $('#nav');
  function fermer() { n.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); b.setAttribute('aria-label', 'Ouvrir le menu'); }
  b.addEventListener('click', function () { var o = n.classList.toggle('open'); b.setAttribute('aria-expanded', String(o)); b.setAttribute('aria-label', o ? 'Fermer le menu' : 'Ouvrir le menu'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && n.classList.contains('open')) { fermer(); b.focus(); } });

  /* Apparition au défilement (désactivée si « réduire les animations ») */
  var rv = $$('.reveal');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: .1 });
    rv.forEach(function (e) { io.observe(e); });
  } else rv.forEach(function (e) { e.classList.add('in'); });

  /* Catalogue + filtres (page engins.html) */
  var g = $('#grille');
  if (g && window.CATALOGUE) {
    var f = { cat: 'all', mode: 'all' };
    var B = { location: 'Location', vente: 'Vente', neuf: 'Neuf', occasion: 'Occasion', 'sur demande': 'Neuf ou occasion sur demande' };
    var carte = function (m) {
      var bd = m.mode.concat([m.etat]).map(function (k, i) { return '<span class="badge' + (i >= m.mode.length ? ' o' : '') + '">' + B[k] + '</span>'; }).join('');
      var msg = C.MESSAGES.devis.replace('{nom}', m.nom).replace('{mode}', m.mode.join(' ou '));
      return '<article class="card prod"><img src="assets/img/' + m.image + '" width="800" height="600" loading="lazy" alt="' + m.nom + '"><div class="corps"><div class="badges">' + bd + '</div><h3>' + m.nom + '</h3><p>' + m.description + '</p><p class="mut">Utile pour : ' + m.utilite + '</p><p class="prix">' + m.prix + '</p><div class="actions"><a class="btn btn-gold" href="' + wa(msg) + '" target="_blank" rel="noopener">Demander un devis</a><a class="btn btn-line" href="' + tel(C.PHONE_1) + '">Appeler</a></div></div></article>';
    };
    var rendre = function () {
      var l = window.CATALOGUE.filter(function (m) { return (f.cat === 'all' || m.categorie === f.cat) && (f.mode === 'all' || m.mode.indexOf(f.mode) > -1); });
      g.innerHTML = l.map(carte).join('');
      $('#compte').textContent = l.length ? l.length + (l.length > 1 ? ' machines affichées' : ' machine affichée') : 'Aucune machine pour ce filtre.';
    };
    $$('[data-f]').forEach(function (c) {
      c.addEventListener('click', function () {
        f[c.dataset.f] = c.dataset.v;
        $$('[data-f="' + c.dataset.f + '"]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
        rendre();
      });
    });
    rendre();
  }

  /* Page « Crédits photos » (liste générée par telecharger_images.py dans js/credits.js) */
  var cr = $('#credits');
  if (cr) {
    var K = window.CREDITS || {}, ks = Object.keys(K);
    var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
    cr.innerHTML = ks.length ? ks.map(function (k) {
      var c = K[k], m = (window.CATALOGUE || []).filter(function (x) { return x.image === k + '.webp'; })[0];
      var lien = /^https:\/\/commons\.wikimedia\.org\//.test(c.page) ? ' — <a href="' + esc(c.page) + '" target="_blank" rel="noopener">source</a>' : '';
      return '<li><strong>' + esc(m ? m.nom : k) + '</strong> : ' + esc(c.titre.replace(/^File:/, '')) + ', par ' + esc(c.auteur.slice(0, 120)) + ' — ' + esc(c.licence) + lien + '</li>';
    }).join('') : '<li>Les images actuelles sont des illustrations provisoires : aucun crédit à afficher.</li>';
  }

  /* Formulaire de contact → WhatsApp (rien n’est envoyé à un serveur) */
  var fm = $('#form-contact');
  if (fm) fm.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(fm), nom = (d.get('nom') || '').trim(), tl = (d.get('tel') || '').trim(), ty = d.get('type') || '', ms = (d.get('message') || '').trim(), er = [], box = $('#retour');
    if (nom.length < 2) er.push(['nom', 'Indiquez votre nom.']);
    if (tl.replace(/\D/g, '').length < 8) er.push(['tel', 'Indiquez un numéro de téléphone valide.']);
    if (!ty) er.push(['type', 'Choisissez un type de demande.']);
    if (ms.length < 5) er.push(['message', 'Écrivez votre message.']);
    ['nom', 'tel', 'type', 'message'].forEach(function (k) { fm.elements[k].setAttribute('aria-invalid', String(er.some(function (x) { return x[0] === k; }))); });
    if (er.length) { box.className = 'msg ko'; box.textContent = er.map(function (x) { return x[1]; }).join(' '); fm.elements[er[0][0]].focus(); return; }
    var url = wa('Bonjour,\n\nNom : ' + nom + '\nTéléphone : ' + tl + '\nType de demande : ' + ty + '\nMessage : ' + ms);
    window.open(url, '_blank', 'noopener');
    box.className = 'msg ok';
    box.innerHTML = 'Merci ! WhatsApp s’ouvre avec votre message prêt. Appuyez sur « Envoyer » pour finaliser. Rien ne s’ouvre ? <a href="' + url + '" target="_blank" rel="noopener">Ouvrir WhatsApp</a>.';
    fm.reset();
  });
})();
