// LILA Lab Documentation — Markdown Renderer & Sidebar Navigation

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/LilaLABx/LILA-LAB/main/';
const GITHUB_BLOB_BASE = 'https://github.com/LilaLABx/LILA-LAB/blob/main/';
const SITE_PREFIX = 'docs.html?doc=';

// ── Documentation Index ──────────────────────────────────────────────
// DOC_SECTIONS, PATH_TO_SLUG, getIconSVG defined in docs-sidebar-data.js
// loaded before this script.

// ── DOM References ───────────────────────────────────────────────────
const sidebarNav = document.getElementById('sidebarNav');
const markdownBody = document.getElementById('markdownBody');
const docTitle = document.getElementById('docTitle');
const editOnGitHub = document.getElementById('editOnGitHub');
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const docSearch = document.getElementById('docSearch');
const docsSidebar = document.getElementById('docsSidebar');

// ── State ────────────────────────────────────────────────────────────
let allDocItems = [];
let currentPath = null;
let renderedContentCache = '';

// ── Build Sidebar ────────────────────────────────────────────────────
function buildSidebar() {
    sidebarNav.innerHTML = '';
    allDocItems = [];

    DOC_SECTIONS.forEach((section, idx) => {
        const sectionEl = document.createElement('div');
        sectionEl.className = 'sidebar-section expanded';

        const header = document.createElement('div');
        header.className = 'sidebar-section-header';
        header.innerHTML = `
            ${section.title}
            <svg class="chevron" viewBox="0 0 16 16" fill="currentColor">
                <path d="M6.5 3.5l4 4.5-4 4.5" stroke="currentColor" stroke-width="1.5" fill="none"/>
            </svg>
        `;
        header.addEventListener('click', () => {
            sectionEl.classList.toggle('expanded');
        });

        const list = document.createElement('ul');
        list.className = 'sidebar-items';

        section.items.forEach(item => {
            const li = document.createElement('li');
            const a = document.createElement('a');
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

            item._element = a;
            allDocItems.push(a);

            a.addEventListener('click', (e) => {
                if (item.status === 'coming-soon') {
                    e.preventDefault();
                }
                // Otherwise let browser navigate to the HTML page
            });

            li.appendChild(a);
            list.appendChild(li);
        });

        sectionEl.appendChild(header);
        sectionEl.appendChild(list);
        sidebarNav.appendChild(sectionEl);
    });

    // Handle search
    docSearch.addEventListener('input', filterSidebar);

    // Add search status indicator
    const searchStatus = document.createElement('div');
    searchStatus.id = 'searchStatus';
    searchStatus.className = 'search-status';
    docSearch.parentNode.insertBefore(searchStatus, docSearch.nextSibling);
}

// ── Sidebar Search ───────────────────────────────────────────────────
function filterSidebar() {
    const query = docSearch.value.toLowerCase().trim();

    allDocItems.forEach(el => {
        if (!query) {
            el.classList.remove('hidden');
            return;
        }
        const match = el.textContent.toLowerCase().includes(query);
        el.classList.toggle('hidden', !match);
    });

    // Show/hide sections based on whether they have visible items
    document.querySelectorAll('.sidebar-section').forEach(section => {
        const visibleItems = section.querySelectorAll('.sidebar-item:not(.hidden)');
        section.style.display = visibleItems.length === 0 && query ? 'none' : '';
    });

    // Update search status
    const searchStatus = document.getElementById('searchStatus');
    if (!searchStatus) return;
    if (!query) {
        searchStatus.textContent = '';
        searchStatus.className = 'search-status';
        return;
    }

    // Count visible items
    const visibleItems = document.querySelectorAll('.sidebar-item:not(.hidden)');
    const totalItems = document.querySelectorAll('.sidebar-item');
    let statusText = `${visibleItems.length} of ${totalItems.length} in sidebar`;

    // Check rendered content
    if (renderedContentCache.toLowerCase().includes(query)) {
        statusText += ' · Content match in current doc';
        searchStatus.className = 'search-status has-content-match';
    } else if (visibleItems.length === 0 && renderedContentCache) {
        statusText = 'No matches found';
        searchStatus.className = 'search-status no-match';
    }

    searchStatus.textContent = statusText;
}

// ── Activate Sidebar Item ────────────────────────────────────────────
function setActiveItem(path) {
    allDocItems.forEach(el => {
        el.classList.toggle('active', el.dataset.path === path);
    });
}

