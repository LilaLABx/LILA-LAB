// LILA Lab Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavigation();
    initStatCounters();
    initCharts();
    initScrollAnimations();
});

// Navigation Toggle
function initNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }
}

// Animated Stat Counters
function initStatCounters() {
    const statValues = document.querySelectorAll('.stat-value');

    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    statValues.forEach(stat => observer.observe(stat));
}

function animateCounter(element) {
    const target = parseFloat(element.dataset.target);
    const suffix = element.dataset.suffix || '';
    const duration = 2000;
    const start = performance.now();
    const isNegative = target < 0;
    const absTarget = Math.abs(target);
    const isDecimal = target % 1 !== 0;

    function update(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = absTarget * easeOutQuart;

        let displayValue;
        if (isDecimal) {
            displayValue = current.toFixed(2);
        } else {
            displayValue = Math.floor(current).toLocaleString();
        }

        if (isNegative) {
            displayValue = '-' + displayValue;
        }

        element.textContent = displayValue + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// Initialize Charts
function initCharts() {
    // Chart.js defaults
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.color = '#4A5568';

    // Color palette
    const colors = {
        teal: '#006D77',
        tealLight: 'rgba(0, 109, 119, 0.1)',
        gold: '#E29578',
        goldLight: 'rgba(226, 149, 120, 0.1)',
        coral: '#E76F51',
        coralLight: 'rgba(231, 111, 81, 0.1)',
        sand: '#FFDDD2',
        gray: '#A0AEC0'
    };

    // 1. BENI Index vs CPI Chart
    const indexVsCpiCtx = document.getElementById('indexVsCpiChart');
    if (indexVsCpiCtx) {
        // Generate sample data showing inverse correlation
        const months = [];
        const beniIndex = [];
        const cpi = [];

        for (let i = 0; i < 79; i++) {
            const year = 2014 + Math.floor(i / 12);
            const month = (i % 12) + 1;
            months.push(`${year}-${String(month).padStart(2, '0')}`);

            // Simulated inverse correlation
            const baseIndex = 50 + Math.sin(i / 12 * Math.PI) * 20 + (Math.random() - 0.5) * 10;
            const baseCpi = 100 + i * 0.3 + Math.sin(i / 6 * Math.PI) * 5 + (Math.random() - 0.5) * 3;

            beniIndex.push(baseIndex.toFixed(1));
            cpi.push(baseCpi.toFixed(1));
        }

        new Chart(indexVsCpiCtx, {
            type: 'line',
            data: {
                labels: months.filter((_, i) => i % 6 === 0), // Show every 6th month
                datasets: [
                    {
                        label: 'BENI Index',
                        data: beniIndex.filter((_, i) => i % 6 === 0),
                        borderColor: colors.teal,
                        backgroundColor: colors.tealLight,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        borderWidth: 2
                    },
                    {
                        label: 'CPI',
                        data: cpi.filter((_, i) => i % 6 === 0),
                        borderColor: colors.gold,
                        backgroundColor: colors.goldLight,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 5,
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
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(45, 55, 72, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.y;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxTicksLimit: 8
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'BENI Index'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'CPI'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    // 2. Model Comparison Chart
    const modelComparisonCtx = document.getElementById('modelComparisonChart');
    if (modelComparisonCtx) {
        new Chart(modelComparisonCtx, {
            type: 'bar',
            data: {
                labels: ['TF-IDF + LogReg', 'BanglaBERT', 'LLM (Claude)', 'LLM (GPT-4o)', 'Ensemble'],
                datasets: [{
                    label: 'Accuracy (%)',
                    data: [91.7, 89.2, 90.5, 89.8, 92.1],
                    backgroundColor: [
                        colors.teal,
                        colors.gold,
                        colors.coral,
                        '#9CD5F0',
                        '#88BFFF'
                    ],
                    borderRadius: 8,
                    barThickness: 40
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(45, 55, 72, 0.9)',
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
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // 3. Article Volume Chart
    const articleVolumeCtx = document.getElementById('articleVolumeChart');
    if (articleVolumeCtx) {
        // Generate monthly volume data
        const months = [];
        const volumes = [];

        for (let i = 0; i < 79; i++) {
            const year = 2014 + Math.floor(i / 12);
            const month = (i % 12) + 1;
            if (i % 6 === 0) {
                months.push(`${year}-${String(month).padStart(2, '0')}`);
                // Simulated volume with some variation
                volumes.push(Math.floor(8000 + Math.random() * 4000 + Math.sin(i / 12 * Math.PI) * 1000));
            }
        }

        new Chart(articleVolumeCtx, {
            type: 'bar',
            data: {
                labels: months,
                datasets: [{
                    label: 'Articles',
                    data: volumes,
                    backgroundColor: colors.tealLight,
                    borderColor: colors.teal,
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(45, 55, 72, 0.9)',
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y.toLocaleString() + ' articles';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxTicksLimit: 8
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return (value / 1000).toFixed(0) + 'K';
                            }
                        }
                    }
                }
            }
        });
    }

    // 4. Annotation Cost Chart
    const annotationCostCtx = document.getElementById('annotationCostChart');
    if (annotationCostCtx) {
        new Chart(annotationCostCtx, {
            type: 'doughnut',
            data: {
                labels: ['Claude ($0.02)', 'GPT-4o ($0.03)', 'Human ($0.50)'],
                datasets: [{
                    data: [0.02, 0.03, 0.50],
                    backgroundColor: [
                        colors.teal,
                        colors.gold,
                        colors.coral
                    ],
                    borderWidth: 0,
                    hoverOffset: 10
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
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(45, 55, 72, 0.9)',
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

// Scroll Animations
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.stat-card, .finding-card, .chart-card, .pipeline-card, .blog-card');

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
