// LILA Lab Documentation — Shared Page Script
// Each individual doc page defines a PAGE_CONFIG object that tells this
// script which markdown file to load from GitHub.

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/LilaLABx/LILA-LAB/main/';
const GITHUB_BLOB_BASE = 'https://github.com/LilaLABx/LILA-LAB/blob/main/';

// ── Documentation Index ──────────────────────────────────────────────
const DOC_SECTIONS = [
    {
        title: '🚀 Getting Started',
        items: [
            { slug: 'about-lila-lab',   title: 'About LILA Lab',       path: 'README.md',                                          icon: 'book' },
            { slug: 'quickstart-guide',  title: 'Quickstart Guide',     path: 'docs/CONTRIBUTOR_QUICKSTART.md',                      icon: 'rocket' },
            { slug: 'pipeline-flow',     title: 'Pipeline Flow',        path: 'docs/PIPELINE_FLOW.md',                               icon: 'flow' },
            { slug: 'faq',               title: 'FAQ',                  path: 'FAQ.md',                                              icon: 'help' },
        ]
    },
    {
        title: '📚 Knowledge Base',
        items: [
            { slug: 'research-papers',        title: 'Research Papers',            path: 'technical-reports/README.md',                            icon: 'paper' },
            { slug: 'datasets',               title: 'Datasets',                   path: 'dataset/README.md',                                      icon: 'database' },
            { slug: 'project-roadmap',        title: 'Project Roadmap',            path: 'ROADMAP.md',                                             icon: 'map' },
            { slug: 'xeni-naming-convention', title: 'XENI Naming Convention',     path: 'docs/adr/ADR-001-xeni-naming-convention.md',             icon: 'adr' },
        ]
    },
    {
        title: '🔧 Pipeline Reference',
        items: [
            { slug: 'xeni-framework',        title: 'XENI Framework',           path: 'pipelines/README.md',                                       icon: 'pipeline' },
            { slug: 'beni-bangla',           title: 'BENI — Bangla',           path: 'pipelines/BENI/README.md',                                  icon: 'lang' },
            { slug: 'beni-pilot-experiment', title: 'BENI Pilot Experiment',    path: 'pipelines/BENI/experiment/beni_pilot/README.md',            icon: 'experiment' },
            { slug: 'template-pipeline',     title: 'Template Pipeline',        path: 'pipelines/template/README.md',                              icon: 'template' },
            { slug: 'aeni-assamese',         title: 'AENI — Assamese',          path: 'pipelines/AENI/README.md',                                  icon: 'lang', status: 'coming-soon' },
            { slug: 'neni-nepali',           title: 'NENI — Nepali',            path: 'pipelines/NENI/README.md',                                  icon: 'lang', status: 'coming-soon' },
            { slug: 'seni-sylheti',          title: 'SENI — Sylheti',           path: 'pipelines/SENI/README.md',                                  icon: 'lang', status: 'coming-soon' },
            { slug: 'audio-annotation-lab',  title: 'Audio Annotation Lab',     path: 'pipelines/audio-annotation-lab/README.md',                 icon: 'audio' },
        ]
    },
    {
        title: '🤝 Contribution',
        items: [
            { slug: 'collaboration-framework', title: 'Collaboration Framework',  path: 'COLLABORATION.md',                icon: 'handshake' },
            { slug: 'linguistic-contribution', title: 'Linguistic Contribution',  path: 'LINGUISTIC_CONTRIBUTION_GUIDE.md', icon: 'globe' },
            { slug: 'code-contribution',       title: 'Code Contribution',        path: 'CONTRIBUTING.md',                  icon: 'code' },
            { slug: 'code-of-conduct',         title: 'Code of Conduct',          path: 'CODE_OF_CONDUCT.md',               icon: 'shield' },
        ]
    },
    {
        title: '📋 Reference',
        items: [
            { slug: 'infrastructure',  title: 'Infrastructure',   path: 'infrastructure/README.md',  icon: 'server' },
            { slug: 'security-policy', title: 'Security Policy',  path: 'SECURITY.md',               icon: 'lock' },
        ]
    }
];

// ── Path → Slug Mapping (for rewriting in-doc links) ──
const PATH_TO_SLUG = {};
DOC_SECTIONS.forEach(function(section) {
    section.items.forEach(function(item) {
        PATH_TO_SLUG[item.path] = item.slug;
    });
});