// ── Load Document ────────────────────────────────────────────────────
async function loadDoc(path, pushState = true) {
    if (!path) return;

    // Extract hash fragment for scrolling after render
    const hashIndex = path.indexOf('#');
    const docPath = hashIndex >= 0 ? path.substring(0, hashIndex) : path;
    const hashFragment = hashIndex >= 0 ? path.substring(hashIndex) : '';

    currentPath = docPath;
    setActiveItem(docPath);

    // Switch from welcome page to doc view
    enterDocView();

    // Update URL
    if (pushState) {
        const url = SITE_PREFIX + encodeURIComponent(docPath) + hashFragment;
        history.pushState({ path: docPath, hash: hashFragment }, '', url);
    }

    // Show loading
    markdownBody.innerHTML = `
        <div class="doc-loading">
            <div class="doc-loading-spinner"></div>
            <span>Loading document…</span>
        </div>
    `;

    // Use raw URL to fetch markdown from GitHub (strip hash)
    const rawUrl = GITHUB_RAW_BASE + docPath;

    let response;
    try {
        response = await fetch(rawUrl, { cache: 'no-cache' });

        if (!response.ok) {
            throw new Error(`Failed to load (${response.status})`);
        }

        const markdown = await response.text();
        renderDoc(markdown, docPath);

        // Scroll to hash fragment if present, after render
        if (hashFragment) {
            setTimeout(() => {
                const targetId = hashFragment.replace('#', '');
                const el = document.getElementById(targetId);
                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        }

    } catch (err) {
        const statusCode = response ? response.status : 0;
        const notFound = statusCode === 404;
        markdownBody.innerHTML = `
            <div class="doc-error">
                <div class="doc-error-icon">📄</div>
                <h3>Document not found</h3>
                <p>The document <strong>${docPath}</strong> could not be loaded.</p>
                ${notFound
                    ? '<p>This document may not exist yet. Check the repository directly for available documentation.</p>'
                    : `<p>${err.message}</p>`}
                <div class="doc-error-actions">
                    <button class="btn-retry" onclick="loadDoc('${path}', false)">Retry</button>
                    <a href="${GITHUB_BLOB_BASE + docPath}" target="_blank" class="btn-repo">View on GitHub →</a>
                </div>
            </div>
        `;
    }

    // Close sidebar on mobile
    docsSidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');

    if (!hashFragment) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// ── Render Markdown ──────────────────────────────────────────────────
function renderDoc(markdown, path) {
    // Configure marked for security
    marked.setOptions({
        breaks: true,
        gfm: true,
    });

    const html = marked.parse(markdown);

    // Extract title from first h1
    const titleMatch = markdown.match(/^#\s+(.+)/m);
    const title = titleMatch ? titleMatch[1].trim() : path.split('/').pop().replace('.md', '').replace(/_/g, ' ');
    docTitle.textContent = title;

    // Update Edit on GitHub link
    editOnGitHub.href = GITHUB_BLOB_BASE + path;

    // Wrap in content div
    markdownBody.innerHTML = `
        <div class="markdown-body">${html}</div>
        <div class="doc-source">
            <span>Source: <a href="${GITHUB_BLOB_BASE + path}" target="_blank">${path}</a></span>
            <span>
                <a href="${editOnGitHub.href}" target="_blank">Edit on GitHub</a>
            </span>
        </div>
    `;

    // Cache rendered text for search
    const textContent = markdownBody.textContent || '';
    renderedContentCache = textContent;

    // Rewrite relative links to GitHub
    rewriteRelativeLinks(path);

    // Post-render enhancements
    if (typeof hljs !== 'undefined') {
        document.querySelectorAll('.markdown-body pre code').forEach(function(el) {
            hljs.highlightElement(el);
        });
    }
    addHeadingAnchors();
    addCopyButtons();
    buildToc();
}

// ── Rewrite Relative Links ───────────────────────────────────────────
function rewriteRelativeLinks(currentPath) {
    const baseDir = currentPath.includes('/')
        ? currentPath.substring(0, currentPath.lastIndexOf('/') + 1)
        : '';

    document.querySelectorAll('.markdown-body a').forEach(a => {
        const href = a.getAttribute('href');

        if (!href || href.startsWith('http') || href.startsWith('#') || href.startsWith('mailto:')) {
            return;
        }

        // Resolve relative to the base directory of the current doc
        let resolved;
        if (href.startsWith('./')) {
            resolved = baseDir + href.slice(2);
        } else if (href.startsWith('../')) {
            let dir = baseDir;
            let rest = href;
            while (rest.startsWith('../')) {
                dir = dir.replace(/\/?[^/]+\/?$/, '');
                if (!dir) dir = '';
                rest = rest.slice(3);
            }
            resolved = dir ? dir + '/' + rest : rest;
        } else if (href.startsWith('/')) {
            resolved = href.slice(1); // absolute from repo root
        } else {
            resolved = baseDir + href;
        }

        if (resolved.endsWith('.md')) {
            const slug = PATH_TO_SLUG[resolved];
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
    document.querySelectorAll('.markdown-body img').forEach(img => {
        const src = img.getAttribute('src');
        if (src && !src.startsWith('http')) {
            let resolved;
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

// ── Mobile Sidebar Toggle ────────────────────────────────────────────
sidebarToggle.addEventListener('click', () => {
    docsSidebar.classList.toggle('open');
    sidebarOverlay.classList.toggle('active');
});

sidebarOverlay.addEventListener('click', () => {
    docsSidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
});

// ── Handle Browser Back/Forward ──────────────────────────────────────
window.addEventListener('popstate', (e) => {
    if (e.state && e.state.path) {
        const pathWithHash = e.state.hash
            ? e.state.path + e.state.hash
            : e.state.path;
        loadDoc(pathWithHash, false);
    } else {
        showWelcome();
    }
});

// ── Show Welcome Page ────────────────────────────────────────────────
function showWelcome() {
    docTitle.textContent = 'Documentation';
    editOnGitHub.href = '#';
    setActiveItem(null);
    currentPath = null;

    document.getElementById('contentHeader').style.display = 'none';
    const welcomePage = document.querySelector('.welcome-page');
    if (welcomePage) welcomePage.style.display = '';

    // Clear rendered markdown
    const mdBody = document.getElementById('markdownBody');
    if (mdBody) mdBody.innerHTML = '';

    // Hide TOC
    const tocContainer = document.getElementById('sidebarToc');
    if (tocContainer) tocContainer.style.display = 'none';
}

// ── Hide Welcome, Show Doc Content ────────────────────────────────────
function enterDocView() {
    document.getElementById('contentHeader').style.display = 'flex';
    const welcomePage = document.querySelector('.welcome-page');
    if (welcomePage) welcomePage.style.display = 'none';
}

// ── Add Heading Anchors ───────────────────────────────────────────────
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

// ── Copy-Code Buttons ─────────────────────────────────────────────────
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

// ── Build Table of Contents ──────────────────────────────────────────
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

// ── Toc Scroll-Spy ────────────────────────────────────────────────────
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

// ── Reading Progress Bar ──────────────────────────────────────────────
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

// ── Init ─────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    buildSidebar();

    // Reading progress bar
    window.addEventListener('scroll', updateReadingProgress);

    // Load from URL query param
    const params = new URLSearchParams(window.location.search);
    const docParam = params.get('doc');

    if (docParam) {
        loadDoc(decodeURIComponent(docParam), false);
    } else {
        showWelcome();
    }
});

function navigateToDoc(docPath) {
    const hashIndex = docPath.indexOf('#');
    const path = hashIndex >= 0 ? docPath.substring(0, hashIndex) : docPath;
    const hash = hashIndex >= 0 ? docPath.substring(hashIndex) : '';

    const slug = PATH_TO_SLUG[path];
    if (slug) {
        window.location.href = slug + '.html' + hash;
        return;
    }

    // Fallback: if path has no docs/ prefix, try with it
    if (!path.startsWith('docs/')) {
        const prefixed = 'docs/' + path;
        const slug2 = PATH_TO_SLUG[prefixed];
        if (slug2) {
            window.location.href = slug2 + '.html' + hash;
            return;
        }
    }

    window.location.href = GITHUB_BLOB_BASE + path;
}

// Re-bind all doc links on the welcome page
document.addEventListener('click', function(e) {
    // Scroll-to-section links (onboarding strip)
    const scrollLink = e.target.closest('[data-scroll]');
    if (scrollLink) {
        e.preventDefault();
        const targetId = scrollLink.dataset.scroll;
        const target = document.getElementById(targetId);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        return;
    }

    // All doc-link types share data-doc attribute
    const link = e.target.closest('[data-doc]');
    if (link && !link.classList.contains('path-card')) {
        e.preventDefault();
        navigateToDoc(link.dataset.doc);
        return;
    }

    // Path cards — load the recommended doc + scroll to content
    const pathCard = e.target.closest('.path-card');
    if (pathCard && pathCard.dataset.doc) {
        e.preventDefault();
        navigateToDoc(pathCard.dataset.doc);
        return;
    }

    // Roadmap step links
    const stepLink = e.target.closest('.step-links a');
    if (stepLink && stepLink.dataset.doc) {
        e.preventDefault();
        navigateToDoc(stepLink.dataset.doc);
    }
});

// ── Mobile Nav Toggle ────────────────────────────────────────────────
(function() {
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    if (!navToggle || !navLinks) return;

    let scrollPosition = 0;

    function lockBodyScroll() {
        scrollPosition = window.scrollY;
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.top = '-' + scrollPosition + 'px';
        document.body.style.width = '100%';
    }

    function unlockBodyScroll() {
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        window.scrollTo(0, scrollPosition);
    }

    function closeMobileNav() {
        navToggle.classList.remove('active');
        navLinks.classList.remove('open');
        unlockBodyScroll();
    }

    navToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        navLinks.classList.toggle('open');
        if (navLinks.classList.contains('open')) {
            lockBodyScroll();
        } else {
            unlockBodyScroll();
        }
    });

    navLinks.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', closeMobileNav);
    });
})();
