<template>
<footer class="keywords-footer">
<div v-if="keywords.length">
<strong>Keywords:</strong>
<span
v-for="k in keywords"
:key="k.word"
class="chip"
@click="clickKeyword(k.word)">
{{ k.word }}<small v-if="k.count"> ({{ k.count }})</small>
</span>
</div>
<div v-else>
<em>No hay palabras clave por mostrar.</em>
</div>
</footer>
</template>


<script setup>
import { computed } from 'vue'


const props = defineProps({
games: { type: Array, default: () => [] },
limit: { type: Number, default: 20 }
})
const emit = defineEmits(['keyword-click'])

const stopwords = new Set([
'y','de','el','la','los','las','del','en','con','por','para','un','una','que','es','su','se','al','lo','como','más','pero','no','o','si','the','and','a','of','in','with','for','to','is'
])


const keywords = computed(() => {

const text = props.games.map(g => g.description || '').join(' ')
const raw = text.toLowerCase().split(/\W+/).filter(Boolean)
const freq = Object.create(null)
for (const w of raw) {
if (w.length < 3) continue
if (stopwords.has(w)) continue
freq[w] = (freq[w] || 0) + 1
}
return Object.entries(freq)
.sort((a,b) => b[1] - a[1])
.slice(0, props.limit)
.map(([word,count])=>({word,count}))
})


function clickKeyword(w){
emit('keyword-click', w)
}
</script>


<style scoped>
.keywords-footer{padding:1rem;border-top:1px solid #eee;margin-top:1rem}
.chip{display:inline-block;padding:.25rem .5rem;margin:.2rem;background:#f3f3f3;border-radius:999px;cursor:pointer}
.chip:hover{background:#e0e0e0}
</style>