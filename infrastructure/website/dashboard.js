// LILA Lab Control Room — Dashboard JavaScript
// Laboratory aesthetic: data monitoring, network visualization, terminal-style counters

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

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

    // 1. BENI Index vs CPI
    var indexVsCpiCtx = document.getElementById('indexVsCpiChart');
    if (indexVsCpiCtx) {
        var months = [];
        var beniIndex = [];
        var cpi = [];
        var labels = [];

        for (var i = 0; i < 79; i++) {
            var year = 2014 + Math.floor(i / 12);
            var month = (i % 12) + 1;
            months.push(year + '-' + String(month).padStart(2, '0'));

            var baseIndex = 50 + Math.sin(i / 12 * Math.PI) * 20 + (Math.random() - 0.5) * 10;
            var baseCpi = 100 + i * 0.3 + Math.sin(i / 6 * Math.PI) * 5 + (Math.random() - 0.5) * 3;

            beniIndex.push(parseFloat(baseIndex.toFixed(1)));
            cpi.push(parseFloat(baseCpi.toFixed(1)));

            if (i % 6 === 0) {
                labels.push(months[i]);
            }
        }

        var beniFiltered = beniIndex.filter(function(_, idx) { return idx % 6 === 0; });
        var cpiFiltered = cpi.filter(function(_, idx) { return idx % 6 === 0; });

        new Chart(indexVsCpiCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'BENI Index',
                        data: beniFiltered,
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
                        data: cpiFiltered,
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

    // 2. Model Comparison
    var modelComparisonCtx = document.getElementById('modelComparisonChart');
    if (modelComparisonCtx) {
        new Chart(modelComparisonCtx, {
            type: 'bar',
            data: {
                labels: ['TF-IDF + LogReg', 'BanglaBERT', 'LLM (Claude)', 'LLM (GPT-4o)', 'Ensemble'],
                datasets: [{
                    label: 'Accuracy (%)',
                    data: [91.7, 89.2, 90.5, 89.8, 92.1],
                    backgroundColor: [
                        colors.cyan,
                        colors.gold,
                        colors.coral,
                        '#5B8DEF',
                        '#7C6FE0'
                    ],
                    borderRadius: 6,
                    barThickness: 36
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
                                return context.parsed.x + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        min: 85,
                        max: 95,
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

    // 3. Article Volume
    var articleVolumeCtx = document.getElementById('articleVolumeChart');
    if (articleVolumeCtx) {
        var volMonths = [];
        var volumes = [];

        for (var j = 0; j < 79; j++) {
            if (j % 6 === 0) {
                var vy = 2014 + Math.floor(j / 12);
                var vm = (j % 12) + 1;
                volMonths.push(vy + '-' + String(vm).padStart(2, '0'));
                volumes.push(Math.floor(8000 + Math.random() * 4000 + Math.sin(j / 12 * Math.PI) * 1000));
            }
        }

        new Chart(articleVolumeCtx, {
            type: 'bar',
            data: {
                labels: volMonths,
                datasets: [{
                    label: 'Articles',
                    data: volumes,
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
