<script setup lang="ts">
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth', () => navigateTo(useLocalePath()('/dashboard/projects'))],
});
</script>
