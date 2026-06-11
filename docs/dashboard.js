// LILA Lab Control Room — Dashboard JavaScript
// Laboratory aesthetic: data monitoring, network visualization, terminal-style counters

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    initTheme();
    initNavigation();
    initStatCounters();
    initCharts();
    initScrollAnimations();
    initNavbarScroll();
    smoothScroll();
});

// ── Navigation Toggle ──
function initNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            navLinks.classList.toggle('open');
            document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
        });

        navLinks.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                navToggle.classList.remove('active');
                navLinks.classList.remove('open');
                document.body.style.overflow = '';
            });
        });
    }
}

// ── Navbar Scroll Effect ──
function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    var lastScroll = 0;
    window.addEventListener('scroll', function() {
        var currentScroll = window.pageYOffset;
        if (currentScroll > 60) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        lastScroll = currentScroll;
    }, { passive: true });
}

// ── Animated Stat Counters (Terminal-style) ──
function initStatCounters() {
    const statValues = document.querySelectorAll('.stat-value');

    if (!statValues.length) return;

    var observerOptions = { threshold: 0.5, rootMargin: '0px' };

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    statValues.forEach(function(stat) {
        observer.observe(stat);
    });
}

function animateCounter(element) {
    var target = parseFloat(element.getAttribute('data-target'));
    var suffix = element.getAttribute('data-suffix') || '';
    var duration = 2000;
    var start = performance.now();
    var isNegative = target < 0;
    var absTarget = Math.abs(target);
    var isDecimal = target % 1 !== 0;

    function update(currentTime) {
        var elapsed = currentTime - start;
        var progress = Math.min(elapsed / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 4);
        var current = absTarget * eased;

        var displayValue;
        if (isDecimal) {
            displayValue = current.toFixed(2);
        } else {
            displayValue = Math.floor(current).toLocaleString();
        }

        if (isNegative) {
            displayValue = 'r = −' + displayValue;
        }

        element.textContent = displayValue + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// ── Charts (Dark Theme) ──
function initCharts() {
    // Chart.js dark defaults
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.color = '#8899AA';

    var colors = {
        cyan: '#00D4E0',
        cyanDim: 'rgba(0, 212, 224, 0.1)',
        gold: '#E29578',
        goldDim: 'rgba(226, 149, 120, 0.1)',
        coral: '#E76F51',
        coralDim: 'rgba(231, 111, 81, 0.1)',
        sand: '#FFDDD2',
        gray: '#5A7A8A',
        gridColor: 'rgba(255, 255, 255, 0.04)',
        tooltipBg: 'rgba(7, 18, 21, 0.95)'
    };

    // 1. BENI Index vs CPI — Real data from exploration pipeline (79 months, 2014–2020)
    var months = ["2014-06","2014-07","2014-08","2014-09","2014-10","2014-11","2014-12","2015-01","2015-02","2015-03","2015-04","2015-05","2015-06","2015-07","2015-08","2015-09","2015-10","2015-11","2015-12","2016-01","2016-02","2016-03","2016-04","2016-05","2016-06","2016-07","2016-08","2016-09","2016-10","2016-11","2016-12","2017-01","2017-02","2017-03","2017-04","2017-05","2017-06","2017-07","2017-08","2017-09","2017-10","2017-11","2017-12","2018-01","2018-02","2018-03","2018-04","2018-05","2018-06","2018-07","2018-08","2018-09","2018-10","2018-11","2018-12","2019-01","2019-02","2019-03","2019-04","2019-05","2019-06","2019-07","2019-08","2019-09","2019-10","2019-11","2019-12","2020-01","2020-02","2020-03","2020-04","2020-05","2020-06","2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"];
    var beniIndex = [137.6,138.1,135.7,137.1,133.2,135.8,134.0,104.0,103.0,105.0,102.0,105.5,107.1,103.6,100.7,101.2,100.1,100.1,101.0,102.7,102.2,105.1,102.9,101.5,105.5,99.8,101.5,101.8,102.4,103.1,103.0,103.7,102.6,103.9,104.7,102.0,103.3,98.0,98.5,98.7,97.6,100.1,98.5,96.7,97.5,97.4,97.5,97.2,98.8,98.1,95.8,96.8,95.8,94.7,94.4,98.7,98.1,98.4,97.0,100.0,100.8,99.6,97.7,99.4,98.3,98.9,98.4,101.5,102.2,101.1,104.7,102.1,102.1,101.5,98.3,100.0,98.0,96.7,97.8];
    var cpi = [64.0,65.0,65.8,66.8,67.2,67.2,67.5,68.3,68.5,68.7,68.7,67.9,68.0,69.1,69.9,70.9,71.4,71.3,71.7,72.4,72.3,72.6,72.6,71.6,71.7,72.8,73.6,74.8,75.4,75.1,75.3,76.2,76.2,76.5,76.6,75.7,76.0,76.9,78.0,79.4,79.9,79.6,79.6,80.6,80.5,80.8,80.9,79.9,80.2,81.1,82.3,83.7,84.2,83.9,83.9,85.0,84.9,85.3,85.4,84.4,84.7,85.7,86.8,88.4,88.8,88.9,88.7,89.8,89.6,90.0,90.5,88.9,89.7,90.4,91.7,93.6,94.6,93.8,93.4];
    var labels = ["2014-06","2014-12","2015-06","2015-12","2016-06","2016-12","2017-06","2017-12","2018-06","2018-12","2019-06","2019-12","2020-06","2020-12"];

    var indexVsCpiCtx = document.getElementById('indexVsCpiChart');
    if (indexVsCpiCtx) {

        new Chart(indexVsCpiCtx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'BENI Index',
                        data: beniIndex,
                        borderColor: colors.cyan,
                        backgroundColor: colors.cyanDim,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        pointHoverBackgroundColor: colors.cyan,
                        borderWidth: 2
                    },
                    {
                        label: 'CPI',
                        data: cpi,
                        borderColor: colors.gold,
                        backgroundColor: colors.goldDim,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        pointHoverBackgroundColor: colors.gold,
                        borderWidth: 2,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            color: '#E8E6E3'
                        }
                    },
                    tooltip: {
                        backgroundColor: colors.tooltipBg,
                        titleColor: '#00D4E0',
                        bodyColor: '#E8E6E3',
                        borderColor: 'rgba(0, 212, 224, 0.2)',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: {
                            maxTicksLimit: 8,
                            color: '#5A7A8A'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'BENI Index',
                            color: '#00D4E0'
                        },
                        grid: {
                            color: colors.gridColor
                        },
                        ticks: { color: '#5A7A8A' }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'CPI',
                            color: '#E29578'
                        },
                        grid: {
                            drawOnChartArea: false
                        },
                        ticks: { color: '#5A7A8A' }
                    }
                }
            }
        });
    }

    // 2. Model Comparison — Real results + planned benchmarks
    var modelComparisonCtx = document.getElementById('modelComparisonChart');
    if (modelComparisonCtx) {
        new Chart(modelComparisonCtx, {
            type: 'bar',
            data: {
                labels: [
                    'TF-IDF (Unified 933K)',
                    'TF-IDF (Potrika Pilot)',
                    'BanglaBERT-small',
                    'BanglaBERT',
                    'Bangla-BERT-base',
                    'sahajBERT',
                    'mBERT',
                    'XLM-RoBERTa'
                ],
                datasets: [{
                    label: 'Accuracy (%)',
                    data: [94.77, 91.7, null, null, null, null, null, null],
                    backgroundColor: [
                        colors.cyan,
                        colors.sand,
                        '#3A5A6A',
                        '#3A5A6A',
                        '#3A5A6A',
                        '#3A5A6A',
                        '#3A5A6A',
                        '#3A5A6A'
                    ],
                    borderRadius: 6,
                    barThickness: 28
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: colors.tooltipBg,
                        titleColor: '#E8E6E3',
                        bodyColor: '#00D4E0',
                        borderColor: 'rgba(0, 212, 224, 0.2)',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                if (context.parsed.x === null) {
                                    return 'Kaggle GPU training planned';
                                }
                                return context.parsed.x + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        min: 80,
                        max: 100,
                        grid: { color: colors.gridColor },
                        ticks: {
                            color: '#5A7A8A',
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: '#8899AA' }
                    }
                }
            }
        });
    }

    // 3. Article Volume — Real monthly article counts from exploration pipeline
    var articleVolumes = [85,385,423,433,374,403,413,2066,2113,1984,2351,2271,2137,2768,3146,2916,3050,2836,3055,5624,7256,7442,7190,7854,8382,7465,7924,7632,7482,7166,6642,6943,6398,6396,6021,5923,5609,6609,6814,6156,7136,7229,6775,7246,6673,6759,6868,8197,7925,9122,9148,10173,9856,8585,7090,6327,6172,6569,6266,6121,5960,6409,6115,7118,7028,6673,6229,7813,7048,7457,6086,6130,7905,8103,7446,9487,9068,10421,10853];

    var articleVolumeCtx = document.getElementById('articleVolumeChart');
    if (articleVolumeCtx) {
        new Chart(articleVolumeCtx, {
            type: 'bar',
            data: {
                labels: months,
                datasets: [{
                    label: 'Articles',
                    data: articleVolumes,
                    backgroundColor: 'rgba(0, 212, 224, 0.15)',
                    borderColor: colors.cyan,
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: colors.tooltipBg,
                        titleColor: '#E8E6E3',
                        bodyColor: '#00D4E0',
                        borderColor: 'rgba(0, 212, 224, 0.2)',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y.toLocaleString() + ' articles';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: {
                            maxTicksLimit: 8,
                            color: '#5A7A8A'
                        }
                    },
                    y: {
                        grid: { color: colors.gridColor },
                        ticks: {
                            color: '#5A7A8A',
                            callback: function(value) {
                                return (value / 1000).toFixed(0) + 'K';
                            }
                        }
                    }
                }
            }
        });
    }

    // 4. Annotation Cost
    var annotationCostCtx = document.getElementById('annotationCostChart');
    if (annotationCostCtx) {
        new Chart(annotationCostCtx, {
            type: 'doughnut',
            data: {
                labels: ['Claude ($0.02)', 'GPT-4o ($0.03)', 'Human ($0.50)'],
                datasets: [{
                    data: [0.02, 0.03, 0.50],
                    backgroundColor: [
                        colors.cyan,
                        colors.gold,
                        colors.coral
                    ],
                    borderWidth: 0,
                    hoverOffset: 12
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            color: '#E8E6E3'
                        }
                    },
                    tooltip: {
                        backgroundColor: colors.tooltipBg,
                        titleColor: '#E8E6E3',
                        bodyColor: '#00D4E0',
                        borderColor: 'rgba(0, 212, 224, 0.2)',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                return context.label + ' per article';
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });
    }
}

// ── Scroll Animations ──
function initScrollAnimations() {
    var fadeSections = document.querySelectorAll('.fade-section');

    if (!fadeSections.length) return;

    var sectionObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                sectionObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    });

    fadeSections.forEach(function(section) {
        sectionObserver.observe(section);
    });
}

// ── Smooth Scroll for Anchor Links ──
function smoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            var href = this.getAttribute('href');
            if (href === '#') return;
            e.preventDefault();
            var target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ── Theme Toggle ──
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
