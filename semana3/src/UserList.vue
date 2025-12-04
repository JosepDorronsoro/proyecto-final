<template>
  <div>
    <form @submit.prevent="addTodo">
      <input __________(2)__________="newTodoText" placeholder="Nueva tarea">
      <button>Añadir</button>
    </form>
    
    <ul>
      <TodoItem
        __________(3)__________="item in todos"
        __________(4)__________="item.id"
        :todo="__________(5)_________"
        __________(6)__________="handleToggle"
      />
    </ul>
  </div>
</template>

<script setup>
import { __________(7)_________ } from 'vue';

// --- ESTADO DEL COMPONENTE PADRE ---
const newTodoText = __________(7)_________('');
const todos = __________(7)_________([
  { id: 1, text: 'Aprender Vue', done: false },
  { id: 2, text: 'Hacer ejercicio', done: true }
]);
let nextId = 3;

// --- MÉTODOS DEL COMPONENTE PADRE ---
function __________(1)__________() {
  if (newTodoText.value.trim() === '') return;
  todos.value.push({
    id: nextId++,
    text: newTodoText.value,
    done: false
  });
  newTodoText.value = '';
}

function __________(8)_________(id) {
  const todo = todos.value.find(t => t.id === id);
  if (todo) {
    todo.done = !todo.done;
  }
}

// --- DEFINICIÓN DEL COMPONENTE HIJO (TodoItem) ---

// Definimos el componente hijo aquí mismo para el ejercicio
const TodoItem = {
  // 9. Define las 'props' que este componente espera recibir
  props: __________(9)_________(AQUÍ_FALTARÍA_UN_ARRAY), 
  
  // 10. Define los eventos personalizados que este componente puede emitir
  emits: __________(10)_________(AQUÍ_FALTARÍA_UN_ARRAY),

  // 11. El 'template' para cada 'TodoItem'
  template: `
    <li>
      <span __________(11)__________="{ done: todo.done }">
        {{ todo.text }}
      </span>
      <button __________(12)__________="$emit('toggle-done', todo.id)">
        Marcar
      </button>
    </li>
  `
};

</script>

<style>
/* 13. Estilo para la clase 'done' */
.done {
  text-decoration: line-through;
  opacity: 0.6;
}
</style>