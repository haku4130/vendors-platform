<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', () => navigateTo('/dashboard/projects')],
});
</script>
