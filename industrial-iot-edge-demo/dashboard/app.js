const machineGrid = document.querySelector("#machine-grid");
const alarmList = document.querySelector("#alarm-list");
const alarmCount = document.querySelector("#alarm-count");
const connectionState = document.querySelector("#connection-state");
const pulse = document.querySelector(".pulse");

function fmt(value, digits = 1) {
  return Number(value).toFixed(digits);
}

function statusClass(status) {
  return ["healthy", "warning", "critical"].includes(status) ? status : "warning";
}

function renderMachines(items) {
  if (!items.length) {
    machineGrid.innerHTML = '<article class="empty-state">Waiting for machine samples...</article>';
    return;
  }

  machineGrid.innerHTML = items.map((machine) => {
    const health = Math.max(0, Math.min(100, machine.health_score));
    const status = statusClass(machine.status);
    return `
      <article class="machine-card">
        <div class="card-top">
          <div>
            <h2>${machine.machine_id}</h2>
            <span class="source">${machine.source}</span>
          </div>
          <span class="badge ${status}">${machine.status}</span>
        </div>

        <div class="metrics">
          <div class="metric"><small>RPM</small><strong>${machine.rpm}</strong></div>
          <div class="metric"><small>Temp</small><strong>${fmt(machine.temperature_c)}°C</strong></div>
          <div class="metric"><small>Vibration</small><strong>${fmt(machine.vibration_mm_s, 2)}</strong></div>
          <div class="metric"><small>Current</small><strong>${fmt(machine.current_a, 2)}A</strong></div>
        </div>

        <div class="health">
          <div class="health-row"><span>Health score</span><strong>${health}%</strong></div>
          <div class="bar"><span style="width:${health}%"></span></div>
        </div>
      </article>`;
  }).join("");
}

function renderAlarms(items) {
  alarmCount.textContent = String(items.length);
  if (!items.length) {
    alarmList.innerHTML = '<p class="muted">No alarms yet.</p>';
    return;
  }

  alarmList.innerHTML = items.slice(0, 12).map((alarm) => {
    const time = new Date(alarm.timestamp).toLocaleTimeString();
    return `
      <div class="alarm-item ${alarm.severity}">
        <strong>${alarm.severity}</strong>
        <span>${alarm.machine_id}: ${alarm.message}</span>
        <span class="alarm-time">${time}</span>
      </div>`;
  }).join("");
}

async function refresh() {
  try {
    const [machinesRes, alarmsRes] = await Promise.all([
      fetch("/api/machines/latest"),
      fetch("/api/alarms"),
    ]);

    if (!machinesRes.ok || !alarmsRes.ok) throw new Error("API error");

    const machines = await machinesRes.json();
    const alarms = await alarmsRes.json();

    renderMachines(machines);
    renderAlarms(alarms);
    connectionState.textContent = "Online";
    pulse.classList.add("online");
  } catch (error) {
    connectionState.textContent = "Offline";
    pulse.classList.remove("online");
  }
}

refresh();
setInterval(refresh, 1000);
