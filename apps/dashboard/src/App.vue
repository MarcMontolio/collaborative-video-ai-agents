<script setup lang="ts">
const projectName = 'Collaborative Real-Time Video Analysis'
</script>

<template>
  <main class="dashboard">
    <section class="hero">
      <p class="eyebrow">Dashboard</p>
      <h1>{{ projectName }}</h1>
      <p class="description">
        Real-time detection events, stream status and alerts will be displayed here.
      </p>
    </section>

    <section class="grid">
      <article class="card">
        <h2>Detection Stream</h2>
        <p>WebSocket detection events will appear in this panel.</p>
      </article>

      <article class="card">
        <h2>Stream Status</h2>
        <p>Connection state and stream will be added in future issues.</p>
      </article>

      <article class="card">
        <h2>Alerts</h2>
        <p>Alert events generated from detection summaries will be shown here.</p>
      </article>
    </section>
  </main>
</template>
