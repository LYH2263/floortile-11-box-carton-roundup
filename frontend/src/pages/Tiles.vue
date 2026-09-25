<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const items = ref([])
const err = ref('')

onMounted(load)
async function load() {
  items.value = (await getJSON('/api/tiles')).items
}

async function saveBox(t) {
  err.value = ''
  const n = Number(t.box_size)
  if (!Number.isInteger(n) || n <= 0) {
    err.value = `「${t.name}」每箱片数 N 必须为正整数，已拒绝 ${t.box_size}`
    return load()
  }
  try {
    const updated = await patchJSON(`/api/tiles/${t.id}`, { box_size: n })
    t.box_size = updated.box_size
  } catch (e) {
    err.value = e.message
    load()
  }
}
</script>
<template>
  <div class="page">
    <h1>砖型库</h1>
    <p>维护每箱片数 N：测算时面积法订货量会向上取整到 N 的整倍。改 N 只影响新测算，不会重算已保存的单据。</p>
    <p v-if="err" class="alert">{{ err }}</p>
    <div class="tile-cards">
      <div v-for="t in items" :key="t.id" class="tile-card" :class="{ dirty: t.data_quality === 'dirty' }">
        <strong>{{ t.name }}</strong>
        <span>{{ t.tile_l }} × {{ t.tile_w }} m</span>
        <em v-if="t.data_quality === 'dirty'">无效规格</em>
        <label>每箱
          <input v-model.number="t.box_size" type="number" min="1" step="1" style="width: 5rem" />
          片
        </label>
        <button @click="saveBox(t)">保存 N</button>
      </div>
    </div>
  </div>
</template>
