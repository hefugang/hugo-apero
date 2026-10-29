(() => {
  const root = document.querySelector('[data-training-pathway]');
  if (!root) return;
  const tabs = [...root.querySelectorAll('[data-training-tab]')];
  const title = root.querySelector('[data-training-title]');
  const body = root.querySelector('[data-training-body]');
  const tags = root.querySelector('[data-training-tags]');
  const index = root.querySelector('[data-training-index]');
  const progress = root.querySelector('[data-training-progress]');
  const counter = root.querySelector('[data-training-counter]');
  const next = root.querySelector('[data-training-next]');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const items = [
    { title: 'Physical and Technical Foundations', body: 'Build consistent conditioning, movement quality, basic first aid, and equipment handling around real operational tasks.', tags: ['Fitness assessment','Movement and control','Safety fundamentals'] },
    { title: 'Tactical and Firearms Safety', body: 'Organize training around risk recognition, communication, and lawful use of force. All firearms content requires certified instructors and a compliant training site.', tags: ['Firearms safety','Scenario judgment','Proportionality'] },
    { title: 'Command and Coordination', body: 'Connect information, command decisions, task allocation, and field execution in one training map, with emphasis on cross-team communication and resource coordination.', tags: ['Information assessment','Task allocation','Team coordination'] },
    { title: 'Review & Transfer', body: 'Use structured review to record decisions, actions, and outcomes, turning each exercise into reusable curriculum resources and the next improvement task.', tags: ['After-action review','Evidence capture','Curriculum updates'] }
  ];
  let current = 0;
  const render = (nextIndex, focus = false) => {
    current = (nextIndex + items.length) % items.length;
    const item = items[current];
    tabs.forEach((tab, i) => {
      const selected = i === current;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && focus) tab.focus();
    });
    title.textContent = item.title;
    body.textContent = item.body;
    tags.replaceChildren(...item.tags.map(tag => { const el = document.createElement('span'); el.textContent = tag; return el; }));
    index.textContent = String(current + 1).padStart(2, '0');
    progress.style.width = `${(current + 1) * 25}%`;
    counter.textContent = `${String(current + 1).padStart(2, '0')} / 04`;
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => render(i));
    tab.addEventListener('keydown', event => {
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') { event.preventDefault(); render(i + 1, true); }
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') { event.preventDefault(); render(i - 1, true); }
      if (event.key === 'Home') { event.preventDefault(); render(0, true); }
      if (event.key === 'End') { event.preventDefault(); render(items.length - 1, true); }
    });
  });
  next?.addEventListener('click', () => render(current + 1));
  render(0);

  const scenario = document.querySelector('[data-scenario-lab]');
  if (scenario) {
    const choices = [...scenario.querySelectorAll('[data-scenario-choice]')];
    const title = scenario.querySelector('[data-scenario-title]');
    const body = scenario.querySelector('[data-scenario-body]');
    const metrics = scenario.querySelector('[data-scenario-metrics]');
    const cases = [
      ['Field enforcement and use-of-force decisions', 'Design decision exercises around field information, communication, proportionality, and after-action records.', ['Information judgment','De-escalation communication','Proportionality']],
      ['Major-event traffic and public-order management', 'Simulate pre-event planning, field command, traffic organization, and coordination during disruptions.', ['Task allocation','Command communication','Resource dispatch']],
      ['Railway emergency incident response', 'Connect the full response chain from risk recognition and passenger protection to reporting and post-incident improvement.', ['Risk recognition','Passenger protection','After-action review']]
    ];
    const selectScenario = index => {
      const item = cases[index];
      choices.forEach((choice, i) => choice.setAttribute('aria-selected', String(i === index)));
      title.textContent = item[0]; body.textContent = item[1];
      metrics.replaceChildren(...item[2].map(label => { const el = document.createElement('span'); el.textContent = label; return el; }));
    };
    choices.forEach((choice, index) => choice.addEventListener('click', () => selectScenario(index)));
    selectScenario(0);
  }

  const filter = document.querySelector('[data-research-filter]');
  if (filter) {
    const buttons = [...filter.querySelectorAll('[data-research-category]')];
    const items = [...filter.querySelectorAll('[data-research-item]')];
    const count = filter.querySelector('[data-research-count]');
    buttons.forEach(button => button.addEventListener('click', () => {
      const category = button.dataset.researchCategory;
      buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      let visible = 0;
      items.forEach(item => { const show = category === 'all' || item.dataset.researchGroup === category; item.hidden = !show; if (show) visible++; });
      count.textContent = `${visible} outputs`;
    }));
  }
})();
