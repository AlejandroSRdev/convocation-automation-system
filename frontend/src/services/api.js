import { API_BASE_URL } from '../config.js'

export async function fetchMatches() {
  const response = await fetch(`${API_BASE_URL}/matches/`)
  if (!response.ok) throw new Error(`Failed to fetch matches: ${response.status}`)
  return response.json()
}

export async function fetchPlayers() {
  const response = await fetch(`${API_BASE_URL}/players/`)
  if (!response.ok) throw new Error(`Failed to fetch players: ${response.status}`)
  return response.json()
}

export async function fetchStaffMembers() {
  const response = await fetch(`${API_BASE_URL}/staff-members/`)
  if (!response.ok) throw new Error(`Failed to fetch staff members: ${response.status}`)
  return response.json()
}

export async function generateConvocation(payload) {
  const response = await fetch(`${API_BASE_URL}/convocations/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!response.ok) throw new Error(`Failed to generate convocation: ${response.status}`)
  return response.json()
}

export async function refineConvocation(payload) {
  const response = await fetch(`${API_BASE_URL}/convocations/refine`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!response.ok) throw new Error(`Failed to refine convocation: ${response.status}`)
  return response.json()
}
