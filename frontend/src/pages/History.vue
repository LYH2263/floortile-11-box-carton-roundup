<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import OrderSummary from '../components/OrderSummary.vue'

const items = ref([])
const detail = ref(null)
const err = ref('')

onMounted(async () => { items.value = (await getJSON('/api/runs')).items })

async function openRun(r) {
  err.value = ''
  try {
    detail.value = await getJSON(`/api/runs/${r.id}`)
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead>
        <tr><th>时间</th><th>房间</th><th>砖型</th><th>进位前(片)</th><th>箱数</th><th>进位后(片)</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-for="r in items" :key="r">
          <td>{{ r.created_at?.slice(0, 19) }}</td>
          <td>{{ r.room_name }}</td>
          <td>{{ r.tile_name }}</td>
          <td>{{ r.result?.order_count }}</td>
          <td v-if="r.result?.boxed_count != null">
            {{ r.result.box_count }} 箱 × {{ r.result.box_size ?? r.box_size }} 片
          </td>
          <td v-else>—</td>
          <td v-if="r.result?.boxed_count != null">{{ r.result.boxed_count }}</td>
          <td v-else>—（旧单）</td>
          <td><button @click="openRun(r)">详情</button></td>
        </tr>
      </tbody>
    </table>

    <p v-if="err" class="alert">{{ err }}</p>

    <div v-if="detail" class="cards" style="margin-top: 1rem">
      <article style="min-width: 320px; border-left-color: #2c3e50">
        <h3 style="margin-top: 0">#{{ detail.id }} 单据详情（只读快照）</h3>
        <p>{{ detail.room_name }} × {{ detail.tile_name }}，损耗 {{ detail.waste_pct }}%</p>
        <p>
          当时每箱片数 N：
          <strong v-if="detail.box_size != null">{{ detail.box_size }}</strong>
          <span v-else class="muted">未配置（N=1，无进位）</span>
        </p>
        <OrderSummary :result="detail.result" />
      </article>
    </div>
  </div>
</template>
