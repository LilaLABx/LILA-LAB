// LILA Lab Documentation — Shared Page Script
// Each individual doc page defines a PAGE_CONFIG object that tells this
// script which markdown file to load from GitHub.

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/LilaLABx/LILA-LAB/main/';
const GITHUB_BLOB_BASE = 'https://github.com/LilaLABx/LILA-LAB/blob/main/';

// ── Documentation Index ──────────────────────────────────────────────
// DOC_SECTIONS, PATH_TO_SLUG, getIconSVG defined in docs-sidebar-data.js
// loaded before this script.

// ── DOM References ──
var sidebarNav = document.getElementById('sidebarNav');
var markdownBody = document.getElementById('markdownBody');
var docTitle = document.getElementById('docTitle');
var editOnGitHub = document.getElementById('editOnGitHub');
var sidebarToggle = document.getElementById('sidebarToggle');
var sidebarOverlay = document.getElementById('sidebarOverlay');
var docSearch = document.getElementById('docSearch');
var docsSidebar = document.getElementById('docsSidebar');

// ── State ──
var allDocItems = [];
var currentPath = null;
var renderedContentCache = '';

// ── Build Sidebar ──
function buildSidebar() {
    sidebarNav.innerHTML = '';
    allDocItems = [];

    DOC_SECTIONS.forEach(function(section, idx) {
        var sectionEl = document.createElement('div');
        sectionEl.className = 'sidebar-section expanded';

        var header = document.createElement('div');
        header.className = 'sidebar-section-header';
        header.innerHTML = section.title + '<svg class="chevron" viewBox="0 0 16 16" fill="currentColor"><path d="M6.5 3.5l4 4.5-4 4.5" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>';
        header.addEventListener('click', function() {
            sectionEl.classList.toggle('expanded');
        });

        var list = document.createElement('ul');
        list.className = 'sidebar-items';

        section.items.forEach(function(item) {
            var li = document.createElement('li');
            var a = document.createElement('a');
            a.className = 'sidebar-item';
            a.href = item.slug + '.html';
            a.dataset.path = item.path;
            a.dataset.slug = item.slug;
            a.dataset.status = item.status || '';
            a.innerHTML = getIconSVG(item.icon) + item.title;
            if (item.status === 'coming-soon') {
                a.classList.add('disabled');
                a.innerHTML += '<span class="sidebar-item-badge">Coming Soon</span>';
            }

            a.addEventListener('click', function(e) {
                if (item.status === 'coming-soon') {
                    e.preventDefault();
                }
                // Otherwise let the browser navigate naturally
            });

            item._element = a;
            allDocItems.push(a);

            li.appendChild(a);
            list.appendChild(li);
        });

        sectionEl.appendChild(header);
        sectionEl.appendChild(list);
        sidebarNav.appendChild(sectionEl);
    });

    // Sidebar search
    docSearch.addEventListener('input', filterSidebar);

    var searchStatus = document.createElement('div');
    searchStatus.id = 'searchStatus';
    searchStatus.className = 'search-status';
    docSearch.parentNode.insertBefore(searchStatus, docSearch.nextSibling);
}

// ── Sidebar Search ──
function filterSidebar() {
    var query = docSearch.value.toLowerCase().trim();

    allDocItems.forEach(function(el) {
        if (!query) {
            el.classList.remove('hidden');
            return;
        }
        var match = el.textContent.toLowerCase().includes(query);
        el.classList.toggle('hidden', !match);
    });

    document.querySelectorAll('.sidebar-section').forEach(function(section) {
        var visibleItems = section.querySelectorAll('.sidebar-item:not(.hidden)');
        section.style.display = visibleItems.length === 0 && query ? 'none' : '';
    });

    var searchStatus = document.getElementById('searchStatus');
    if (!searchStatus) return;
    if (!query) {
        searchStatus.textContent = '';
        searchStatus.className = 'search-status';
        return;
    }

    var visibleItems = document.querySelectorAll('.sidebar-item:not(.hidden)');
    var totalItems = document.querySelectorAll('.sidebar-item');
    var statusText = visibleItems.length + ' of ' + totalItems.length + ' in sidebar';

    if (renderedContentCache.toLowerCase().includes(query)) {
        statusText += ' \u00b7 Content match in current doc';
        searchStatus.className = 'search-status has-content-match';
    } else if (visibleItems.length === 0 && renderedContentCache) {
        statusText = 'No matches found';
        searchStatus.className = 'search-status no-match';
    }

    searchStatus.textContent = statusText;
}