// ── SVG Icons ──
function getIconSVG(type) {
    var icons = {
        book: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M1 2.828c.885-.37 2.154-.769 4-.9 1.71-.12 3.372.09 5 .73V13.5a7.36 7.36 0 00-5-.7c-1.3-.12-2.47-.16-4-.25V2.828zm11 .4c1.71.27 2.93.54 4 .73V4.8c-.82-.13-1.7-.24-2.59-.33l-.63-.05-1.16-.22-1.38-.54v-1.1l.52.19c.42.16.85.32 1.28.46.66.22 1.28.41 1.83.53z"/><path d="M15 12.87c-.5-.08-1.13-.18-2-.28-1.41-.16-2.67-.04-3.86.26-1.2.3-2.25.66-3.14 1.02V4.66c1.04-.38 2.21-.65 3.5-.82 1.5-.2 2.82-.03 3.96.43.32.13.59.27.79.4.13.08.25.16.35.24.03.02.06.05.1.08.26.22.44.47.56.67.08.14.14.27.18.38.08.23.12.44.12.62v6.33z"/></svg>',
        map: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C5.2 0 3 2.2 3 5c0 3.4 5 11 5 11s5-7.6 5-11c0-2.8-2.2-5-5-5zm0 8c-1.7 0-3-1.3-3-3s1.3-3 3-3 3 1.3 3 3-1.3 3-3 3z"/></svg>',
        help: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 100 16A8 8 0 008 0zm.75 12.25h-1.5v-1.5h1.5v1.5zM9.5 8.5c-.5.31-.75.62-.75 1.25h-1.5c0-1 .42-1.56 1.06-2 .56-.39 1.19-.78 1.19-1.5 0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5H5A3 3 0 018 3.5c1.66 0 3 1.34 3 3 0 1.06-.58 1.56-1.5 2z"/></svg>',
        flow: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M8.5 1.5A1.5 1.5 0 0110 0h4a1.5 1.5 0 011.5 1.5v2A1.5 1.5 0 0114 5h-4a1.5 1.5 0 01-1.5-1.5v-2zM.5 8.5A1.5 1.5 0 012 7h4a1.5 1.5 0 011.5 1.5v5A1.5 1.5 0 016 15H2a1.5 1.5 0 01-1.5-1.5v-5zm0-6A1.5 1.5 0 012 1h4a1.5 1.5 0 011.5 1.5v.5A1.5 1.5 0 016 4.5H2A1.5 1.5 0 01.5 3v-.5zm8.5 5A1.5 1.5 0 018.5 6h4A1.5 1.5 0 0114 7.5v.5a1.5 1.5 0 01-1.5 1.5h-4A1.5 1.5 0 019 8v-.5z"/></svg>',
        rocket: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M12.17 9.17c-.67.67-1.43 1.08-2.17 1.25l-1.5 4.1L6.5 13c-.85-.85-2.12-1.16-3.38-1.06-.78-1.29.13-2.5.56-3.27.17-.74.58-1.5 1.25-2.17 1.24-1.24 3.28-1.44 4.58-.14l1.28 1.28c1.3 1.3 1.1 3.34-.14 4.58z"/><path d="M12.67 3.33c-1.56-1.56-4.37-1.3-6.28.61-.38.38-1-.38-.62-.77 1.91-1.91 4.72-2.28 6.9-.1.38.38-.33 1-.62.38z"/><path d="M13.43 2.57c.9-.9 1.8-.67 1.8-.67s.23.9-.67 1.8c-.89.89-1.8.67-1.8.67s-.23-.9.67-1.8z"/></svg>',
        pipeline: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M0 1.5A1.5 1.5 0 011.5 0h3A1.5 1.5 0 016 1.5V3h4V1.5A1.5 1.5 0 0111.5 0h3A1.5 1.5 0 0116 1.5v3A1.5 1.5 0 0114.5 6H13v4h1.5a1.5 1.5 0 011.5 1.5v3a1.5 1.5 0 01-1.5 1.5h-3a1.5 1.5 0 01-1.5-1.5V13H6v1.5A1.5 1.5 0 014.5 16h-3A1.5 1.5 0 010 14.5v-3A1.5 1.5 0 011.5 10H3V6H1.5A1.5 1.5 0 010 4.5v-3zM4 6v4h4V6H4zm1.5-4.5h-3v3h3v-3zm8 0h-3v3h3v-3zM4 11.5h-3v3h3v-3zm8 0h-3v3h3v-3z"/></svg>',
        template: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M2 1.5A1.5 1.5 0 013.5 0h9A1.5 1.5 0 0114 1.5v13a1.5 1.5 0 01-1.5 1.5h-9A1.5 1.5 0 012 14.5V1.5zM13 4H3v10.5c0 .27.23.5.5.5h9a.5.5 0 00.5-.5V4zM5 7a.5.5 0 01.5-.5h5a.5.5 0 010 1h-5A.5.5 0 015 7zm0 2.5a.5.5 0 01.5-.5h5a.5.5 0 010 1h-5a.5.5 0 01-.5-.5z"/></svg>',
        lang: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M0 2a2 2 0 012-2h12a2 2 0 012 2v8a2 2 0 01-2 2H9.5l-1.75 2.25a.75.75 0 01-1.2 0L4.5 12H2a2 2 0 01-2-2V2zm3.5 1a.5.5 0 000 1h1.6c.11.35.34.76.64 1.24.1.16.21.32.31.46.2.28.35.55.38.8h.04c.03-.25.18-.52.38-.8.1-.14.21-.3.31-.46.3-.48.53-.89.64-1.24h1.6a.5.5 0 000-1h-2.5a.5.5 0 000 1h.43c-.19.25-.42.57-.66.91-.2.28-.41.56-.56.75-.15-.19-.36-.47-.56-.75-.24-.34-.47-.66-.66-.91h.43a.5.5 0 000-1H3.5zm4 5c.22 0 .43.05.62.14.26.12.52.32.74.59.45.55.64 1.21.64 1.77 0 .56-.19 1.22-.64 1.77-.22.27-.48.47-.74.59A1.5 1.5 0 017.5 13a.5.5 0 010-1c.11 0 .28-.07.44-.23.17-.2.34-.5.41-.77h-.85a.5.5 0 010-1H8.5c0-.14-.06-.4-.28-.62a.6.6 0 00-.33-.2.5.5 0 01-.39-.18zM10.5 5a.5.5 0 01.42.24l1.5 2.5a.5.5 0 11-.86.5l-.56-.94-1.5 2.5a.5.5 0 11-.86-.5l1.5-2.5-1.5-2.5a.5.5 0 01.86-.5l.56.94.56-.94A.5.5 0 0110.5 5zm.28 1.74L11.5 8l.72-1.26H10.78z"/></svg>',
        experiment: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M6.5 1.5A1.5 1.5 0 018 0h2a1.5 1.5 0 010 3H8a1.5 1.5 0 01-1.5-1.5zM11 3.5A1.5 1.5 0 0112.5 2h1A1.5 1.5 0 0115 3.5v.78A2 2 0 0114 6.22V14a2 2 0 01-2 2H4a2 2 0 01-2-2V6.22A2 2 0 011 4.28V3.5A1.5 1.5 0 012.5 2h1A1.5 1.5 0 015 3.5v.5h6v-.5zM12 6H4v3h3v1H4v4h8V6z"/></svg>',
        audio: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M3 2.5a.5.5 0 01.5-.5h9a.5.5 0 01.5.5v11a.5.5 0 01-.5.5h-9a.5.5 0 01-.5-.5v-11zM8 4a2 2 0 100 4 2 2 0 000-4zm-2.5 5.5A1.5 1.5 0 007 11h2a1.5 1.5 0 001.5-1.5c0-.76-.56-1.38-1.3-1.48L8 7.5l-1.2.52A1.5 1.5 0 005.5 9.5z"/></svg>',
        handshake: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M8.5.5a.5.5 0 00-.9-.3L5.1 3.5H3a1 1 0 00-1 1v4a1 1 0 001 1h2.1l2.5 3.3a.5.5 0 00.9-.3V.5zM3.5 7a.5.5 0 110-1 .5.5 0 010 1z"/><path d="M13.5 7a.5.5 0 110-1 .5.5 0 010 1zm-.9-3.5a.5.5 0 00-.9.3v7.4a.5.5 0 00.9.3l2.4-3.2a.5.5 0 000-.6l-2.4-3.2z"/></svg>',
        globe: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 100 16A8 8 0 008 0zm0 14.5a6.5 6.5 0 010-13 6.5 6.5 0 010 13z"/><path d="M5.5 4.5a4 4 0 015 0l-.5.5A1.5 1.5 0 018 5.5 1.5 1.5 0 016.5 4l-.5-.5z"/><path d="M10.5 11.5a4 4 0 01-5 0l.5-.5A1.5 1.5 0 008 10.5 1.5 1.5 0 009.5 12l.5-.5z"/><path d="M8 4a2 2 0 100 4 2 2 0 000-4z"/><path d="M5 8h1.5v1.5H5z"/><path d="M9.5 8H11v1.5H9.5z"/></svg>',
        code: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M4.78 4.97a.75.75 0 010 1.06L2.81 8l1.97 1.97a.75.75 0 11-1.06 1.06l-2.5-2.5a.75.75 0 010-1.06l2.5-2.5a.75.75 0 011.06 0zm6.44 0a.75.75 0 011.06 0l2.5 2.5a.75.75 0 010 1.06l-2.5 2.5a.75.75 0 01-1.06-1.06L13.19 8l-1.97-1.97a.75.75 0 010-1.06zM9.18 3.3a.75.75 0 01.52.92l-2.5 9.5a.75.75 0 01-1.44-.4l2.5-9.5a.75.75 0 01.92-.52z"/></svg>',
        shield: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M8 .5a.5.5 0 01.5.5v1a.5.5 0 01-1 0V1A.5.5 0 018 .5zM8 15a.5.5 0 01-.5-.5v-1a.5.5 0 011 0v1a.5.5 0 01-.5.5z"/><path d="M8 0a8 8 0 100 16A8 8 0 008 0zM4 5a1 1 0 011-1h6a1 1 0 011 1v3.5c0 2.5-2 4-4 4s-4-1.5-4-4V5z"/><path d="M5 5.5A.5.5 0 015.5 5h5a.5.5 0 01.5.5v3c0 1.5-.9 3-3 3s-3-1.5-3-3v-3z"/></svg>',
        paper: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M0 1.5A1.5 1.5 0 011.5 0h9A1.5 1.5 0 0112 1.5V2h2.5A1.5 1.5 0 0116 3.5v10a1.5 1.5 0 01-1.5 1.5h-11A1.5 1.5 0 012 13.5V13H1.5A1.5 1.5 0 010 11.5v-10zM11 13V3.5a.5.5 0 00-.5-.5h-9a.5.5 0 00-.5.5v8a.5.5 0 00.5.5H11zm2.5-1H13V3.5a1.5 1.5 0 00-.5-1.1V11.5a.5.5 0 01-.5.5h-9a.5.5 0 010 1h10a.5.5 0 00.5-.5v-10a.5.5 0 00-.5-.5H12v10.5z"/></svg>',
        database: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C4.8 0 1 .9 1 3v10c0 2.1 3.8 3 7 3s7-.9 7-3V3c0-2.1-3.8-3-7-3zM2 13V9.5c1.2.8 3.5 1.5 6 1.5s4.8-.7 6-1.5V13c0 .8-2.5 2-6 2s-6-1.2-6-2zm0-5V5.5c1.2.8 3.5 1.5 6 1.5s4.8-.7 6-1.5V8c0 .8-2.5 2-6 2s-6-1.2-6-2zm12-4.5c0 .8-2.5 2-6 2s-6-1.2-6-2 2.5-2 6-2 6 1.2 6 2z"/></svg>',
        server: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M1 2.5A1.5 1.5 0 012.5 1h11A1.5 1.5 0 0115 2.5v2A1.5 1.5 0 0113.5 6h-11A1.5 1.5 0 011 4.5v-2zM1 8.5A1.5 1.5 0 012.5 7h11A1.5 1.5 0 0115 8.5v2A1.5 1.5 0 0113.5 12h-11A1.5 1.5 0 011 10.5v-2zm0 6A1.5 1.5 0 012.5 13h11a1.5 1.5 0 011.5 1.5v2a1.5 1.5 0 01-1.5 1.5h-11A1.5 1.5 0 011 16v-2z"/></svg>',
        lock: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a3 3 0 00-3 3v2H3.5A1.5 1.5 0 002 7.5v6A1.5 1.5 0 003.5 15h9a1.5 1.5 0 001.5-1.5v-6A1.5 1.5 0 0012.5 6H11V4a3 3 0 00-3-3zm2 5H6V4a2 2 0 114 0v2z"/></svg>',
        adr: '<svg class="sidebar-item-icon" viewBox="0 0 16 16" fill="currentColor"><path d="M2 1.5A1.5 1.5 0 013.5 0h9A1.5 1.5 0 0114 1.5v13a1.5 1.5 0 01-1.5 1.5h-9A1.5 1.5 0 012 14.5V1.5zM13 4H3v10.5c0 .27.23.5.5.5h9a.5.5 0 00.5-.5V4zM5 7a.5.5 0 01.5-.5h5a.5.5 0 010 1h-5A.5.5 0 015 7zm0 2.5a.5.5 0 01.5-.5h5a.5.5 0 010 1h-5a.5.5 0 01-.5-.5z"/></svg>',
    };
    return icons[type] || icons.book;
}

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

    var html = marked.parse(markdown);

    var titleMatch = markdown.match(/^#\s+(.+)/m);
    var title = titleMatch ? titleMatch[1].trim() : path.split('/').pop().replace('.md', '').replace(/_/g, ' ');
    docTitle.textContent = title;
    editOnGitHub.href = GITHUB_BLOB_BASE + path;

    markdownBody.innerHTML = (
        '<div class="markdown-body">' + html + '</div>' +
        '<div class="doc-source">' +
            '<span>Source: <a href="' + GITHUB_BLOB_BASE + path + '" target="_blank">' + path + '</a></span>' +
            '<span><a href="' + editOnGitHub.href + '" target="_blank">Edit on GitHub</a></span>' +
        '</div>'
    );

    renderedContentCache = markdownBody.textContent || '';

    rewriteRelativeLinks(path);

    if (typeof hljs !== 'undefined') {
        document.querySelectorAll('.markdown-body pre code').forEach(function(el) {
            hljs.highlightElement(el);
        });
    }

    addHeadingAnchors();
    addCopyButtons();
    buildToc();
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
