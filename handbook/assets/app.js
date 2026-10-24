(function () {
  'use strict';
  var menu = document.getElementById('menu-button');
  var sidebar = document.getElementById('sidebar');
  var search = document.getElementById('chapter-search');
  var results = document.getElementById('search-results');
  var toast = document.getElementById('toast');
  var toastTimer;
  function announce(message) {
    toast.textContent = message;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.textContent = ''; }, 4200);
  }
  function closeMenu() {
    sidebar.classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
  }
  menu.addEventListener('click', function () {
    var open = sidebar.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
    if (open) { search.focus(); }
  });
  document.addEventListener('click', function (event) {
    if (!sidebar.contains(event.target) && !menu.contains(event.target)) { closeMenu(); }
  });
  document.addEventListener('keydown', function (event) {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      if (window.innerWidth <= 720) { sidebar.classList.add('open'); menu.setAttribute('aria-expanded', 'true'); }
      search.focus();
    }
    if (event.key === 'Escape') {
      if (results && !results.hidden) { search.value = ''; results.hidden = true; search.focus(); }
      else if (sidebar.classList.contains('open')) { closeMenu(); menu.focus(); }
    }
  });
  function fallbackCopy(value) {
    var field = document.createElement('textarea');
    var active = document.activeElement;
    field.value = value;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.left = '-9999px';
    field.style.top = '0';
    document.body.appendChild(field);
    field.select();
    field.setSelectionRange(0, value.length);
    var copied = false;
    try { copied = document.execCommand('copy'); } catch (error) { copied = false; }
    field.remove();
    if (active) { active.focus(); }
    return copied;
  }
  document.querySelectorAll('[data-copy]').forEach(function (button) {
    button.addEventListener('click', async function () {
      var source = document.getElementById(button.getAttribute('data-copy'));
      var value = source.textContent;
      var copied = false;
      if (navigator.clipboard && window.isSecureContext) {
        try { await navigator.clipboard.writeText(value); copied = true; } catch (error) { copied = false; }
      }
      if (!copied) { copied = fallbackCopy(value); }
      if (copied) {
        button.textContent = '已複製 ✓';
        announce('已複製，可以貼到 Codex。');
        setTimeout(function () { button.textContent = '複製'; }, 2200);
      } else {
        var selection = window.getSelection();
        var range = document.createRange();
        range.selectNodeContents(source);
        selection.removeAllRanges();
        selection.addRange(range);
        announce('瀏覽器未允許自動複製。內容已選取，請按 Ctrl+C（Mac：⌘C）。');
      }
    });
  });
  search.addEventListener('input', function () {
    var query = search.value.trim().toLocaleLowerCase();
    results.textContent = '';
    results.hidden = !query;
    if (!query) { return; }
    var terms = query.split(/\s+/);
    var matches = (window.HANDBOOK_SEARCH || []).filter(function (entry) {
      var text = (entry.title + ' ' + entry.text).toLocaleLowerCase();
      return terms.every(function (term) { return text.indexOf(term) !== -1; });
    }).slice(0, 8);
    if (!matches.length) {
      var empty = document.createElement('li');
      empty.textContent = '找不到章節，試試「待確認」或技能英文名稱。';
      empty.style.padding = '10px';
      results.appendChild(empty);
    }
    matches.forEach(function (entry) {
      var item = document.createElement('li');
      var link = document.createElement('a');
      link.href = entry.url;
      link.textContent = entry.title;
      var context = document.createElement('small');
      context.textContent = entry.chapter;
      link.appendChild(context);
      link.addEventListener('keydown', function (event) {
        var links = Array.from(results.querySelectorAll('a'));
        var index = links.indexOf(link);
        if (event.key === 'ArrowDown') { event.preventDefault(); links[(index + 1) % links.length].focus(); }
        if (event.key === 'ArrowUp') { event.preventDefault(); if (!index) { search.focus(); } else { links[index - 1].focus(); } }
      });
      item.appendChild(link);
      results.appendChild(item);
    });
  });
  search.addEventListener('keydown', function (event) {
    var first = results.querySelector('a');
    if (event.key === 'ArrowDown' && first) { event.preventDefault(); first.focus(); }
    if (event.key === 'Enter' && first) { event.preventDefault(); first.click(); }
  });
})();
