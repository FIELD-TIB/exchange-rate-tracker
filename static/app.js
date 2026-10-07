// The front-end script pulls data from the Flask API and updates the screen.
// It is intentionally simple and lightweight, which fits the low-latency requirement.

async function loadLatestRate() {
  const response = await fetch('/api/rates/latest');
  if (!response.ok) {
    document.getElementById('latest-rate').textContent = 'No data';
    document.getElementById('updated-at').textContent = 'Waiting for first update';
    return;
  }

  const data = await response.json();
  document.getElementById('latest-rate').textContent = Number(data.rate).toFixed(4);
  const time = new Date(data.fetched_at);
  document.getElementById('updated-at').textContent = time.toLocaleString();
}

async function loadHistory() {
  const response = await fetch('/api/rates/history?limit=12');
  if (!response.ok) {
    document.getElementById('history-table-body').innerHTML = '<tr><td colspan="2">No history available.</td></tr>';
    return;
  }

  const data = await response.json();
  const rows = data.history || [];

  if (rows.length === 0) {
    document.getElementById('history-table-body').innerHTML = '<tr><td colspan="2">No saved updates yet.</td></tr>';
    return;
  }

  const body = rows
    .slice()
    .reverse()
    .map((row) => {
      const time = new Date(row.fetched_at).toLocaleString();
      return `<tr><td>${time}</td><td>${Number(row.rate).toFixed(4)}</td></tr>`;
    })
    .join('');

  document.getElementById('history-table-body').innerHTML = body;
}

(async function init() {
  await loadLatestRate();
  await loadHistory();
})();
