import { state } from './state/state.js'
import { fetchMatches, fetchPlayers, fetchStaffMembers, generateConvocation, refineConvocation } from './services/api.js'
import { renderMatchSelector, renderStaffCheckboxes, renderPlayerTable, renderGeneratedMessage, renderRefinedMessage, renderError, clearError } from './ui/render.js'

async function initApp() {
  try {
    const [matches, players, staffMembers] = await Promise.all([
      fetchMatches(),
      fetchPlayers(),
      fetchStaffMembers()
    ])
    state.matches = matches
    state.players = players
    state.staffMembers = staffMembers
    renderMatchSelector(state.matches)
    renderStaffCheckboxes(state.staffMembers)
    renderPlayerTable(state.players)
  } catch (error) {
    const el = document.getElementById('startup-error')
    el.textContent = 'Error al cargar datos del backend. Verifica la conexión y recarga la página.'
    el.classList.remove('hidden')
  }
}

async function handleGenerate() {
  clearError('generate')

  const matchIdRaw = parseInt(document.getElementById('match-select').value)
  if (isNaN(matchIdRaw) || matchIdRaw === 0) {
    renderError('generate', 'Selecciona un partido.')
    return
  }

  const convocationTime = document.getElementById('convocation-time').value
  if (convocationTime === '') {
    renderError('generate', 'Introduce la hora de convocatoria.')
    return
  }

  const selectedStaffIds = Array.from(document.querySelectorAll('.staff-checkbox'))
    .filter(el => el.checked)
    .map(el => parseInt(el.value))

  const excludedPlayerIds = []
  const playerInnings = {}

  const rows = document.querySelectorAll('#player-tbody tr')
  for (const tr of rows) {
    const checkbox = tr.querySelector('.player-checkbox')
    const inningsInput = tr.querySelector('.innings-input')
    if (!checkbox) continue
    const playerId = parseInt(checkbox.value)
    if (!checkbox.checked) {
      excludedPlayerIds.push(playerId)
    } else if (inningsInput.value.trim() !== '') {
      playerInnings[String(playerId)] = inningsInput.value.trim()
    }
  }

  const invitedPlayers = []
  const invitedRows = document.querySelectorAll('#invited-list .invited-row')
  for (const row of invitedRows) {
    const name = row.querySelector('.invited-name').value.trim()
    if (name === '') continue
    const numberRaw = row.querySelector('.invited-number').value.trim()
    const numberParsed = parseInt(numberRaw)
    if (numberRaw !== '' && !isNaN(numberParsed)) {
      invitedPlayers.push({ name, number: numberParsed })
    } else {
      invitedPlayers.push({ name })
    }
  }

  const notesRaw = document.getElementById('manual-notes').value
  const manualNotes = notesRaw.split('\n').filter(line => line.trim() !== '')

  const payload = {
    match_id: matchIdRaw,
    convocation_time: convocationTime,
    selected_staff_ids: selectedStaffIds,
    player_innings: playerInnings,
    excluded_player_ids: excludedPlayerIds,
    invited_players: invitedPlayers,
    manual_notes: manualNotes
  }

  const btn = document.getElementById('generate-btn')
  btn.disabled = true
  btn.textContent = 'Generando...'

  try {
    const data = await generateConvocation(payload)
    state.generatedMessage = data.rendered_message
    state.criticalFragments = data.critical_fragments
    state.refinedMessage = ''
    renderGeneratedMessage(state.generatedMessage)
  } catch (error) {
    renderError('generate', 'Error al generar la convocatoria: ' + error.message)
  } finally {
    btn.disabled = false
    btn.textContent = 'Generar convocatoria'
  }
}

async function handleRefine() {
  clearError('refine')

  if (state.generatedMessage === '') {
    renderError('refine', 'Genera el mensaje primero.')
    return
  }

  const style = document.getElementById('refine-style').value.trim() || null

  const payload = {
    message: state.generatedMessage,
    critical_fragments: state.criticalFragments,
    style: style
  }

  const btn = document.getElementById('refine-btn')
  btn.disabled = true
  btn.textContent = 'Refinando...'

  try {
    const data = await refineConvocation(payload)
    state.refinedMessage = data.refined_message
    renderRefinedMessage(state.refinedMessage)
  } catch (error) {
    renderError('refine', 'Error al refinar: ' + error.message)
  } finally {
    btn.disabled = false
    btn.textContent = 'Refinar con IA'
  }
}

async function handleCopy() {
  const message = state.refinedMessage !== '' ? state.refinedMessage : state.generatedMessage
  const btn = document.getElementById('copy-btn')

  try {
    await navigator.clipboard.writeText(message)
    btn.textContent = '¡Copiado!'
    setTimeout(() => { btn.textContent = 'Copiar mensaje' }, 1500)
  } catch {
    btn.textContent = 'Error al copiar'
    setTimeout(() => { btn.textContent = 'Copiar mensaje' }, 1500)
  }
}

function addInvitedRow() {
  const row = document.createElement('div')
  row.className = 'invited-row'

  const nameInput = document.createElement('input')
  nameInput.type = 'text'
  nameInput.className = 'invited-name'
  nameInput.placeholder = 'Nombre del jugador'

  const numberInput = document.createElement('input')
  numberInput.type = 'text'
  numberInput.className = 'invited-number'
  numberInput.placeholder = '#'

  const removeBtn = document.createElement('button')
  removeBtn.type = 'button'
  removeBtn.className = 'remove-invited-btn'
  removeBtn.textContent = 'Eliminar'
  removeBtn.addEventListener('click', () => row.remove())

  row.appendChild(nameInput)
  row.appendChild(numberInput)
  row.appendChild(removeBtn)

  document.getElementById('invited-list').appendChild(row)
}

document.getElementById('generate-btn').addEventListener('click', handleGenerate)
document.getElementById('refine-btn').addEventListener('click', handleRefine)
document.getElementById('copy-btn').addEventListener('click', handleCopy)
document.getElementById('add-invited-btn').addEventListener('click', addInvitedRow)

initApp()
