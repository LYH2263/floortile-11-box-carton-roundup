<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const items = ref([])
const openId = ref(null)

onMounted(async () => { items.value = (await getJSON('/api/runs')).items })

function toggle(id) {
  openId.value = openId.value === id ? null : id
}

// All values come from the run's saved snapshot, so old runs keep the N
// and rounded counts that were current when they were written.
// Runs saved before box rounding existed fall back to N=1.
function snap(run) {
  const r = run.result || {}
  const n = r.pieces_per_box ?? 1
  return {
    piecesPerBox: n,
    before: r.order_count,
    boxes: r.box_count ?? r.order_count,
    rounded: r.order_count_rounded ?? r.order_count,
  }
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>片数</th></tr></thead>
      <tbody>
        <template v-for="r in items" :key="r.id">
          <tr class="clickable" @click="toggle(r.id)">
            <td>{{ r.created_at?.slice(0, 19) }}</td>
            <td>{{ r.room_name }}</td>
            <td>{{ r.tile_name }}</td>
            <td>{{ snap(r).rounded }}</td>
          </tr>
          <tr v-if="openId === r.id" class="run-detail">
            <td colspan="4">
              <dl>
                <dt>进位前</dt><dd>{{ snap(r).before }} 片</dd>
                <dt>每箱片数</dt><dd>{{ snap(r).piecesPerBox }}</dd>
                <dt>箱数</dt><dd>{{ snap(r).boxes }}</dd>
                <dt>进位后</dt><dd>{{ snap(r).rounded }} 片</dd>
                <dt>损耗</dt><dd>{{ r.waste_pct }}%</dd>
                <dt v-if="r.note">备注</dt><dd v-if="r.note">{{ r.note }}</dd>
              </dl>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