// ── Activate Sidebar Item ──
function setActiveItem(path) {
    allDocItems.forEach(function(el) {
        el.classList.toggle('active', el.dataset.path === path);
    });
}

// ── Load Document ──
async function loadDoc(path) {
    if (!path) return;

    currentPath = path;
    setActiveItem(path);

    markdownBody.innerHTML = '<div class="doc-loading"><div class="doc-loading-spinner"></div><span>Loading document\u2026</span></div>';

    var rawUrl = GITHUB_RAW_BASE + path;

    try {
        var response = await fetch(rawUrl, { cache: 'no-cache' });
        if (!response.ok) {
            throw new Error('Failed to load (' + response.status + ')');
        }
        var markdown = await response.text();
        renderDoc(markdown, path);
    } catch (err) {
        var statusMatch = err.message.match(/\((\d+)\)/);
        var statusCode = statusMatch ? parseInt(statusMatch[1]) : 0;
        var notFound = statusCode === 404;
        markdownBody.innerHTML = (
            '<div class="doc-error">' +
                '<div class="doc-error-icon">\ud83d\udcc4</div>' +
                '<h3>Document not found</h3>' +
                '<p>The document <strong>' + path + '</strong> could not be loaded.</p>' +
                (notFound
                    ? '<p>This document may not exist yet. Check the repository directly for available documentation.</p>'
                    : '<p>' + err.message + '</p>') +
                '<div class="doc-error-actions">' +
                    '<button class="btn-retry" onclick="loadDoc(\'' + path + '\')">Retry</button>' +
                    '<a href="' + GITHUB_BLOB_BASE + path + '" target="_blank" class="btn-repo">View on GitHub \u2192</a>' +
                '</div>' +
            '</div>'
        );
    }

    // Close sidebar on mobile
    docsSidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── Render Markdown ──
function renderDoc(markdown, path) {
    marked.setOptions({ breaks: true, gfm: true });

    // Extract the first h1 from markdown for the page hero title
    var titleMatch = markdown.match(/^#\s+(.+)/m);
    var title = titleMatch ? titleMatch[1].trim() : path.split('/').pop().replace('.md', '').replace(/_/g, ' ');

    // Update the static hero title from the actual markdown content
    docTitle.textContent = title;
    document.title = title + ' — LILA Lab';
    editOnGitHub.href = GITHUB_BLOB_BASE + path;

    // Update hero description — use first paragraph after h1 if available
    var descMatch = markdown.match(/^#\s+.+\n+([^#\n][\s\S]*?)(?=\n##|\n#|\n$)/);
    var heroDesc = document.querySelector('.page-hero-desc');
    if (descMatch && heroDesc) {
        var firstPara = descMatch[1].trim().replace(/\n+/g, ' ').slice(0, 200);
        if (firstPara) heroDesc.textContent = firstPara;
    }

    // Strip the first h1 and its following content up to the first h2 from the HTML
    // to avoid duplicating the hero title
    var html = marked.parse(markdown);

    // Remove the first h1 from the rendered HTML (it's in the page hero)
    html = html.replace(/^<h1[^>]*>.*?<\/h1>\s*/i, '');

    markdownBody.innerHTML = (
        '<div class="markdown-body">' + html + '</div>' +
        '<div class="doc-source">' +
            '<span>Source: <a href="' + GITHUB_BLOB_BASE + path + '" target="_blank">' + path + '</a></span>' +
            '<span><a href="' + editOnGitHub.href + '" target="_blank">Edit on GitHub</a></span>' +
        '</div>'
    );

    renderedContentCache = markdownBody.textContent || '';

    wrapBadgeRow();
    rewriteRelativeLinks(path);

    if (typeof hljs !== 'undefined') {
        document.querySelectorAll('.markdown-body pre code').forEach(function(el) {
            hljs.highlightElement(el);
            // Add language label from highlight.js detected class
            var pre = el.closest('pre');
            if (pre && !pre.getAttribute('data-language')) {
                var langMatch = el.className.match(/language-(\w+)/);
                if (langMatch) {
                    pre.setAttribute('data-language', langMatch[1]);
                }
            }
        });
    }

    addHeadingAnchors();
    addCopyButtons();
    buildToc();
}

// ── Wrap shields.io badges in a horizontal row ──
function wrapBadgeRow() {
    var inner = document.querySelector('#markdownBody > .markdown-body');
    if (!inner) return;
    var badgeParagraphs = [];
    inner.querySelectorAll('p').forEach(function(p) {
        if (p.querySelector('a > img[src*="shields.io"]') && p.textContent.trim() === '') {
            badgeParagraphs.push(p);
        }
    });
    if (!badgeParagraphs.length) return;

    var ref = badgeParagraphs[0].previousElementSibling || inner.firstChild;
    var parent = ref.parentNode;

    var wrapper = document.createElement('div');
    wrapper.className = 'badge-row';
    badgeParagraphs.forEach(function(p) {
        p.querySelectorAll('a').forEach(function(a) { wrapper.appendChild(a); });
        p.remove();
    });

    if (parent) {
        parent.insertBefore(wrapper, ref.nextSibling);
    } else {
        inner.insertBefore(wrapper, inner.firstChild);
    }
}

// ── Rewrite Relative Links ──
function rewriteRelativeLinks(currentPath) {
    var baseDir = currentPath.includes('/')
        ? currentPath.substring(0, currentPath.lastIndexOf('/') + 1)
        : '';

    document.querySelectorAll('.markdown-body a').forEach(function(a) {
        var href = a.getAttribute('href');
        if (!href || href.startsWith('http') || href.startsWith('#') || href.startsWith('mailto:')) return;

        var resolved;
        if (href.startsWith('./')) {
            resolved = baseDir + href.slice(2);
        } else if (href.startsWith('../')) {
            var dir = baseDir;
            var rest = href;
            while (rest.startsWith('../')) {
                dir = dir.replace(/\/?[^/]+\/?$/, '');
                if (!dir) dir = '';
                rest = rest.slice(3);
            }
            resolved = dir ? dir + '/' + rest : rest;
        } else if (href.startsWith('/')) {
            resolved = href.slice(1);
        } else {
            resolved = baseDir + href;
        }

        if (resolved.endsWith('.md')) {
            var slug = PATH_TO_SLUG[resolved];
            if (slug) {
                a.href = slug + '.html';
                a.target = '';
            } else {
                a.href = GITHUB_BLOB_BASE + resolved;
                a.target = '_blank';
            }
        } else {
            a.href = GITHUB_BLOB_BASE + resolved;
            a.target = '_blank';
        }
    });

    // Fix image sources
    document.querySelectorAll('.markdown-body img').forEach(function(img) {
        var src = img.getAttribute('src');
        if (src && !src.startsWith('http')) {
            var resolved;
            if (src.startsWith('./')) {
                resolved = baseDir + src.slice(2);
            } else if (src.startsWith('/')) {
                resolved = src.slice(1);
            } else {
                resolved = baseDir + src;
            }
            img.src = GITHUB_RAW_BASE + resolved;
        }
    });
}

// ── Mobile Sidebar Toggle ──
sidebarToggle.addEventListener('click', function() {
    docsSidebar.classList.toggle('open');
    sidebarOverlay.classList.toggle('active');
});

sidebarOverlay.addEventListener('click', function() {
    docsSidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
});

// ── Heading Anchors ──
function addHeadingAnchors() {
    document.querySelectorAll('.markdown-body h1[id], .markdown-body h2[id], .markdown-body h3[id], .markdown-body h4[id], .markdown-body h5[id], .markdown-body h6[id]').forEach(function(heading) {
        var anchor = document.createElement('a');
        anchor.className = 'heading-anchor';
        anchor.href = '#' + heading.id;
        anchor.setAttribute('aria-label', 'Link to this section');
        anchor.textContent = '#';
        heading.classList.add('heading-anchored');
        heading.appendChild(anchor);
    });
}

// ── Copy-Code Buttons ──
function addCopyButtons() {
    document.querySelectorAll('.markdown-body pre').forEach(function(pre) {
        if (pre.querySelector('.copy-code-btn')) return;
        var btn = document.createElement('button');
        btn.className = 'copy-code-btn';
        btn.textContent = 'Copy';
        btn.addEventListener('click', function() {
            var code = pre.querySelector('code');
            if (!code) return;
            var text = code.textContent || '';
            navigator.clipboard.writeText(text).then(function() {
                btn.textContent = 'Copied!';
                btn.classList.add('copied');
                setTimeout(function() {
                    btn.textContent = 'Copy';
                    btn.classList.remove('copied');
                }, 2000);
            }).catch(function() {
                btn.textContent = 'Failed';
            });
        });
        pre.appendChild(btn);
    });
}

// ── Build Table of Contents ──
function buildToc() {
    var tocContainer = document.getElementById('sidebarToc');
    var tocLinks = document.getElementById('sidebarTocLinks');
    if (!tocContainer || !tocLinks) return;

    var headings = document.querySelectorAll('.markdown-body h2, .markdown-body h3');
    if (headings.length < 2) {
        tocContainer.style.display = 'none';
        return;
    }

    tocLinks.innerHTML = '';
    tocContainer.style.display = '';

    headings.forEach(function(heading) {
        if (!heading.id) return;
        var li = document.createElement('a');
        li.className = 'toc-item';
        if (heading.tagName === 'H3') {
            li.className += ' toc-item-nested';
        }
        li.href = '#' + heading.id;
        li.textContent = heading.textContent.replace(/#$/, '').trim();
        li.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.getElementById(heading.id);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                history.pushState(null, '', '#' + heading.id);
            }
        });
        tocLinks.appendChild(li);
    });

    updateTocActive();
}

// ── TOC Scroll-Spy ──
function updateTocActive() {
    var tocItems = document.querySelectorAll('.toc-item');
    if (!tocItems.length) return;

    var headings = [];
    tocItems.forEach(function(item) {
        var id = item.getAttribute('href').replace('#', '');
        var el = document.getElementById(id);
        if (el) headings.push({ el: el, item: item });
    });

    function onScroll() {
        var scrollPos = window.scrollY + 100;
        var current = null;
        headings.forEach(function(h) {
            if (h.el.offsetTop <= scrollPos) {
                current = h.item;
            }
        });
        tocItems.forEach(function(item) { item.classList.remove('toc-active'); });
        if (current) current.classList.add('toc-active');
    }

    window.addEventListener('scroll', onScroll);
    onScroll();
}

// ── Reading Progress ──
function updateReadingProgress() {
    var progressBar = document.getElementById('readingProgress');
    if (!progressBar) return;
    var scrollTop = window.scrollY;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (docHeight <= 0) {
        progressBar.style.width = '0%';
        return;
    }
    var progress = Math.min((scrollTop / docHeight) * 100, 100);
    progressBar.style.width = progress + '%';
    progressBar.setAttribute('aria-valuenow', Math.round(progress));
}

// ── Theme Init ──
function initTheme() {
    var html = document.documentElement;
    var toggle = document.getElementById('themeToggle');
    if (!toggle) return;

    var saved = localStorage.getItem('lila-theme');
    var prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
    var theme = saved || (prefersLight ? 'light' : 'dark');
    html.setAttribute('data-theme', theme);

    toggle.addEventListener('click', function() {
        var current = html.getAttribute('data-theme');
        var next = current === 'light' ? 'dark' : 'light';
        html.setAttribute('data-theme', next);
        localStorage.setItem('lila-theme', next);
    });
}

// ── Init ──
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    buildSidebar();

    // Reading progress bar
    window.addEventListener('scroll', updateReadingProgress);

    // Load doc from PAGE_CONFIG (defined in each HTML page)
    if (typeof PAGE_CONFIG !== 'undefined' && PAGE_CONFIG.path) {
        if (PAGE_CONFIG.title) {
            document.title = PAGE_CONFIG.title + ' \u2014 LILA Lab';
        }
        if (PAGE_CONFIG.status === 'coming-soon') {
            setActiveItem(PAGE_CONFIG.path);
            docTitle.textContent = PAGE_CONFIG.title;
            editOnGitHub.href = GITHUB_BLOB_BASE + PAGE_CONFIG.path;
            var tocContainer = document.getElementById('sidebarToc');
            if (tocContainer) tocContainer.style.display = 'none';
        } else {
            loadDoc(PAGE_CONFIG.path);
        }
    }
});
