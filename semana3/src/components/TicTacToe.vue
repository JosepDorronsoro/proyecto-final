<template>
  <section class="tictactoe">
    <h2>Tres en raya</h2>

    <div class="board">
      <button
        v-for="(cell, idx) in board"
        :key="idx"
        class="cell"
        @click="play(idx)"
      >
        {{ cell }}
      </button>
    </div>

    <div class="status">{{ status }}</div>

    <div class="controls">
      <button @click="reset">Reiniciar</button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const board = ref(Array(9).fill(null))
const current = ref('X')
const winner = ref(null)

function play(i) {
  if (board.value[i] || winner.value) return
  board.value[i] = current.value
  checkWinner()
  if (!winner.value) current.value = current.value === 'X' ? 'O' : 'X'
}

function checkWinner() {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ]
  for (const [a, b, c] of lines) {
    if (
      board.value[a] &&
      board.value[a] === board.value[b] &&
      board.value[a] === board.value[c]
    ) {
      winner.value = board.value[a]
      return
    }
  }
  if (board.value.every(Boolean)) winner.value = 'Empate'
}

function reset() {
  board.value = Array(9).fill(null)
  current.value = 'X'
  winner.value = null
}

const status = computed(() => {
  if (winner.value)
    return winner.value === 'Empate'
      ? 'Empate'
      : `Ganador: ${winner.value}`
  return `Turno: ${current.value}`
})
</script>

<style scoped>
.tictactoe {
  margin-top: 1rem;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.board {
  display: grid;
  grid-template-columns: repeat(3, 64px);
  gap: 8px;
  margin: 1rem 0;
}
.cell {
  width: 64px;
  height: 64px;
  font-size: 1.2rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  background: #fafafa;
}
.status {
  margin-bottom: 0.5rem;
}
.controls button {
  padding: 0.4rem 0.6rem;
}
</style>
