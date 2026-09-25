<script setup>
import { computed } from 'vue'

const props = defineProps({
  result: { type: Object, default: null },
})

// 旧单 result_json 里没有进位字段，按 N 缺失做降级展示（只显示进位前片数）
const boxed = computed(() => (props.result?.boxed_count ?? null))
const boxCount = computed(() => (props.result?.box_count ?? null))
const boxSize = computed(() => (props.result?.box_size ?? null))
</script>
<template>
  <div v-if="result" class="order-summary">
    <template v-if="boxed !== null">
      <div class="hero">{{ boxed }} 片</div>
      <ul>
        <li>
          整箱进位后：{{ boxCount }} 箱 × {{ boxSize }} 片/箱
          <span v-if="boxed === result.order_count" class="muted">（N={{ boxSize }}，进位前后相同）</span>
        </li>
        <li>进位前面积法订货量：{{ result.order_count }} 片</li>
        <li>净用量 {{ result.raw_count }} 片，损耗 {{ result.waste_pct }}%</li>
        <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
      </ul>
    </template>
    <template v-else>
      <div class="hero">{{ result.order_count }} 片</div>
      <ul>
        <li>净用量 {{ result.raw_count }} 片，损耗 {{ result.waste_pct }}%</li>
        <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
        <li class="muted">该单保存时尚无整箱进位配置，按当时片数展示。</li>
      </ul>
    </template>
  </div>
</template>
