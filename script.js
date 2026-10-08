// Keep every project visible when JavaScript is unavailable.
const filters = document.querySelector('.project-filters');
const cards = document.querySelectorAll('#projects .project-card');
const filterStatus = document.querySelector('#filter-status');

if (filters) {
  filters.hidden = false;

  filters.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;

    const category = button.dataset.filter;
    let visibleCount = 0;

    filters.querySelectorAll('button').forEach((filter) => {
      filter.setAttribute('aria-pressed', String(filter === button));
    });

    cards.forEach((card) => {
      const matches = category === 'all' || card.dataset.category.split(' ').includes(category);
      card.hidden = !matches;
      if (matches) visibleCount += 1;
    });

    filterStatus.textContent = `${visibleCount} projects shown.`;
  });
}
