/* =====================================================================
   FrontPage 90s kit — behaviors. Vanilla JS, no dependencies, works from file://.
   Every feature switches on only when its markup exists, so include the whole
   file and use what you need. User text is always inserted with textContent.
   ===================================================================== */
(function () {
  'use strict';
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  };
  var reduceMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var lang = (document.documentElement.lang || navigator.language || 'en');
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  /* Field name for confirmations/messages: data-label > group legend (radios/checkboxes) > <label> > name */
  function fieldLabel(f) {
    var lab = f.getAttribute('data-label');
    if (!lab && (f.type === 'radio' || f.type === 'checkbox')) {
      var fs = f.closest && f.closest('fieldset'), lg = fs && fs.querySelector('legend');
      lab = (lg && lg.textContent) || f.name;
    }
    if (!lab) lab = (f.labels && f.labels[0] && f.labels[0].textContent) || f.name;
    return lab.replace(/\s+/g, ' ').replace(/[:*\s]+$/, '').trim();
  }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  /* Fixed-size boxes (88x31 badges, banner ads) center their content with flexbox; wrap mixed content
     ("<b>Click</b> here<br>now") in one span so it flows as text instead of splitting into columns. */
  $all('.fp-ad, .fp-badge').forEach(function (box) {
    var nodes = Array.prototype.slice.call(box.childNodes);
    var meaningful = nodes.filter(function (n) { return n.nodeType === 1 || (n.nodeType === 3 && n.textContent.trim()); });
    if (meaningful.length < 2 || box.classList.contains('fp-badge')) return;
    var wrap = el('span');
    nodes.forEach(function (n) { wrap.appendChild(n); });
    box.appendChild(wrap);
  });

  /* Navigation bars: mark the current page (lets every page share an identical border). */
  var here = location.pathname.split('/').pop() || 'index.html';
  $all('.fp-navbar a[href], .fp-navbar-v a[href], .fp-textnav a[href]').forEach(function (a) {
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#' || /^[a-z]+:/i.test(href)) return;
    var file = href.split('#')[0].split('?')[0].split('/').pop() || 'index.html';
    if (file === here && !a.hasAttribute('aria-current')) a.setAttribute('aria-current', 'page');
  });

  /* Inside a frame, hide "View with frames" links (data-fp-noframes-only); outside, show them. */
  var framed = false;
  try { framed = window.self !== window.top; } catch (e) { framed = true; }
  if (framed) $all('[data-fp-noframes-only]').forEach(function (n) { n.hidden = true; });

  /* Framed pages tell the frameset which page is showing, so the contents frame highlights the right button. */
  if (framed) { try { window.parent.postMessage({ fpPage: here }, '*'); } catch (e) {} }
  window.addEventListener('message', function (ev) {
    if (!ev.data || !ev.data.fpPage) return;
    $all('iframe[name]').forEach(function (fr) {
      if (fr.contentWindow !== ev.source) return;
      $all('a[target="' + fr.getAttribute('name') + '"]').forEach(function (a) {
        var file = (a.getAttribute('href') || '').split('#')[0].split('/').pop();
        if (file === ev.data.fpPage) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
      });
    });
  });

  /* Collapsible outlines: arriving at #id inside a closed <details> opens it (links, search results). */
  function openTarget() {
    var id = decodeURIComponent(location.hash.slice(1)), t = id && document.getElementById(id);
    for (var n = t; n; n = n.parentElement) if (n.tagName === 'DETAILS') n.open = true;
    if (t && t.scrollIntoView) t.scrollIntoView();
  }
  window.addEventListener('hashchange', openTarget);
  if (location.hash) openTarget();

  /* Frames: links that target a frame (<a target="main">) mark themselves current when clicked,
     and the one matching the iframe's starting page is marked on load. */
  $all('a[target]').forEach(function (a) {
    var name = a.getAttribute('target'), frame = document.querySelector('iframe[name="' + name + '"]');
    if (!frame) return;
    var start = (frame.getAttribute('src') || '').split('#')[0];
    if (start && a.getAttribute('href').split('#')[0] === start && !document.querySelector('a[target="' + name + '"][aria-current]')) a.setAttribute('aria-current', 'page');
    a.addEventListener('click', function () {
      $all('a[target="' + name + '"][aria-current]').forEach(function (o) { o.removeAttribute('aria-current'); });
      a.setAttribute('aria-current', 'page');
    });
  });

  /* Hit Counter: <span class="fp-counter" data-fp-counter="home" data-digits="6"></span>
     Counts page loads in THIS browser only (localStorage). Label it honestly in the markup. */
  $all('[data-fp-counter]').forEach(function (box) {
    var key = 'fp-counter:' + (box.getAttribute('data-fp-counter') || here);
    var start = parseInt(box.getAttribute('data-start') || '0', 10) || 0;
    var digits = parseInt(box.getAttribute('data-digits') || '6', 10) || 6;
    var n = (parseInt(store.get(key) || '0', 10) || 0) + 1;
    store.set(key, String(n));
    var s = String(start + n);
    while (s.length < digits) s = '0' + s;
    box.textContent = '';
    box.setAttribute('role', 'img');
    box.setAttribute('aria-label', String(start + n));
    s.split('').forEach(function (d) {
      var c = el('span', 'fp-digit', d);
      c.setAttribute('aria-hidden', 'true');
      box.appendChild(c);
    });
  });

  /* Guestbook: <form data-fp-guestbook="mysite" data-list="gb-list"> with fields name, from, message.
     Entries live in this browser only. Static entries already inside the list are kept below new ones. */
  $all('form[data-fp-guestbook]').forEach(function (form) {
    var key = 'fp-guestbook:' + (form.getAttribute('data-fp-guestbook') || here);
    var list = document.getElementById(form.getAttribute('data-list') || '') || form.parentNode.querySelector('.fp-gb-entries');
    if (!list) { list = el('div', 'fp-gb-entries'); form.parentNode.insertBefore(list, form.nextSibling); }
    var status = form.querySelector('.fp-gb-status') || form.appendChild(el('p', 'fp-note fp-gb-status'));
    status.setAttribute('role', 'status');
    var staticEntries = $all('.fp-gb-entry', list);
    function load() { try { return JSON.parse(store.get(key) || '[]') || []; } catch (e) { return []; } }
    function render() {
      $all('.fp-gb-entry[data-local]', list).forEach(function (n) { n.remove(); });
      var first = staticEntries[0] || null;
      load().forEach(function (it) {
        var item = el('div', 'fp-gb-entry');
        item.setAttribute('data-local', '');
        var meta = el('div', 'fp-gb-meta');
        meta.appendChild(el('b', '', it.name));
        if (it.from) meta.appendChild(document.createTextNode(' — ' + it.from));
        meta.appendChild(document.createTextNode(' · ' + it.date));
        item.appendChild(meta);
        item.appendChild(el('div', '', it.message));
        list.insertBefore(item, first);
      });
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = form.elements;
      var name = ((f.name && f.name.value) || '').trim().slice(0, 60);
      var message = ((f.message && f.message.value) || '').trim().slice(0, 1000);
      if (!name || !message) { status.textContent = form.getAttribute('data-error') || 'Please fill in your name and a message.'; return; }
      var entries = load();
      entries.unshift({ name: name, from: ((f.from && f.from.value) || '').trim().slice(0, 60), message: message,
        date: new Date().toLocaleDateString(lang) });
      var ok = store.set(key, JSON.stringify(entries.slice(0, 50)));
      render();
      form.reset();
      status.textContent = ok
        ? (form.getAttribute('data-thanks') || 'Thanks for signing! Your entry is saved in this browser only.')
        : (form.getAttribute('data-nostore') || 'Your browser blocked local storage, so this entry will disappear on reload.');
    });
    render();
  });

  /* Demo forms (Feedback / Order / Contact templates):
     <form data-fp-demo data-confirm="confirm-id"> — shows a FrontPage-style confirmation page
     listing what was typed, and makes clear nothing was sent. Leave data-fp-demo off for real backends. */
  $all('form[data-fp-demo]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var box = document.getElementById(form.getAttribute('data-confirm') || '');
      if (!box) { box = el('div', 'fp-confirm'); form.parentNode.insertBefore(box, form.nextSibling); }
      var dl = box.querySelector('dl') || box.appendChild(el('dl'));
      dl.textContent = '';
      $all('input, select, textarea', form).forEach(function (f) {
        if (!f.name || /^(submit|reset|button|hidden)$/i.test(f.type) || ((f.type === 'radio' || f.type === 'checkbox') && !f.checked)) return;
        dl.appendChild(el('dt', '', fieldLabel(f)));
        dl.appendChild(el('dd', '', f.value || '—'));
      });
      box.hidden = false;
      box.setAttribute('tabindex', '-1');
      box.focus();
    });
  });

  /* Search Form component: <form data-fp-search="#content" data-results="results-id"> with input name="q".
     Searches the headings + text of the current page and lists matching sections. */
  function fold(s) { return String(s).toLowerCase().normalize ? String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '') : String(s).toLowerCase(); }
  $all('form[data-fp-search]').forEach(function (form) {
    var label = form.getAttribute('data-found') || 'Number of documents found:';
    /* Site-wide mode: data-fp-search="site" + theme/search-index.js from scripts/build_search_index.py */
    if (form.getAttribute('data-fp-search') === 'site') {
      var res = document.getElementById(form.getAttribute('data-results') || '') || form.appendChild(el('div', 'fp-search-results'));
      res.setAttribute('role', 'status');
      var target = form.getAttribute('data-target');
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var q = fold(((form.elements.q && form.elements.q.value) || '').trim());
        res.textContent = '';
        if (!q) return;
        var idx = window.FP_SEARCH_INDEX || [], words = q.split(/\s+/), hits = idx.filter(function (d) {
          var hay = fold(d.title + ' ' + d.text);
          return words.every(function (w) { return hay.indexOf(w) > -1; });
        });
        if (!window.FP_SEARCH_INDEX) { res.appendChild(el('p', 'fp-note', 'Search index missing: run scripts/build_search_index.py on the site folder.')); return; }
        res.appendChild(el('p', '', label + ' ' + hits.length));
        var tbl = el('table', 'fp-table'), head = el('tr');
        if (!hits.length) return;
        head.appendChild(el('th', '', form.getAttribute('data-col-title') || 'Document'));
        head.appendChild(el('th', '', form.getAttribute('data-col-page') || 'Page'));
        tbl.appendChild(head);
        hits.slice(0, 50).forEach(function (d) {
          var tr = el('tr'), td = el('td'), a = el('a', '', d.title);
          a.href = d.url; if (target && framed) a.target = target;  // standalone page: open results in place
          td.appendChild(a); tr.appendChild(td); tr.appendChild(el('td', '', d.page || d.url.split('#')[0])); tbl.appendChild(tr);
        });
        res.appendChild(tbl);
      });
      form.addEventListener('reset', function () { res.textContent = ''; });
      return;
    }
    var scope = document.querySelector(form.getAttribute('data-fp-search') || 'body') || document.body;
    var out = document.getElementById(form.getAttribute('data-results') || '') || form.appendChild(el('div', 'fp-search-results'));
    out.setAttribute('role', 'status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = fold(((form.elements.q && form.elements.q.value) || '').trim());
      out.textContent = '';
      if (!q) return;
      var heads = $all('h1, h2, h3', scope), hits = [];
      heads.forEach(function (h, i) {
        var text = h.textContent, n = h.nextElementSibling;
        while (n && !/^H[1-3]$/.test(n.tagName) && !n.querySelector('h1,h2,h3')) { text += ' ' + n.textContent; n = n.nextElementSibling; }
        if (fold(text).indexOf(q) > -1) {
          if (!h.id) h.id = 'fp-sec-' + i;
          hits.push(h);
        }
      });
      out.appendChild(el('p', '', label + ' ' + hits.length));
      if (!hits.length) return;
      var ul = el('ul', 'fp-bullets');
      hits.forEach(function (h) {
        var li = el('li'), a = el('a', '', h.textContent.trim());
        a.href = '#' + h.id;
        li.appendChild(a); ul.appendChild(li);
      });
      out.appendChild(ul);
    });
    form.addEventListener('reset', function () { out.textContent = ''; });
  });

  /* Banner Ad Manager: <div class="fp-adrotator" data-fp-rotator="4000"> with 2+ children.
     Pauses on hover/focus; does not rotate when the visitor prefers reduced motion. */
  $all('[data-fp-rotator]').forEach(function (box) {
    var items = Array.prototype.slice.call(box.children);
    if (items.length < 2) return;
    var i = 0, paused = false, ms = Math.max(2500, parseInt(box.getAttribute('data-fp-rotator'), 10) || 4000);
    items.forEach(function (it, j) { it.hidden = j !== 0; });
    if (reduceMotion) return;
    box.addEventListener('mouseenter', function () { paused = true; });
    box.addEventListener('mouseleave', function () { paused = false; });
    box.addEventListener('focusin', function () { paused = true; });
    box.addEventListener('focusout', function () { paused = false; });
    setInterval(function () {
      if (paused || document.hidden) return;
      items[i].hidden = true; i = (i + 1) % items.length; items[i].hidden = false;
    }, ms);
  });

  /* Timestamp component: <span data-fp-timestamp="long|short"></span> -> this file's real modified date.
     For a fictional 1998 page, just write the date as plain text instead. */
  $all('[data-fp-timestamp]').forEach(function (t) {
    var d = new Date(document.lastModified);
    if (isNaN(d)) return;
    var long = t.getAttribute('data-fp-timestamp') !== 'short';
    t.textContent = d.toLocaleDateString(lang, long ? { year: 'numeric', month: 'long', day: 'numeric' }
      : { year: '2-digit', month: '2-digit', day: '2-digit' });
  });

  /* Message composer — an honest contact form that needs no backend:
     <form data-fp-compose="whatsapp:5493415550199" data-subject="Consulta desde la web">  or  data-fp-compose="mailto:me@example.com"
     Builds a message from the labeled fields and opens WhatsApp or the visitor's mail program with it ready to send.
     The page itself sends nothing. */
  $all('form[data-fp-compose]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var spec = form.getAttribute('data-fp-compose') || '', kind = spec.split(':')[0], dest = spec.slice(kind.length + 1);
      var lines = [];
      $all('input, select, textarea', form).forEach(function (f) {
        if (!f.name || !f.value || /^(submit|reset|button|hidden)$/i.test(f.type) || ((f.type === 'radio' || f.type === 'checkbox') && !f.checked)) return;
        lines.push(fieldLabel(f) + ': ' + f.value);
      });
      var body = lines.join('\n'), subject = form.getAttribute('data-subject') || document.title;
      if (kind === 'whatsapp') {
        window.open('https://wa.me/' + dest.replace(/[^0-9]/g, '') + '?text=' + encodeURIComponent(subject + '\n\n' + body), '_blank', 'noopener');
      } else {
        location.href = 'mailto:' + dest + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      }
    });
  });

  /* "Background MIDI", minus the autoplay: <button class="fp-btn" type="button" data-fp-midi="E5 D5 C5 D5 E5 E5 E5:2 - D5 D5 D5:2"
     data-tempo="160" data-stop-label="■ Stop">♪ Play MIDI</button>. Square-wave chiptune via WebAudio, only on click.
     Notes: letter + optional # or b + octave 0-8 (e.g. C4, F#5, Bb3), ":2" = two beats, "-" = rest. */
  $all('[data-fp-midi]').forEach(function (btn) {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) { btn.disabled = true; return; }
    var ctx = null, oscs = [], timer = null, playLabel = btn.textContent;
    var NOTE = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
    function stop() {
      oscs.forEach(function (o) { try { o.stop(); } catch (e) {} });
      oscs = []; clearTimeout(timer); timer = null; btn.textContent = playLabel; btn.setAttribute('aria-pressed', 'false');
    }
    btn.setAttribute('aria-pressed', 'false');
    btn.addEventListener('click', function () {
      if (timer) { stop(); return; }
      ctx = ctx || new AC();
      var beat = 60 / (parseInt(btn.getAttribute('data-tempo') || '150', 10) || 150), t = ctx.currentTime + 0.05;
      (btn.getAttribute('data-fp-midi') || '').trim().split(/\s+/).forEach(function (tok) {
        var parts = tok.split(':'), len = (parseFloat(parts[1]) || 1) * beat, m = /^([A-G])([#b]?)(\d)$/.exec(parts[0]);
        if (m) {
          var midi = 12 * (parseInt(m[3], 10) + 1) + NOTE[m[1]] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0);
          var o = ctx.createOscillator(), g = ctx.createGain();
          o.type = 'square'; o.frequency.value = 440 * Math.pow(2, (midi - 69) / 12);
          g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.05, t + 0.01);
          g.gain.exponentialRampToValueAtTime(0.0001, t + len * 0.9);
          o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + len); oscs.push(o);
        }
        t += len;
      });
      btn.textContent = btn.getAttribute('data-stop-label') || '■ Stop';
      btn.setAttribute('aria-pressed', 'true');
      timer = setTimeout(stop, (t - ctx.currentTime) * 1000 + 100);
    });
  });

  /* Countdown: <span class="fp-countdown" data-fp-countdown="2027-03-14T21:00:00-03:00"
     data-units="days|hours|min|sec" data-done="¡Llegó el día!"></span>  (always give the UTC offset) */
  $all('[data-fp-countdown]').forEach(function (box) {
    var target = new Date(box.getAttribute('data-fp-countdown')).getTime();
    if (isNaN(target)) return;
    var units = (box.getAttribute('data-units') || 'days|hours|min|sec').split('|'), cells = [];
    box.textContent = '';
    box.setAttribute('role', 'timer');
    units.forEach(function (u) {
      var unit = el('span', 'fp-cd-unit'), num = el('span', 'fp-cd-num', '--');
      unit.appendChild(num); unit.appendChild(el('span', '', u)); box.appendChild(unit); cells.push(num);
    });
    function tick() {
      var ms = target - Date.now();
      if (ms <= 0) { box.textContent = box.getAttribute('data-done') || 'Today!'; clearInterval(timer); return; }
      var s = Math.floor(ms / 1000), parts = [Math.floor(s / 86400), Math.floor(s / 3600) % 24, Math.floor(s / 60) % 60, s % 60];
      cells.forEach(function (c, i) { c.textContent = String(parts[i]).length < 2 ? '0' + parts[i] : String(parts[i]); });
      box.setAttribute('aria-label', parts[0] + ' ' + units[0]);
    }
    var timer = setInterval(tick, 1000);
    tick();
  });

  /* Optional welcome status line: <p data-fp-greeting></p> -> "Good morning!" style text by local hour. */
  $all('[data-fp-greeting]').forEach(function (g) {
    var h = new Date().getHours();
    var words = (g.getAttribute('data-fp-greeting') || 'Good morning!|Good afternoon!|Good evening!').split('|');
    g.textContent = h < 12 ? words[0] : h < 19 ? (words[1] || words[0]) : (words[2] || words[0]);
  });
})();
