<template>
<div class="search-bar">
<input
v-model="localQuery"
type="search"
placeholder="Buscar por palabra (nombre o descripción)"
@keyup.enter.prevent
/>


<div class="controls">
<label>
Orden:
<select v-model="localSort">
<option value="desc">Más recientes</option>
<option value="asc">Más antiguos</option>
</select>
</label>


<button @click="clear">Limpiar</button>
</div>
</div>
</template>


<script setup>
import { ref, watch } from 'vue'


const props = defineProps({
query: { type: String, default: '' },
sort: { type: String, default: 'desc' }
})
const emit = defineEmits(['update:query', 'update:sort', 'clear'])


const localQuery = ref(props.query)
const localSort = ref(props.sort)


watch(localQuery, (v) => emit('update:query', v))
watch(localSort, (v) => emit('update:sort', v))


function clear() {
localQuery.value = ''
emit('clear')
}


</script>


<style scoped>
.search-bar{display:flex;gap:1rem;align-items:center}
.search-bar input{flex:1;padding:.5rem;border-radius:6px;border:1px solid #ccc}
.controls{display:flex;gap:.5rem;align-items:center}
.controls select{padding:.3rem}
.controls button{padding:.4rem .6rem;border-radius:6px;border:none;background:#eee}
</style>