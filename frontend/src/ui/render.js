import { state } from '../state/state.js'

export function renderMatchSelector(matches) {
  const select = document.getElementById('match-select')
  select.innerHTML = ''

  if (matches.length === 0) {
    const option = document.createElement('option')
    option.disabled = true
    option.textContent = 'No matches available'
    select.appendChild(option)
    return
  }

  for (const match of matches) {
    const option = document.createElement('option')
    option.value = match.id

    const [year, month, day] = match.match_date.split('-')
    const formattedDate = `${day}/${month}/${year}`
    const formattedTime = match.match_time.slice(0, 5)

    option.textContent = `${match.home_team} vs ${match.away_team} — ${formattedDate} — ${formattedTime}`
    select.appendChild(option)
  }
}

export function renderStaffCheckboxes(staff) {
  const container = document.getElementById('staff-list')
  container.innerHTML = ''

  if (staff.length === 0) {
    const p = document.createElement('p')
    p.textContent = 'No staff members available.'
    container.appendChild(p)
    return
  }

  for (const member of staff) {
    const label = document.createElement('label')

    const checkbox = document.createElement('input')
    checkbox.type = 'checkbox'
    checkbox.className = 'staff-checkbox'
    checkbox.value = member.id
    checkbox.checked = true

    label.appendChild(checkbox)
    label.appendChild(document.createTextNode(` ${member.name} — ${member.role}`))
    container.appendChild(label)
  }
}

export function renderPlayerTable(players) {
  const tbody = document.getElementById('player-tbody')
  tbody.innerHTML = ''

  if (players.length === 0) {
    const tr = document.createElement('tr')
    const td = document.createElement('td')
    td.colSpan = 3
    td.textContent = 'No players available.'
    tr.appendChild(td)
    tbody.appendChild(tr)
    return
  }

  for (const player of players) {
    const tr = document.createElement('tr')

    const tdCheckbox = document.createElement('td')
    const checkbox = document.createElement('input')
    checkbox.type = 'checkbox'
    checkbox.className = 'player-checkbox'
    checkbox.value = player.id
    checkbox.checked = true
    tdCheckbox.appendChild(checkbox)

    const tdName = document.createElement('td')
    tdName.textContent = player.number !== null ? `#${player.number} ${player.name}` : player.name

    const tdInnings = document.createElement('td')
    const inningsInput = document.createElement('input')
    inningsInput.type = 'text'
    inningsInput.className = 'innings-input'
    inningsInput.dataset.playerId = player.id
    inningsInput.placeholder = '?/?'
    inningsInput.value = ''
    tdInnings.appendChild(inningsInput)

    tr.appendChild(tdCheckbox)
    tr.appendChild(tdName)
    tr.appendChild(tdInnings)
    tbody.appendChild(tr)
  }
}

export function renderGeneratedMessage(message) {
  document.getElementById('generated-message').value = message
  const section = document.getElementById('output-section')
  section.classList.remove('hidden')
  section.style.display = 'block'
}

export function renderRefinedMessage(message) {
  document.getElementById('refined-message').value = message
  const section = document.getElementById('refined-section')
  section.classList.remove('hidden')
  section.style.display = 'block'
}

export function renderError(sectionId, message) {
  const el = document.getElementById(`${sectionId}-error`)
  el.textContent = message
  el.classList.remove('hidden')
}

export function clearError(sectionId) {
  const el = document.getElementById(`${sectionId}-error`)
  el.textContent = ''
  el.classList.add('hidden')
}
